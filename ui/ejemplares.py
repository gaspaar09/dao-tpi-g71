"""Pestaña de Ejemplares (copias físicas de los libros)."""

from tkinter import ttk

from constantes import EstadoFisico
from dao.ejemplar_dao import EjemplarDAO
from dao.libro_dao import LibroDAO
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase
from validadores import validar_codigo_inventario

CAMPOS = ['codigo_inventario', 'libro', 'sede', 'estado_fisico']
# Identifican la copia: no se modifican (ver EjemplarDAO.modificar)
CAMPOS_FIJOS = ['codigo_inventario', 'libro', 'sede']


class PestaniaEjemplares(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = EjemplarDAO()

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_campo(formulario, 'codigo_inventario', "Código de inventario:", 0, validar_codigo_inventario)
        self.crear_combo(formulario, 'libro', "Libro:", 1, LibroDAO().opciones, ancho=50)
        self.crear_combo(formulario, 'sede', "Sede:", 2, SedeDAO().opciones)
        self.crear_combo(formulario, 'estado_fisico', "Estado físico:", 3,
                         lambda: [(estado, estado) for estado in EstadoFisico.TODOS])
        ttk.Label(formulario, text="Al editar solo se cambia el estado físico.",
                  foreground="gray").grid(row=8, column=1, sticky="w", padx=5)

        self.crear_botones(self, [("Dar de baja", self.dar_de_baja)]).pack(anchor="w", pady=10)
        marco, self.tabla = self.crear_tabla(self, [
            ('codigo_inventario', "Código", 110), ('libro', "Libro", 260), ('sede', "Sede", 180),
            ('estado', "Estado", 110), ('estado_fisico', "Estado físico", 110)])
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def campos_formulario(self):
        if self.id_editando is None:
            return CAMPOS
        return ['estado_fisico']

    def crear(self):
        self.dao.crear(self.valor('codigo_inventario'), self.valor('libro'), self.valor('sede'),
                       self.valor('estado_fisico'))

    def modificar(self, id):
        self.dao.modificar(id, self.valor('estado_fisico'))

    def cargar_formulario(self, fila):
        # Se muestran los datos fijos, pero deshabilitados
        self.poner('codigo_inventario', fila['codigo_inventario'])
        self.campos['libro']['widget'].set(fila['libro'])
        self.campos['sede']['widget'].set(fila['sede'])
        self.poner('estado_fisico', fila['estado_fisico'])
        for nombre in CAMPOS_FIJOS:
            self.campos[nombre]['widget'].config(state="disabled")

    def limpiar(self):
        for nombre in CAMPOS_FIJOS:
            estado = "readonly" if self.es_combo(nombre) else "normal"
            self.campos[nombre]['widget'].config(state=estado)
        super().limpiar_campos(CAMPOS)
        self.id_editando = None
        self.boton_guardar.config(text="Guardar")
        self.tabla.selection_remove(self.tabla.selection())

    def dar_de_baja(self):
        self.accion_sobre_seleccion(self.dao.dar_de_baja, "¿Dar de baja el ejemplar seleccionado?",
                                    "Ejemplar dado de baja")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
