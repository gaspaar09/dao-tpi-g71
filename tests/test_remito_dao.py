from datetime import date, timedelta

import pytest

from constantes import (DiaSemana, EstadoEjemplar, EstadoFisico, EstadoPrestamo, EstadoRemito, RolEmpleado,
                        TipoIncidencia, TipoPrestamo)
from dao.ejemplar_dao import EjemplarDAO
from dao.empleado_dao import EmpleadoDAO
from dao.libro_dao import LibroDAO
from dao.prestamo_dao import PrestamoDAO
from dao.remito_dao import RemitoDAO
from dao.sede_dao import SedeDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError, TransicionInvalidaError
from modelos.sede import Sede
from tests.test_prestamo_dao import preparar as preparar_prestamos, id_por_texto

dao = RemitoDAO()
prestamos = PrestamoDAO()
INTER = TipoPrestamo.INTERBIBLIOTECARIO


def preparar():
    """Lo de los tests de préstamos, más un empleado, un segundo ejemplar en
    Central y una tercera sede (Sur)."""
    ids = preparar_prestamos()
    SedeDAO().crear("Sur", "Calle 3", "54", "3514000002", "", [(DiaSemana.LUNES, "08:00", "18:00")])
    ids['sur'] = id_por_texto(SedeDAO().opciones(), "Sur")
    EmpleadoDAO().crear("Laura", RolEmpleado.BIBLIOTECARIO, ids['central'])
    ids['empleado'] = EmpleadoDAO().opciones()[0][0]
    EjemplarDAO().crear("EJ-002", LibroDAO().opciones()[0][0], ids['central'], EstadoFisico.BUENO)
    ids['ejemplares'] = sorted([fila['id'] for fila in EjemplarDAO().listar()])
    return ids


def aprobar_inter(ids, ejemplar_id, destino='norte'):
    prestamos.solicitar(INTER, ids['socio'], ejemplar_id, ids['central'], ids[destino])
    prestamo_id = prestamos.listar()[0]['id']
    prestamos.aprobar(prestamo_id)
    return prestamo_id


def crear_remito(ids, prestamos_ids):
    dao.crear_ida(ids['central'], ids['norte'], prestamos_ids, ids['empleado'])
    return dao.listar()[0]['id']


def estado_prestamo(prestamo_id):
    for fila in prestamos.listar():
        if fila['id'] == prestamo_id:
            return fila['estado']


def estados_ejemplares():
    return [fila['estado'] for fila in sorted(EjemplarDAO().listar(), key=lambda fila: fila['id'])]


class TestCrearIda:
    def test_agrupa_prestamos_y_los_pone_en_envio(self):
        ids = preparar()
        p1 = aprobar_inter(ids, ids['ejemplares'][0])
        p2 = aprobar_inter(ids, ids['ejemplares'][1])
        assert [id for id, texto in dao.prestamos_para_enviar(ids['central'], ids['norte'])] == [p1, p2]
        remito_id = crear_remito(ids, [p1, p2])
        remito = dao.listar()[0]
        assert remito['nro_remito'] == "REM-000001"
        assert remito['estado'] == EstadoRemito.EMPAQUETADO
        assert remito['ejemplares'] == "EJ-001, EJ-002"
        assert estado_prestamo(p1) == estado_prestamo(p2) == EstadoPrestamo.EN_ENVIO
        assert estados_ejemplares() == [EstadoEjemplar.RESERVADO] * 2
        assert [m['estado_nuevo'] for m in dao.listar_movimientos(remito_id)] == [EstadoRemito.EMPAQUETADO]
        # Ya no esperan remito
        assert dao.prestamos_para_enviar(ids['central'], ids['norte']) == []

    def test_numero_correlativo(self):
        ids = preparar()
        crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][1])])
        assert [fila['nro_remito'] for fila in dao.listar()] == ["REM-000002", "REM-000001"]

    def test_rechazos(self):
        ids = preparar()
        aprobado = aprobar_inter(ids, ids['ejemplares'][0])
        with pytest.raises(ValidacionError, match="al menos un préstamo"):
            dao.crear_ida(ids['central'], ids['norte'], [], ids['empleado'])
        # Con sedes iguales y sin préstamos, el error que se informa es el de las sedes
        with pytest.raises(ReglaNegocioError, match="deben ser distintas"):
            dao.crear_ida(ids['central'], ids['central'], [], ids['empleado'])
        with pytest.raises(ValidacionError, match="empleado actual"):
            dao.crear_ida(ids['central'], ids['norte'], [aprobado], None)
        with pytest.raises(ReglaNegocioError, match="deben ser distintas"):
            dao.crear_ida(ids['central'], ids['central'], [aprobado], ids['empleado'])
        with pytest.raises(ReglaNegocioError, match="no va de Central a Sur"):
            dao.crear_ida(ids['central'], ids['sur'], [aprobado], ids['empleado'])
        # Solicitado (sin aprobar) y local
        prestamos.solicitar(INTER, ids['socio'], ids['ejemplares'][1], ids['central'], ids['norte'])
        solicitado = prestamos.listar()[0]['id']
        with pytest.raises(ReglaNegocioError, match="SOLICITADO no puede pasar a EN_ENVIO"):
            dao.crear_ida(ids['central'], ids['norte'], [aprobado, solicitado], ids['empleado'])
        prestamos.cancelar(solicitado)  # el mismo socio no puede repetir la solicitud
        prestamos.solicitar(TipoPrestamo.LOCAL, ids['socio'], ids['ejemplares'][1], ids['central'], None)
        local = prestamos.listar()[0]['id']
        with pytest.raises(ReglaNegocioError, match="es local"):
            dao.crear_ida(ids['central'], ids['norte'], [local], ids['empleado'])
        # Ninguno de los intentos dejó nada a medias
        assert dao.listar() == []
        assert estado_prestamo(aprobado) == EstadoPrestamo.APROBADO

    def test_sede_de_baja(self):
        ids = preparar()
        aprobado = aprobar_inter(ids, ids['ejemplares'][0])
        # Directo en el modelo: SedeDAO no da de baja una sede con préstamos en curso
        with obtener_session() as session:
            session.query(Sede).filter_by(id=ids['norte']).first().dar_de_baja()
        with pytest.raises(ReglaNegocioError, match="Norte está dada de baja"):
            crear_remito(ids, [aprobado])


