import pytest

from constantes import EstadoPrestamo, EstadoSocio, TipoPrestamo
from dao.socio_dao import SocioDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.prestamo import Prestamo
from tests.auxiliares import preparar_base_en_memoria, crear_sede, crear_ejemplar

dao = SocioDAO()


def crear_socio(nro="1", dni="30111222"):
    dao.crear(nro, dni, "Ana", "Martínez", "ana@example.com", "351 5550001")
    return dao.listar()[-1]['id']


class TestAltaSocio:
    def test_alta_normaliza(self):
        preparar_base_en_memoria()
        dao.crear(" 15 ", "30.111.222", "  Ana  María ", "Martínez", "", "351 5550001")
        socio = dao.listar()[0]
        assert socio['nro_socio'] == 15
        assert socio['dni'] == "30111222"
        assert socio['nombre'] == "Ana María"
        assert socio['estado'] == EstadoSocio.ACTIVO

    def test_guion_de_defensa(self):
        """Guion 1 y 2 de VALIDACIONES.md."""
        preparar_base_en_memoria()
        dnis_invalidos = ["abc", "-5", "1234567890123", ""]
        for dni in dnis_invalidos:
            with pytest.raises(ValidacionError, match="DNI"):
                dao.crear("1", dni, "Ana", "Martínez", "", "351 5550001")
        for nombre in ["", "Ana123", "a" * 200]:
            with pytest.raises(ValidacionError, match="nombre"):
                dao.crear("1", "30111222", nombre, "Martínez", "", "351 5550001")
        for nro in ["-1", "0", "abc", "1.5"]:
            with pytest.raises(ValidacionError, match="número de socio"):
                dao.crear(nro, "30111222", "Ana", "Martínez", "", "351 5550001")
        assert dao.listar() == []

    def test_duplicados(self):
        preparar_base_en_memoria()
        crear_socio("1", "30111222")
        with pytest.raises(ReglaNegocioError, match="DNI 30111222"):
            crear_socio("2", " 30.111.222 ")
        with pytest.raises(ReglaNegocioError, match="número 1"):
            crear_socio("1", "28333444")


class TestEstadosDelSocio:
    def test_inhabilitar_y_habilitar(self):
        preparar_base_en_memoria()
        socio_id = crear_socio()
        dao.inhabilitar(socio_id)
        assert dao.listar()[0]['estado'] == EstadoSocio.INHABILITADO
        assert dao.opciones() == []
        dao.habilitar(socio_id)
        assert dao.listar()[0]['estado'] == EstadoSocio.ACTIVO

    def test_habilitar_solo_inhabilitados(self):
        preparar_base_en_memoria()
        socio_id = crear_socio()
        with pytest.raises(ReglaNegocioError, match="Solo se puede habilitar"):
            dao.habilitar(socio_id)
        dao.dar_de_baja(socio_id)
        with pytest.raises(ReglaNegocioError, match="Solo se puede habilitar"):
            dao.habilitar(socio_id)

    def test_baja(self):
        preparar_base_en_memoria()
        socio_id = crear_socio()
        dao.dar_de_baja(socio_id)
        assert dao.listar()[0]['estado'] == EstadoSocio.BAJA
        with pytest.raises(ReglaNegocioError, match="ya está dado de baja"):
            dao.dar_de_baja(socio_id)

    def test_no_se_da_de_baja_con_prestamos_en_curso(self):
        preparar_base_en_memoria()
        socio_id = crear_socio()
        with obtener_session() as session:
            sede = crear_sede()
            session.add(Prestamo(tipo=TipoPrestamo.LOCAL, estado=EstadoPrestamo.ACTIVO, socio_id=socio_id,
                                 ejemplar=crear_ejemplar(sede), sede_origen=sede, sede_destino=sede))
        with pytest.raises(ReglaNegocioError, match="préstamos en curso"):
            dao.dar_de_baja(socio_id)


class TestModificarSocio:
    def test_modificar(self):
        preparar_base_en_memoria()
        socio_id = crear_socio("1", "30111222")
        dao.modificar(socio_id, "1", "30111222", "Ana", "Paz", "", "351 5550009")
        socio = dao.listar()[0]
        assert (socio['apellido'], socio['telefono'], socio['email']) == ("Paz", "351 5550009", "")

    def test_modificar_con_dni_de_otro(self):
        preparar_base_en_memoria()
        crear_socio("1", "30111222")
        otro_id = crear_socio("2", "28333444")
        with pytest.raises(ReglaNegocioError, match="DNI"):
            dao.modificar(otro_id, "2", "30111222", "Ana", "Paz", "", "351 5550009")
