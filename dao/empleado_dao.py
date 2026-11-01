"""Acceso a datos de empleados."""

from config import LARGO_NOMBRE_EMPLEADO
from constantes import RolEmpleado
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.empleado import Empleado
from modelos.remito import MovimientoRemito
from modelos.sede import Sede
from validadores import validar_legajo, validar_solo_letras, validar_opcion


def validar_datos_empleado(legajo, nombre, rol):
    legajo = validar_legajo(legajo)
    nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_EMPLEADO)
    rol = validar_opcion(rol, RolEmpleado.TODOS, "rol")
    return legajo, nombre, rol


class EmpleadoDAO:
    """Operaciones de acceso a datos sobre empleados."""

    def verificar_legajo_unico(self, session, legajo, id_actual=None):
        empleado = session.query(Empleado).filter_by(legajo=legajo).first()
        if empleado is not None and empleado.id != id_actual:
            raise ReglaNegocioError(f"Ya existe un empleado con el legajo {legajo}")

    def buscar_sede_activa(self, session, sede_id):
        sede = buscar_por_id(session, Sede, sede_id, "la sede")
        if not sede.esta_activa():
            raise ReglaNegocioError(f"La sede {sede.nombre} está dada de baja")
        return sede

    def crear(self, legajo, nombre, rol, sede_id):
        legajo, nombre, rol = validar_datos_empleado(legajo, nombre, rol)
        with obtener_session() as session:
            sede = self.buscar_sede_activa(session, sede_id)
            self.verificar_legajo_unico(session, legajo)
            session.add(Empleado(legajo=legajo, nombre=nombre, rol=rol, sede=sede))

    def modificar(self, id, legajo, nombre, rol, sede_id):
        legajo, nombre, rol = validar_datos_empleado(legajo, nombre, rol)
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, id, "el empleado")
            sede = self.buscar_sede_activa(session, sede_id)
            self.verificar_legajo_unico(session, legajo, id_actual=empleado.id)
            empleado.legajo = legajo
            empleado.nombre = nombre
            empleado.rol = rol
            empleado.sede = sede

    def eliminar(self, id):
        """Solo se elimina si no registró movimientos: la trazabilidad de
        los remitos tiene que conservar quién hizo cada cambio."""
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, id, "el empleado")
            if session.query(MovimientoRemito).filter_by(empleado_id=empleado.id).first() is not None:
                raise ReglaNegocioError("No se puede eliminar: el empleado registró movimientos de remitos")
            session.delete(empleado)

    def listar(self):
        with obtener_session() as session:
            empleados = session.query(Empleado).order_by(Empleado.legajo).all()
            return [
                {
                    'id': empleado.id,
                    'legajo': empleado.legajo,
                    'nombre': empleado.nombre,
                    'rol': empleado.rol,
                    'sede': empleado.sede.nombre,
                    'sede_id': empleado.sede_id,
                }
                for empleado in empleados
            ]

    def opciones(self):
        with obtener_session() as session:
            empleados = session.query(Empleado).order_by(Empleado.legajo).all()
            return [(empleado.id, str(empleado)) for empleado in empleados]
