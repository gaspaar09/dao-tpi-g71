"""Pestaña de Empleados."""

from tkinter import ttk

from config import LARGO_NOMBRE_EMPLEADO
from constantes import RolEmpleado
from dao.empleado_dao import EmpleadoDAO
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase
from validadores import validar_legajo, validar_solo_letras

CAMPOS = ['legajo', 'nombre', 'rol', 'sede']


class PestaniaEmpleados(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = EmpleadoDAO()

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_campo(formulario, 'legajo', "Legajo:", 0, validar_legajo)
        self.crear_campo(formulario, 'nombre', "Nombre y apellido:", 1,
                         lambda v: validar_solo_letras(v, "nombre", 2, LARGO_NOMBRE_EMPLEADO))
        self.crear_combo(formulario, 'rol', "Rol:", 2, lambda: [(rol, rol) for rol in RolEmpleado.TODOS])
        self.crear_combo(formulario, 'sede', "Sede:", 3, SedeDAO().opciones)

        self.crear_botones(self, [("Eliminar", self.eliminar)]).pack(anchor="w", pady=10)

        marco, self.tabla = self.crear_tabla(self, [
            ('legajo', "Legajo", 100), ('nombre', "Nombre", 220), ('rol', "Rol", 140), ('sede', "Sede", 200)])
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def campos_formulario(self):
        return CAMPOS

    def crear(self):
        self.dao.crear(self.valor('legajo'), self.valor('nombre'), self.valor('rol'), self.valor('sede'))

    def modificar(self, id):
        self.dao.modificar(id, self.valor('legajo'), self.valor('nombre'), self.valor('rol'), self.valor('sede'))

    def cargar_formulario(self, fila):
        self.poner('legajo', fila['legajo'])
        self.poner('nombre', fila['nombre'])
        self.poner('rol', fila['rol'])
        self.poner('sede', fila['sede_id'])

    def eliminar(self):
        self.accion_sobre_seleccion(self.dao.eliminar, "¿Eliminar el empleado seleccionado?", "Empleado eliminado")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
