"""Tests de AutorDAO, CategoriaDAO y LibroDAO (el catálogo)."""

from datetime import date

import pytest

from constantes import DiaSemana, EstadoFisico, TipoMaterial
from dao.autor_dao import AutorDAO
from dao.categoria_dao import CategoriaDAO
from dao.ejemplar_dao import EjemplarDAO
from dao.libro_dao import LibroDAO
from dao.sede_dao import SedeDAO
from excepciones import ValidacionError, ReglaNegocioError
from tests.auxiliares import preparar_base_en_memoria

autor_dao = AutorDAO()
categoria_dao = CategoriaDAO()
libro_dao = LibroDAO()


def preparar_catalogo():
    """Base con una categoría y un autor; devuelve sus ids."""
    preparar_base_en_memoria()
    categoria_dao.crear("Novela")
    autor_dao.crear("Julio", "Cortázar")
    return categoria_dao.opciones()[0][0], autor_dao.opciones()[0][0]


def crear_libro(categoria_id, autor_id, isbn="978-950-07-0001-1"):
    libro_dao.crear(isbn, "Rayuela", "Sudamericana", "1963", "Español", TipoMaterial.LIBRO,
                    categoria_id, [autor_id])
    return libro_dao.listar()[-1]['id']


class TestAutores:
    def test_alta_y_duplicado(self):
        preparar_base_en_memoria()
        autor_dao.crear("Jorge Luis", "Borges")
        assert autor_dao.opciones()[0][1] == "Borges, Jorge Luis"
        with pytest.raises(ReglaNegocioError, match="ya existe"):
            autor_dao.crear(" jorge  luis ", "BORGES")

    def test_nombres_invalidos(self):
        preparar_base_en_memoria()
        for nombre, apellido in [("", "Borges"), ("Jorge", "B0rges"), ("<script>", "Borges")]:
            with pytest.raises(ValidacionError):
                autor_dao.crear(nombre, apellido)

    def test_no_se_elimina_con_libros(self):
        categoria_id, autor_id = preparar_catalogo()
        crear_libro(categoria_id, autor_id)
        with pytest.raises(ReglaNegocioError, match="tiene libros"):
            autor_dao.eliminar(autor_id)


class TestCategorias:
    def test_alta_modificar_y_eliminar(self):
        preparar_base_en_memoria()
        categoria_dao.crear("Novela")
        categoria_id = categoria_dao.opciones()[0][0]
        categoria_dao.modificar(categoria_id, "Novela histórica")
        assert categoria_dao.listar()[0]['nombre'] == "Novela Histórica"  # se capitaliza
        categoria_dao.eliminar(categoria_id)
        assert categoria_dao.listar() == []

    def test_duplicada_sin_mayusculas(self):
        preparar_base_en_memoria()
        categoria_dao.crear("Novela")
        with pytest.raises(ReglaNegocioError, match="ya existe"):
            categoria_dao.crear("  NOVELA ")

    def test_no_se_elimina_con_libros(self):
        categoria_id, autor_id = preparar_catalogo()
        crear_libro(categoria_id, autor_id)
        with pytest.raises(ReglaNegocioError, match="tiene libros"):
            categoria_dao.eliminar(categoria_id)


class TestLibros:
    def test_alta(self):
        categoria_id, autor_id = preparar_catalogo()
        crear_libro(categoria_id, autor_id)
        libro = libro_dao.listar()[0]
        assert libro['isbn'] == "9789500700011"
        assert libro['autores'] == "Julio Cortázar"
        assert libro['categoria'] == "Novela"
        assert libro['ejemplares'] == 0  # un título puede no tener ejemplares

    def test_guion_de_defensa(self):
        """Guion 3 de VALIDACIONES.md: año -1, 3000, 'dos mil' e ISBN repetido."""
        categoria_id, autor_id = preparar_catalogo()
        for anio in ["-1", "3000", "dos mil", str(date.today().year + 1)]:
            with pytest.raises(ValidacionError, match="año de edición"):
                libro_dao.crear("9789500700011", "Rayuela", "Sudamericana", anio, "Español",
                                TipoMaterial.LIBRO, categoria_id, [autor_id])
        crear_libro(categoria_id, autor_id, "978-950-07-0001-1")
        with pytest.raises(ReglaNegocioError, match="Ya existe un título"):
            crear_libro(categoria_id, autor_id, "9789500700011")

    def test_textos_solo_numericos(self):
        categoria_id, autor_id = preparar_catalogo()
        casos = [("123", "Sudamericana", "Español", "título"),
                 ("Rayuela", "999", "Español", "editorial"),
                 ("Rayuela", "Sudamericana", "123", "idioma"),
                 ("Rayuela", "Sudamericana", "Esp4ñol", "idioma")]
        for titulo, editorial, idioma, campo in casos:
            with pytest.raises(ValidacionError, match=campo):
                libro_dao.crear("9789500700011", titulo, editorial, "1963", idioma,
                                TipoMaterial.LIBRO, categoria_id, [autor_id])
        with pytest.raises(ValidacionError, match="solo puede tener letras"):
            categoria_dao.crear("12345")

    def test_requiere_autor_categoria_y_tipo(self):
        categoria_id, autor_id = preparar_catalogo()
        with pytest.raises(ValidacionError, match="al menos un autor"):
            libro_dao.crear("9789500700011", "Rayuela", "Sudamericana", "1963", "Español",
                            TipoMaterial.LIBRO, categoria_id, [])
        with pytest.raises(ValidacionError, match="tipo de material"):
            libro_dao.crear("9789500700011", "Rayuela", "Sudamericana", "1963", "Español",
                            "PELICULA", categoria_id, [autor_id])
        with pytest.raises(ValidacionError, match="categoría"):
            libro_dao.crear("9789500700011", "Rayuela", "Sudamericana", "1963", "Español",
                            TipoMaterial.LIBRO, None, [autor_id])
        with pytest.raises(ReglaNegocioError, match="autor"):
            libro_dao.crear("9789500700011", "Rayuela", "Sudamericana", "1963", "Español",
                            TipoMaterial.LIBRO, categoria_id, [99])

    def test_modificar_autores(self):
        categoria_id, autor_id = preparar_catalogo()
        autor_dao.crear("Jorge Luis", "Borges")
        borges_id = autor_dao.opciones()[0][0]
        libro_id = crear_libro(categoria_id, autor_id)
        libro_dao.modificar(libro_id, "9789500700011", "Rayuela", "Alfaguara", "1963", "Español",
                            TipoMaterial.LIBRO, categoria_id, [autor_id, borges_id])
        libro = libro_dao.listar()[0]
        assert libro['editorial'] == "Alfaguara"
        assert sorted(libro['autores_ids']) == sorted([autor_id, borges_id])

    def test_no_se_elimina_con_ejemplares(self):
        categoria_id, autor_id = preparar_catalogo()
        libro_id = crear_libro(categoria_id, autor_id)
        SedeDAO().crear("Central", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")])
        EjemplarDAO().crear("EJ-001", libro_id, SedeDAO().opciones()[0][0], EstadoFisico.NUEVO)
        with pytest.raises(ReglaNegocioError, match="tiene ejemplares"):
            libro_dao.eliminar(libro_id)
