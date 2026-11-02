"""Acceso a datos de préstamos: solicitud, aprobación y cancelación.

El estado del préstamo no usa un patrón: se controla con un diccionario de
transiciones permitidas. Las reglas que solo miran el propio préstamo están
en Prestamo.validar_prestamo(); el plazo lo calcula la estrategia que el
DAO elige en ESTRATEGIAS (selección externa del patrón Strategy).
"""

from constantes import EstadoEjemplar, EstadoMulta, EstadoPrestamo, TipoPrestamo
from dao.comun import buscar_por_id, asignar_a_reserva_pendiente
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.ejemplar import Ejemplar
from modelos.empleado import Empleado
from modelos.prestamo import Prestamo
from modelos.remito import ItemRemito
from modelos.sede import Sede
from modelos.socio import Socio
from patrones.estrategia_prestamo import ESTRATEGIAS
from validadores import validar_opcion

# Transiciones permitidas (confirmadas por el grupo). VENCIDO no está porque
# no se guarda: se calcula sobre un préstamo ACTIVO.
TRANSICIONES = {
    EstadoPrestamo.SOLICITADO: [EstadoPrestamo.APROBADO, EstadoPrestamo.CANCELADO],
    EstadoPrestamo.APROBADO: [EstadoPrestamo.EN_ENVIO, EstadoPrestamo.ACTIVO, EstadoPrestamo.CANCELADO],
    EstadoPrestamo.EN_ENVIO: [EstadoPrestamo.ACTIVO, EstadoPrestamo.CANCELADO],
    EstadoPrestamo.ACTIVO: [EstadoPrestamo.DEVUELTO],
    EstadoPrestamo.DEVUELTO: [],
    EstadoPrestamo.CANCELADO: [],
}


def verificar_transicion(prestamo, nuevo_estado):
    """Lanza ReglaNegocioError si el préstamo no puede pasar a nuevo_estado."""
    if nuevo_estado not in TRANSICIONES[prestamo.estado]:
        raise ReglaNegocioError(f"Un préstamo {prestamo.estado} no puede pasar a {nuevo_estado}")


def formatear_fecha(fecha):
    if fecha is None:
        return ""
    return fecha.strftime("%d/%m/%Y")


