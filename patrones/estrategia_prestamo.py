"""Patrón Strategy: plazo de vencimiento y multa según el tipo de préstamo.

Igual que EstrategiaEnvio en los apuntes: una clase abstracta define el
contrato y cada estrategia concreta implementa su propio cálculo.

La selección es externa (como enseñan los apuntes, el contexto no elige):
el DAO busca la estrategia en ESTRATEGIAS según el tipo de préstamo y se la
pasa por parámetro a Prestamo.activar() y a Multa.calcular_monto().
"""

from abc import ABC, abstractmethod
from datetime import timedelta

from config import (DIAS_PRESTAMO_LOCAL, MULTA_DIARIA_LOCAL,
                    DIAS_PRESTAMO_INTERBIBLIOTECARIO, MULTA_DIARIA_INTERBIBLIOTECARIO)
from constantes import TipoPrestamo


class EstrategiaPrestamo(ABC):
    """Contrato común a todas las estrategias de préstamo."""

    @abstractmethod
    def calcular_vencimiento(self, fecha_prestamo):
        """Devuelve la fecha en que vence un préstamo que empieza en fecha_prestamo."""
        pass

    @abstractmethod
    def calcular_multa(self, dias_atraso):
        """Devuelve el monto de la multa por los días de atraso (0 si no hay atraso)."""
        pass


class EstrategiaPrestamoLocal(EstrategiaPrestamo):
    """El socio retira en la misma sede: plazo y multa de config.py (31 días, $100 por día)."""
    plazo_dias: int = DIAS_PRESTAMO_LOCAL
    multa_por_dia: float = MULTA_DIARIA_LOCAL

    def calcular_vencimiento(self, fecha_prestamo):
        return fecha_prestamo + timedelta(days=self.plazo_dias)

    def calcular_multa(self, dias_atraso):
        if dias_atraso <= 0:
            return 0.0
        return round(dias_atraso * self.multa_por_dia, 2)


class EstrategiaPrestamoInterbibliotecario(EstrategiaPrestamo):
    """El ejemplar viajó desde otra sede: más plazo y multa más alta
    (38 días, $150 por día), porque el material tiene que volver a su sede."""
    plazo_dias: int = DIAS_PRESTAMO_INTERBIBLIOTECARIO
    multa_por_dia: float = MULTA_DIARIA_INTERBIBLIOTECARIO

    def calcular_vencimiento(self, fecha_prestamo):
        return fecha_prestamo + timedelta(days=self.plazo_dias)

    def calcular_multa(self, dias_atraso):
        if dias_atraso <= 0:
            return 0.0
        return round(dias_atraso * self.multa_por_dia, 2)


# Selección externa: quien usa la estrategia la elige según el tipo
ESTRATEGIAS = {
    TipoPrestamo.LOCAL: EstrategiaPrestamoLocal(),
    TipoPrestamo.INTERBIBLIOTECARIO: EstrategiaPrestamoInterbibliotecario(),
}
