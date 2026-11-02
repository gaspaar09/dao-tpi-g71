from datetime import date, timedelta

import pytest

from constantes import DiaSemana, EstadoEjemplar, EstadoFisico, EstadoPrestamo, TipoMaterial, TipoPrestamo
from dao.autor_dao import AutorDAO
from dao.categoria_dao import CategoriaDAO
from dao.ejemplar_dao import EjemplarDAO
from dao.libro_dao import LibroDAO
from dao.prestamo_dao import PrestamoDAO, TRANSICIONES
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.prestamo import Prestamo
from tests.auxiliares import preparar_base_en_memoria

dao = PrestamoDAO()
LOCAL = TipoPrestamo.LOCAL
INTER = TipoPrestamo.INTERBIBLIOTECARIO


def id_por_texto(opciones, texto):
    for id, descripcion in opciones:
        if descripcion.startswith(texto):
            return id


def preparar():
    """Dos sedes, un socio y un ejemplar en Central. Devuelve un diccionario de ids."""
    preparar_base_en_memoria()
    sedes = SedeDAO()
    sedes.crear("Central", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")])
    sedes.crear("Norte", "Calle 2", "54", "3514000001", "", [(DiaSemana.LUNES, "08:00", "18:00")])
    SocioDAO().crear("30111222", "Ana", "Martínez", "", "54", "3515550001")
    CategoriaDAO().crear("Novela")
    AutorDAO().crear("Julio", "Cortázar")
    LibroDAO().crear("9789500700011", "Rayuela", "Sudamericana", "1963", "Español", TipoMaterial.LIBRO,
                     CategoriaDAO().opciones()[0][0], [AutorDAO().opciones()[0][0]])
    central = id_por_texto(sedes.opciones(), "Central")
    EjemplarDAO().crear("EJ-001", LibroDAO().opciones()[0][0], central, EstadoFisico.BUENO)
    return {
        'central': central,
        'norte': id_por_texto(sedes.opciones(), "Norte"),
        'socio': SocioDAO().opciones()[0][0],
        'ejemplar': EjemplarDAO().listar()[0]['id'],
    }


def solicitar(ids, tipo=LOCAL, destino=None):
    dao.solicitar(tipo, ids['socio'], ids['ejemplar'], ids['central'], destino)
    return dao.listar()[0]['id']


def estado_ejemplar():
    return EjemplarDAO().listar()[0]['estado']


class TestSolicitud:
    def test_local_toma_la_misma_sede_de_destino(self):
        ids = preparar()
        solicitar(ids)
        prestamo = dao.listar()[0]
        assert prestamo['estado'] == EstadoPrestamo.SOLICITADO
        assert prestamo['origen'] == prestamo['destino'] == "Central"
        assert prestamo['fecha_vencimiento'] == ""  # se fija al activar
        assert estado_ejemplar() == EstadoEjemplar.DISPONIBLE

    def test_tipo_invalido(self):
        ids = preparar()
        for tipo in ["", "EXPRESS", None]:
            with pytest.raises(ValidacionError, match="tipo de préstamo"):
                solicitar(ids, tipo)

    def test_reglas_de_negocio(self):
        ids = preparar()
        with pytest.raises(ReglaNegocioError, match="local debe tener la misma sede"):
            solicitar(ids, LOCAL, ids['norte'])
        with pytest.raises(ReglaNegocioError, match="sedes de origen y destino distintas"):
            solicitar(ids, INTER, ids['central'])
        SocioDAO().inhabilitar(ids['socio'])
        with pytest.raises(ReglaNegocioError, match="no está habilitado"):
            solicitar(ids)
        assert dao.listar() == []

    def test_ejemplar_de_otra_sede(self):
        ids = preparar()
        with pytest.raises(ReglaNegocioError, match="no pertenece a la sede de origen"):
            dao.solicitar(INTER, ids['socio'], ids['ejemplar'], ids['norte'], ids['central'])

    def test_sede_de_baja(self):
        ids = preparar()
        SedeDAO().dar_de_baja(ids['norte'])
        with pytest.raises(ReglaNegocioError, match="destino .* dada de baja"):
            solicitar(ids, INTER, ids['norte'])


class TestAprobacion:
    def test_local_se_activa_al_aprobar(self):
        ids = preparar()
        prestamo_id = solicitar(ids)
        dao.aprobar(prestamo_id)
        prestamo = dao.listar()[0]
        assert prestamo['estado'] == EstadoPrestamo.ACTIVO
        assert prestamo['fecha_prestamo'] == date.today().strftime("%d/%m/%Y")
        assert prestamo['fecha_vencimiento'] == (date.today() + timedelta(days=31)).strftime("%d/%m/%Y")
        assert estado_ejemplar() == EstadoEjemplar.PRESTADO  # directo, sin pasar por RESERVADO

    def test_interbibliotecario_reserva_el_ejemplar(self):
        ids = preparar()
        prestamo_id = solicitar(ids, INTER, ids['norte'])
        dao.aprobar(prestamo_id)
        prestamo = dao.listar()[0]
        assert prestamo['estado'] == EstadoPrestamo.APROBADO
        assert prestamo['fecha_vencimiento'] == ""  # se fija cuando llega el remito
        assert estado_ejemplar() == EstadoEjemplar.RESERVADO

    def test_dos_solicitudes_del_mismo_ejemplar(self):
        """Dos socios pueden pedir el mismo ejemplar: se lo lleva la primera que se aprueba."""
        ids = preparar()
        primero = solicitar(ids)
        SocioDAO().crear("30111333", "Bruno", "Paz", "", "54", "3515550002")
        otro_socio = [id for id, texto in SocioDAO().opciones() if id != ids['socio']][0]
        dao.solicitar(LOCAL, otro_socio, ids['ejemplar'], ids['central'], None)
        segundo = dao.listar()[0]['id']
        dao.aprobar(primero)
        with pytest.raises(ReglaNegocioError, match="no está disponible"):
            dao.aprobar(segundo)

    def test_el_mismo_socio_no_repite_la_solicitud(self):
        """Por ejemplo, un doble clic en Registrar solicitud."""
        ids = preparar()
        primero = solicitar(ids)
        with pytest.raises(ReglaNegocioError, match="ya tiene una solicitud SOLICITADO"):
            solicitar(ids)
        # Cancelada la primera, puede volver a pedirlo
        dao.cancelar(primero)
        solicitar(ids)
        assert len(dao.listar()) == 2

    def test_no_se_aprueba_dos_veces(self):
        ids = preparar()
        prestamo_id = solicitar(ids)
        dao.aprobar(prestamo_id)
        with pytest.raises(ReglaNegocioError, match="ACTIVO no puede pasar a APROBADO"):
            dao.aprobar(prestamo_id)


class TestCancelacion:
    def test_cancelar_solicitado(self):
        ids = preparar()
        prestamo_id = solicitar(ids)
        dao.cancelar(prestamo_id)
        assert dao.listar()[0]['estado'] == EstadoPrestamo.CANCELADO

    def test_cancelar_aprobado_libera_el_ejemplar(self):
        ids = preparar()
        prestamo_id = solicitar(ids, INTER, ids['norte'])
        dao.aprobar(prestamo_id)
        dao.cancelar(prestamo_id)
        assert dao.listar()[0]['estado'] == EstadoPrestamo.CANCELADO
        assert estado_ejemplar() == EstadoEjemplar.DISPONIBLE

    def test_no_se_cancela_activo_ni_cancelado(self):
        ids = preparar()
        activo = solicitar(ids)
        dao.aprobar(activo)
        with pytest.raises(ReglaNegocioError, match="ACTIVO no puede pasar a CANCELADO"):
            dao.cancelar(activo)

    def test_no_se_cancela_dos_veces(self):
        ids = preparar()
        prestamo_id = solicitar(ids)
        dao.cancelar(prestamo_id)
        with pytest.raises(ReglaNegocioError, match="CANCELADO no puede pasar a CANCELADO"):
            dao.cancelar(prestamo_id)

    # Cancelar un préstamo EN_ENVIO se prueba en test_remito_dao.py, porque necesita un remito


class TestTransiciones:
    def test_tabla_de_transiciones(self):
        """Recorre todos los pares de estados guardables contra el diccionario."""
        permitidas = [
            (EstadoPrestamo.SOLICITADO, EstadoPrestamo.APROBADO), (EstadoPrestamo.SOLICITADO, EstadoPrestamo.CANCELADO),
            (EstadoPrestamo.APROBADO, EstadoPrestamo.EN_ENVIO), (EstadoPrestamo.APROBADO, EstadoPrestamo.ACTIVO),
            (EstadoPrestamo.APROBADO, EstadoPrestamo.CANCELADO), (EstadoPrestamo.EN_ENVIO, EstadoPrestamo.ACTIVO),
            (EstadoPrestamo.EN_ENVIO, EstadoPrestamo.CANCELADO), (EstadoPrestamo.ACTIVO, EstadoPrestamo.DEVUELTO),
        ]
        for origen in TRANSICIONES:
            for destino in TRANSICIONES:
                assert (destino in TRANSICIONES[origen]) == ((origen, destino) in permitidas)

    def test_vencido_se_calcula(self):
        ids = preparar()
        prestamo_id = solicitar(ids)
        dao.aprobar(prestamo_id)
        with obtener_session() as session:
            session.query(Prestamo).filter_by(id=prestamo_id).first().fecha_vencimiento = date.today() - timedelta(days=1)
        assert dao.listar()[0]['estado'] == EstadoPrestamo.VENCIDO
        with obtener_session() as session:
            assert session.query(Prestamo).filter_by(id=prestamo_id).first().estado == EstadoPrestamo.ACTIVO
