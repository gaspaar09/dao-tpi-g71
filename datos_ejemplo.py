"""Datos de ejemplo para probar el sistema y para la defensa.

Igual que cargar_datos_ejemplo() del ejemplo de biblioteca de los apuntes:
solo carga si la base está vacía.

Primero se cargan los datos maestros (sedes, socios, catálogo, ejemplares).
Después los préstamos y remitos se arman con los DAO, igual que desde la
pantalla, así pasan por las mismas reglas y quedan en estados coherentes:
hay un préstamo, remito y reserva en cada estado para poder probar cada botón.
"""

from datetime import date, time, timedelta

from constantes import (DiaSemana, EstadoEjemplar, EstadoFisico, EstadoPrestamo, EstadoSede, EstadoSocio,
                        RolEmpleado, TipoIncidencia, TipoMaterial, TipoPrestamo)
from dao.devolucion_dao import DevolucionDAO
from dao.prestamo_dao import PrestamoDAO
from dao.remito_dao import RemitoDAO
from dao.reserva_dao import ReservaDAO
from database import obtener_session
from modelos.sede import Sede, HorarioSede
from modelos.empleado import Empleado
from modelos.socio import Socio
from modelos.catalogo import Autor, Categoria, Libro
from modelos.ejemplar import Ejemplar
from modelos.prestamo import Prestamo
from modelos.reserva import Reserva
from modelos.remito import Remito
from patrones.estrategia_prestamo import ESTRATEGIAS

LOCAL = TipoPrestamo.LOCAL
INTER = TipoPrestamo.INTERBIBLIOTECARIO


def crear_sede(nombre, direccion, telefono, email):
    # Todas las sedes son de Argentina: prefijo_pais queda en su valor por defecto (54)
    """Sede abierta de lunes a viernes de 8 a 18 y los sábados de 9 a 13."""
    sede = Sede(nombre=nombre, direccion=direccion, telefono=telefono, email=email,
                estado=EstadoSede.ACTIVA)
    for dia in [DiaSemana.LUNES, DiaSemana.MARTES, DiaSemana.MIERCOLES,
                DiaSemana.JUEVES, DiaSemana.VIERNES]:
        sede.horarios.append(HorarioSede(dia_semana=dia, hora_apertura=time(8, 0), hora_cierre=time(18, 0)))
    sede.horarios.append(HorarioSede(dia_semana=DiaSemana.SABADO, hora_apertura=time(9, 0),
                                     hora_cierre=time(13, 0)))
    return sede


def cargar_datos_ejemplo():
    """Carga datos de ejemplo. Devuelve True si los cargó o False si la base
    ya tenía datos."""
    if not cargar_datos_maestros():
        return False
    cargar_prestamos_y_remitos()
    cargar_reservas_y_devoluciones()
    return True


