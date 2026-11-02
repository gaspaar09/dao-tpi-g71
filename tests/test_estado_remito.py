from datetime import date

import pytest

from constantes import EstadoEjemplar, EstadoRemito, TipoEnvio
from excepciones import TransicionInvalidaError
from modelos.empleado import Empleado
from modelos.remito import Remito, ItemRemito
from patrones.estado_remito import ESTADOS_REMITO, EstadoRemitoBase
from tests.auxiliares import crear_ejemplar, crear_prestamo, crear_sede

EMPLEADO = Empleado(legajo="B1", nombre="Laura", rol="BIBLIOTECARIO")

# Tabla de CLAUDE.md: (estado, acción) -> estado al que pasa. Lo que no
# figura acá tiene que lanzar TransicionInvalidaError.
PERMITIDAS = {
    (EstadoRemito.EMPAQUETADO, 'avanzar'): EstadoRemito.DESPACHADO,
    (EstadoRemito.EMPAQUETADO, 'cancelar'): EstadoRemito.CANCELADO,
    (EstadoRemito.DESPACHADO, 'avanzar'): EstadoRemito.EN_TRANSITO,
    (EstadoRemito.EN_TRANSITO, 'avanzar'): EstadoRemito.RECIBIDO,
    (EstadoRemito.EN_TRANSITO, 'extraviar'): EstadoRemito.EXTRAVIADO,
}
ACCIONES = ['avanzar', 'cancelar', 'extraviar']


def crear_remito(tipo=TipoEnvio.IDA, cantidad_items=1, estado_ejemplar=EstadoEjemplar.RESERVADO):
    """Remito recién creado (EMPAQUETADO, con su primer movimiento)."""
    remito = Remito(nro_remito="REM-000001", tipo=tipo, sede_origen=crear_sede("Central"),
                    sede_destino=crear_sede("Norte"))
    for _ in range(cantidad_items):
        remito.items.append(ItemRemito(ejemplar=crear_ejemplar(remito.sede_origen, estado_ejemplar),
                                       prestamo=crear_prestamo()))
    remito.cambiar_estado(EstadoRemito.EMPAQUETADO, EMPLEADO, "Remito creado")
    return remito


def llevar_a(remito, estado):
    """Avanza o cancela el remito hasta el estado pedido."""
    caminos = {
        EstadoRemito.EMPAQUETADO: [],
        EstadoRemito.DESPACHADO: ['avanzar'],
        EstadoRemito.EN_TRANSITO: ['avanzar', 'avanzar'],
        EstadoRemito.RECIBIDO: ['avanzar', 'avanzar', 'avanzar'],
        EstadoRemito.CANCELADO: ['cancelar'],
        EstadoRemito.EXTRAVIADO: ['avanzar', 'avanzar', 'extraviar'],
    }
    for accion in caminos[estado]:
        ejecutar(remito, accion)
    return remito


def ejecutar(remito, accion):
    if accion == 'avanzar':
        remito.avanzar_estado(EMPLEADO, "obs")
    elif accion == 'cancelar':
        remito.cancelar(EMPLEADO, "obs")
    else:
        remito.extraviar(EMPLEADO, "obs")


def estados_ejemplares(remito):
    return [item.ejemplar.estado for item in remito.items]


class TestTablaDeTransiciones:
    def test_recorre_todos_los_estados_y_acciones(self):
        for estado in EstadoRemito.TODOS:
            for accion in ACCIONES:
                remito = llevar_a(crear_remito(), estado)
                if (estado, accion) in PERMITIDAS:
                    ejecutar(remito, accion)
                    assert remito.estado == PERMITIDAS[(estado, accion)]
                else:
                    with pytest.raises(TransicionInvalidaError, match=estado):
                        ejecutar(remito, accion)
                    assert remito.estado == estado  # no cambió

    def test_no_se_salta_de_empaquetado_a_recibido(self):
        remito = crear_remito()
        remito.avanzar_estado(EMPLEADO, None)
        assert remito.estado == EstadoRemito.DESPACHADO

    def test_cada_estado_tiene_su_instancia(self):
        for estado in EstadoRemito.TODOS:
            assert ESTADOS_REMITO[estado].codigo() == estado
            assert isinstance(ESTADOS_REMITO[estado], EstadoRemitoBase)

    def test_la_base_es_abstracta(self):
        with pytest.raises(TypeError):
            EstadoRemitoBase()


