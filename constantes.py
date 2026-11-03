"""Enumeraciones del diagrama de clases.

En clase no se vio enum.Enum, así que cada enumeración es una clase con
constantes de texto. En la base se guardan como String, igual que
estado = Column(String(20)) en los apuntes. TODOS sirve para validar que
un valor sea válido y para llenar los Combobox.
"""


class EstadoSede:
    ACTIVA = "ACTIVA"
    BAJA = "BAJA"
    TODOS = [ACTIVA, BAJA]


class EstadoSocio:
    ACTIVO = "ACTIVO"
    INHABILITADO = "INHABILITADO"
    BAJA = "BAJA"
    TODOS = [ACTIVO, INHABILITADO, BAJA]


class TipoMaterial:
    LIBRO = "LIBRO"
    REVISTA = "REVISTA"
    MATERIAL_CONSULTA = "MATERIAL_CONSULTA"
    TODOS = [LIBRO, REVISTA, MATERIAL_CONSULTA]


class Idioma:
    # Lista cerrada: el idioma se elige de un desplegable, así no se carga uno inexistente.
    ESPANOL = "Español"
    INGLES = "Inglés"
    PORTUGUES = "Portugués"
    FRANCES = "Francés"
    ITALIANO = "Italiano"
    ALEMAN = "Alemán"
    OTRO = "Otro"
    TODOS = [ESPANOL, INGLES, PORTUGUES, FRANCES, ITALIANO, ALEMAN, OTRO]


class EstadoEjemplar:
    DISPONIBLE = "DISPONIBLE"
    RESERVADO = "RESERVADO"
    PRESTADO = "PRESTADO"
    EN_TRANSITO = "EN_TRANSITO"
    DANADO = "DAÑADO"
    EXTRAVIADO = "EXTRAVIADO"
    BAJA = "BAJA"
    TODOS = [DISPONIBLE, RESERVADO, PRESTADO, EN_TRANSITO, DANADO, EXTRAVIADO, BAJA]


class EstadoFisico:
    NUEVO = "NUEVO"
    BUENO = "BUENO"
    REGULAR = "REGULAR"
    DANADO = "DAÑADO"
    DESTRUIDO = "DESTRUIDO"
    TODOS = [NUEVO, BUENO, REGULAR, DANADO, DESTRUIDO]


class TipoPrestamo:
    LOCAL = "LOCAL"
    INTERBIBLIOTECARIO = "INTERBIBLIOTECARIO"
    TODOS = [LOCAL, INTERBIBLIOTECARIO]


class EstadoPrestamo:
    SOLICITADO = "SOLICITADO"
    APROBADO = "APROBADO"
    EN_ENVIO = "EN_ENVIO"
    ACTIVO = "ACTIVO"
    # VENCIDO no se guarda en la base: se calcula sobre un préstamo ACTIVO
    # cuya fecha de vencimiento ya pasó.
    VENCIDO = "VENCIDO"
    DEVUELTO = "DEVUELTO"
    CANCELADO = "CANCELADO"
    TODOS = [SOLICITADO, APROBADO, EN_ENVIO, ACTIVO, VENCIDO, DEVUELTO, CANCELADO]


class EstadoReserva:
    PENDIENTE = "PENDIENTE"
    DISPONIBLE = "DISPONIBLE"
    CUMPLIDA = "CUMPLIDA"
    CANCELADA = "CANCELADA"
    VENCIDA = "VENCIDA"
    TODOS = [PENDIENTE, DISPONIBLE, CUMPLIDA, CANCELADA, VENCIDA]


class EstadoMulta:
    PENDIENTE = "PENDIENTE"
    PAGADA = "PAGADA"
    TODOS = [PENDIENTE, PAGADA]


class TipoEnvio:
    IDA = "IDA"
    DEVOLUCION = "DEVOLUCION"
    TODOS = [IDA, DEVOLUCION]


class EstadoRemito:
    EMPAQUETADO = "EMPAQUETADO"
    DESPACHADO = "DESPACHADO"
    EN_TRANSITO = "EN_TRANSITO"
    RECIBIDO = "RECIBIDO"
    CANCELADO = "CANCELADO"
    EXTRAVIADO = "EXTRAVIADO"
    TODOS = [EMPAQUETADO, DESPACHADO, EN_TRANSITO, RECIBIDO, CANCELADO, EXTRAVIADO]


class TipoIncidencia:
    EXTRAVIO = "EXTRAVIO"
    DANIO = "DAÑO"
    DEMORA = "DEMORA"
    TODOS = [EXTRAVIO, DANIO, DEMORA]


class PaisTelefono:
    # Países de Sudamérica y su código telefónico internacional (sin "+").
    # El usuario elige el país y el código sale de acá: no se escribe a mano.
    ARGENTINA = "54"
    PAISES = [("Argentina", "54"), ("Bolivia", "591"), ("Brasil", "55"), ("Chile", "56"),
              ("Colombia", "57"), ("Ecuador", "593"), ("Guyana", "592"), ("Paraguay", "595"),
              ("Perú", "51"), ("Surinam", "597"), ("Uruguay", "598"), ("Venezuela", "58")]
    TODOS = [codigo for pais, codigo in PAISES]


class DiaSemana:
    # Días de HorarioSede, sin tildes
    LUNES = "LUNES"
    MARTES = "MARTES"
    MIERCOLES = "MIERCOLES"
    JUEVES = "JUEVES"
    VIERNES = "VIERNES"
    SABADO = "SABADO"
    DOMINGO = "DOMINGO"
    TODOS = [LUNES, MARTES, MIERCOLES, JUEVES, VIERNES, SABADO, DOMINGO]


class RolEmpleado:
    BIBLIOTECARIO = "BIBLIOTECARIO"
    ADMINISTRADOR = "ADMINISTRADOR"
    TODOS = [BIBLIOTECARIO, ADMINISTRADOR]
    # Letra con la que empieza el legajo según el rol (B1, B2... / A1, A2...)
    PREFIJO_LEGAJO = {BIBLIOTECARIO: "B", ADMINISTRADOR: "A"}
