"""Acceso a datos de empleados."""

from config import LARGO_NOMBRE_EMPLEADO
from constantes import RolEmpleado
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.empleado import Empleado
from modelos.remito import MovimientoRemito
from modelos.sede import Sede
from validadores import validar_solo_letras, validar_opcion


def validar_datos_empleado(nombre, rol):
    nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_EMPLEADO)
    rol = validar_opcion(rol, RolEmpleado.TODOS, "rol")
    return nombre, rol


def numero_de_legajo(legajo):
    """La parte numérica de un legajo como "B12" (12). Los legajos que no
    siguen el formato (letra + número) cuentan como 0."""
    numero = legajo[1:]
    if numero.isdigit():
        return int(numero)
    return 0


class EmpleadoDAO:
    """Operaciones de acceso a datos sobre empleados."""

    def siguiente_legajo(self, session, rol):
        """El legajo lo asigna el sistema: la letra del rol y el número
        siguiente al último de esa letra (B1, B2... / A1, A2...)."""
        prefijo = RolEmpleado.PREFIJO_LEGAJO[rol]
        numeros = [numero_de_legajo(empleado.legajo) for empleado in session.query(Empleado).all()
                   if empleado.legajo.startswith(prefijo)]
        return f"{prefijo}{max(numeros, default=0) + 1}"

    def buscar_sede_activa(self, session, sede_id):
        sede = buscar_por_id(session, Sede, sede_id, "la sede")
        if not sede.esta_activa():
            raise ReglaNegocioError(f"La sede {sede.nombre} está dada de baja")
        return sede

    def crear(self, nombre, rol, sede_id):
        """Da de alta el empleado y devuelve el legajo asignado."""
        nombre, rol = validar_datos_empleado(nombre, rol)
        with obtener_session() as session:
            sede = self.buscar_sede_activa(session, sede_id)
            legajo = self.siguiente_legajo(session, rol)
            session.add(Empleado(legajo=legajo, nombre=nombre, rol=rol, sede=sede))
            return legajo

    def modificar(self, id, nombre, rol, sede_id):
        """Si cambia el rol, el empleado recibe un legajo nuevo con la letra
        del rol nuevo (decisión del grupo). Los movimientos de remitos que
        registró no se pierden: apuntan al empleado por su id, no por el legajo."""
        nombre, rol = validar_datos_empleado(nombre, rol)
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, id, "el empleado")
            sede = self.buscar_sede_activa(session, sede_id)
            if rol != empleado.rol:
                empleado.legajo = self.siguiente_legajo(session, rol)
            empleado.nombre = nombre
            empleado.rol = rol
            empleado.sede = sede
            return empleado.legajo

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
            # Por letra y número: B2 va antes que B10 (como texto quedaría al revés)
            empleados = sorted(session.query(Empleado).all(),
                               key=lambda e: (e.legajo[0], numero_de_legajo(e.legajo)))
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
            # Por letra y número: B2 va antes que B10 (como texto quedaría al revés)
            empleados = sorted(session.query(Empleado).all(),
                               key=lambda e: (e.legajo[0], numero_de_legajo(e.legajo)))
            return [(empleado.id, str(empleado)) for empleado in empleados]
