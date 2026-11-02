"""Pasada por el checklist de docs/VALIDACIONES.md ("Casos a probar en todos
los campos"): cada valor inválido tiene que terminar en ValidacionError o
ReglaNegocioError, nunca guardarse ni romper con otra excepción (por ejemplo
un IntegrityError de la base).

Se parte de un alta válida y se reemplaza un campo por vez. Como una
operación rechazada no guarda nada (obtener_session hace rollback), la base
de ejemplo se carga una sola vez por DAO.
"""

from datetime import date

import pytest

from dao.autor_dao import AutorDAO
from dao.categoria_dao import CategoriaDAO
from dao.devolucion_dao import DevolucionDAO
from dao.ejemplar_dao import EjemplarDAO
from dao.empleado_dao import EmpleadoDAO
from dao.libro_dao import LibroDAO
from dao.prestamo_dao import PrestamoDAO
from dao.remito_dao import RemitoDAO
from dao.reserva_dao import ReservaDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from datos_ejemplo import cargar_datos_ejemplo
from excepciones import ValidacionError, ReglaNegocioError
from tests.auxiliares import preparar_base_en_memoria

HOY = date.today().strftime("%d/%m/%Y")
TEXTOS = ["", "   ", "x" * 400, "😀😀", None]
NUMEROS = ["-5", "0", "1.5", "1e5", "1,5", "99999999999999999999", "abc", " ", None]
FECHAS = ["30/02/2026", "2026-01-01", "1/1/26", "01/01/3000", "aa/bb/cccc", "", None]
IDS = [None, "", 999999, -1]


def preparar():
    preparar_base_en_memoria()
    cargar_datos_ejemplo()


def id_sede(nombre):
    return [id for id, texto in SedeDAO().opciones(solo_activas=False) if texto == nombre][0]


def id_ejemplar(codigo):
    return [fila['id'] for fila in EjemplarDAO().listar() if fila['codigo_inventario'] == codigo][0]


def rechaza_cada_valor(operacion, valida, campos):
    """operacion(*args) con args = valida y un campo reemplazado por cada valor
    inválido. campos = {posición del argumento: [valores inválidos]}."""
    for posicion, valores in campos.items():
        for valor in valores:
            args = list(valida)
            args[posicion] = valor
            with pytest.raises((ValidacionError, ReglaNegocioError)):
                operacion(*args)


class TestAltasConDatosInvalidos:
    def test_sede(self):
        preparar()
        valida = ["Sede Oeste", "Calle 1", "54", "3514000099", "o@b.org", [("LUNES", "08:00", "18:00")]]
        rechaza_cada_valor(SedeDAO().crear, valida, {
            0: TEXTOS + ["7", "77", "Sede #7", "Biblioteca central"],  # el último, duplicado
            1: TEXTOS + ["Av. Colón 1200", "1234"],
            2: TEXTOS + ["999", "+54"],
            3: NUMEROS + ["351 400", "(351)4000000"],
            4: ["x" * 400 + "@b.org", "a@", "@b.c", "a b@c.d", "sin arroba"],
            5: [[],  # ningún día de apertura
                [("FERIADO", "08:00", "18:00")], [("", "08:00", "18:00")], [(None, "08:00", "18:00")],
                [("LUNES", "25:00", "18:00")], [("LUNES", "8", "18:00")], [("LUNES", "08:60", "18:00")],
                [("LUNES", "", "18:00")], [("LUNES", "08:00", "abc")],
                [("LUNES", "08:00", "07:00")], [("LUNES", "08:00", "08:00")],  # cierre antes o igual
                [("LUNES", "08:00", "18:00"), ("LUNES", "09:00", "12:00")],  # día repetido
                [("LUNES", "08:00", "18:00"), ("MARTES", "18:00", "08:00")]],  # un solo día mal
        })
        assert len(SedeDAO().listar()) == 3

    def test_empleado(self):
        preparar()
        valida = ["Pedro Gil", "BIBLIOTECARIO", id_sede("Biblioteca Central")]
        rechaza_cada_valor(EmpleadoDAO().crear, valida, {
            0: TEXTOS + ["Pedro2", "P"],
            1: TEXTOS + ["GERENTE"],
            2: IDS,
        })

    def test_socio(self):
        preparar()
        valida = ["40111222", "Luis", "Paz", "", "54", "3515550099"]
        rechaza_cada_valor(SocioDAO().crear, valida, {
            0: NUMEROS + ["1.000000", "00000005", "123456789", "999999", "30.111.222"],  # el último, repetido
            1: TEXTOS + ["Luis3", "L"],
            2: TEXTOS + ["<script>"],
            3: ["x" * 400, "a@", "sin arroba"],
            4: TEXTOS + ["999"],
            5: NUMEROS[6:] + TEXTOS + ["12345", "1234567890123456", "351-555"],
        })
        assert len(SocioDAO().listar()) == 4

    def test_catalogo(self):
        preparar()
        rechaza_cada_valor(AutorDAO().crear, ["Ana", "Lopez"], {0: TEXTOS + ["Ana1"], 1: TEXTOS})
        with pytest.raises(ReglaNegocioError):
            AutorDAO().crear("julio", "  cortázar ")  # duplicado normalizado
        rechaza_cada_valor(CategoriaDAO().crear, ["Poesía"], {0: TEXTOS + ["123", "novela"]})
        valida = ["9780000000019", "Libro nuevo", "Editorial", "2000", "Español", "LIBRO",
                  CategoriaDAO().opciones()[0][0], [AutorDAO().opciones()[0][0]]]
        rechaza_cada_valor(LibroDAO().crear, valida, {
            0: TEXTOS + ["123", "12345678901234", "ABCDEFGH", "978-950-070-001-1"],  # el último, repetido
            1: TEXTOS + ["12345"],
            2: TEXTOS,
            3: NUMEROS + ["1449", str(date.today().year + 1)],
            4: TEXTOS + ["Español 2"],
            5: TEXTOS + ["COMIC"],
            6: IDS,
            7: [[], None, [999999]],
        })

    def test_ejemplar(self):
        preparar()
        valida = ["NUE-001", LibroDAO().opciones()[0][0], id_sede("Biblioteca Central"), "BUENO"]
        rechaza_cada_valor(EjemplarDAO().crear, valida, {
            0: TEXTOS + ["AB", "A B", "nue_001", "ray-001"],  # el último, repetido en minúsculas
            1: IDS,
            2: IDS,
            3: TEXTOS + ["ROTO"],
        })


