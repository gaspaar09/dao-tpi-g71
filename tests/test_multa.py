from modelos.prestamo import Multa
from tests.auxiliares import EstrategiaDePrueba


class TestMulta:
    def test_calcula_monto_con_la_estrategia_recibida(self):
        multa = Multa(dias_atraso=3)
        assert multa.calcular_monto(EstrategiaDePrueba(31, 100)) == 300
        assert multa.monto == 300

    def test_misma_multa_distinta_estrategia(self):
        multa = Multa(dias_atraso=3)
        assert multa.calcular_monto(EstrategiaDePrueba(38, 150)) == 450

    def test_atraso_cero(self):
        multa = Multa(dias_atraso=0)
        assert multa.calcular_monto(EstrategiaDePrueba(31, 100)) == 0

    def test_redondea_a_dos_decimales(self):
        multa = Multa(dias_atraso=3)
        assert multa.calcular_monto(EstrategiaDePrueba(31, 0.333)) == 1.0