class TestCicloDeIda:
    def test_recibir_activa_el_prestamo_con_la_estrategia(self):
        ids = preparar()
        prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
        remito_id = crear_remito(ids, [prestamo_id])
        dao.avanzar(remito_id, ids['empleado'], "")
        assert dao.listar()[0]['fecha_despacho'] == date.today().strftime("%d/%m/%Y")
        assert estados_ejemplares()[0] == EstadoEjemplar.EN_TRANSITO
        dao.avanzar(remito_id, ids['empleado'], "En camino")
        assert estado_prestamo(prestamo_id) == EstadoPrestamo.EN_ENVIO
        dao.avanzar(remito_id, ids['empleado'], "")
        assert dao.listar()[0]['estado'] == EstadoRemito.RECIBIDO
        prestamo = prestamos.listar()[0]
        assert prestamo['estado'] == EstadoPrestamo.ACTIVO
        assert prestamo['fecha_prestamo'] == date.today().strftime("%d/%m/%Y")
        # Plazo interbibliotecario: 38 días desde la recepción
        assert prestamo['fecha_vencimiento'] == (date.today() + timedelta(days=38)).strftime("%d/%m/%Y")
        assert estados_ejemplares()[0] == EstadoEjemplar.PRESTADO
        movimientos = dao.listar_movimientos(remito_id)
        assert [m['estado_nuevo'] for m in movimientos] == [
            EstadoRemito.EMPAQUETADO, EstadoRemito.DESPACHADO, EstadoRemito.EN_TRANSITO, EstadoRemito.RECIBIDO]
        assert movimientos[2]['observacion'] == "En camino"
        assert movimientos[1]['empleado'] == "Laura (Legajo B1)"

    def test_un_remito_recibido_no_avanza(self):
        ids = preparar()
        remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        for _ in range(3):
            dao.avanzar(remito_id, ids['empleado'], "")
        with pytest.raises(TransicionInvalidaError, match="RECIBIDO no puede avanzar"):
            dao.avanzar(remito_id, ids['empleado'], "")

    def test_observacion_demasiado_larga(self):
        ids = preparar()
        remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        with pytest.raises(ValidacionError, match="200 caracteres"):
            dao.avanzar(remito_id, ids['empleado'], "x" * 201)


class TestCancelarYExtraviar:
    def test_cancelar_empaquetado(self):
        ids = preparar()
        prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
        remito_id = crear_remito(ids, [prestamo_id])
        dao.cancelar(remito_id, ids['empleado'], "El socio desistió")
        assert dao.listar()[0]['estado'] == EstadoRemito.CANCELADO
        assert estado_prestamo(prestamo_id) == EstadoPrestamo.CANCELADO
        assert estados_ejemplares()[0] == EstadoEjemplar.DISPONIBLE

    def test_no_se_cancela_despachado(self):
        ids = preparar()
        prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
        remito_id = crear_remito(ids, [prestamo_id])
        dao.avanzar(remito_id, ids['empleado'], "")
        with pytest.raises(TransicionInvalidaError, match="DESPACHADO no se puede cancelar"):
            dao.cancelar(remito_id, ids['empleado'], "El socio desistió")
        assert estado_prestamo(prestamo_id) == EstadoPrestamo.EN_ENVIO

    def test_observacion_obligatoria(self):
        ids = preparar()
        remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        for observacion in ["", "   ", None]:
            with pytest.raises(ValidacionError, match="observación es obligatorio"):
                dao.cancelar(remito_id, ids['empleado'], observacion)
            with pytest.raises(ValidacionError, match="observación es obligatorio"):
                dao.extraviar(remito_id, ids['empleado'], observacion)
        with pytest.raises(ValidacionError, match="al menos 5"):
            dao.cancelar(remito_id, ids['empleado'], "no")

    def test_extraviar_en_transito(self):
        ids = preparar()
        prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
        remito_id = crear_remito(ids, [prestamo_id])
        with pytest.raises(TransicionInvalidaError, match="EMPAQUETADO no se puede dar por extraviado"):
            dao.extraviar(remito_id, ids['empleado'], "No llegó a destino")
        dao.avanzar(remito_id, ids['empleado'], "")
        dao.avanzar(remito_id, ids['empleado'], "")
        dao.extraviar(remito_id, ids['empleado'], "No llegó a destino")
        assert dao.listar()[0]['estado'] == EstadoRemito.EXTRAVIADO
        assert estado_prestamo(prestamo_id) == EstadoPrestamo.CANCELADO
        assert estados_ejemplares()[0] == EstadoEjemplar.EXTRAVIADO
        incidencias = dao.listar_incidencias(remito_id)
        assert len(incidencias) == 1
        assert incidencias[0]['tipo'] == TipoIncidencia.EXTRAVIO
        assert incidencias[0]['descripcion'] == "No llegó a destino"