def cargar_datos_maestros():
    with obtener_session() as session:
        if session.query(Sede).count() > 0:
            return False

        # Sedes
        central = crear_sede("Biblioteca Central", "Avenida Colón 1200", "3514210000", "central@biblio.org")
        norte = crear_sede("Sede Norte", "Avenida Rafael Núñez 4500", "3514810000", "norte@biblio.org")
        sur = crear_sede("Sede Sur", "Avenida Vélez Sarsfield 3000", "3514640000", None)

        # Empleados
        empleados = [
            Empleado(legajo="A1", nombre="Laura Gómez", rol=RolEmpleado.ADMINISTRADOR, sede=central),
            Empleado(legajo="B1", nombre="Martín Díaz", rol=RolEmpleado.BIBLIOTECARIO, sede=norte),
            Empleado(legajo="B2", nombre="Sofía Herrera", rol=RolEmpleado.BIBLIOTECARIO, sede=sur),
        ]

        # Socios
        socios = [
            Socio(nro_socio=1, dni="30111222", nombre="Ana", apellido="Martínez",
                  email="ana@example.com", telefono="3515550001", estado=EstadoSocio.ACTIVO),
            Socio(nro_socio=2, dni="28333444", nombre="Carlos", apellido="López",
                  email="carlos@example.com", telefono="3515550002", estado=EstadoSocio.ACTIVO),
            Socio(nro_socio=3, dni="35555666", nombre="Lucía", apellido="Fernández",
                  email=None, telefono="3515550003", estado=EstadoSocio.ACTIVO),
            Socio(nro_socio=4, dni="4777888", nombre="Jorge", apellido="Ramírez",
                  email="jorge@example.com", telefono="3515550004", estado=EstadoSocio.INHABILITADO),
        ]

        # Catálogo
        novela = Categoria(nombre="Novela")
        cuento = Categoria(nombre="Cuento")
        divulgacion = Categoria(nombre="Divulgación")

        cortazar = Autor(nombre="Julio", apellido="Cortázar")
        borges = Autor(nombre="Jorge Luis", apellido="Borges")
        bioy = Autor(nombre="Adolfo", apellido="Bioy Casares")
        ocampo = Autor(nombre="Silvina", apellido="Ocampo")

        rayuela = Libro(isbn="9789500700011", titulo="Rayuela", editorial="Sudamericana",
                        anio_edicion=1963, idioma="Español", tipo_material=TipoMaterial.LIBRO,
                        categoria=novela)
        rayuela.autores.append(cortazar)
        ficciones = Libro(isbn="9789500700028", titulo="Ficciones", editorial="Emecé",
                          anio_edicion=1944, idioma="Español", tipo_material=TipoMaterial.LIBRO,
                          categoria=cuento)
        ficciones.autores.append(borges)
        antologia = Libro(isbn="9789500700035", titulo="Antología de la literatura fantástica",
                          editorial="Sudamericana", anio_edicion=1940, idioma="Español",
                          tipo_material=TipoMaterial.LIBRO, categoria=cuento)
        antologia.autores.extend([borges, bioy, ocampo])
        morel = Libro(isbn="9789500700042", titulo="La invención de Morel", editorial="Losada",
                      anio_edicion=1940, idioma="Español", tipo_material=TipoMaterial.LIBRO,
                      categoria=novela)
        morel.autores.append(bioy)
        revista = Libro(isbn="0317847X", titulo="Revista de Ciencia Hoy", editorial="Asociación Ciencia Hoy",
                        anio_edicion=2020, idioma="Español", tipo_material=TipoMaterial.REVISTA,
                        categoria=divulgacion)
        revista.autores.append(ocampo)

        # Ejemplares: cada uno pertenece a una sede
        ejemplares = []
        reparto = [
            ("RAY-001", rayuela, central), ("RAY-002", rayuela, central), ("RAY-003", rayuela, norte),
            ("FIC-001", ficciones, central), ("FIC-002", ficciones, sur),
            ("ANT-001", antologia, norte),
            ("MOR-001", morel, sur), ("MOR-002", morel, sur),
            ("REV-001", revista, central), ("REV-002", revista, norte),
            ("FIC-003", ficciones, central), ("ANT-002", antologia, central),
            ("MOR-003", morel, norte), ("RAY-004", rayuela, sur), ("REV-003", revista, sur),
        ]
        for codigo, libro, sede in reparto:
            ejemplares.append(Ejemplar(codigo_inventario=codigo, libro=libro, sede=sede,
                                       estado=EstadoEjemplar.DISPONIBLE, estado_fisico=EstadoFisico.BUENO))

        session.add_all([central, norte, sur] + empleados + socios + ejemplares)
        return True


# ------------------------------------------------- préstamos y remitos

def buscar_id(clase, **filtro):
    """Id de la fila que cumple el filtro (por ejemplo, codigo_inventario="RAY-001")."""
    with obtener_session() as session:
        return session.query(clase).filter_by(**filtro).first().id


