from datetime import date, timedelta

import pytest

from constantes import EstadoEjemplar, EstadoPrestamo, EstadoSede, EstadoSocio, TipoPrestamo
from excepciones import ReglaNegocioError
from tests.auxiliares import crear_prestamo, crear_sede, EstrategiaDePrueba


class TestValidarPrestamo:
    def test_prestamos_validos(self):
        for tipo in TipoPrestamo.TODOS:
            crear_prestamo(tipo).validar_prestamo()  # no lanza

    def test_socio_no_habilitado(self):
        for estado in [EstadoSocio.INHABILITADO, EstadoSocio.BAJA]:
            prestamo = crear_prestamo()
            prestamo.socio.estado = estado
            with pytest.raises(ReglaNegocioError, match="no está habilitado"):
                prestamo.validar_prestamo()

    def test_ejemplar_no_disponible(self):
        for estado in [EstadoEjemplar.PRESTADO, EstadoEjemplar.RESERVADO, EstadoEjemplar.EN_TRANSITO]:
            prestamo = crear_prestamo()
            prestamo.ejemplar.estado = estado
            with pytest.raises(ReglaNegocioError, match="no está disponible"):
                prestamo.validar_prestamo()

    def test_ejemplar_de_otra_sede(self):
        prestamo = crear_prestamo()
        prestamo.ejemplar.sede = crear_sede("Sur")
        with pytest.raises(ReglaNegocioError, match="no pertenece a la sede de origen"):
            prestamo.validar_prestamo()

    def test_sede_de_baja(self):
        prestamo = crear_prestamo(TipoPrestamo.INTERBIBLIOTECARIO)
        prestamo.sede_origen.estado = EstadoSede.BAJA
        with pytest.raises(ReglaNegocioError, match="origen .* dada de baja"):
            prestamo.validar_prestamo()

        prestamo = crear_prestamo(TipoPrestamo.INTERBIBLIOTECARIO)
        prestamo.sede_destino.estado = EstadoSede.BAJA
        with pytest.raises(ReglaNegocioError, match="destino .* dada de baja"):
            prestamo.validar_prestamo()

    def test_local_con_sedes_distintas(self):
        prestamo = crear_prestamo(TipoPrestamo.LOCAL)
        prestamo.sede_destino = crear_sede("Norte")
        with pytest.raises(ReglaNegocioError, match="local debe tener la misma sede"):
            prestamo.validar_prestamo()

    def test_interbibliotecario_con_la_misma_sede(self):
        prestamo = crear_prestamo(TipoPrestamo.INTERBIBLIOTECARIO)
        prestamo.sede_destino = prestamo.sede_origen
        with pytest.raises(ReglaNegocioError, match="sedes de origen y destino distintas"):
            prestamo.validar_prestamo()


class TestActivarYVencimiento:
    def test_activar_fija_fechas_y_presta_el_ejemplar(self):
        prestamo = crear_prestamo()
        prestamo.activar(EstrategiaDePrueba(31, 100))
        assert prestamo.estado == EstadoPrestamo.ACTIVO
        assert prestamo.fecha_prestamo == date.today()
        assert prestamo.fecha_vencimiento == date.today() + timedelta(days=31)
        assert prestamo.ejemplar.estado == EstadoEjemplar.PRESTADO

    def test_activo_dentro_del_plazo_no_esta_vencido(self):
        prestamo = crear_prestamo()
        prestamo.activar(EstrategiaDePrueba(31, 100))
        assert not prestamo.esta_vencido
        assert prestamo.estado_efectivo == EstadoPrestamo.ACTIVO

    def test_vence_el_dia_siguiente_al_vencimiento(self):
        prestamo = crear_prestamo()
        prestamo.activar(EstrategiaDePrueba(31, 100))
        prestamo.fecha_vencimiento = date.today()
        assert not prestamo.esta_vencido
        prestamo.fecha_vencimiento = date.today() - timedelta(days=1)
        assert prestamo.esta_vencido
        assert prestamo.estado_efectivo == EstadoPrestamo.VENCIDO
        assert prestamo.estado == EstadoPrestamo.ACTIVO  # VENCIDO no se guarda

    def test_solo_un_activo_puede_estar_vencido(self):
        prestamo = crear_prestamo()
        prestamo.fecha_vencimiento = date.today() - timedelta(days=10)
        for estado in [EstadoPrestamo.SOLICITADO, EstadoPrestamo.DEVUELTO, EstadoPrestamo.CANCELADO]:
            prestamo.estado = estado
            assert not prestamo.esta_vencido