class TestMovimientos:
    def test_el_remito_nace_con_su_movimiento(self):
        remito = crear_remito()
        assert len(remito.movimientos) == 1
        assert remito.movimientos[0].estado_anterior is None
        assert remito.movimientos[0].estado_nuevo == EstadoRemito.EMPAQUETADO

    def test_cada_cambio_crea_un_movimiento(self):
        remito = llevar_a(crear_remito(), EstadoRemito.RECIBIDO)
        pares = [(m.estado_anterior, m.estado_nuevo) for m in remito.movimientos]
        assert pares == [(None, EstadoRemito.EMPAQUETADO),
                         (EstadoRemito.EMPAQUETADO, EstadoRemito.DESPACHADO),
                         (EstadoRemito.DESPACHADO, EstadoRemito.EN_TRANSITO),
                         (EstadoRemito.EN_TRANSITO, EstadoRemito.RECIBIDO)]
        for movimiento in remito.movimientos:
            assert movimiento.empleado is EMPLEADO

    def test_una_transicion_rechazada_no_deja_movimiento(self):
        remito = llevar_a(crear_remito(), EstadoRemito.DESPACHADO)
        with pytest.raises(TransicionInvalidaError):
            remito.cancelar(EMPLEADO, "obs")
        assert len(remito.movimientos) == 2


class TestEfectos:
    def test_despacho(self):
        remito = llevar_a(crear_remito(cantidad_items=2), EstadoRemito.DESPACHADO)
        assert remito.fecha_despacho == date.today()
        assert estados_ejemplares(remito) == [EstadoEjemplar.EN_TRANSITO] * 2

    def test_recepcion_de_ida_no_libera_los_ejemplares(self):
        # En la IDA el ejemplar pasa a PRESTADO cuando el DAO activa el préstamo
        remito = llevar_a(crear_remito(), EstadoRemito.RECIBIDO)
        assert remito.fecha_recepcion == date.today()
        assert estados_ejemplares(remito) == [EstadoEjemplar.EN_TRANSITO]

    def test_recepcion_de_devolucion(self):
        remito = llevar_a(crear_remito(TipoEnvio.DEVOLUCION, 2, EstadoEjemplar.PRESTADO), EstadoRemito.RECIBIDO)
        assert estados_ejemplares(remito) == [EstadoEjemplar.DISPONIBLE] * 2

    def test_cancelar_ida_libera_los_ejemplares(self):
        remito = llevar_a(crear_remito(cantidad_items=2), EstadoRemito.CANCELADO)
        assert estados_ejemplares(remito) == [EstadoEjemplar.DISPONIBLE] * 2

    def test_cancelar_devolucion_no_cambia_el_ejemplar(self):
        remito = llevar_a(crear_remito(TipoEnvio.DEVOLUCION, 1, EstadoEjemplar.PRESTADO), EstadoRemito.CANCELADO)
        assert estados_ejemplares(remito) == [EstadoEjemplar.PRESTADO]

    def test_extravio(self):
        remito = llevar_a(crear_remito(cantidad_items=2), EstadoRemito.EXTRAVIADO)
        assert estados_ejemplares(remito) == [EstadoEjemplar.EXTRAVIADO] * 2


class TestQuitarItem:
    def test_con_varios_items_solo_sale_ese(self):
        remito = crear_remito(cantidad_items=2)
        item = remito.items[0]
        remito.quitar_item(item, EMPLEADO, "obs")
        assert item not in remito.items
        assert len(remito.items) == 1
        assert remito.estado == EstadoRemito.EMPAQUETADO

    def test_si_era_el_unico_se_cancela_el_remito(self):
        remito = crear_remito()
        remito.quitar_item(remito.items[0], EMPLEADO, "obs")
        assert remito.estado == EstadoRemito.CANCELADO
        assert len(remito.items) == 1  # queda para el historial
        assert remito.movimientos[-1].estado_nuevo == EstadoRemito.CANCELADO

    def test_no_se_quita_despues_del_despacho(self):
        for estado in EstadoRemito.TODOS:
            if estado == EstadoRemito.EMPAQUETADO:
                continue
            remito = llevar_a(crear_remito(cantidad_items=2), estado)
            with pytest.raises(TransicionInvalidaError, match="no se le pueden quitar"):
                remito.quitar_item(remito.items[0], EMPLEADO, "obs")
