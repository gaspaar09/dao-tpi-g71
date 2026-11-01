from dao.ejemplar_dao import EjemplarDAO
from dao.empleado_dao import EmpleadoDAO
from dao.libro_dao import LibroDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from datos_ejemplo import cargar_datos_ejemplo
from tests.auxiliares import preparar_base_en_memoria


class TestDatosEjemplo:
    def test_carga_una_sola_vez(self):
        preparar_base_en_memoria()
        assert cargar_datos_ejemplo() is True
        assert cargar_datos_ejemplo() is False
        assert len(SedeDAO().listar()) == 3

    def test_datos_coherentes(self):
        preparar_base_en_memoria()
        cargar_datos_ejemplo()
        assert len(EmpleadoDAO().listar()) == 3
        assert len(SocioDAO().listar()) == 4
        assert len(SocioDAO().opciones()) == 3  # uno está inhabilitado
        assert len(LibroDAO().listar()) == 5
        assert len(EjemplarDAO().listar()) == 10
