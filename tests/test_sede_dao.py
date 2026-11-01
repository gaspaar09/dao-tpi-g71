from datetime import date

import pytest

from constantes import DiaSemana, EstadoReserva, EstadoSede, TipoMaterial
from dao.sede_dao import SedeDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.catalogo import Libro, Categoria
from modelos.reserva import Reserva
from tests.auxiliares import preparar_base_en_memoria, crear_socio

dao = SedeDAO()


def crear_sede(nombre="Central"):
    """Crea una sede válida y devuelve su id."""
    dao.crear(nombre, "Avenida Colón 1200", "54", "3514210000", "central@biblio.org",
              DiaSemana.LUNES, "08:00", "18:00")
    for sede in dao.listar():
        if sede['nombre'] == nombre:
            return sede['id']


class TestAltaSede:
    def test_alta_con_su_primer_horario(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        sede = dao.listar()[0]
        assert sede['nombre'] == "Central"
        assert sede['estado'] == EstadoSede.ACTIVA
        assert dao.listar_horarios(sede_id) == [
            {'id': 1, 'dia': DiaSemana.LUNES, 'apertura': "08:00", 'cierre': "18:00"}]

    def test_email_opcional(self):
        preparar_base_en_memoria()
        dao.crear("Norte", "Calle 1", "54", "3514000000", "", DiaSemana.LUNES, "08:00", "18:00")
        assert dao.listar()[0]['email'] == ""

    def test_datos_invalidos(self):
        preparar_base_en_memoria()
        casos = [
            ("", "Calle 1", "54", "3514000000", "", DiaSemana.LUNES, "08:00", "18:00"),
            ("12345", "Calle 1", "54", "3514000000", "", DiaSemana.LUNES, "08:00", "18:00"),
            ("Norte", "", "54", "3514000000", "", DiaSemana.LUNES, "08:00", "18:00"),
            ("Norte", "1234", "54", "3514000000", "", DiaSemana.LUNES, "08:00", "18:00"),
            ("Norte", "Calle 1", "54", "tel-abc", "", DiaSemana.LUNES, "08:00", "18:00"),
            ("Norte", "Calle 1", "54", "3514000000", "sin-arroba", DiaSemana.LUNES, "08:00", "18:00"),
            ("Norte", "Calle 1", "54", "3514000000", "", "FERIADO", "08:00", "18:00"),
            ("Norte", "Calle 1", "54", "3514000000", "", DiaSemana.LUNES, "25:00", "18:00"),
            ("Norte", "Calle 1", "54", "3514000000", "", DiaSemana.LUNES, "18:00", "08:00"),
        ]
        for caso in casos:
            with pytest.raises(ValidacionError):
                dao.crear(*caso)
        assert dao.listar() == []

    def test_nombre_duplicado_sin_importar_mayusculas(self):
        preparar_base_en_memoria()
        crear_sede("Central")
        for nombre in ["Central", "central", "  CENTRAL  "]:
            with pytest.raises(ReglaNegocioError, match="Ya existe una sede"):
                crear_sede(nombre)


class TestModificarSede:
    def test_modificar_sin_chocar_consigo_misma(self):
        preparar_base_en_memoria()
        sede_id = crear_sede("Central")
        dao.modificar(sede_id, "central", "Otra dirección 50", "54", "3514999999", "")
        sede = dao.listar()[0]
        assert sede['nombre'] == "Central"  # se guarda capitalizado
        assert sede['direccion'] == "Otra dirección 50"

    def test_modificar_con_nombre_de_otra(self):
        preparar_base_en_memoria()
        crear_sede("Central")
        norte_id = crear_sede("Norte")
        with pytest.raises(ReglaNegocioError, match="Ya existe una sede"):
            dao.modificar(norte_id, "CENTRAL", "Calle 1", "54", "3514000000", "")

    def test_sede_inexistente(self):
        preparar_base_en_memoria()
        with pytest.raises(ReglaNegocioError, match="No se encontró"):
            dao.modificar(99, "Norte", "Calle 1", "54", "3514000000", "")
        with pytest.raises(ValidacionError, match="Seleccione"):
            dao.modificar(None, "Norte", "Calle 1", "54", "3514000000", "")


class TestHorarios:
    def test_agregar_y_quitar(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.agregar_horario(sede_id, DiaSemana.MARTES, "09:00", "13:00")
        horarios = dao.listar_horarios(sede_id)
        assert [h['dia'] for h in horarios] == [DiaSemana.LUNES, DiaSemana.MARTES]
        dao.quitar_horario(horarios[0]['id'])
        assert [h['dia'] for h in dao.listar_horarios(sede_id)] == [DiaSemana.MARTES]

    def test_dia_repetido(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        with pytest.raises(ReglaNegocioError, match="ya tiene un horario"):
            dao.agregar_horario(sede_id, DiaSemana.LUNES, "09:00", "13:00")

    def test_no_se_quita_el_ultimo_horario(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        horario_id = dao.listar_horarios(sede_id)[0]['id']
        with pytest.raises(ReglaNegocioError, match="al menos un horario"):
            dao.quitar_horario(horario_id)


class TestBajaSede:
    def test_baja(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.dar_de_baja(sede_id)
        assert dao.listar()[0]['estado'] == EstadoSede.BAJA
        assert dao.opciones() == []
        assert dao.opciones(solo_activas=False) == [(sede_id, "Central")]

    def test_no_se_da_de_baja_dos_veces(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.dar_de_baja(sede_id)
        with pytest.raises(ReglaNegocioError, match="ya está dada de baja"):
            dao.dar_de_baja(sede_id)

    def test_no_se_da_de_baja_con_reservas_pendientes(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        with obtener_session() as session:
            libro = Libro(isbn="9789500700011", titulo="Rayuela", editorial="Sudamericana",
                          anio_edicion=1963, idioma="Español", tipo_material=TipoMaterial.LIBRO,
                          categoria=Categoria(nombre="Novela"))
            session.add(Reserva(socio=crear_socio(), libro=libro, sede_retiro_id=sede_id,
                                estado=EstadoReserva.PENDIENTE, fecha_vencimiento=date.today()))
        with pytest.raises(ReglaNegocioError, match="reservas pendientes"):
            dao.dar_de_baja(sede_id)
