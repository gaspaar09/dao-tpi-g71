from datetime import date, timedelta

import pytest

from constantes import EstadoEjemplar, EstadoFisico, EstadoPrestamo, EstadoReserva, TipoPrestamo
from dao.ejemplar_dao import EjemplarDAO
from dao.libro_dao import LibroDAO
from dao.prestamo_dao import PrestamoDAO
from dao.reserva_dao import ReservaDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.reserva import Reserva
from tests.test_prestamo_dao import preparar as preparar_prestamos

dao = ReservaDAO()
prestamos = PrestamoDAO()


def preparar():
    """Sedes Central y Norte, un ejemplar (EJ-001) en Central y dos socios."""
    ids = preparar_prestamos()
    SocioDAO().crear("30111333", "Bruno", "Paz", "", "54", "3515550002")
    ids['socios'] = [id for id, texto in SocioDAO().opciones()]
    ids['libro'] = LibroDAO().opciones()[0][0]
    return ids


def prestar_ejemplar(ids):
    """Deja el único ejemplar PRESTADO con un préstamo local."""
    prestamos.solicitar(TipoPrestamo.LOCAL, ids['socio'], ids['ejemplar'], ids['central'], None)
    prestamo_id = prestamos.listar()[0]['id']
    prestamos.aprobar(prestamo_id)
    return prestamo_id


def reservas_por_socio():
    """{nombre del socio: (estado, ejemplar)}"""
    return dict((fila['socio'].split(" (")[0], (fila['estado'], fila['ejemplar'])) for fila in dao.listar())


def estado_ejemplar():
    return EjemplarDAO().listar()[0]['estado']


def correr_vencimiento(dias):
    """Corre hacia atrás el vencimiento de todas las reservas."""
    with obtener_session() as session:
        for reserva in session.query(Reserva).all():
            reserva.fecha_vencimiento = date.today() - timedelta(days=dias)


class TestCrear:
    def test_con_ejemplar_libre_se_asigna_en_el_acto(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['central'])
        reserva = dao.listar()[0]
        assert reserva['estado'] == EstadoReserva.DISPONIBLE
        assert reserva['ejemplar'] == "EJ-001"
        assert reserva['fecha_vencimiento'] == (date.today() + timedelta(days=2)).strftime("%d/%m/%Y")
        assert estado_ejemplar() == EstadoEjemplar.RESERVADO

    def test_sin_ejemplar_libre_queda_pendiente(self):
        ids = preparar()
        # En Norte no hay ejemplares de ese libro
        dao.crear(ids['socio'], ids['libro'], ids['norte'])
        reserva = dao.listar()[0]
        assert reserva['estado'] == EstadoReserva.PENDIENTE
        assert reserva['ejemplar'] == ""
        assert reserva['fecha_vencimiento'] == (date.today() + timedelta(days=45)).strftime("%d/%m/%Y")

    def test_rechazos(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['norte'])
        with pytest.raises(ReglaNegocioError, match="ya tiene una reserva PENDIENTE"):
            dao.crear(ids['socio'], ids['libro'], ids['central'])
        with pytest.raises(ValidacionError, match="Seleccione el libro"):
            dao.crear(ids['socio'], None, ids['central'])
        SocioDAO().inhabilitar(ids['socios'][1])
        with pytest.raises(ReglaNegocioError, match="no está habilitado"):
            dao.crear(ids['socios'][1], ids['libro'], ids['central'])
        assert len(dao.listar()) == 1

    def test_sede_de_baja(self):
        ids = preparar()
        SedeDAO().dar_de_baja(ids['norte'])
        with pytest.raises(ReglaNegocioError, match="dada de baja"):
            dao.crear(ids['socio'], ids['libro'], ids['norte'])


