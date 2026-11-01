"""Acceso a datos de categorías."""

from config import LARGO_NOMBRE_PERSONA
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.catalogo import Categoria
from validadores import validar_solo_letras


class CategoriaDAO:
    """Operaciones de acceso a datos sobre categorías."""

    def verificar_nombre_unico(self, session, nombre, id_actual=None):
        for categoria in session.query(Categoria).all():
            if categoria.nombre.lower() == nombre.lower() and categoria.id != id_actual:
                raise ReglaNegocioError(f"La categoría {categoria.nombre} ya existe")

    def crear(self, nombre):
        nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_PERSONA)
        with obtener_session() as session:
            self.verificar_nombre_unico(session, nombre)
            session.add(Categoria(nombre=nombre))

    def modificar(self, id, nombre):
        nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_PERSONA)
        with obtener_session() as session:
            categoria = buscar_por_id(session, Categoria, id, "la categoría")
            self.verificar_nombre_unico(session, nombre, id_actual=categoria.id)
            categoria.nombre = nombre

    def eliminar(self, id):
        with obtener_session() as session:
            categoria = buscar_por_id(session, Categoria, id, "la categoría")
            if len(categoria.libros) > 0:
                raise ReglaNegocioError(f"No se puede eliminar: la categoría {categoria.nombre} tiene libros")
            session.delete(categoria)

    def listar(self):
        with obtener_session() as session:
            categorias = session.query(Categoria).order_by(Categoria.nombre).all()
            return [
                {'id': categoria.id, 'nombre': categoria.nombre, 'libros': len(categoria.libros)}
                for categoria in categorias
            ]

    def opciones(self):
        with obtener_session() as session:
            categorias = session.query(Categoria).order_by(Categoria.nombre).all()
            return [(categoria.id, categoria.nombre) for categoria in categorias]
