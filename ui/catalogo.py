"""Pestaña de Catálogo: sub-pestañas de Libros, Autores y Categorías."""

import tkinter as tk
from tkinter import ttk

from config import LARGO_TITULO, LARGO_EDITORIAL, LARGO_IDIOMA, LARGO_NOMBRE_PERSONA
from constantes import TipoMaterial
from dao.autor_dao import AutorDAO
from dao.categoria_dao import CategoriaDAO
from dao.libro_dao import LibroDAO
from ui.base import PestaniaBase
from validadores import validar_isbn, validar_texto_con_letras, validar_anio_edicion, validar_solo_letras


class PestaniaCatalogo(ttk.Frame):
    """Agrupa las tres sub-pestañas del catálogo en un Notebook interno."""

    def __init__(self, padre):
        super().__init__(padre)
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True)
        self.libros = PestaniaLibros(notebook)
        self.autores = PestaniaAutores(notebook)
        self.categorias = PestaniaCategorias(notebook)
        notebook.add(self.libros, text="Libros")
        notebook.add(self.autores, text="Autores")
        notebook.add(self.categorias, text="Categorías")

    def refrescar(self):
        self.libros.refrescar()
        self.autores.refrescar()
        self.categorias.refrescar()


class PestaniaLibros(PestaniaBase):
    CAMPOS = ['isbn', 'titulo', 'editorial', 'anio', 'idioma', 'tipo_material', 'categoria']

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = LibroDAO()
        self.autores_ids = []  # id de cada renglón del Listbox de autores

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        datos = ttk.Frame(formulario)
        datos.pack(side="left", anchor="n")
        self.crear_campo(datos, 'isbn', "ISBN / ISSN:", 0, validar_isbn)
        self.crear_campo(datos, 'titulo', "Título:", 1, lambda v: validar_texto_con_letras(v, "título", LARGO_TITULO))
        self.crear_campo(datos, 'editorial', "Editorial:", 2,
                         lambda v: validar_texto_con_letras(v, "editorial", LARGO_EDITORIAL))
        self.crear_campo(datos, 'anio', "Año de edición:", 3, validar_anio_edicion, numerico=True, ancho=10)
        self.crear_campo(datos, 'idioma', "Idioma:", 4, lambda v: validar_solo_letras(v, "idioma", 2, LARGO_IDIOMA))
        self.crear_combo(datos, 'tipo_material', "Tipo de material:", 5,
                         lambda: [(tipo, tipo) for tipo in TipoMaterial.TODOS])
        self.crear_combo(datos, 'categoria', "Categoría:", 6, CategoriaDAO().opciones)

        # Varios autores: Listbox (visto en clase) con selección múltiple.
        # selectmode="multiple" no figura en los apuntes, pero un libro puede
        # tener varios autores y un Combobox solo permite elegir uno.
        marco_autores = ttk.Frame(formulario)
        marco_autores.pack(side="left", anchor="n", padx=20)
        ttk.Label(marco_autores, text="Autores (clic para marcar uno o varios):").pack(anchor="w")
        self.lista_autores = tk.Listbox(marco_autores, selectmode="multiple", height=8, width=35,
                                        exportselection=False)
        self.lista_autores.pack()
        self.lista_autores.bind("<FocusIn>", lambda evento: self.recargar_autores())

        self.crear_botones(self, [("Eliminar", self.eliminar)]).pack(anchor="w", pady=10)
        marco, self.tabla = self.crear_tabla(self, [
            ('isbn', "ISBN/ISSN", 110), ('titulo', "Título", 220), ('autores', "Autores", 200),
            ('editorial', "Editorial", 120), ('anio', "Año", 50), ('tipo_material', "Tipo", 120),
            ('categoria', "Categoría", 100), ('ejemplares', "Ejemplares", 80)], alto=8)
        marco.pack(fill="both", expand=True)
        self.recargar_autores()
        self.refrescar()

    def recargar_autores(self):
        """Recarga la lista conservando los autores marcados."""
        marcados = self.autores_seleccionados()
        self.lista_autores.delete(0, tk.END)
        self.autores_ids = []
        for id, texto in AutorDAO().opciones():
            self.lista_autores.insert(tk.END, texto)
            self.autores_ids.append(id)
        self.marcar_autores(marcados)

    def autores_seleccionados(self):
        return [self.autores_ids[indice] for indice in self.lista_autores.curselection()]

    def marcar_autores(self, ids):
        for indice in range(len(self.autores_ids)):
            if self.autores_ids[indice] in ids:
                self.lista_autores.selection_set(indice)

    def campos_formulario(self):
        return self.CAMPOS

    def datos(self):
        return (self.valor('isbn'), self.valor('titulo'), self.valor('editorial'), self.valor('anio'),
                self.valor('idioma'), self.valor('tipo_material'), self.valor('categoria'),
                self.autores_seleccionados())

    def crear(self):
        self.dao.crear(*self.datos())

    def modificar(self, id):
        self.dao.modificar(id, *self.datos())

    def cargar_formulario(self, fila):
        for nombre in ['isbn', 'titulo', 'editorial', 'anio', 'idioma', 'tipo_material']:
            self.poner(nombre, fila[nombre])
        self.poner('categoria', fila['categoria_id'])
        self.recargar_autores()
        self.marcar_autores(fila['autores_ids'])

    def limpiar(self):
        super().limpiar()
        self.lista_autores.selection_clear(0, tk.END)

    def eliminar(self):
        self.accion_sobre_seleccion(self.dao.eliminar, "¿Eliminar el libro seleccionado?", "Libro eliminado")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)


