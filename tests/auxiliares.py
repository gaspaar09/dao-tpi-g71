"""Funciones auxiliares para los tests.

Los modelos de SQLAlchemy se pueden crear y relacionar en memoria sin
sesión, así que los métodos de dominio se prueban sin tocar la base.
Los DAO, en cambio, usan una base SQLite en memoria (preparar_base_en_memoria).
"""

from datetime import timedelta

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

import database
from constantes import EstadoEjemplar, EstadoPrestamo, EstadoSede, TipoPrestamo
# Se importan todos los modelos (aunque no se usen acá) para que SQLAlchemy
# pueda resolver las relaciones declaradas con el nombre de la clase en texto
from modelos.sede import Sede
from modelos.empleado import Empleado
from modelos.socio import Socio
from modelos.catalogo import Libro, Autor, Categoria
from modelos.ejemplar import Ejemplar
from modelos.prestamo import Prestamo, Devolucion, Multa
from modelos.reserva import Reserva
from modelos.remito import Remito, ItemRemito, MovimientoRemito, IncidenciaEnvio


def preparar_base_en_memoria():
    """Apunta la aplicación a una base nueva y vacía en memoria.

    obtener_session() usa database.Session cada vez que se llama, así que
    al reemplazarla todos los DAO pasan a usar esta base. Cada test la llama
    al empezar, para no depender de lo que dejó otro test.
    """
    database.engine = create_engine('sqlite:///:memory:')
    database.Session = sessionmaker(bind=database.engine, expire_on_commit=False)
    database.crear_tablas()


def crear_sede(nombre="Central"):
    return Sede(nombre=nombre, direccion="Av. Siempre Viva 123", telefono="3514000000",
                estado=EstadoSede.ACTIVA)


def crear_socio(estado="ACTIVO"):
    return Socio(nro_socio=1, dni="12345678", nombre="Ana", apellido="Martínez",
                 telefono="3515550001", estado=estado)


def crear_ejemplar(sede, estado=EstadoEjemplar.DISPONIBLE):
    libro = Libro(isbn="9789500700011", titulo="Rayuela", editorial="Sudamericana",
                  anio_edicion=1963, idioma="Español", tipo_material="LIBRO",
                  categoria=Categoria(nombre="Novela"))
    return Ejemplar(codigo_inventario="EJ-001", estado=estado, libro=libro, sede=sede)


def crear_prestamo(tipo=TipoPrestamo.LOCAL):
    """Préstamo válido: local con una sola sede o interbibliotecario con dos."""
    origen = crear_sede("Central")
    destino = origen if tipo == TipoPrestamo.LOCAL else crear_sede("Norte")
    return Prestamo(tipo=tipo, estado=EstadoPrestamo.SOLICITADO, socio=crear_socio(),
                    ejemplar=crear_ejemplar(origen), sede_origen=origen, sede_destino=destino)


class EstrategiaDePrueba:
    """Reemplaza a la Strategy real (Fase 4): plazo fijo y multa fija por día."""

    def __init__(self, dias, multa_por_dia):
        self.dias = dias
        self.multa_por_dia = multa_por_dia

    def calcular_vencimiento(self, fecha_prestamo):
        return fecha_prestamo + timedelta(days=self.dias)

    def calcular_multa(self, dias_atraso):
        return dias_atraso * self.multa_por_dia
