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
SEMANA = [(DiaSemana.LUNES, "08:00", "18:00")]


def crear_sede(nombre="Central"):
    """Crea una sede válida y devuelve su id."""
    dao.crear(nombre, "Avenida Colón 1200", "54", "3514210000", "central@biblio.org",
              [(DiaSemana.LUNES, "08:00", "18:00")])
    for sede in dao.listar():
        if sede['nombre'] == nombre:
            return sede['id']


class TestAltaSede:
    def test_alta_con_su_horario(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        sede = dao.listar()[0]
        assert sede['nombre'] == "Central"
        assert sede['estado'] == EstadoSede.ACTIVA
        assert dao.listar_horarios(sede_id) == [
            {'id': 1, 'dia': DiaSemana.LUNES, 'apertura': "08:00", 'cierre': "18:00"}]

    def test_email_opcional(self):
        preparar_base_en_memoria()
        dao.crear("Norte", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")])
        assert dao.listar()[0]['email'] == ""

    def test_datos_invalidos(self):
        preparar_base_en_memoria()
        casos = [
            ("", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")]),
            ("Norte", "Calle 1", "54", "3514000000", "", []),
            ("12345", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")]),
            ("Norte", "", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")]),
            ("Norte", "1234", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")]),
            ("Norte", "Calle 1", "54", "tel-abc", "", [(DiaSemana.LUNES, "08:00", "18:00")]),
            ("Norte", "Calle 1", "54", "3514000000", "sin-arroba", [(DiaSemana.LUNES, "08:00", "18:00")]),
            ("Norte", "Calle 1", "54", "3514000000", "", [("FERIADO", "08:00", "18:00")]),
            ("Norte", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "25:00", "18:00")]),
            ("Norte", "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "18:00", "08:00")]),
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


    def test_nombre_con_numeros(self):
        preparar_base_en_memoria()
        crear_sede("7 soles")
        assert dao.listar()[0]['nombre'] == "7 Soles"


class TestModificarSede:
    def test_modificar_sin_chocar_consigo_misma(self):
        preparar_base_en_memoria()
        sede_id = crear_sede("Central")
        dao.modificar(sede_id, "central", "Otra dirección 50", "54", "3514999999", "", SEMANA)
        sede = dao.listar()[0]
        assert sede['nombre'] == "Central"  # se guarda capitalizado
        assert sede['direccion'] == "Otra dirección 50"

    def test_modificar_con_nombre_de_otra(self):
        preparar_base_en_memoria()
        crear_sede("Central")
        norte_id = crear_sede("Norte")
        with pytest.raises(ReglaNegocioError, match="Ya existe una sede"):
            dao.modificar(norte_id, "CENTRAL", "Calle 1", "54", "3514000000", "", SEMANA)

    def test_sede_inexistente(self):
        preparar_base_en_memoria()
        with pytest.raises(ReglaNegocioError, match="No se encontró"):
            dao.modificar(99, "Norte", "Calle 1", "54", "3514000000", "", SEMANA)
        with pytest.raises(ValidacionError, match="Seleccione"):
            dao.modificar(None, "Norte", "Calle 1", "54", "3514000000", "", SEMANA)


class TestHorarios:
    def test_varios_dias_cada_uno_con_su_horario(self):
        preparar_base_en_memoria()
        semana = [(DiaSemana.SABADO, "09:00", "13:00"), (DiaSemana.LUNES, "08:00", "18:00"),
                  (DiaSemana.MIERCOLES, "08:00", "20:30")]
        dao.crear("Norte", "Calle 1", "54", "3514000000", "", semana)
        sede_id = dao.listar()[0]['id']
        horarios = [(h['dia'], h['apertura'], h['cierre']) for h in dao.listar_horarios(sede_id)]
        # Se listan ordenados por día de la semana
        assert horarios == [(DiaSemana.LUNES, "08:00", "18:00"), (DiaSemana.MIERCOLES, "08:00", "20:30"),
                            (DiaSemana.SABADO, "09:00", "13:00")]

    def test_modificar_reemplaza_la_semana(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.modificar(sede_id, "Central", "Calle 1", "54", "3514000000", "",
                      [(DiaSemana.MARTES, "09:00", "13:00"), (DiaSemana.JUEVES, "10:00", "14:00")])
        assert [h['dia'] for h in dao.listar_horarios(sede_id)] == [DiaSemana.MARTES, DiaSemana.JUEVES]

    def test_semana_invalida(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        casos = {
            "al menos un día": [],
            "repetido": [(DiaSemana.LUNES, "08:00", "18:00"), (DiaSemana.LUNES, "09:00", "12:00")],
            "MARTES: La hora de apertura debe ser anterior": [(DiaSemana.LUNES, "08:00", "18:00"),
                                                              (DiaSemana.MARTES, "18:00", "08:00")],
            "Elija la hora de apertura y la de cierre del MARTES": [(DiaSemana.MARTES, "", "18:00")],
        }
        for mensaje, semana in casos.items():
            with pytest.raises(ValidacionError, match=mensaje):
                dao.modificar(sede_id, "Central", "Calle 1", "54", "3514000000", "", semana)
        # La semana anterior queda como estaba
        assert [h['dia'] for h in dao.listar_horarios(sede_id)] == [DiaSemana.LUNES]


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

    def test_volver_a_dar_de_alta(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.dar_de_baja(sede_id)
        dao.reactivar(sede_id)
        assert dao.listar()[0]['estado'] == EstadoSede.ACTIVA
        assert dao.opciones() == [(sede_id, "Central")]
        with pytest.raises(ReglaNegocioError, match="ya está activa"):
            dao.reactivar(sede_id)

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
