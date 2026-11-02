"""Pestaña de Catálogo: sub-pestañas de Libros, Autores y Categorías."""

import tkinter as tk
# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk

from config import LARGO_TITULO, LARGO_EDITORIAL, LARGO_IDIOMA, LARGO_NOMBRE_PERSONA
from constantes import TipoMaterial
from dao.autor_dao import AutorDAO
from dao.categoria_dao import CategoriaDAO
from dao.libro_dao import LibroDAO
from ui.base import PestaniaBase, ICONO_EDITAR, ICONO_BAJA
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

    def avisar_cambios_a(self, funcion):
        # Mismo método que PestaniaBase (polimorfismo): main.py no necesita
        # saber que esta pestaña tiene sub-pestañas
        self.libros.avisar_cambios_a(funcion)
        self.autores.avisar_cambios_a(funcion)
        self.categorias.avisar_cambios_a(funcion)


class PestaniaLibros(PestaniaBase):
    TITULO_NUEVO = "Nuevo título"
    TITULO_EDITAR = "Editar título"
    CAMPOS = ['isbn', 'titulo', 'editorial', 'anio', 'idioma', 'tipo_material', 'categoria']

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = LibroDAO()
        self.autores_ids = []  # id de cada renglón del Listbox de autores
        self.crear_encabezado("Libros, revistas y material de consulta",
                              "Títulos del catálogo; las copias físicas se cargan en Ejemplares",
                              [("Nuevo título", self.nuevo, True)])
        self.crear_barra_seleccion("Con el título elegido:", [])
        self.crear_tabla_principal(self, [
            ('isbn', "ISBN/ISSN", 120), ('titulo', "Título", 250), ('autores', "Autores", 230),
            ('editorial', "Editorial", 130), ('anio', "Año", 60), ('tipo_material', "Tipo", 140),
            ('categoria', "Categoría", 110), ('ejemplares', "Ejemplares", 90)],
            doble_clic=self.editar_seleccionado,
            iconos=[(ICONO_EDITAR, self.editar_seleccionado), (ICONO_BAJA, self.eliminar)]).pack(fill="both", expand=True)
        self.refrescar()

    def armar_formulario(self, contenedor):
        datos = ttk.Frame(contenedor)
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
        marco_autores = ttk.Frame(contenedor)
        marco_autores.pack(side="left", anchor="n", padx=(24, 0))
        ttk.Label(marco_autores, text="Autores").pack(anchor="w")
        ttk.Label(marco_autores, text="Clic para marcar uno o varios", bootstyle="secondary").pack(anchor="w")
        self.lista_autores = tk.Listbox(marco_autores, selectmode="multiple", height=12, width=32,
                                        exportselection=False)
        self.lista_autores.pack(pady=(4, 0))
        self.recargar_autores()

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
        if not self.autores_ids:
            return []
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
        self.marcar_autores(fila['autores_ids'])

    def eliminar(self):
        self.accion_sobre_seleccion(self.dao.eliminar, "¿Eliminar el título seleccionado?", "Título eliminado")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)


class PestaniaAutores(PestaniaBase):
    TITULO_NUEVO = "Nuevo autor"
    TITULO_EDITAR = "Editar autor"

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = AutorDAO()
        self.crear_encabezado("Autores", "Personas que escribieron los títulos del catálogo",
                              [("Nuevo autor", self.nuevo, True)])
        self.crear_barra_seleccion("Con el autor elegido:", [])
        self.crear_tabla_principal(self, [
            ('apellido', "Apellido", 220), ('nombre', "Nombre", 220), ('libros', "Títulos", 90)],
            doble_clic=self.editar_seleccionado,
            iconos=[(ICONO_EDITAR, self.editar_seleccionado), (ICONO_BAJA, self.eliminar)]).pack(fill="both", expand=True)
        self.refrescar()

    def armar_formulario(self, contenedor):
        self.crear_campo(contenedor, 'nombre', "Nombre:", 0,
                         lambda v: validar_solo_letras(v, "nombre", 2, LARGO_NOMBRE_PERSONA))
        self.crear_campo(contenedor, 'apellido', "Apellido:", 1,
                         lambda v: validar_solo_letras(v, "apellido", 2, LARGO_NOMBRE_PERSONA))

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
    TITULO_NUEVO = "Nueva categoría"
    TITULO_EDITAR = "Editar categoría"

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = CategoriaDAO()
        self.crear_encabezado("Categorías", "Temas con los que se clasifica cada título",
                              [("Nueva categoría", self.nuevo, True)])
        self.crear_barra_seleccion("Con la categoría elegida:", [])
        self.crear_tabla_principal(self, [('nombre', "Nombre", 260), ('libros', "Títulos", 90)],
                                   doble_clic=self.editar_seleccionado,
            iconos=[(ICONO_EDITAR, self.editar_seleccionado), (ICONO_BAJA, self.eliminar)]).pack(fill="both", expand=True)
        self.refrescar()

    def armar_formulario(self, contenedor):
        self.crear_campo(contenedor, 'nombre', "Nombre:", 0,
                         lambda v: validar_solo_letras(v, "nombre", 2, LARGO_NOMBRE_PERSONA))

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
