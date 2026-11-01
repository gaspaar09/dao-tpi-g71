"""Funciones que comparten todos los DAO."""

from excepciones import ValidacionError, ReglaNegocioError


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
