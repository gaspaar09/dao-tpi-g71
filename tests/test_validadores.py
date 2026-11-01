"""Tests de validadores.py con los casos de docs/VALIDACIONES.md."""

from datetime import date, time, timedelta

import pytest

from constantes import DiaSemana
from excepciones import ValidacionError
from validadores import (normalizar_texto, validar_texto, validar_texto_opcional,
                         validar_solo_letras, validar_entero, validar_numero_no_negativo,
                         validar_nro_socio, validar_anio_edicion, validar_dni, validar_email,
                         validar_telefono, validar_isbn, validar_codigo_inventario,
                         validar_legajo, validar_fecha, validar_fecha_no_futura,
                         validar_hora, validar_rango_horario, validar_opcion)

# Textos maliciosos o raros que los profes suelen probar
TEXTOS_RAROS = ["<script>alert(1)</script>", "' OR 1=1 --", "Ana😀", "Ana123", "Ana_Paz"]


class TestTexto:
    def test_normaliza_espacios(self):
        assert normalizar_texto("  Av.   Colón   123  ") == "Av. Colón 123"
        assert normalizar_texto(None) == ""

    def test_texto_valido(self):
        assert validar_texto("  Biblioteca  Central ", "nombre", 80) == "Biblioteca Central"

    def test_texto_vacio(self):
        for valor in ["", "   ", None]:
            with pytest.raises(ValidacionError, match="obligatorio"):
                validar_texto(valor, "nombre", 80)

    def test_largo_fuera_de_rango(self):
        with pytest.raises(ValidacionError, match="no puede superar los 80"):
            validar_texto("a" * 200, "nombre", 80)
        with pytest.raises(ValidacionError, match="al menos 2"):
            validar_texto("a", "nombre", 80, minimo=2)

    def test_texto_opcional(self):
        for valor in ["", "   ", None]:
            assert validar_texto_opcional(valor, "observaciones", 300) is None
        assert validar_texto_opcional(" Tapa rota ", "observaciones", 300) == "Tapa rota"
        with pytest.raises(ValidacionError, match="no puede superar"):
            validar_texto_opcional("a" * 301, "observaciones", 300)


class TestSoloLetras:
    def test_nombres_validos(self):
        for nombre in ["Ana", "José María", "O'Brien", "Pérez-Gómez", "Ñandú"]:
            assert validar_solo_letras(nombre, "nombre", 2, 50) == nombre

    def test_nombres_invalidos(self):
        for valor in TEXTOS_RAROS + ["12345", "Ana.", "Ana@"]:
            with pytest.raises(ValidacionError, match="solo puede tener letras"):
                validar_solo_letras(valor, "nombre", 2, 50)

    def test_largo(self):
        for valor in ["A", "a" * 51]:
            with pytest.raises(ValidacionError):
                validar_solo_letras(valor, "nombre", 2, 50)


class TestEntero:
    def test_entero_valido(self):
        assert validar_entero(" 42 ", "cantidad", 1) == 42
        assert validar_entero(7, "cantidad", 1) == 7

    def test_no_es_entero(self):
        for valor in ["abc", "1.5", "1e5", "1,5", "dos mil", "12a", "²"]:
            with pytest.raises(ValidacionError, match="número entero"):
                validar_entero(valor, "cantidad", 1)

    def test_vacio(self):
        for valor in ["", "  ", None]:
            with pytest.raises(ValidacionError, match="obligatorio"):
                validar_entero(valor, "cantidad", 1)

    def test_fuera_de_rango(self):
        for valor in ["-5", "0", "99999999999999999999"]:
            with pytest.raises(ValidacionError, match="debe estar entre"):
                validar_entero(valor, "cantidad", 1)

    def test_nro_socio(self):
        assert validar_nro_socio("15") == 15
        for valor in ["-1", "0", "abc"]:
            with pytest.raises(ValidacionError):
                validar_nro_socio(valor)

    def test_anio_edicion(self):
        assert validar_anio_edicion("1963") == 1963
        assert validar_anio_edicion(str(date.today().year)) == date.today().year
        for valor in ["-1", "1449", "3000", str(date.today().year + 1), "dos mil"]:
            with pytest.raises(ValidacionError):
                validar_anio_edicion(valor)


class TestNumeroNoNegativo:
    def test_validos(self):
        assert validar_numero_no_negativo("0", "monto") == 0
        assert validar_numero_no_negativo("150.456", "monto") == 150.46

    def test_invalidos(self):
        for valor in ["-1", "abc", "1,5", "nan", "inf", "", "-inf"]:
            with pytest.raises(ValidacionError):
                validar_numero_no_negativo(valor, "monto")


class TestDni:
    def test_dni_valido(self):
        assert validar_dni("12345678") == "12345678"
        assert validar_dni(" 12.345.678 ") == "12345678"
        assert validar_dni("1234567") == "1234567"

    def test_dni_con_letras_o_signos(self):
        for valor in ["abc", "-5", "1234567a", "12,345,678"]:
            with pytest.raises(ValidacionError, match="solo puede tener números"):
                validar_dni(valor)

    def test_dni_largo_invalido(self):
        for valor in ["123456", "1234567890123"]:
            with pytest.raises(ValidacionError, match="7 u 8 dígitos"):
                validar_dni(valor)

    def test_dni_vacio(self):
        for valor in ["", "   ", "..."]:
            with pytest.raises(ValidacionError, match="obligatorio"):
                validar_dni(valor)


