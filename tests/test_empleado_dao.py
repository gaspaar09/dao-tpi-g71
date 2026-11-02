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
    SedeDAO().crear(nombre, "Calle 1", "54", "3514000000", "", [(DiaSemana.LUNES, "08:00", "18:00")])
    return SedeDAO().opciones(solo_activas=False)[-1][0]


class TestAltaEmpleado:
    def test_alta(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        assert dao.crear("Laura Gómez", RolEmpleado.BIBLIOTECARIO, sede_id) == "B1"
        empleado = dao.listar()[0]
        assert empleado['legajo'] == "B1"
        assert empleado['sede'] == "Central"
        assert dao.opciones() == [(empleado['id'], "Laura Gómez (Legajo B1)")]

    def test_datos_invalidos(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        casos = [
            ("", RolEmpleado.BIBLIOTECARIO, sede_id),
            ("Laura123", RolEmpleado.BIBLIOTECARIO, sede_id),
            ("L", RolEmpleado.BIBLIOTECARIO, sede_id),
            ("Laura", "GERENTE", sede_id),
            ("Laura", "", sede_id),
            ("Laura", RolEmpleado.BIBLIOTECARIO, None),
        ]
        for caso in casos:
            with pytest.raises(ValidacionError):
                dao.crear(*caso)

    def test_legajo_correlativo_por_rol(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        legajos = [dao.crear("Laura", RolEmpleado.BIBLIOTECARIO, sede_id),
                   dao.crear("Martín", RolEmpleado.ADMINISTRADOR, sede_id),
                   dao.crear("Sofía", RolEmpleado.BIBLIOTECARIO, sede_id),
                   dao.crear("Pedro", RolEmpleado.ADMINISTRADOR, sede_id)]
        assert legajos == ["B1", "A1", "B2", "A2"]

    def test_sigue_al_ultimo_registrado(self):
        """Si se elimina un empleado del medio, el siguiente no repite número."""
        preparar_base_en_memoria()
        sede_id = crear_sede()
        for nombre in ["Laura", "Sofía", "Pedro"]:
            dao.crear(nombre, RolEmpleado.BIBLIOTECARIO, sede_id)
        dao.eliminar([e['id'] for e in dao.listar() if e['legajo'] == "B2"][0])
        assert dao.crear("Ana", RolEmpleado.BIBLIOTECARIO, sede_id) == "B4"

    def test_orden_numerico(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        for numero in range(10):
            dao.crear("Persona " + chr(65 + numero), RolEmpleado.BIBLIOTECARIO, sede_id)
        assert [e['legajo'] for e in dao.listar()][-2:] == ["B9", "B10"]

    def test_sede_de_baja(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        SedeDAO().dar_de_baja(sede_id)
        with pytest.raises(ReglaNegocioError, match="dada de baja"):
            dao.crear("Laura", RolEmpleado.BIBLIOTECARIO, sede_id)


class TestModificarYEliminarEmpleado:
    def test_modificar(self):
        preparar_base_en_memoria()
        central = crear_sede("Central")
        norte = crear_sede("Norte")
        dao.crear("Laura", RolEmpleado.BIBLIOTECARIO, central)
        empleado_id = dao.listar()[0]['id']
        # Mismo rol: el legajo no cambia
        assert dao.modificar(empleado_id, "Laura Paz", RolEmpleado.BIBLIOTECARIO, norte) == "B1"
        empleado = dao.listar()[0]
        assert (empleado['nombre'], empleado['rol'], empleado['sede']) == ("Laura Paz", "BIBLIOTECARIO", "Norte")

    def test_cambio_de_rol_da_legajo_nuevo(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        dao.crear("Pedro", RolEmpleado.ADMINISTRADOR, sede_id)
        dao.crear("Laura", RolEmpleado.BIBLIOTECARIO, sede_id)
        laura_id = [e['id'] for e in dao.listar() if e['legajo'] == "B1"][0]
        assert dao.modificar(laura_id, "Laura", RolEmpleado.ADMINISTRADOR, sede_id) == "A2"
        assert [e['legajo'] for e in dao.listar()] == ["A1", "A2"]

    def test_eliminar(self):
        preparar_base_en_memoria()
        dao.crear("Laura", RolEmpleado.BIBLIOTECARIO, crear_sede())
        dao.eliminar(dao.listar()[0]['id'])
        assert dao.listar() == []

    def test_no_se_elimina_si_registro_movimientos(self):
        preparar_base_en_memoria()
        sede_id = crear_sede()
        otra_id = crear_sede("Norte")
        dao.crear("Laura", RolEmpleado.BIBLIOTECARIO, sede_id)
        empleado_id = dao.listar()[0]['id']
        with obtener_session() as session:
            remito = Remito(nro_remito="REM-000001", tipo=TipoEnvio.IDA, sede_origen_id=sede_id,
                            sede_destino_id=otra_id, fecha_creacion=date.today())
            remito.movimientos.append(MovimientoRemito(empleado_id=empleado_id,
                                                       estado_nuevo=EstadoRemito.EMPAQUETADO))
            session.add(remito)
        with pytest.raises(ReglaNegocioError, match="registró movimientos"):
            dao.eliminar(empleado_id)
