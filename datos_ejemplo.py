"""Datos de ejemplo para probar el sistema y para la defensa.

Igual que cargar_datos_ejemplo() del ejemplo de biblioteca de los apuntes:
solo carga si la base está vacía.
"""

from datetime import time

from constantes import (DiaSemana, EstadoEjemplar, EstadoFisico, EstadoSede, EstadoSocio,
                        RolEmpleado, TipoMaterial)
from database import obtener_session
from modelos.sede import Sede, HorarioSede
from modelos.empleado import Empleado
from modelos.socio import Socio
from modelos.catalogo import Autor, Categoria, Libro
from modelos.ejemplar import Ejemplar


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
    with obtener_session() as session:
        if session.query(Sede).count() > 0:
            return False

        # Sedes
        central = crear_sede("Biblioteca Central", "Avenida Colón 1200", "3514210000", "central@biblio.org")
        norte = crear_sede("Sede Norte", "Avenida Rafael Núñez 4500", "3514810000", "norte@biblio.org")
        sur = crear_sede("Sede Sur", "Avenida Vélez Sarsfield 3000", "3514640000", None)

        # Empleados
        empleados = [
            Empleado(legajo="E001", nombre="Laura Gómez", rol=RolEmpleado.ADMINISTRADOR, sede=central),
            Empleado(legajo="E002", nombre="Martín Díaz", rol=RolEmpleado.BIBLIOTECARIO, sede=norte),
            Empleado(legajo="E003", nombre="Sofía Herrera", rol=RolEmpleado.BIBLIOTECARIO, sede=sur),
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
        ]
        for codigo, libro, sede in reparto:
            ejemplares.append(Ejemplar(codigo_inventario=codigo, libro=libro, sede=sede,
                                       estado=EstadoEjemplar.DISPONIBLE, estado_fisico=EstadoFisico.BUENO))

        session.add_all([central, norte, sur] + empleados + socios + ejemplares)
        return True