def solicitar(tipo, nro_socio, codigo, origen, destino):
    """Registra la solicitud con PrestamoDAO y devuelve el id del préstamo."""
    PrestamoDAO().solicitar(tipo, buscar_id(Socio, nro_socio=nro_socio),
                            buscar_id(Ejemplar, codigo_inventario=codigo),
                            buscar_id(Sede, nombre=origen), buscar_id(Sede, nombre=destino))
    return PrestamoDAO().listar()[0]['id']


def aprobar(tipo, nro_socio, codigo, origen, destino):
    prestamo_id = solicitar(tipo, nro_socio, codigo, origen, destino)
    PrestamoDAO().aprobar(prestamo_id)
    return prestamo_id


def crear_remito(origen, destino, prestamos_ids, legajo):
    RemitoDAO().crear_ida(buscar_id(Sede, nombre=origen), buscar_id(Sede, nombre=destino),
                          prestamos_ids, buscar_id(Empleado, legajo=legajo))
    return RemitoDAO().listar()[0]['id']


def cargar_prestamos_y_remitos():
    """Un préstamo y un remito en cada estado."""
    prestamos = PrestamoDAO()
    remitos = RemitoDAO()
    central, norte, sur = "Biblioteca Central", "Sede Norte", "Sede Sur"
    laura = buscar_id(Empleado, legajo="A1")
    martin = buscar_id(Empleado, legajo="B1")

    # Préstamos locales: activo, vencido, solicitado (sin aprobar) y cancelado
    vencido_3_dias = aprobar(LOCAL, 1, "RAY-001", central, central)
    vencido_9_dias = aprobar(LOCAL, 2, "MOR-001", sur, sur)  # se devuelve más abajo, con multa
    solicitar(LOCAL, 3, "FIC-001", central, central)
    prestamos.cancelar(solicitar(LOCAL, 1, "REV-001", central, central))

    # Préstamos vencidos sin esperar 31 días: se corre la fecha de préstamo
    # hacia atrás y el vencimiento lo vuelve a calcular la estrategia
    with obtener_session() as session:
        for prestamo_id, dias in [(vencido_3_dias, 34), (vencido_9_dias, 40)]:
            prestamo = session.query(Prestamo).filter_by(id=prestamo_id).first()
            prestamo.fecha_prestamo = date.today() - timedelta(days=dias)
            # La solicitud también se corre, para que no quede posterior al préstamo
            prestamo.fecha_solicitud = prestamo.fecha_prestamo
            prestamo.fecha_vencimiento = ESTRATEGIAS[prestamo.tipo].calcular_vencimiento(prestamo.fecha_prestamo)

    # Interbibliotecarios aprobados que esperan remito (se pueden agrupar en uno)
    aprobar(INTER, 3, "RAY-002", central, norte)
    aprobar(INTER, 2, "FIC-003", central, norte)

    # Remito EMPAQUETADO: se puede cancelar, o cancelar su préstamo desde Préstamos
    crear_remito(norte, sur, [aprobar(INTER, 1, "ANT-001", norte, sur)], "B1")

    # Remito DESPACHADO: ya no se puede cancelar
    remito = crear_remito(norte, central, [aprobar(INTER, 2, "REV-002", norte, central)], "B1")
    remitos.avanzar(remito, martin, "Sale con el transporte de la mañana")

    # Remito EN_TRANSITO con una demora: se puede recibir o dar por extraviado
    remito = crear_remito(sur, central, [aprobar(INTER, 3, "MOR-002", sur, central)], "B2")
    remitos.avanzar(remito, martin, "")
    remitos.avanzar(remito, martin, "")
    remitos.registrar_incidencia(remito, TipoIncidencia.DEMORA, date.today().strftime("%d/%m/%Y"),
                                 "El transporte se retrasó por lluvia")

    # Remito RECIBIDO: el préstamo quedó ACTIVO con el plazo interbibliotecario
    remito = crear_remito(norte, central, [aprobar(INTER, 1, "RAY-003", norte, central)], "B1")
    for _ in range(3):
        remitos.avanzar(remito, laura, "")
    # Para que el reporte de movimiento tenga un tiempo de tránsito distinto de 0:
    # se simula que se armó hace 4 días y se despachó hace 3
    with obtener_session() as session:
        recibido = session.query(Remito).filter_by(id=remito).first()
        recibido.fecha_creacion = date.today() - timedelta(days=4)
        recibido.fecha_despacho = date.today() - timedelta(days=3)

    # Remito CANCELADO: el préstamo se canceló y el ejemplar volvió a estar disponible
    remito = crear_remito(sur, norte, [aprobar(INTER, 2, "FIC-002", sur, norte)], "B2")
    remitos.cancelar(remito, laura, "El socio ya no lo necesita")

    # Remito EXTRAVIADO: ejemplar perdido e incidencia de extravío
    remito = crear_remito(central, sur, [aprobar(INTER, 3, "ANT-002", central, sur)], "A1")
    remitos.avanzar(remito, laura, "")
    remitos.avanzar(remito, laura, "")
    remitos.extraviar(remito, laura, "El paquete no llegó a destino")


