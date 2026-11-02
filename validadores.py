"""Validaciones de formato de los datos ingresados.

Cada función normaliza el valor, lo valida y lo devuelve limpio, o lanza
ValidacionError con un mensaje concreto. Los DAO las usan siempre antes de
tocar la base (el backend es la fuente de verdad), por ejemplo:
    dni = validar_dni(dni)

Sin expresiones regulares: solo métodos de str, int(), float() y date().
"""

from datetime import date, time

from config import (LARGO_EMAIL, LARGO_TELEFONO, LARGO_CODIGO_INVENTARIO, MAXIMO_ENTERO,
                    ANIO_MINIMO_EDICION, DNI_MINIMO, DNI_MAXIMO)
from constantes import PaisTelefono
from excepciones import ValidacionError

# Se comprueba carácter por carácter contra estas cadenas. No se usa
# isnumeric() porque acepta caracteres como "²" o "½", que no son dígitos.
DIGITOS = "0123456789"
LETRAS_MAYUSCULAS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"


def solo_digitos(texto):
    """True si el texto no está vacío y tiene solo dígitos del 0 al 9."""
    if texto == "":
        return False
    for caracter in texto:
        if caracter not in DIGITOS:
            return False
    return True


def normalizar_texto(valor):
    """Quita espacios al principio y al final, y colapsa los repetidos."""
    if valor is None:
        return ""
    return " ".join(str(valor).split())


# ---------------------------------------------------------------- texto

def validar_texto(valor, campo, maximo, minimo=1):
    texto = normalizar_texto(valor)
    if texto == "":
        raise ValidacionError(f"El campo {campo} es obligatorio")
    if len(texto) < minimo:
        raise ValidacionError(f"El campo {campo} debe tener al menos {minimo} caracteres")
    if len(texto) > maximo:
        raise ValidacionError(f"El campo {campo} no puede superar los {maximo} caracteres")
    return texto


def validar_texto_con_letras(valor, campo, maximo, minimo=1):
    """Para nombres que pueden llevar números ("Sede 9 de Julio") pero no
    ser solo números o signos."""
    texto = validar_texto(valor, campo, maximo, minimo)
    for caracter in texto:
        if caracter.isalpha():
            return texto
    raise ValidacionError(f"El campo {campo} debe contener al menos una letra")


def validar_texto_opcional(valor, campo, maximo):
    """Para observaciones y otros campos no obligatorios: vacío devuelve None."""
    texto = normalizar_texto(valor)
    if texto == "":
        return None
    return validar_texto(texto, campo, maximo)


def capitalizar(texto):
    """"cArLos pÉrez" -> "Carlos Pérez". Si se escribió todo en mayúsculas
    se respeta tal cual ("CARLOS")."""
    if texto.isupper():
        return texto
    return texto.title()


def validar_solo_letras(valor, campo, minimo, maximo):
    """Nombres: letras (con tildes), espacios, apóstrofo y guion.
    Se guarda con mayúscula inicial en cada palabra."""
    texto = validar_texto(valor, campo, maximo, minimo)
    if not texto.replace(" ", "").replace("-", "").replace("'", "").isalpha():
        raise ValidacionError(f"El campo {campo} solo puede tener letras, espacios, apóstrofo y guion")
    return capitalizar(texto)


def validar_direccion(valor, campo, maximo):
    """Como un nombre, pero además admite números (la altura de la calle).
    Tiene que tener al menos una letra."""
    texto = validar_texto(valor, campo, maximo)
    tiene_letra = False
    for caracter in texto:
        if caracter.isalpha():
            tiene_letra = True
        elif caracter not in DIGITOS + " -'":
            raise ValidacionError(f"El campo {campo} solo puede tener letras, números, espacios, apóstrofo y guion")
    if not tiene_letra:
        raise ValidacionError(f"El campo {campo} debe contener al menos una letra")
    return texto


def validar_nombre_con_numeros(valor, campo, minimo, maximo):
    """Nombres que pueden llevar números ("7 Soles", "Sede 9 De Julio"):
    misma regla que la dirección y mayúscula inicial como los demás nombres."""
    texto = validar_texto(valor, campo, maximo, minimo)
    return capitalizar(validar_direccion(texto, campo, maximo))


