from datetime import date, timedelta

import pytest

from config import DIAS_RETIRO_RESERVA
from constantes import EstadoEjemplar, EstadoReserva
from excepciones import ReglaNegocioError
from modelos.reserva import Reserva
from tests.auxiliares import crear_ejemplar, crear_sede, crear_socio


def crear_reserva(estado=EstadoReserva.PENDIENTE):
    sede = crear_sede()
    return Reserva(estado=estado, socio=crear_socio(), sede_retiro=sede,
                   fecha_vencimiento=date.today() + timedelta(days=45))


class TestAsignarEjemplar:
    def test_asignar_ejemplar_disponible(self):
        reserva = crear_reserva()
        ejemplar = crear_ejemplar(reserva.sede_retiro)
        reserva.asignar_ejemplar(ejemplar)
        assert reserva.estado == EstadoReserva.DISPONIBLE
        assert reserva.ejemplar is ejemplar
        assert ejemplar.estado == EstadoEjemplar.RESERVADO
        assert reserva.fecha_vencimiento == date.today() + timedelta(days=DIAS_RETIRO_RESERVA)

    def test_ejemplar_no_disponible(self):
        reserva = crear_reserva()
        ejemplar = crear_ejemplar(reserva.sede_retiro, EstadoEjemplar.PRESTADO)
        with pytest.raises(ReglaNegocioError, match="no está disponible"):
            reserva.asignar_ejemplar(ejemplar)
        assert reserva.estado == EstadoReserva.PENDIENTE

    def test_reserva_no_pendiente(self):
        for estado in [EstadoReserva.DISPONIBLE, EstadoReserva.CUMPLIDA,
                       EstadoReserva.CANCELADA, EstadoReserva.VENCIDA]:
            reserva = crear_reserva(estado)
            with pytest.raises(ReglaNegocioError, match="PENDIENTE"):
                reserva.asignar_ejemplar(crear_ejemplar(reserva.sede_retiro))


class TestCancelarReserva:
    def test_cancelar_pendiente(self):
        reserva = crear_reserva()
        reserva.cancelar()
        assert reserva.estado == EstadoReserva.CANCELADA

    def test_cancelar_disponible_libera_el_ejemplar(self):
        reserva = crear_reserva()
        ejemplar = crear_ejemplar(reserva.sede_retiro)
        reserva.asignar_ejemplar(ejemplar)
        reserva.cancelar()
        assert reserva.estado == EstadoReserva.CANCELADA
        assert ejemplar.estado == EstadoEjemplar.DISPONIBLE

    def test_no_se_cancela_en_estado_final(self):
        for estado in [EstadoReserva.CUMPLIDA, EstadoReserva.CANCELADA, EstadoReserva.VENCIDA]:
            with pytest.raises(ReglaNegocioError, match="No se puede cancelar"):
                crear_reserva(estado).cancelar()
