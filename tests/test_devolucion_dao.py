from datetime import date, timedelta

import pytest

from constantes import (EstadoEjemplar, EstadoFisico, EstadoMulta, EstadoPrestamo, EstadoRemito, EstadoReserva,
                        TipoEnvio, TipoPrestamo)
from dao.devolucion_dao import DevolucionDAO
from dao.libro_dao import LibroDAO
from dao.prestamo_dao import PrestamoDAO
from dao.remito_dao import RemitoDAO
from dao.reserva_dao import ReservaDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.prestamo import Prestamo
from tests.test_remito_dao import preparar, aprobar_inter, crear_remito, estados_ejemplares

dao = DevolucionDAO()
prestamos = PrestamoDAO()
remitos = RemitoDAO()
BUENO = EstadoFisico.BUENO


def hoy(dias=0):
    return (date.today() + timedelta(days=dias)).strftime("%d/%m/%Y")


def prestamo_local_activo(ids, ejemplar=0):
    prestamos.solicitar(TipoPrestamo.LOCAL, ids['socio'], ids['ejemplares'][ejemplar], ids['central'], None)
    prestamo_id = prestamos.listar()[0]['id']
    prestamos.aprobar(prestamo_id)
    return prestamo_id


def prestamo_inter_activo(ids):
    """Interbibliotecario Central -> Norte, con su remito de ida ya recibido."""
    prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
    remito_id = crear_remito(ids, [prestamo_id])
    for _ in range(3):
        remitos.avanzar(remito_id, ids['empleado'], "")
    return prestamo_id


def correr_fechas(prestamo_id, dias):
    """Simula que el préstamo empezó hace `dias` días (vence a los 31 o 38)."""
    with obtener_session() as session:
        prestamo = session.query(Prestamo).filter_by(id=prestamo_id).first()
        plazo = (prestamo.fecha_vencimiento - prestamo.fecha_prestamo).days
        prestamo.fecha_prestamo = date.today() - timedelta(days=dias)
        prestamo.fecha_vencimiento = prestamo.fecha_prestamo + timedelta(days=plazo)


def fila_prestamo(prestamo_id):
    for fila in prestamos.listar():
        if fila['id'] == prestamo_id:
            return fila


class TestDevolucionLocal:
    def test_en_termino_sin_multa(self):
        ids = preparar()
        prestamo_id = prestamo_local_activo(ids)
        dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        fila = fila_prestamo(prestamo_id)
        assert fila['estado'] == EstadoPrestamo.DEVUELTO
        assert fila['multa'] == ""
        assert estados_ejemplares()[0] == EstadoEjemplar.DISPONIBLE

    def test_con_atraso_genera_multa_de_la_estrategia(self):
        ids = preparar()
        prestamo_id = prestamo_local_activo(ids)
        correr_fechas(prestamo_id, 40)  # venció hace 9 días
        dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        assert fila_prestamo(prestamo_id)['multa'] == "$900.00 (9 días) - PENDIENTE"
        prestamos.pagar_multa(prestamo_id)
        assert fila_prestamo(prestamo_id)['multa'] == f"$900.00 (9 días) - {EstadoMulta.PAGADA}"
        with pytest.raises(ReglaNegocioError, match="ya está pagada"):
            prestamos.pagar_multa(prestamo_id)

    def test_devuelto_el_dia_del_vencimiento_no_tiene_multa(self):
        ids = preparar()
        prestamo_id = prestamo_local_activo(ids)
        correr_fechas(prestamo_id, 31)
        dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        assert fila_prestamo(prestamo_id)['multa'] == ""
        with pytest.raises(ReglaNegocioError, match="no tiene multa"):
            prestamos.pagar_multa(prestamo_id)

    def test_danado_o_destruido_sale_de_circulacion(self):
        ids = preparar()
        for indice, estado_fisico, esperado in [(0, EstadoFisico.DANADO, EstadoEjemplar.DANADO),
                                                (1, EstadoFisico.DESTRUIDO, EstadoEjemplar.BAJA)]:
            prestamo_id = prestamo_local_activo(ids, indice)
            dao.registrar(prestamo_id, hoy(), estado_fisico, "Tapa rota", ids['empleado'])
            assert estados_ejemplares()[indice] == esperado

    def test_pasa_a_la_reserva_que_espera(self):
        ids = preparar()
        prestamo_id = prestamo_local_activo(ids, 0)
        prestamo_local_activo(ids, 1)
        # Los dos ejemplares de Central están prestados: la reserva espera
        ReservaDAO().crear(ids['socio'], LibroDAO().opciones()[0][0], ids['central'])
        assert ReservaDAO().listar()[0]['estado'] == EstadoReserva.PENDIENTE
        dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        assert ReservaDAO().listar()[0]['estado'] == EstadoReserva.DISPONIBLE
        assert estados_ejemplares() == [EstadoEjemplar.RESERVADO, EstadoEjemplar.PRESTADO]