# -------------------------------------------------------------- números

def validar_entero(valor, campo, minimo, maximo=MAXIMO_ENTERO):
    texto = normalizar_texto(valor)
    if texto == "":
        raise ValidacionError(f"El campo {campo} es obligatorio")
    try:
        numero = int(texto)  # rechaza letras, decimales, "1e5" y "1,5"
    except ValueError:
        raise ValidacionError(f"El campo {campo} debe ser un número entero")
    if numero < minimo or numero > maximo:
        raise ValidacionError(f"El campo {campo} debe estar entre {minimo} y {maximo}")
    return numero


def validar_numero_no_negativo(valor, campo):
    texto = normalizar_texto(valor)
    if texto == "":
        raise ValidacionError(f"El campo {campo} es obligatorio")
    try:
        numero = float(texto)
    except ValueError:
        raise ValidacionError(f"El campo {campo} debe ser un número (use punto para los decimales)")
    # float() acepta "nan" e "inf": nan es distinto de sí mismo
    if numero != numero or numero == float("inf") or numero == float("-inf"):
        raise ValidacionError(f"El campo {campo} debe ser un número válido")
    if numero < 0:
        raise ValidacionError(f"El campo {campo} no puede ser negativo")
    return round(numero, 2)


def validar_anio_edicion(valor):
    return validar_entero(valor, "año de edición", ANIO_MINIMO_EDICION, date.today().year)


# ------------------------------------------------- identificadores y contacto

def formatear_dni(texto):
    """Pone los puntos de miles: "12345678" -> "12.345.678".
    Ignora los puntos que ya tenga el texto."""
    digitos = texto.replace(".", "")
    grupos = []
    while len(digitos) > 3:
        grupos.insert(0, digitos[-3:])
        digitos = digitos[:-3]
    if digitos != "":
        grupos.insert(0, digitos)
    return ".".join(grupos)


def validar_dni(valor):
    """Se admite con o sin puntos (12.345.678 o 12345678); si tiene puntos,
    tienen que estar bien ubicados. Se guardan solo los dígitos."""
    texto = normalizar_texto(valor).replace(" ", "")
    dni = texto.replace(".", "")
    if dni == "":
        raise ValidacionError("El DNI es obligatorio")
    if not solo_digitos(dni):
        raise ValidacionError("El DNI solo puede tener números")
    if "." in texto and texto != formatear_dni(dni):
        raise ValidacionError("Los puntos del DNI están mal ubicados (ejemplo: 12.345.678)")
    if dni[0] == "0":
        raise ValidacionError("El DNI no puede empezar con 0")
    if int(dni) < DNI_MINIMO or int(dni) > DNI_MAXIMO:
        raise ValidacionError("El DNI debe estar entre 1.000.000 y 99.999.999")
    return dni


def validar_email(valor, campo="email", obligatorio=True):
    email = normalizar_texto(valor).lower()
    if email == "":
        if obligatorio:
            raise ValidacionError(f"El campo {campo} es obligatorio")
        return None
    if len(email) > LARGO_EMAIL:
        raise ValidacionError(f"El campo {campo} no puede superar los {LARGO_EMAIL} caracteres")
    if " " in email or email.count("@") != 1:
        raise ValidacionError(f"El campo {campo} debe tener el formato usuario@dominio.com")
    usuario, dominio = email.split("@")
    if usuario == "" or "." not in dominio or dominio.startswith(".") or dominio.endswith("."):
        raise ValidacionError(f"El campo {campo} debe tener el formato usuario@dominio.com")
    return email


def validar_telefono(valor, campo="teléfono"):
    """Número plano, sin el código de país (se elige aparte): solo dígitos,
    sin espacios, guiones ni "+"."""
    telefono = normalizar_texto(valor)
    if telefono == "":
        raise ValidacionError(f"El campo {campo} es obligatorio")
    if not solo_digitos(telefono):
        raise ValidacionError(f"El campo {campo} solo puede tener números, sin espacios, guiones ni +")
    if len(telefono) < 6 or len(telefono) > LARGO_TELEFONO:
        raise ValidacionError(f"El campo {campo} debe tener entre 6 y {LARGO_TELEFONO} dígitos")
    return telefono