class TestOperacionesConDatosInvalidos:
    def test_prestamo(self):
        preparar()
        valida = ["LOCAL", SocioDAO().opciones()[0][0], id_ejemplar("MOR-003"), id_sede("Sede Norte"), None]
        rechaza_cada_valor(PrestamoDAO().solicitar, valida, {0: TEXTOS + ["EXPRESS"], 1: IDS, 2: IDS, 3: IDS})

    def test_reserva(self):
        preparar()
        valida = [SocioDAO().opciones()[0][0], LibroDAO().opciones()[0][0], id_sede("Sede Norte")]
        rechaza_cada_valor(ReservaDAO().crear, valida, {0: IDS, 1: IDS, 2: IDS})

    def test_remito(self):
        preparar()
        empaquetado = RemitoDAO().listar()[-1]['id']
        empleado = EmpleadoDAO().opciones()[0][0]
        rechaza_cada_valor(RemitoDAO().registrar_incidencia, [empaquetado, "DEMORA", HOY, "Descripción válida"], {
            0: IDS, 1: TEXTOS + ["INCENDIO"], 2: FECHAS, 3: TEXTOS + ["roto"],
        })
        rechaza_cada_valor(RemitoDAO().avanzar, [empaquetado, empleado, ""], {0: IDS, 1: IDS, 2: ["x" * 201]})
        rechaza_cada_valor(RemitoDAO().cancelar, [empaquetado, empleado, "Motivo válido"],
                           {0: IDS, 1: IDS, 2: TEXTOS + ["no"]})

    def test_devolucion(self):
        preparar()
        prestamo = [fila['id'] for fila in PrestamoDAO().listar() if fila['ejemplar'] == "RAY-001"][0]
        valida = [prestamo, HOY, "BUENO", "", EmpleadoDAO().opciones()[0][0]]
        rechaza_cada_valor(DevolucionDAO().registrar, valida, {
            0: IDS, 1: FECHAS, 2: TEXTOS + ["ROTO"], 3: ["x" * 301], 4: IDS,
        })
        # Dañado sin observaciones
        with pytest.raises(ValidacionError):
            DevolucionDAO().registrar(prestamo, HOY, "DAÑADO", "  ", EmpleadoDAO().opciones()[0][0])


class TestIdsInexistentes:
    def test_acciones_sobre_algo_que_no_existe(self):
        """Por ejemplo, un registro que se eliminó mientras otra pestaña lo mostraba."""
        preparar()
        acciones = [SedeDAO().dar_de_baja, SedeDAO().reactivar,
                    SocioDAO().inhabilitar, SocioDAO().habilitar, SocioDAO().dar_de_baja,
                    EmpleadoDAO().eliminar, AutorDAO().eliminar, CategoriaDAO().eliminar, LibroDAO().eliminar,
                    EjemplarDAO().dar_de_baja, PrestamoDAO().aprobar, PrestamoDAO().cancelar,
                    PrestamoDAO().pagar_multa, ReservaDAO().retirar, ReservaDAO().cancelar]
        for accion in acciones:
            for id in IDS:
                with pytest.raises((ValidacionError, ReglaNegocioError)):
                    accion(id)