class TestRetirar:
    def test_crea_un_prestamo_local_activo(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['central'])
        dao.retirar(dao.listar()[0]['id'])
        assert dao.listar()[0]['estado'] == EstadoReserva.CUMPLIDA
        prestamo = prestamos.listar()[0]
        assert prestamo['tipo'] == TipoPrestamo.LOCAL
        assert prestamo['estado'] == EstadoPrestamo.ACTIVO
        assert prestamo['origen'] == prestamo['destino'] == "Central"
        assert prestamo['fecha_vencimiento'] == (date.today() + timedelta(days=31)).strftime("%d/%m/%Y")
        assert estado_ejemplar() == EstadoEjemplar.PRESTADO

    def test_solo_se_retira_una_disponible(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['norte'])
        with pytest.raises(ReglaNegocioError, match="Solo se retira una reserva DISPONIBLE"):
            dao.retirar(dao.listar()[0]['id'])
        assert prestamos.listar() == []

    def test_socio_inhabilitado_no_retira(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['central'])
        SocioDAO().inhabilitar(ids['socio'])
        with pytest.raises(ReglaNegocioError, match="no está habilitado"):
            dao.retirar(dao.listar()[0]['id'])
        # Se deshizo todo: la reserva sigue esperando con su ejemplar
        assert dao.listar()[0]['estado'] == EstadoReserva.DISPONIBLE
        assert estado_ejemplar() == EstadoEjemplar.RESERVADO


class TestAsignacion:
    def test_cancelar_pasa_el_ejemplar_a_la_siguiente(self):
        ids = preparar()
        primero, segundo = ids['socios']
        dao.crear(primero, ids['libro'], ids['central'])
        dao.crear(segundo, ids['libro'], ids['central'])
        assert [fila['estado'] for fila in dao.listar()] == [EstadoReserva.PENDIENTE, EstadoReserva.DISPONIBLE]
        dao.cancelar(dao.listar()[1]['id'])
        assert [fila['estado'] for fila in dao.listar()] == [EstadoReserva.DISPONIBLE, EstadoReserva.CANCELADA]
        assert estado_ejemplar() == EstadoEjemplar.RESERVADO

    def test_cancelar_un_prestamo_aprobado_libera_para_la_reserva(self):
        ids = preparar()
        prestamos.solicitar(TipoPrestamo.INTERBIBLIOTECARIO, ids['socio'], ids['ejemplar'], ids['central'],
                            ids['norte'])
        prestamo_id = prestamos.listar()[0]['id']
        prestamos.aprobar(prestamo_id)
        dao.crear(ids['socios'][1], ids['libro'], ids['central'])
        assert dao.listar()[0]['estado'] == EstadoReserva.PENDIENTE
        prestamos.cancelar(prestamo_id)
        assert dao.listar()[0]['estado'] == EstadoReserva.DISPONIBLE
        assert estado_ejemplar() == EstadoEjemplar.RESERVADO

    def test_no_se_cancela_dos_veces(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['norte'])
        dao.cancelar(dao.listar()[0]['id'])
        with pytest.raises(ReglaNegocioError, match="No se puede cancelar una reserva CANCELADA"):
            dao.cancelar(dao.listar()[0]['id'])


class TestVencimientos:
    def test_pendiente_que_paso_la_espera(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['norte'])
        assert dao.procesar_vencimientos() == 0
        correr_vencimiento(1)
        assert dao.procesar_vencimientos() == 1
        assert dao.listar()[0]['estado'] == EstadoReserva.VENCIDA

    def test_disponible_no_retirada_libera_el_ejemplar(self):
        ids = preparar()
        primero, segundo = ids['socios']
        dao.crear(primero, ids['libro'], ids['central'])
        dao.crear(segundo, ids['libro'], ids['central'])
        correr_vencimiento(1)
        # Vencen las dos, pero la segunda recibe el ejemplar liberado antes
        # (y con eso un plazo de retiro nuevo), así que no se procesa
        assert dao.procesar_vencimientos() == 1
        estados = [fila['estado'] for fila in reversed(dao.listar())]
        assert estados == [EstadoReserva.VENCIDA, EstadoReserva.DISPONIBLE]
        assert estado_ejemplar() == EstadoEjemplar.RESERVADO

    def test_vencida_sin_otra_reserva_deja_el_ejemplar_libre(self):
        ids = preparar()
        dao.crear(ids['socio'], ids['libro'], ids['central'])
        correr_vencimiento(1)
        dao.procesar_vencimientos()
        assert estado_ejemplar() == EstadoEjemplar.DISPONIBLE
