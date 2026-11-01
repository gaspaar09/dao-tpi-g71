"""Modelos del Remito y su detalle: ítems, movimientos e incidencias.

El Remito es el contexto del patrón State (patrones/estado_remito.py).
"""

from datetime import date, datetime

from sqlalchemy import Column, Integer, String, Date, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from config import LARGO_ESTADO, LARGO_OBSERVACION_MOVIMIENTO, LARGO_DESCRIPCION_INCIDENCIA
from constantes import EstadoRemito
from database import Base
from patrones.estado_remito import ESTADOS_REMITO


class Remito(Base):
    """Envío de uno o más ejemplares entre un par de sedes."""
    __tablename__ = 'remitos'

    id = Column(Integer, primary_key=True)
    nro_remito = Column(String(20), unique=True, nullable=False)
    tipo = Column(String(LARGO_ESTADO), nullable=False)
    estado = Column(String(LARGO_ESTADO), nullable=False, default=EstadoRemito.EMPAQUETADO)
    fecha_creacion = Column(Date, default=date.today, nullable=False)
    fecha_despacho = Column(Date)
    fecha_recepcion = Column(Date)
    sede_origen_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)
    sede_destino_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)

    # Hay dos claves foráneas hacia Sede: SQLAlchemy exige indicar cuál usa cada relación
    sede_origen = relationship('Sede', foreign_keys=[sede_origen_id])
    sede_destino = relationship('Sede', foreign_keys=[sede_destino_id])
    # Composición: el detalle no existe sin su remito
    items = relationship('ItemRemito', back_populates='remito', cascade="all, delete-orphan")
    movimientos = relationship('MovimientoRemito', back_populates='remito', cascade="all, delete-orphan")
    incidencias = relationship('IncidenciaEnvio', back_populates='remito', cascade="all, delete-orphan")

    def __repr__(self):
        return f"<Remito(nro_remito='{self.nro_remito}')>"

    def __str__(self):
        return f"{self.nro_remito} ({self.tipo}) - {self.estado}"

    # ------------------------------------------------ patrón State (contexto)

    @property
    def estado_actual(self):
        """En la base se guarda solo el texto: acá se obtiene la instancia del estado."""
        return ESTADOS_REMITO[self.estado]

    def cambiar_estado(self, nuevo, empleado, observacion):
        """Como en el semáforo: sale del estado anterior y entra al nuevo.
        Cada cambio deja un MovimientoRemito (trazabilidad del envío)."""
        anterior = self.estado
        # Un remito recién creado todavía no tiene estado del que salir
        if anterior is not None:
            self.estado_actual.salir(self)
        self.estado = nuevo
        self.movimientos.append(MovimientoRemito(estado_anterior=anterior, estado_nuevo=nuevo,
                                                 empleado=empleado, observacion=observacion))
        self.estado_actual.entrar(self, empleado, observacion)

    # El remito no decide nada: delega en su estado actual
    def avanzar_estado(self, empleado, observacion):
        self.estado_actual.avanzar(self, empleado, observacion)

    def cancelar(self, empleado, observacion):
        self.estado_actual.cancelar(self, empleado, observacion)

    def extraviar(self, empleado, observacion):
        self.estado_actual.extraviar(self, empleado, observacion)

    def quitar_item(self, item, empleado, observacion):
        self.estado_actual.quitar_item(self, item, empleado, observacion)


class ItemRemito(Base):
    """Ejemplar que viaja en un remito, junto con el préstamo que lo originó
    (Association Object, como en los apuntes)."""
    __tablename__ = 'items_remito'

    id = Column(Integer, primary_key=True)
    remito_id = Column(Integer, ForeignKey('remitos.id'), nullable=False)
    ejemplar_id = Column(Integer, ForeignKey('ejemplares.id'), nullable=False)
    prestamo_id = Column(Integer, ForeignKey('prestamos.id'), nullable=False)
    estado_recepcion = Column(String(LARGO_ESTADO))  # se completa al recibir

    remito = relationship('Remito', back_populates='items')
    ejemplar = relationship('Ejemplar')
    prestamo = relationship('Prestamo')

    def __repr__(self):
        return f"<ItemRemito(remito_id={self.remito_id}, ejemplar_id={self.ejemplar_id})>"

    def __str__(self):
        return f"{self.ejemplar.codigo_inventario} (préstamo #{self.prestamo_id})"


class MovimientoRemito(Base):
    """Un cambio de estado del remito: deja la trazabilidad del envío."""
    __tablename__ = 'movimientos_remito'

    id = Column(Integer, primary_key=True)
    remito_id = Column(Integer, ForeignKey('remitos.id'), nullable=False)
    empleado_id = Column(Integer, ForeignKey('empleados.id'), nullable=False)
    fecha_hora = Column(DateTime, default=datetime.now, nullable=False)
    estado_anterior = Column(String(LARGO_ESTADO))  # vacío en el primer movimiento
    estado_nuevo = Column(String(LARGO_ESTADO), nullable=False)
    observacion = Column(String(LARGO_OBSERVACION_MOVIMIENTO))

    remito = relationship('Remito', back_populates='movimientos')
    empleado = relationship('Empleado')

    def __repr__(self):
        return f"<MovimientoRemito(remito_id={self.remito_id}, estado_nuevo='{self.estado_nuevo}')>"

    def __str__(self):
        return f"{self.fecha_hora:%d/%m/%Y %H:%M} {self.estado_anterior} -> {self.estado_nuevo}"


class IncidenciaEnvio(Base):
    """Problema registrado durante un envío (extravío, daño, demora)."""
    __tablename__ = 'incidencias_envio'

    id = Column(Integer, primary_key=True)
    remito_id = Column(Integer, ForeignKey('remitos.id'), nullable=False)
    tipo = Column(String(LARGO_ESTADO), nullable=False)
    fecha = Column(Date, default=date.today, nullable=False)
    descripcion = Column(String(LARGO_DESCRIPCION_INCIDENCIA), nullable=False)

    remito = relationship('Remito', back_populates='incidencias')

    def __repr__(self):
        return f"<IncidenciaEnvio(remito_id={self.remito_id}, tipo='{self.tipo}')>"

    def __str__(self):
        return f"{self.tipo} el {self.fecha:%d/%m/%Y}: {self.descripcion}"
