"""Acceso a datos de reservas: alta, retiro, cancelación y vencimientos.

Una reserva es sobre un título y una sede de retiro. Si hay un ejemplar
libre se asigna en el acto; si no, queda PENDIENTE y se le asigna el primero
que se libere en esa sede (asignar_a_reserva_pendiente, en dao/comun.py).
"""

from datetime import date, timedelta

from config import DIAS_ESPERA_RESERVA
from constantes import EstadoEjemplar, EstadoPrestamo, EstadoReserva, TipoPrestamo
from dao.comun import buscar_por_id, asignar_a_reserva_pendiente
from dao.prestamo_dao import verificar_transicion, formatear_fecha
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.catalogo import Libro
from modelos.ejemplar import Ejemplar
from modelos.prestamo import Prestamo
from modelos.reserva import Reserva
from modelos.sede import Sede
from modelos.socio import Socio
from patrones.estrategia_prestamo import ESTRATEGIAS


class ReservaDAO:
    """Operaciones de acceso a datos sobre reservas."""

    def crear(self, socio_id, libro_id, sede_retiro_id):
        with obtener_session() as session:
            socio = buscar_por_id(session, Socio, socio_id, "el socio")
            libro = buscar_por_id(session, Libro, libro_id, "el libro")
            sede = buscar_por_id(session, Sede, sede_retiro_id, "la sede de retiro")
            if not socio.esta_habilitado():
                raise ReglaNegocioError(f"El socio {socio.nro_socio} no está habilitado")
            if not sede.esta_activa():
                raise ReglaNegocioError(f"La sede {sede.nombre} está dada de baja")
            for reserva in session.query(Reserva).filter_by(socio_id=socio.id, libro_id=libro.id).all():
                if reserva.esta_en_curso():
                    raise ReglaNegocioError(f"El socio ya tiene una reserva {reserva.estado} de {libro.titulo}")
            reserva = Reserva(socio=socio, libro=libro, sede_retiro=sede, estado=EstadoReserva.PENDIENTE,
                              fecha_reserva=date.today(),
                              fecha_vencimiento=date.today() + timedelta(days=DIAS_ESPERA_RESERVA))
            session.add(reserva)
            # Si ya hay un ejemplar libre en esa sede, se aparta en el acto
            ejemplar = session.query(Ejemplar).filter_by(libro_id=libro.id, sede_id=sede.id,
                                                         estado=EstadoEjemplar.DISPONIBLE).first()
            if ejemplar is not None:
                reserva.asignar_ejemplar(ejemplar)

    def retirar(self, id):
        """El socio retira el ejemplar apartado: la reserva se cumple y se crea
        un préstamo local en la sede de retiro, activo en el acto."""
        with obtener_session() as session:
            reserva = buscar_por_id(session, Reserva, id, "la reserva")
            reserva.cumplir()
            prestamo = Prestamo(tipo=TipoPrestamo.LOCAL, estado=EstadoPrestamo.SOLICITADO, socio=reserva.socio,
                                ejemplar=reserva.ejemplar, sede_origen=reserva.sede_retiro,
                                sede_destino=reserva.sede_retiro)
            # Mismas reglas que un préstamo pedido desde la pestaña Préstamos
            prestamo.validar_prestamo()
            prestamo.estado = EstadoPrestamo.APROBADO
            verificar_transicion(prestamo, EstadoPrestamo.ACTIVO)
            prestamo.activar(ESTRATEGIAS[prestamo.tipo])
            session.add(prestamo)

    def cancelar(self, id):
        with obtener_session() as session:
            reserva = buscar_por_id(session, Reserva, id, "la reserva")
            reserva.cancelar()
            if reserva.ejemplar is not None:
                asignar_a_reserva_pendiente(session, reserva.ejemplar)

    def procesar_vencimientos(self):
        """Vence las reservas en curso cuyo plazo pasó (espera de 45 días o
        retiro de 2) y pasa el ejemplar liberado a la siguiente. Modifica
        datos, por eso se guarda el estado. Devuelve cuántas venció."""
        with obtener_session() as session:
            vencidas = 0
            reservas = session.query(Reserva).order_by(Reserva.fecha_reserva, Reserva.id).all()
            for reserva in reservas:
                if reserva.esta_en_curso() and reserva.fecha_vencimiento < date.today():
                    reserva.vencer()
                    vencidas += 1
                    if reserva.ejemplar is not None:
                        asignar_a_reserva_pendiente(session, reserva.ejemplar)
            return vencidas

    def listar(self):
        with obtener_session() as session:
            reservas = session.query(Reserva).order_by(Reserva.id.desc()).all()
            return [
                {
                    'id': reserva.id,
                    'socio': str(reserva.socio),
                    'libro': reserva.libro.titulo,
                    'sede': reserva.sede_retiro.nombre,
                    'ejemplar': reserva.ejemplar.codigo_inventario if reserva.ejemplar else "",
                    'estado': reserva.estado,
                    'fecha_reserva': formatear_fecha(reserva.fecha_reserva),
                    'fecha_vencimiento': formatear_fecha(reserva.fecha_vencimiento),
                }
                for reserva in reservas
            ]
