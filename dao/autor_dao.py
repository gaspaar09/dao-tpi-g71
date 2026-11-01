"""Acceso a datos de autores."""

from config import LARGO_NOMBRE_PERSONA
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.catalogo import Autor
from validadores import validar_solo_letras


class AutorDAO:
    """Operaciones de acceso a datos sobre autores."""

    def verificar_duplicado(self, session, nombre, apellido, id_actual=None):
        # Duplicado = mismo nombre y apellido sin distinguir mayúsculas
        for autor in session.query(Autor).all():
            if (autor.nombre.lower() == nombre.lower() and autor.apellido.lower() == apellido.lower()
                    and autor.id != id_actual):
                raise ReglaNegocioError(f"El autor {autor} ya existe")

    def crear(self, nombre, apellido):
        nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_PERSONA)
        apellido = validar_solo_letras(apellido, "apellido", 2, LARGO_NOMBRE_PERSONA)
        with obtener_session() as session:
            self.verificar_duplicado(session, nombre, apellido)
            session.add(Autor(nombre=nombre, apellido=apellido))

    def modificar(self, id, nombre, apellido):
        nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_PERSONA)
        apellido = validar_solo_letras(apellido, "apellido", 2, LARGO_NOMBRE_PERSONA)
        with obtener_session() as session:
            autor = buscar_por_id(session, Autor, id, "el autor")
            self.verificar_duplicado(session, nombre, apellido, id_actual=autor.id)
            autor.nombre = nombre
            autor.apellido = apellido

    def eliminar(self, id):
        with obtener_session() as session:
            autor = buscar_por_id(session, Autor, id, "el autor")
            if len(autor.libros) > 0:
                raise ReglaNegocioError(f"No se puede eliminar: {autor} tiene libros en el catálogo")
            session.delete(autor)

    def listar(self):
        with obtener_session() as session:
            autores = session.query(Autor).order_by(Autor.apellido).all()
            return [
                {
                    'id': autor.id,
                    'nombre': autor.nombre,
                    'apellido': autor.apellido,
                    'libros': len(autor.libros),
                }
                for autor in autores
            ]

    def opciones(self):
        with obtener_session() as session:
            autores = session.query(Autor).order_by(Autor.apellido).all()
            return [(autor.id, f"{autor.apellido}, {autor.nombre}") for autor in autores]