class PestaniaAutores(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = AutorDAO()
        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_campo(formulario, 'nombre', "Nombre:", 0,
                         lambda v: validar_solo_letras(v, "nombre", 2, LARGO_NOMBRE_PERSONA))
        self.crear_campo(formulario, 'apellido', "Apellido:", 1,
                         lambda v: validar_solo_letras(v, "apellido", 2, LARGO_NOMBRE_PERSONA))
        self.crear_botones(self, [("Eliminar", self.eliminar)]).pack(anchor="w", pady=10)
        marco, self.tabla = self.crear_tabla(self, [
            ('apellido', "Apellido", 200), ('nombre', "Nombre", 200), ('libros', "Libros", 80)])
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def campos_formulario(self):
        return ['nombre', 'apellido']

    def crear(self):
        self.dao.crear(self.valor('nombre'), self.valor('apellido'))

    def modificar(self, id):
        self.dao.modificar(id, self.valor('nombre'), self.valor('apellido'))

    def cargar_formulario(self, fila):
        self.poner('nombre', fila['nombre'])
        self.poner('apellido', fila['apellido'])

    def eliminar(self):
        self.accion_sobre_seleccion(self.dao.eliminar, "¿Eliminar el autor seleccionado?", "Autor eliminado")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)


class PestaniaCategorias(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = CategoriaDAO()
        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_campo(formulario, 'nombre', "Nombre:", 0,
                         lambda v: validar_solo_letras(v, "nombre", 2, LARGO_NOMBRE_PERSONA))
        self.crear_botones(self, [("Eliminar", self.eliminar)]).pack(anchor="w", pady=10)
        marco, self.tabla = self.crear_tabla(self, [('nombre', "Nombre", 250), ('libros', "Libros", 80)])
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def campos_formulario(self):
        return ['nombre']

    def crear(self):
        self.dao.crear(self.valor('nombre'))

    def modificar(self, id):
        self.dao.modificar(id, self.valor('nombre'))

    def cargar_formulario(self, fila):
        self.poner('nombre', fila['nombre'])

    def eliminar(self):
        self.accion_sobre_seleccion(self.dao.eliminar, "¿Eliminar la categoría seleccionada?",
                                    "Categoría eliminada")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
