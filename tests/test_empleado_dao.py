from datetime import date

import pytest

from constantes import DiaSemana, EstadoRemito, RolEmpleado, TipoEnvio
from dao.empleado_dao import EmpleadoDAO
from dao.sede_dao import SedeDAO
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.remito import Remito, MovimientoRemito
from tests.auxiliares import preparar_base_en_memoria

dao = EmpleadoDAO()


def crear_sede(nombre="Central"):
    SedeDAO().crear(nombre, "Calle 1", "54", "3514000000", "", DiaSemana.LUNES, "08:00", "18:00")
    return SedeDAO().opciones(solo_activas=False)[-1][0]


class TestAltaEmpleado:
    def test_alta(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.crear(" e001 ", "Laura Gómez", RolEmpleado.BIBLIOTECARIO, sede_id)
        empleado = dao.listar()[0]
        assert empleado['legajo'] == "E001"
        assert empleado['sede'] == "Central"
        assert dao.opciones() == [(empleado['id'], "Laura Gómez (Legajo E001)")]

    def test_datos_invalidos(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        casos = [
            ("", "Laura", RolEmpleado.BIBLIOTECARIO, sede_id),
            ("E-01", "Laura", RolEmpleado.BIBLIOTECARIO, sede_id),
            ("E01", "Laura123", RolEmpleado.BIBLIOTECARIO, sede_id),
            ("E01", "L", RolEmpleado.BIBLIOTECARIO, sede_id),
            ("E01", "Laura", "GERENTE", sede_id),
            ("E01", "Laura", RolEmpleado.BIBLIOTECARIO, None),
        ]
        for caso in casos:
            with pytest.raises(ValidacionError):
                dao.crear(*caso)

    def test_legajo_duplicado(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.crear("E001", "Laura", RolEmpleado.BIBLIOTECARIO, sede_id)
        with pytest.raises(ReglaNegocioError, match="legajo E001"):
            dao.crear("e001", "Otra", RolEmpleado.BIBLIOTECARIO, sede_id)

    def test_sede_de_baja(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        SedeDAO().dar_de_baja(sede_id)
        with pytest.raises(ReglaNegocioError, match="dada de baja"):
            dao.crear("E001", "Laura", RolEmpleado.BIBLIOTECARIO, sede_id)


class TestModificarYEliminarEmpleado:
    def test_modificar(self):
        preparar_base_en_memoria()
        central = crear_sede("Central")
        norte = crear_sede("Norte")
        dao.crear("E001", "Laura", RolEmpleado.BIBLIOTECARIO, central)
        empleado_id = dao.listar()[0]['id']
        dao.modificar(empleado_id, "E001", "Laura Paz", RolEmpleado.ADMINISTRADOR, norte)
        empleado = dao.listar()[0]
        assert (empleado['nombre'], empleado['rol'], empleado['sede']) == ("Laura Paz", "ADMINISTRADOR", "Norte")

    def test_eliminar(self):
        preparar_base_en_memoria()
        dao.crear("E001", "Laura", RolEmpleado.BIBLIOTECARIO, crear_sede())
        dao.eliminar(dao.listar()[0]['id'])
        assert dao.listar() == []

    def test_no_se_elimina_si_registro_movimientos(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        otra_id = crear_sede("Norte")
        dao.crear("E001", "Laura", RolEmpleado.BIBLIOTECARIO, sede_id)
        empleado_id = dao.listar()[0]['id']
        with obtener_session() as session:
            remito = Remito(nro_remito="REM-000001", tipo=TipoEnvio.IDA, sede_origen_id=sede_id,
                            sede_destino_id=otra_id, fecha_creacion=date.today())
            remito.movimientos.append(MovimientoRemito(empleado_id=empleado_id,
                                                       estado_nuevo=EstadoRemito.EMPAQUETADO))
            session.add(remito)
        with pytest.raises(ReglaNegocioError, match="registró movimientos"):
            dao.eliminar(empleado_id)
