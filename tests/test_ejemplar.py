import pytest

from constantes import EstadoEjemplar, EstadoFisico
from excepciones import ValidacionError
from tests.auxiliares import crear_ejemplar, crear_sede


class TestEjemplar:
    def test_disponible(self):
        assert crear_ejemplar(crear_sede()).esta_disponible()

    def test_no_disponible_en_otros_estados(self):
        for estado in EstadoEjemplar.TODOS:
            if estado != EstadoEjemplar.DISPONIBLE:
                assert not crear_ejemplar(crear_sede(), estado).esta_disponible()

    def test_cambiar_estado_valido(self):
        ejemplar = crear_ejemplar(crear_sede())
        ejemplar.cambiar_estado(EstadoEjemplar.PRESTADO)
        assert ejemplar.estado == EstadoEjemplar.PRESTADO

    def test_cambiar_estado_invalido(self):
        ejemplar = crear_ejemplar(crear_sede())
        for valor in ["", "prestado", "PERDIDO", None]:
            with pytest.raises(ValidacionError, match="Estado de ejemplar inválido"):
                ejemplar.cambiar_estado(valor)
        assert ejemplar.estado == EstadoEjemplar.DISPONIBLE


class TestVolverACircular:
    def test_segun_el_estado_fisico(self):
        casos = [(EstadoFisico.NUEVO, EstadoEjemplar.DISPONIBLE), (EstadoFisico.BUENO, EstadoEjemplar.DISPONIBLE),
                 (EstadoFisico.REGULAR, EstadoEjemplar.DISPONIBLE), (EstadoFisico.DANADO, EstadoEjemplar.DANADO),
                 (EstadoFisico.DESTRUIDO, EstadoEjemplar.BAJA)]
        for estado_fisico, esperado in casos:
            ejemplar = crear_ejemplar(crear_sede(), EstadoEjemplar.PRESTADO)
            ejemplar.estado_fisico = estado_fisico
            ejemplar.volver_a_circular()
            assert ejemplar.estado == esperado
