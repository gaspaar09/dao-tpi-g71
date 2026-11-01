"""Acceso a datos de libros (títulos del catálogo)."""

from config import LARGO_TITULO, LARGO_EDITORIAL, LARGO_IDIOMA
from constantes import TipoMaterial
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.catalogo import Libro, Autor, Categoria
from modelos.reserva import Reserva
from validadores import validar_isbn, validar_texto_con_letras, validar_solo_letras, validar_anio_edicion, validar_opcion


def validar_datos_libro(isbn, titulo, editorial, anio, idioma, tipo_material, autores_ids):
    isbn = validar_isbn(isbn)
    titulo = validar_texto_con_letras(titulo, "título", LARGO_TITULO)
    editorial = validar_texto_con_letras(editorial, "editorial", LARGO_EDITORIAL)
    anio = validar_anio_edicion(anio)
    idioma = validar_solo_letras(idioma, "idioma", 2, LARGO_IDIOMA)
    tipo_material = validar_opcion(tipo_material, TipoMaterial.TODOS, "tipo de material")
    if not autores_ids:
        raise ValidacionError("Seleccione al menos un autor")
    return isbn, titulo, editorial, anio, idioma, tipo_material


class LibroDAO:
    """Operaciones de acceso a datos sobre libros."""

    def verificar_isbn_unico(self, session, isbn, id_actual=None):
        libro = session.query(Libro).filter_by(isbn=isbn).first()
        if libro is not None and libro.id != id_actual:
            raise ReglaNegocioError(f"Ya existe un título con el ISBN/ISSN {isbn}: {libro.titulo}")

    def buscar_autores(self, session, autores_ids):
        return [buscar_por_id(session, Autor, autor_id, "el autor") for autor_id in autores_ids]

    def crear(self, isbn, titulo, editorial, anio, idioma, tipo_material, categoria_id, autores_ids):
        datos = validar_datos_libro(isbn, titulo, editorial, anio, idioma, tipo_material, autores_ids)
        isbn, titulo, editorial, anio, idioma, tipo_material = datos
        with obtener_session() as session:
            categoria = buscar_por_id(session, Categoria, categoria_id, "la categoría")
            autores = self.buscar_autores(session, autores_ids)
            self.verificar_isbn_unico(session, isbn)
            libro = Libro(isbn=isbn, titulo=titulo, editorial=editorial, anio_edicion=anio,
                          idioma=idioma, tipo_material=tipo_material, categoria=categoria)
            libro.autores.extend(autores)
            session.add(libro)

    def modificar(self, id, isbn, titulo, editorial, anio, idioma, tipo_material, categoria_id, autores_ids):
        datos = validar_datos_libro(isbn, titulo, editorial, anio, idioma, tipo_material, autores_ids)
        isbn, titulo, editorial, anio, idioma, tipo_material = datos
        with obtener_session() as session:
            libro = buscar_por_id(session, Libro, id, "el libro")
            categoria = buscar_por_id(session, Categoria, categoria_id, "la categoría")
            autores = self.buscar_autores(session, autores_ids)
            self.verificar_isbn_unico(session, isbn, id_actual=libro.id)
            libro.isbn = isbn
            libro.titulo = titulo
            libro.editorial = editorial
            libro.anio_edicion = anio
            libro.idioma = idioma
            libro.tipo_material = tipo_material
            libro.categoria = categoria
            libro.autores = autores

    def eliminar(self, id):
        with obtener_session() as session:
            libro = buscar_por_id(session, Libro, id, "el libro")
            if len(libro.ejemplares) > 0:
                raise ReglaNegocioError(f"No se puede eliminar: {libro.titulo} tiene ejemplares")
            if session.query(Reserva).filter_by(libro_id=libro.id).first() is not None:
                raise ReglaNegocioError(f"No se puede eliminar: {libro.titulo} tiene reservas")
            session.delete(libro)

    def listar(self):
        with obtener_session() as session:
            libros = session.query(Libro).order_by(Libro.titulo).all()
            return [
                {
                    'id': libro.id,
                    'isbn': libro.isbn,
                    'titulo': libro.titulo,
                    'autores': ', '.join([str(autor) for autor in libro.autores]),
                    'autores_ids': [autor.id for autor in libro.autores],
                    'editorial': libro.editorial,
                    'anio': libro.anio_edicion,
                    'idioma': libro.idioma,
                    'tipo_material': libro.tipo_material,
                    'categoria': libro.categoria.nombre,
                    'categoria_id': libro.categoria_id,
                    'ejemplares': len(libro.ejemplares),
                }
                for libro in libros
            ]

    def opciones(self):
        with obtener_session() as session:
            libros = session.query(Libro).order_by(Libro.titulo).all()
            return [(libro.id, f"{libro.titulo} ({libro.isbn})") for libro in libros]
