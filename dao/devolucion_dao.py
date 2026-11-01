"""Acceso a datos de devoluciones: cierre del préstamo, multa y regreso del ejemplar.

Está en su propio módulo porque usa el diccionario de transiciones de
PrestamoDAO y el armado de remitos de RemitoDAO (si viviera en uno de los
dos, se importarían entre sí).
"""

from config import LARGO_OBSERVACIONES
from constantes import EstadoFisico, EstadoPrestamo, TipoPrestamo
from dao.comun import buscar_por_id, asignar_a_reserva_pendiente
from dao.prestamo_dao import verificar_transicion
from dao.remito_dao import crear_remito_devolucion
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.empleado import Empleado
from modelos.prestamo import Prestamo, Devolucion, Multa
from patrones.estrategia_prestamo import ESTRATEGIAS
from validadores import validar_fecha, validar_fecha_no_futura, validar_opcion, validar_texto_opcional


class DevolucionDAO:
    """Operaciones de acceso a datos sobre devoluciones."""

    def registrar(self, prestamo_id, fecha, estado_fisico, observaciones, empleado_id):
        """El socio devuelve el ejemplar. Si se atrasó se genera la multa con la
        estrategia del tipo de préstamo. Local: el ejemplar vuelve a circular.
        Interbibliotecario: sigue PRESTADO hasta que el remito de devolución
        llegue a su sede."""
        fecha = validar_fecha_no_futura(validar_fecha(fecha, "fecha de devolución"), "fecha de devolución")
        estado_fisico = validar_opcion(estado_fisico, EstadoFisico.TODOS, "estado físico")
        observaciones = validar_texto_opcional(observaciones, "observaciones", LARGO_OBSERVACIONES)
        if estado_fisico in [EstadoFisico.DANADO, EstadoFisico.DESTRUIDO] and observaciones is None:
            raise ValidacionError("Las observaciones son obligatorias si el ejemplar volvió dañado o destruido")
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, empleado_id, "el empleado actual")
            prestamo = buscar_por_id(session, Prestamo, prestamo_id, "el préstamo")
            # Solo un préstamo ACTIVO (vencido o no) puede pasar a DEVUELTO
            verificar_transicion(prestamo, EstadoPrestamo.DEVUELTO)
            if fecha < prestamo.fecha_prestamo:
                raise ReglaNegocioError("La fecha de devolución no puede ser anterior a la del préstamo")

            prestamo.devolucion = Devolucion(fecha_devolucion=fecha, estado_fisico=estado_fisico,
                                             observaciones=observaciones)
            prestamo.estado = EstadoPrestamo.DEVUELTO
            prestamo.ejemplar.estado_fisico = estado_fisico

            # Multa: la estrategia la elige el DAO y llega por parámetro
            dias_atraso = max(0, (fecha - prestamo.fecha_vencimiento).days)
            if dias_atraso > 0:
                prestamo.multa = Multa(dias_atraso=dias_atraso)
                prestamo.multa.calcular_monto(ESTRATEGIAS[prestamo.tipo])

            if prestamo.tipo == TipoPrestamo.LOCAL:
                prestamo.ejemplar.volver_a_circular()
                asignar_a_reserva_pendiente(session, prestamo.ejemplar)
            else:
                crear_remito_devolucion(session, prestamo, empleado)
