from datetime import date

import pytest

from constantes import TipoPrestamo
from modelos.prestamo import Multa
from patrones.estrategia_prestamo import (EstrategiaPrestamo, EstrategiaPrestamoLocal,
                                          EstrategiaPrestamoInterbibliotecario, ESTRATEGIAS)
import tests.auxiliares  # registra todos los modelos


class TestEstrategiaLocal:
    def test_vencimiento_31_dias(self):
        estrategia = EstrategiaPrestamoLocal()
        assert estrategia.calcular_vencimiento(date(2026, 1, 1)) == date(2026, 2, 1)
        # Cruza fin de año
        assert estrategia.calcular_vencimiento(date(2026, 12, 15)) == date(2027, 1, 15)

    def test_multa_100_por_dia(self):
        estrategia = EstrategiaPrestamoLocal()
        for dias, monto in [(1, 100.0), (3, 300.0), (10, 1000.0)]:
            assert estrategia.calcular_multa(dias) == monto

    def test_sin_atraso_no_hay_multa(self):
        for dias in [0, -1, -30]:
            assert EstrategiaPrestamoLocal().calcular_multa(dias) == 0.0


class TestEstrategiaInterbibliotecario:
    def test_vencimiento_38_dias(self):
        estrategia = EstrategiaPrestamoInterbibliotecario()
        assert estrategia.calcular_vencimiento(date(2026, 1, 1)) == date(2026, 2, 8)

    def test_multa_150_por_dia(self):
        estrategia = EstrategiaPrestamoInterbibliotecario()
        for dias, monto in [(1, 150.0), (3, 450.0)]:
            assert estrategia.calcular_multa(dias) == monto

    def test_sin_atraso_no_hay_multa(self):
        assert EstrategiaPrestamoInterbibliotecario().calcular_multa(0) == 0.0


class TestSeleccionExterna:
    def test_diccionario_por_tipo(self):
        assert isinstance(ESTRATEGIAS[TipoPrestamo.LOCAL], EstrategiaPrestamoLocal)
        assert isinstance(ESTRATEGIAS[TipoPrestamo.INTERBIBLIOTECARIO], EstrategiaPrestamoInterbibliotecario)

    def test_la_clase_abstracta_no_se_instancia(self):
        with pytest.raises(TypeError):
            EstrategiaPrestamo()

    def test_misma_multa_distinta_estrategia(self):
        """La Multa no elige: calcula con la estrategia que recibe."""
        for tipo, monto in [(TipoPrestamo.LOCAL, 500.0), (TipoPrestamo.INTERBIBLIOTECARIO, 750.0)]:
            assert Multa(dias_atraso=5).calcular_monto(ESTRATEGIAS[tipo]) == monto