def validar_prefijo_pais(valor):
    return validar_opcion(valor, PaisTelefono.TODOS, "país del teléfono")


def validar_isbn(valor):
    """Acepta ISBN-13, ISBN-10 e ISSN (8). Los dos últimos pueden terminar en X.
    No se verifica el dígito verificador."""
    isbn = normalizar_texto(valor).replace("-", "").replace(" ", "").upper()
    if isbn == "":
        raise ValidacionError("El ISBN/ISSN es obligatorio")
    if len(isbn) == 13:
        valido = solo_digitos(isbn)
    elif len(isbn) == 10 or len(isbn) == 8:
        valido = solo_digitos(isbn[:-1]) and (isbn[-1] in DIGITOS or isbn[-1] == "X")
    else:
        raise ValidacionError("El ISBN/ISSN debe tener 8 (ISSN), 10 o 13 caracteres sin contar los guiones")
    if not valido:
        raise ValidacionError("El ISBN/ISSN solo puede tener números (el ISSN y el ISBN-10 pueden terminar en X)")
    return isbn


def validar_codigo_inventario(valor):
    codigo = normalizar_texto(valor).upper()
    if codigo == "":
        raise ValidacionError("El código de inventario es obligatorio")
    if len(codigo) < 3 or len(codigo) > LARGO_CODIGO_INVENTARIO:
        raise ValidacionError(f"El código de inventario debe tener entre 3 y {LARGO_CODIGO_INVENTARIO} caracteres")
    for caracter in codigo:
        if caracter not in LETRAS_MAYUSCULAS + DIGITOS + "-":
            raise ValidacionError("El código de inventario solo puede tener letras, números y guiones")
    return codigo


# ------------------------------------------------------- fechas y horas

def validar_fecha(valor, campo):
    """Fecha en formato dd/mm/aaaa. date() lanza ValueError ante fechas
    imposibles como el 30/02."""
    texto = normalizar_texto(valor)
    if texto == "":
        raise ValidacionError(f"El campo {campo} es obligatorio")
    partes = texto.split("/")
    if len(partes) != 3 or not (solo_digitos(partes[0]) and solo_digitos(partes[1]) and solo_digitos(partes[2])):
        raise ValidacionError(f"El campo {campo} debe tener el formato dd/mm/aaaa")
    if len(partes[2]) != 4:
        raise ValidacionError(f"El año del campo {campo} debe tener 4 dígitos")
    try:
        return date(int(partes[2]), int(partes[1]), int(partes[0]))
    except ValueError:
        raise ValidacionError(f"El campo {campo} no es una fecha válida")


def validar_fecha_no_futura(fecha, campo):
    if fecha > date.today():
        raise ValidacionError(f"El campo {campo} no puede ser una fecha futura")
    return fecha


def validar_hora(valor, campo):
    """Hora en formato HH:MM."""
    texto = normalizar_texto(valor)
    partes = texto.split(":")
    if len(partes) != 2 or not (solo_digitos(partes[0]) and solo_digitos(partes[1])) or len(partes[1]) != 2:
        raise ValidacionError(f"El campo {campo} debe tener el formato HH:MM")
    try:
        return time(int(partes[0]), int(partes[1]))
    except ValueError:
        raise ValidacionError(f"El campo {campo} no es una hora válida")


def validar_rango_horario(apertura, cierre, dia=""):
    """dia es opcional: con una semana de horarios indica cuál está mal."""
    if apertura >= cierre:
        prefijo = f"{dia}: " if dia else ""
        raise ValidacionError(f"{prefijo}La hora de apertura debe ser anterior a la de cierre")


# ------------------------------------------------------------- opciones

def validar_opcion(valor, opciones, campo):
    """El valor debe estar en la lista (por ejemplo, TODOS de una constante).
    Aunque la UI use un Combobox, el backend lo controla igual."""
    if valor not in opciones:
        raise ValidacionError(f"Seleccione un valor válido para el campo {campo}")
    return valor