class TestValidaciones:
    def test_datos_invalidos(self):
        ids = preparar()
        prestamo_id = prestamo_local_activo(ids)
        casos = [
            (hoy(1), BUENO, "", ValidacionError, "fecha futura"),
            ("31/02/2026", BUENO, "", ValidacionError, "no es una fecha válida"),
            ("", BUENO, "", ValidacionError, "es obligatorio"),
            (hoy(), "ROTO", "", ValidacionError, "estado físico"),
            (hoy(), EstadoFisico.DANADO, "", ValidacionError, "observaciones son obligatorias"),
            (hoy(), EstadoFisico.DESTRUIDO, "  ", ValidacionError, "observaciones son obligatorias"),
            (hoy(), BUENO, "x" * 301, ValidacionError, "300 caracteres"),
            (hoy(-1), BUENO, "", ReglaNegocioError, "anterior a la del préstamo"),
        ]
        for fecha, estado_fisico, observaciones, error, mensaje in casos:
            with pytest.raises(error, match=mensaje):
                dao.registrar(prestamo_id, fecha, estado_fisico, observaciones, ids['empleado'])
        assert fila_prestamo(prestamo_id)['estado'] == EstadoPrestamo.ACTIVO

    def test_no_se_devuelve_dos_veces_ni_sin_activar(self):
        ids = preparar()
        prestamo_id = prestamo_local_activo(ids)
        dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        with pytest.raises(ReglaNegocioError, match="DEVUELTO no puede pasar a DEVUELTO"):
            dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        aprobado = aprobar_inter(ids, ids['ejemplares'][1])
        with pytest.raises(ReglaNegocioError, match="APROBADO no puede pasar a DEVUELTO"):
            dao.registrar(aprobado, hoy(), BUENO, "", ids['empleado'])

    def test_hace_falta_el_empleado(self):
        ids = preparar()
        prestamo_id = prestamo_local_activo(ids)
        with pytest.raises(ValidacionError, match="empleado actual"):
            dao.registrar(prestamo_id, hoy(), BUENO, "", None)


class TestDevolucionInterbibliotecaria:
    def test_crea_el_remito_y_al_recibirlo_vuelve_a_su_sede(self):
        ids = preparar()
        prestamo_id = prestamo_inter_activo(ids)
        correr_fechas(prestamo_id, 40)  # vence a los 38: 2 días de atraso
        dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        assert fila_prestamo(prestamo_id)['multa'] == "$300.00 (2 días) - PENDIENTE"
        remito = remitos.listar()[0]
        assert (remito['tipo'], remito['origen'], remito['destino'], remito['estado']) == \
               (TipoEnvio.DEVOLUCION, "Norte", "Central", EstadoRemito.EMPAQUETADO)
        assert estados_ejemplares()[0] == EstadoEjemplar.PRESTADO  # todavía no salió
        remitos.avanzar(remito['id'], ids['empleado'], "")
        assert estados_ejemplares()[0] == EstadoEjemplar.EN_TRANSITO
        remitos.avanzar(remito['id'], ids['empleado'], "")
        remitos.avanzar(remito['id'], ids['empleado'], "")
        assert estados_ejemplares()[0] == EstadoEjemplar.DISPONIBLE
        # El préstamo ya estaba DEVUELTO: recibir el remito no lo toca
        assert fila_prestamo(prestamo_id)['estado'] == EstadoPrestamo.DEVUELTO

    def test_danado_llega_fuera_de_circulacion(self):
        ids = preparar()
        prestamo_id = prestamo_inter_activo(ids)
        dao.registrar(prestamo_id, hoy(), EstadoFisico.DANADO, "Hojas mojadas", ids['empleado'])
        remito_id = remitos.listar()[0]['id']
        for _ in range(3):
            remitos.avanzar(remito_id, ids['empleado'], "")
        assert estados_ejemplares()[0] == EstadoEjemplar.DANADO

    def test_remito_cancelado_se_reenvia(self):
        ids = preparar()
        prestamo_id = prestamo_inter_activo(ids)
        dao.registrar(prestamo_id, hoy(), BUENO, "", ids['empleado'])
        assert remitos.devoluciones_pendientes() == []
        remitos.cancelar(remitos.listar()[0]['id'], ids['empleado'], "Se rompió la caja")
        assert estados_ejemplares()[0] == EstadoEjemplar.PRESTADO
        assert [id for id, texto in remitos.devoluciones_pendientes()] == [prestamo_id]
        remitos.crear_devolucion(prestamo_id, ids['empleado'])
        assert remitos.listar()[0]['estado'] == EstadoRemito.EMPAQUETADO
        assert remitos.devoluciones_pendientes() == []
        with pytest.raises(ReglaNegocioError, match="no tiene un ejemplar esperando"):
            remitos.crear_devolucion(prestamo_id, ids['empleado'])
