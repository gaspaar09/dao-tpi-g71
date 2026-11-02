import pytest

from constantes import DiaSemana, EstadoEjemplar, EstadoFisico, TipoMaterial
from dao.autor_dao import AutorDAO
from dao.categoria_dao import CategoriaDAO
from dao.ejemplar_dao import EjemplarDAO
from dao.libro_dao import LibroDAO
from dao.sede_dao import SedeDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.ejemplar import Ejemplar
from tests.auxiliares import preparar_base_en_memoria

dao = EjemplarDAO()


def preparar():
    """Base con una sede y un libro; devuelve (libro_id, sede_id)."""
    preparar_base_en_memoria()
    SedeDAO().crear("Central", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")])
    CategoriaDAO().crear("Novela")
    AutorDAO().crear("Julio", "Cortázar")
    LibroDAO().crear("9789500700011", "Rayuela", "Sudamericana", "1963", "Español", TipoMaterial.LIBRO,
                     CategoriaDAO().opciones()[0][0], [AutorDAO().opciones()[0][0]])
    return LibroDAO().opciones()[0][0], SedeDAO().opciones()[0][0]


class TestAltaEjemplar:
    def test_alta_disponible(self):
        libro_id, sede_id = preparar()
        dao.crear(" ej-001 ", libro_id, sede_id, EstadoFisico.NUEVO)
        ejemplar = dao.listar()[0]
        assert ejemplar['codigo_inventario'] == "EJ-001"
        assert ejemplar['estado'] == EstadoEjemplar.DISPONIBLE
        assert (ejemplar['libro'], ejemplar['sede']) == ("Rayuela", "Central")

    def test_datos_invalidos(self):
        libro_id, sede_id = preparar()
        casos = [("", libro_id, sede_id, EstadoFisico.NUEVO),
                 ("EJ_001", libro_id, sede_id, EstadoFisico.NUEVO),
                 ("EJ", libro_id, sede_id, EstadoFisico.NUEVO),
                 ("EJ-001", None, sede_id, EstadoFisico.NUEVO),
                 ("EJ-001", libro_id, None, EstadoFisico.NUEVO),
                 ("EJ-001", libro_id, sede_id, "ROTO")]
        for caso in casos:
            with pytest.raises(ValidacionError):
                dao.crear(*caso)

    def test_codigo_duplicado(self):
        libro_id, sede_id = preparar()
        dao.crear("EJ-001", libro_id, sede_id, EstadoFisico.NUEVO)
        with pytest.raises(ReglaNegocioError, match="Ya existe un ejemplar"):
            dao.crear("ej-001", libro_id, sede_id, EstadoFisico.BUENO)

    def test_sede_de_baja(self):
        libro_id, sede_id = preparar()
        SedeDAO().dar_de_baja(sede_id)
        with pytest.raises(ReglaNegocioError, match="dada de baja"):
            dao.crear("EJ-001", libro_id, sede_id, EstadoFisico.NUEVO)


class TestModificarYBajaEjemplar:
    def test_modificar_estado_fisico(self):
        libro_id, sede_id = preparar()
        dao.crear("EJ-001", libro_id, sede_id, EstadoFisico.NUEVO)
        dao.modificar(dao.listar()[0]['id'], EstadoFisico.REGULAR)
        assert dao.listar()[0]['estado_fisico'] == EstadoFisico.REGULAR

    def test_baja(self):
        libro_id, sede_id = preparar()
        dao.crear("EJ-001", libro_id, sede_id, EstadoFisico.NUEVO)
        ejemplar_id = dao.listar()[0]['id']
        dao.dar_de_baja(ejemplar_id)
        assert dao.listar()[0]['estado'] == EstadoEjemplar.BAJA
        with pytest.raises(ReglaNegocioError, match="ya está dado de baja"):
            dao.dar_de_baja(ejemplar_id)

    def test_no_se_da_de_baja_si_esta_comprometido(self):
        libro_id, sede_id = preparar()
        dao.crear("EJ-001", libro_id, sede_id, EstadoFisico.NUEVO)
        ejemplar_id = dao.listar()[0]['id']
        for estado in [EstadoEjemplar.PRESTADO, EstadoEjemplar.RESERVADO, EstadoEjemplar.EN_TRANSITO]:
            with obtener_session() as session:
                session.query(Ejemplar).filter_by(id=ejemplar_id).first().estado = estado
            with pytest.raises(ReglaNegocioError, match="No se puede dar de baja"):
                dao.dar_de_baja(ejemplar_id)
