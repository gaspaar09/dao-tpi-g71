"""Pestaña de Empleados."""

from tkinter import messagebox

from config import LARGO_NOMBRE_EMPLEADO
from constantes import RolEmpleado
from dao.empleado_dao import EmpleadoDAO
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase, ICONO_EDITAR, ICONO_BAJA
from validadores import validar_solo_letras

# El legajo no se carga: lo asigna el sistema según el rol (B1, B2... / A1, A2...)
CAMPOS = ['nombre', 'rol', 'sede']


class PestaniaEmpleados(PestaniaBase):
    TITULO_NUEVO = "Nuevo empleado"
    TITULO_EDITAR = "Editar empleado"

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = EmpleadoDAO()
        self.crear_encabezado("Empleados", "Personal de las sedes que registra las operaciones",
                              [("Nuevo empleado", self.nuevo, True)])
        self.crear_barra_seleccion("Con el empleado elegido:", [])
        self.crear_tabla_principal(self, [
            ('legajo', "Legajo", 100), ('nombre', "Nombre", 260), ('rol', "Rol", 160), ('sede', "Sede", 220)],
            doble_clic=self.editar_seleccionado,
            iconos=[(ICONO_EDITAR, self.editar_seleccionado), (ICONO_BAJA, self.eliminar)]).pack(fill="both", expand=True)
        self.refrescar()

    def armar_formulario(self, contenedor):
        self.crear_campo(contenedor, 'nombre', "Nombre y apellido:", 0,
                         lambda v: validar_solo_letras(v, "nombre", 2, LARGO_NOMBRE_EMPLEADO))
        self.crear_combo(contenedor, 'rol', "Rol:", 1, lambda: [(rol, rol) for rol in RolEmpleado.TODOS])
        self.crear_combo(contenedor, 'sede', "Sede:", 2, SedeDAO().opciones)
        self.ayuda(contenedor, "El legajo lo asigna el sistema según el rol: B1, B2... para bibliotecarios "
                               "y A1, A2... para administradores.", 3)

    def campos_formulario(self):
        return CAMPOS

    def crear(self):
        self.legajo_asignado = self.dao.crear(self.valor('nombre'), self.valor('rol'), self.valor('sede'))

    def modificar(self, id):
        anterior = self.buscar_fila(id)['legajo']
        legajo = self.dao.modificar(id, self.valor('nombre'), self.valor('rol'), self.valor('sede'))
        if legajo != anterior:
            self.legajo_asignado = legajo

    def guardar(self):
        """Como el legajo lo pone el sistema, se informa cuál quedó (en el
        alta, o al cambiar el rol)."""
        self.legajo_asignado = None
        correcto = super().guardar()
        if correcto and self.legajo_asignado is not None:
            messagebox.showinfo("Legajo", f"Se asignó el legajo {self.legajo_asignado}",
                                parent=self.ventana_actual())
        return correcto

    def cargar_formulario(self, fila):
        self.poner('nombre', fila['nombre'])
        self.poner('rol', fila['rol'])
        self.poner('sede', fila['sede_id'])

    def eliminar(self):
        self.accion_sobre_seleccion(self.dao.eliminar, "¿Eliminar el empleado seleccionado?", "Empleado eliminado")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
