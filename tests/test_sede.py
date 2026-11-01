import pytest

from constantes import EstadoSede
from excepciones import ReglaNegocioError
from tests.auxiliares import crear_sede


class TestSede:
    def test_sede_nueva_esta_activa(self):
        assert crear_sede().esta_activa()

    def test_dar_de_baja(self):
        sede = crear_sede()
        sede.dar_de_baja()
        assert sede.estado == EstadoSede.BAJA
        assert not sede.esta_activa()

    def test_no_se_da_de_baja_dos_veces(self):
        sede = crear_sede()
        sede.dar_de_baja()
        with pytest.raises(ReglaNegocioError, match="ya está dada de baja"):
            sede.dar_de_baja()

    def test_reactivar(self):
        sede = crear_sede()
        sede.dar_de_baja()
        sede.reactivar()
        assert sede.esta_activa()

    def test_no_se_reactiva_una_activa(self):
        with pytest.raises(ReglaNegocioError, match="ya está activa"):
            crear_sede().reactivar()
