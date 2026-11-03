"""Acceso a datos de ejemplares (copias físicas)."""

from constantes import EstadoEjemplar, EstadoFisico
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.catalogo import Libro
from modelos.ejemplar import Ejemplar
from modelos.remito import ItemRemito
from modelos.reserva import Reserva
from modelos.sede import Sede
from validadores import validar_codigo_inventario, validar_opcion

# Un ejemplar en estos estados está comprometido en una operación
ESTADOS_SIN_BAJA = [EstadoEjemplar.PRESTADO, EstadoEjemplar.RESERVADO, EstadoEjemplar.EN_TRANSITO]


class EjemplarDAO:
    """Operaciones de acceso a datos sobre ejemplares."""

    def crear(self, codigo_inventario, libro_id, sede_id, estado_fisico):
        codigo = validar_codigo_inventario(codigo_inventario)
        estado_fisico = validar_opcion(estado_fisico, EstadoFisico.TODOS, "estado físico")
        with obtener_session() as session:
            libro = buscar_por_id(session, Libro, libro_id, "el libro")
            sede = buscar_por_id(session, Sede, sede_id, "la sede")
            if not sede.esta_activa():
                raise ReglaNegocioError(f"La sede {sede.nombre} está dada de baja")
            if session.query(Ejemplar).filter_by(codigo_inventario=codigo).first() is not None:
                raise ReglaNegocioError(f"Ya existe un ejemplar con el código {codigo}")
            session.add(Ejemplar(codigo_inventario=codigo, libro=libro, sede=sede,
                                 estado=EstadoEjemplar.DISPONIBLE, estado_fisico=estado_fisico))

    def modificar(self, id, estado_fisico):
        """Solo se corrige el estado físico. El código, el libro y la sede
        identifican la copia: si están mal, se da de baja y se carga de nuevo."""
        estado_fisico = validar_opcion(estado_fisico, EstadoFisico.TODOS, "estado físico")
        with obtener_session() as session:
            ejemplar = buscar_por_id(session, Ejemplar, id, "el ejemplar")
            ejemplar.estado_fisico = estado_fisico

    def dar_de_baja(self, id):
        with obtener_session() as session:
            ejemplar = buscar_por_id(session, Ejemplar, id, "el ejemplar")
            if ejemplar.estado == EstadoEjemplar.BAJA:
                raise ReglaNegocioError("El ejemplar ya está dado de baja")
            if ejemplar.estado in ESTADOS_SIN_BAJA:
                raise ReglaNegocioError(f"No se puede dar de baja un ejemplar {ejemplar.estado}")
            ejemplar.cambiar_estado(EstadoEjemplar.BAJA)

    def tiene_historial(self, id):
        with obtener_session() as session:
            ejemplar = buscar_por_id(session, Ejemplar, id, "el ejemplar")
            return self.historial_en_sesion(session, ejemplar)

    def historial_en_sesion(self, session, ejemplar):
        """Préstamos, remitos o reservas que lo nombran: borrarlo los dejaría sin ejemplar."""
        return (len(ejemplar.prestamos) > 0
                or session.query(ItemRemito).filter_by(ejemplar_id=ejemplar.id).first() is not None
                or session.query(Reserva).filter_by(ejemplar_id=ejemplar.id).first() is not None)

    def eliminar(self, id):
        """Borra la fila solo si el ejemplar nunca se usó (por ejemplo, cargado por error).
        Con historial se da de baja, para no alterar préstamos, multas ni reportes."""
        with obtener_session() as session:
            ejemplar = buscar_por_id(session, Ejemplar, id, "el ejemplar")
            if self.historial_en_sesion(session, ejemplar):
                raise ReglaNegocioError(f"No se puede eliminar: {ejemplar.codigo_inventario} tiene historial. "
                                        "Puede darlo de baja")
            session.delete(ejemplar)

    def opciones_disponibles(self, sede_id):
        """Ejemplares DISPONIBLE de una sede, para elegir en un préstamo."""
        if sede_id is None:
            return []
        with obtener_session() as session:
            ejemplares = (session.query(Ejemplar)
                          .filter_by(sede_id=sede_id, estado=EstadoEjemplar.DISPONIBLE)
                          .order_by(Ejemplar.codigo_inventario).all())
            return [(ejemplar.id, f"{ejemplar.codigo_inventario} - {ejemplar.libro.titulo}")
                    for ejemplar in ejemplares]

    def listar(self):
        with obtener_session() as session:
            ejemplares = session.query(Ejemplar).order_by(Ejemplar.codigo_inventario).all()
            return [
                {
                    'id': ejemplar.id,
                    'codigo_inventario': ejemplar.codigo_inventario,
                    'libro': ejemplar.libro.titulo,
                    'sede': ejemplar.sede.nombre,
                    'estado': ejemplar.estado,
                    'estado_fisico': ejemplar.estado_fisico,
                }
                for ejemplar in ejemplares
            ]