# ---------------------------------------------- reservas y devoluciones

def prestamo_activo(codigo):
    """Id del préstamo ACTIVO del ejemplar con ese código."""
    with obtener_session() as session:
        ejemplar = session.query(Ejemplar).filter_by(codigo_inventario=codigo).first()
        return session.query(Prestamo).filter_by(ejemplar_id=ejemplar.id, estado=EstadoPrestamo.ACTIVO).first().id


def reservar(nro_socio, titulo, sede):
    ReservaDAO().crear(buscar_id(Socio, nro_socio=nro_socio), buscar_id(Libro, titulo=titulo),
                       buscar_id(Sede, nombre=sede))
    return ReservaDAO().listar()[0]['id']


def cargar_reservas_y_devoluciones():
    """Una reserva en cada estado y dos devoluciones (con multa y con remito)."""
    reservas = ReservaDAO()
    hoy = date.today().strftime("%d/%m/%Y")
    laura = buscar_id(Empleado, legajo="A1")
    central, norte, sur = "Biblioteca Central", "Sede Norte", "Sede Sur"

    # PENDIENTE: el único ejemplar de Norte (ANT-001) está apartado para un envío
    reservar(1, "Antología de la literatura fantástica", norte)

    # DISPONIBLE asignada en el acto: REV-003 estaba libre en Sur
    reservar(2, "Revista de Ciencia Hoy", sur)

    # CUMPLIDA: se aparta RAY-004 y el socio lo retira (préstamo local activo)
    reservas.retirar(reservar(1, "Rayuela", sur))

    # VENCIDA: nadie retiró FIC-002 y pasaron los 2 días; el ejemplar vuelve a estar libre
    vencida = reservar(2, "Ficciones", sur)
    with obtener_session() as session:
        session.query(Reserva).filter_by(id=vencida).first().fecha_vencimiento = date.today() - timedelta(days=1)
    reservas.procesar_vencimientos()

    # CANCELADA: el socio desiste y REV-001 vuelve a estar libre en Central
    reservas.cancelar(reservar(3, "Revista de Ciencia Hoy", central))

    # Devolución local atrasada: MOR-001 venció hace 9 días -> multa de $900.
    # Lucía lo estaba esperando en Sur, así que su reserva pasa a DISPONIBLE.
    reservar(3, "La invención de Morel", sur)
    DevolucionDAO().registrar(prestamo_activo("MOR-001"), hoy, EstadoFisico.BUENO, "", laura)

    # Devolución interbibliotecaria: RAY-003 vuelve de Central a Norte con un remito
    DevolucionDAO().registrar(prestamo_activo("RAY-003"), hoy, EstadoFisico.REGULAR, "Tapa gastada", laura)