class TestIncidencias:
    def test_registrar(self):
        ids = preparar()
        remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        hoy = date.today().strftime("%d/%m/%Y")
        dao.registrar_incidencia(remito_id, TipoIncidencia.DEMORA, hoy, "Se demoró el transporte")
        assert dao.listar_incidencias(remito_id)[0]['fecha'] == hoy

    def test_datos_invalidos(self):
        ids = preparar()
        remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        hoy = date.today().strftime("%d/%m/%Y")
        manana = (date.today() + timedelta(days=1)).strftime("%d/%m/%Y")
        casos = [
            ("INCENDIO", hoy, "Descripción válida", "tipo de incidencia"),
            (TipoIncidencia.DANIO, manana, "Descripción válida", "fecha futura"),
            (TipoIncidencia.DANIO, "30/02/2025", "Descripción válida", "no es una fecha válida"),
            (TipoIncidencia.DANIO, "", "Descripción válida", "fecha es obligatorio"),
            (TipoIncidencia.DANIO, hoy, "roto", "al menos 5"),
            (TipoIncidencia.DANIO, hoy, "x" * 301, "300 caracteres"),
        ]
        for tipo, fecha, descripcion, mensaje in casos:
            with pytest.raises(ValidacionError, match=mensaje):
                dao.registrar_incidencia(remito_id, tipo, fecha, descripcion)
        assert dao.listar_incidencias(remito_id) == []

    def test_fecha_anterior_a_la_creacion(self):
        ids = preparar()
        remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        ayer = (date.today() - timedelta(days=1)).strftime("%d/%m/%Y")
        with pytest.raises(ReglaNegocioError, match="anterior a la creación"):
            dao.registrar_incidencia(remito_id, TipoIncidencia.DANIO, ayer, "Caja golpeada")


class TestCancelarPrestamoEnEnvio:
    """Decisión del grupo: se saca solo ese ítem; si era el único, se cancela el remito."""

    def test_quita_solo_su_item(self):
        ids = preparar()
        p1 = aprobar_inter(ids, ids['ejemplares'][0])
        p2 = aprobar_inter(ids, ids['ejemplares'][1])
        remito_id = crear_remito(ids, [p1, p2])
        prestamos.cancelar(p1, ids['empleado'])
        assert estado_prestamo(p1) == EstadoPrestamo.CANCELADO
        assert estado_prestamo(p2) == EstadoPrestamo.EN_ENVIO
        remito = dao.listar()[0]
        assert remito['estado'] == EstadoRemito.EMPAQUETADO
        assert remito['ejemplares'] == "EJ-002"
        assert estados_ejemplares() == [EstadoEjemplar.DISPONIBLE, EstadoEjemplar.RESERVADO]
        assert len(dao.listar_movimientos(remito_id)) == 1

    def test_si_era_el_unico_cancela_el_remito(self):
        ids = preparar()
        prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
        remito_id = crear_remito(ids, [prestamo_id])
        prestamos.cancelar(prestamo_id, ids['empleado'])
        assert estado_prestamo(prestamo_id) == EstadoPrestamo.CANCELADO
        assert dao.listar()[0]['estado'] == EstadoRemito.CANCELADO
        assert dao.listar_movimientos(remito_id)[-1]['observacion'] == f"Se canceló el préstamo #{prestamo_id}"
        assert estados_ejemplares()[0] == EstadoEjemplar.DISPONIBLE

    def test_rechazado_si_el_remito_ya_salio(self):
        ids = preparar()
        prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
        remito_id = crear_remito(ids, [prestamo_id])
        dao.avanzar(remito_id, ids['empleado'], "")
        with pytest.raises(TransicionInvalidaError, match="ya salió"):
            prestamos.cancelar(prestamo_id, ids['empleado'])
        assert estado_prestamo(prestamo_id) == EstadoPrestamo.EN_ENVIO

    def test_hace_falta_el_empleado(self):
        ids = preparar()
        prestamo_id = aprobar_inter(ids, ids['ejemplares'][0])
        crear_remito(ids, [prestamo_id])
        with pytest.raises(ValidacionError, match="empleado actual"):
            prestamos.cancelar(prestamo_id)