class TestEmail:
    def test_email_valido(self):
        assert validar_email(" Ana.Paz@Mail.com ") == "ana.paz@mail.com"

    def test_email_invalido(self):
        for valor in ["anamail.com", "ana@@mail.com", "ana@mail@com", "ana @mail.com",
                      "ana@mail", "a@b.", "@mail.com", "ana@.com"]:
            with pytest.raises(ValidacionError, match="formato"):
                validar_email(valor)

    def test_email_obligatorio_u_opcional(self):
        with pytest.raises(ValidacionError, match="obligatorio"):
            validar_email("")
        assert validar_email("", obligatorio=False) is None

    def test_email_largo(self):
        with pytest.raises(ValidacionError, match="no puede superar"):
            validar_email("a" * 95 + "@mail.com")


class TestTelefono:
    def test_telefonos_validos(self):
        for valor in ["351 4000000", "+54 (351) 400-0000", "123456"]:
            assert validar_telefono(valor) == valor

    def test_caracteres_invalidos(self):
        for valor in ["abc123456", "351.400.0000", "351#4000000"]:
            with pytest.raises(ValidacionError, match="solo puede tener números"):
                validar_telefono(valor)

    def test_cantidad_de_digitos(self):
        for valor in ["12345", "1234567890123456"]:
            with pytest.raises(ValidacionError, match="entre 6 y 15 dígitos"):
                validar_telefono(valor)


class TestIsbn:
    def test_validos(self):
        assert validar_isbn("978-950-07-0001-1") == "9789500700011"
        assert validar_isbn("0-306-40615-2") == "0306406152"
        assert validar_isbn("0-8044-2957-x") == "080442957X"
        assert validar_isbn("0317-847x") == "0317847X"  # ISSN

    def test_largo_invalido(self):
        for valor in ["123456789", "123456789012", "1234567", "12345678901234"]:
            with pytest.raises(ValidacionError, match="8 \\(ISSN\\), 10 o 13"):
                validar_isbn(valor)

    def test_caracteres_invalidos(self):
        for valor in ["978950070001X", "97895A0700011", "03064X6152", "X306406152"]:
            with pytest.raises(ValidacionError, match="solo puede tener números"):
                validar_isbn(valor)


class TestCodigoInventario:
    def test_validos(self):
        assert validar_codigo_inventario(" ej-001 ") == "EJ-001"
        assert validar_codigo_inventario("ABC") == "ABC"

    def test_largo(self):
        for valor in ["AB", "A" * 21]:
            with pytest.raises(ValidacionError, match="entre 3 y 20"):
                validar_codigo_inventario(valor)

    def test_caracteres(self):
        for valor in ["EJ_001", "EJ 001", "EJ.001", "EJÑ01"]:
            with pytest.raises(ValidacionError, match="letras, números y guiones"):
                validar_codigo_inventario(valor)


class TestLegajo:
    def test_valido(self):
        assert validar_legajo(" e123 ") == "E123"

    def test_invalido(self):
        for valor in ["E-123", "E 123", "E_123", "<script>"]:
            with pytest.raises(ValidacionError, match="letras y números"):
                validar_legajo(valor)
        with pytest.raises(ValidacionError, match="no puede superar"):
            validar_legajo("A" * 21)


class TestFecha:
    def test_fecha_valida(self):
        assert validar_fecha("29/02/2024", "fecha") == date(2024, 2, 29)
        assert validar_fecha(" 1/3/2025 ", "fecha") == date(2025, 3, 1)

    def test_fecha_imposible(self):
        for valor in ["30/02/2024", "31/04/2024", "29/02/2023", "00/01/2024", "01/13/2024"]:
            with pytest.raises(ValidacionError, match="no es una fecha válida"):
                validar_fecha(valor, "fecha")

    def test_formato_invalido(self):
        for valor in ["2024-01-01", "1/1", "aa/bb/cccc", "01/01/2024/1", "-1/01/2024"]:
            with pytest.raises(ValidacionError, match="dd/mm/aaaa"):
                validar_fecha(valor, "fecha")

    def test_anio_de_dos_digitos(self):
        with pytest.raises(ValidacionError, match="4 dígitos"):
            validar_fecha("01/01/24", "fecha")

    def test_no_futura(self):
        assert validar_fecha_no_futura(date.today(), "fecha") == date.today()
        with pytest.raises(ValidacionError, match="futura"):
            validar_fecha_no_futura(date.today() + timedelta(days=1), "fecha")


class TestHora:
    def test_hora_valida(self):
        assert validar_hora("08:30", "apertura") == time(8, 30)
        assert validar_hora("8:00", "apertura") == time(8, 0)

    def test_hora_invalida(self):
        for valor in ["25:00", "12:60", "24:00"]:
            with pytest.raises(ValidacionError, match="no es una hora válida"):
                validar_hora(valor, "apertura")

    def test_formato_invalido(self):
        for valor in ["12", "12:5", "ab:cd", "12:00:00", ""]:
            with pytest.raises(ValidacionError, match="HH:MM"):
                validar_hora(valor, "apertura")

    def test_rango_horario(self):
        validar_rango_horario(time(8, 0), time(18, 0))  # no lanza
        for cierre in [time(8, 0), time(7, 0)]:
            with pytest.raises(ValidacionError, match="anterior a la de cierre"):
                validar_rango_horario(time(8, 0), cierre)


class TestOpcion:
    def test_opcion_valida(self):
        assert validar_opcion(DiaSemana.LUNES, DiaSemana.TODOS, "día") == "LUNES"

    def test_opcion_invalida(self):
        for valor in ["", "Lunes", "FERIADO", None]:
            with pytest.raises(ValidacionError, match="Seleccione un valor válido"):
                validar_opcion(valor, DiaSemana.TODOS, "día")
