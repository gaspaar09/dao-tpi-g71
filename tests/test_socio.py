import pytest

from constantes import EstadoSocio
from excepciones import ReglaNegocioError
from tests.auxiliares import crear_socio


class TestSocio:
    def test_socio_activo_esta_habilitado(self):
        assert crear_socio().esta_habilitado()

    def test_socio_no_activo_no_esta_habilitado(self):
        for estado in [EstadoSocio.INHABILITADO, EstadoSocio.BAJA]:
            assert not crear_socio(estado).esta_habilitado()

    def test_inhabilitar(self):
        socio = crear_socio()
        socio.inhabilitar()
        assert socio.estado == EstadoSocio.INHABILITADO

    def test_no_se_inhabilita_un_socio_no_activo(self):
        for estado in [EstadoSocio.INHABILITADO, EstadoSocio.BAJA]:
            with pytest.raises(ReglaNegocioError, match="no está activo"):
                crear_socio(estado).inhabilitar()