class PrestamoDAO:
    """Operaciones de acceso a datos sobre préstamos."""

    def solicitar(self, tipo, socio_id, ejemplar_id, sede_origen_id, sede_destino_id):
        """Registra la solicitud (estado SOLICITADO). En un préstamo local la
        sede de destino puede quedar vacía: es la misma que la de origen."""
        tipo = validar_opcion(tipo, TipoPrestamo.TODOS, "tipo de préstamo")
        with obtener_session() as session:
            socio = buscar_por_id(session, Socio, socio_id, "el socio")
            origen = buscar_por_id(session, Sede, sede_origen_id, "la sede de origen")
            if tipo == TipoPrestamo.LOCAL and sede_destino_id is None:
                destino = origen
            else:
                destino = buscar_por_id(session, Sede, sede_destino_id, "la sede de destino")
            ejemplar = buscar_por_id(session, Ejemplar, ejemplar_id, "el ejemplar")
            # Evita el duplicado (por ejemplo, un doble clic en Registrar): el
            # mismo socio no pide dos veces el mismo ejemplar. Socios distintos sí.
            for anterior in session.query(Prestamo).filter_by(socio_id=socio.id, ejemplar_id=ejemplar.id).all():
                if anterior.estado in [EstadoPrestamo.SOLICITADO, EstadoPrestamo.APROBADO]:
                    raise ReglaNegocioError(f"El socio ya tiene una solicitud {anterior.estado} de ese ejemplar "
                                            f"(préstamo #{anterior.id})")
            prestamo = Prestamo(tipo=tipo, estado=EstadoPrestamo.SOLICITADO, socio=socio, ejemplar=ejemplar,
                                sede_origen=origen, sede_destino=destino)
            # Reglas del diagrama: socio habilitado, ejemplar disponible y de la
            # sede de origen, sedes activas y coherentes con el tipo
            prestamo.validar_prestamo()
            session.add(prestamo)

    def aprobar(self, id):
        """Aprueba la solicitud. Local: se activa en la misma operación (el
        ejemplar pasa directo a PRESTADO). Interbibliotecario: el ejemplar queda
        RESERVADO hasta que llegue el remito de ida."""
        with obtener_session() as session:
            prestamo = buscar_por_id(session, Prestamo, id, "el préstamo")
            verificar_transicion(prestamo, EstadoPrestamo.APROBADO)
            # Se valida de nuevo: entre la solicitud y la aprobación el socio
            # pudo ser inhabilitado o el ejemplar pudo prestarse a otro
            prestamo.validar_prestamo()
            prestamo.estado = EstadoPrestamo.APROBADO
            if prestamo.tipo == TipoPrestamo.LOCAL:
                verificar_transicion(prestamo, EstadoPrestamo.ACTIVO)
                prestamo.activar(ESTRATEGIAS[prestamo.tipo])
            else:
                prestamo.ejemplar.cambiar_estado(EstadoEjemplar.RESERVADO)

    def cancelar(self, id, empleado_id=None):
        """Desde SOLICITADO o APROBADO no hay remito: solo se libera el ejemplar.
        Desde EN_ENVIO el ejemplar se saca de su remito, lo que solo se puede
        mientras esté EMPAQUETADO (lo decide el estado del remito). El
        empleado hace falta en ese caso, porque puede cancelarse el remito."""
        with obtener_session() as session:
            prestamo = buscar_por_id(session, Prestamo, id, "el préstamo")
            verificar_transicion(prestamo, EstadoPrestamo.CANCELADO)
            if prestamo.estado == EstadoPrestamo.EN_ENVIO:
                empleado = buscar_por_id(session, Empleado, empleado_id, "el empleado actual")
                # Un préstamo EN_ENVIO tiene un solo ítem: el de su remito de ida
                item = session.query(ItemRemito).filter_by(prestamo_id=prestamo.id).first()
                item.remito.quitar_item(item, empleado, f"Se canceló el préstamo #{prestamo.id}")
            if prestamo.estado in [EstadoPrestamo.APROBADO, EstadoPrestamo.EN_ENVIO]:
                prestamo.ejemplar.cambiar_estado(EstadoEjemplar.DISPONIBLE)
            prestamo.estado = EstadoPrestamo.CANCELADO
            # El ejemplar liberado pasa a quien lo estaba esperando
            asignar_a_reserva_pendiente(session, prestamo.ejemplar)

    def pagar_multa(self, id):
        """Solo se registra el pago (el cobro está fuera de alcance)."""
        with obtener_session() as session:
            prestamo = buscar_por_id(session, Prestamo, id, "el préstamo")
            if prestamo.multa is None:
                raise ReglaNegocioError("El préstamo no tiene multa")
            if prestamo.multa.estado != EstadoMulta.PENDIENTE:
                raise ReglaNegocioError("La multa ya está pagada")
            prestamo.multa.estado = EstadoMulta.PAGADA

    def listar(self):
        """Préstamos listos para mostrar, los más nuevos primero. El estado es
        el efectivo: VENCIDO si está ACTIVO y pasó la fecha de vencimiento."""
        with obtener_session() as session:
            prestamos = session.query(Prestamo).order_by(Prestamo.id.desc()).all()
            return [
                {
                    'id': prestamo.id,
                    'socio': str(prestamo.socio),
                    'libro': prestamo.ejemplar.libro.titulo,
                    'ejemplar': prestamo.ejemplar.codigo_inventario,
                    'tipo': prestamo.tipo,
                    'origen': prestamo.sede_origen.nombre,
                    'destino': prestamo.sede_destino.nombre,
                    # Versiones cortas para la tabla de la pestaña
                    'socio_nombre': f"{prestamo.socio.nombre} {prestamo.socio.apellido}",
                    'ruta': f"{prestamo.sede_origen.nombre} → {prestamo.sede_destino.nombre}",
                    'multa_corta': (f"${prestamo.multa.monto:.2f} {prestamo.multa.estado.lower()}"
                                    if prestamo.multa else ""),
                    'estado': prestamo.estado_efectivo,
                    'fecha_solicitud': formatear_fecha(prestamo.fecha_solicitud),
                    'fecha_prestamo': formatear_fecha(prestamo.fecha_prestamo),
                    'fecha_vencimiento': formatear_fecha(prestamo.fecha_vencimiento),
                    'multa': str(prestamo.multa) if prestamo.multa else "",
                }
                for prestamo in prestamos
            ]
