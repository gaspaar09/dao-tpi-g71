"""Funciones que comparten todos los DAO."""

from constantes import EstadoReserva
from excepciones import ValidacionError, ReglaNegocioError
from modelos.reserva import Reserva


def buscar_por_id(session, clase, id, descripcion):
    """Devuelve el objeto con ese id dentro de la sesión.

    descripcion se usa en los mensajes, por ejemplo "la sede".
    Sin id es un error de formato (no se eligió nada en el desplegable);
    con un id que no existe es un error de negocio (se borró mientras
    otra pestaña lo mostraba).
    """
    if id is None or id == "":
        raise ValidacionError(f"Seleccione {descripcion}")
    objeto = session.query(clase).filter_by(id=id).first()
    if objeto is None:
        raise ReglaNegocioError(f"No se encontró {descripcion} (puede haber sido eliminado)")
    return objeto


def asignar_a_reserva_pendiente(session, ejemplar):
    """Si el ejemplar quedó DISPONIBLE, se lo asigna a la reserva PENDIENTE
    más antigua de ese título en su sede. Se llama en la misma sesión de la
    operación que lo liberó, así nadie lo pide en el medio.

    Devuelve la reserva asignada, o None si no había ninguna esperando."""
    if not ejemplar.esta_disponible():
        return None
    reserva = session.query(Reserva).filter_by(
        estado=EstadoReserva.PENDIENTE, libro_id=ejemplar.libro_id,
        sede_retiro_id=ejemplar.sede_id).order_by(Reserva.fecha_reserva, Reserva.id).first()
    if reserva is not None:
        reserva.asignar_ejemplar(ejemplar)
    return reserva
