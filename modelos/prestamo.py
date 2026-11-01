"""Modelos de Préstamo, Devolución y Multa."""

from datetime import date

from sqlalchemy import Column, Integer, String, Float, Date, ForeignKey
from sqlalchemy.orm import relationship

from config import LARGO_ESTADO, LARGO_OBSERVACIONES
from constantes import EstadoEjemplar, EstadoMulta, EstadoPrestamo, TipoPrestamo
from database import Base
from excepciones import ReglaNegocioError


class Prestamo(Base):
    """Préstamo de un ejemplar a un socio, local o interbibliotecario."""
    __tablename__ = 'prestamos'

    id = Column(Integer, primary_key=True)
    tipo = Column(String(LARGO_ESTADO), nullable=False)
    estado = Column(String(LARGO_ESTADO), nullable=False, default=EstadoPrestamo.SOLICITADO)
    fecha_solicitud = Column(Date, default=date.today, nullable=False)
    # Se fijan al activar el préstamo, para que el tránsito no consuma el plazo
    fecha_prestamo = Column(Date)
    fecha_vencimiento = Column(Date)
    socio_id = Column(Integer, ForeignKey('socios.id'), nullable=False)
    ejemplar_id = Column(Integer, ForeignKey('ejemplares.id'), nullable=False)
    sede_origen_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)
    sede_destino_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)

    socio = relationship('Socio', back_populates='prestamos')
    ejemplar = relationship('Ejemplar', back_populates='prestamos')
    # Hay dos claves foráneas hacia Sede: SQLAlchemy exige indicar cuál usa cada relación
    sede_origen = relationship('Sede', foreign_keys=[sede_origen_id])
    sede_destino = relationship('Sede', foreign_keys=[sede_destino_id])
    # 0..1: uselist=False devuelve un objeto (o None) en lugar de una lista
    devolucion = relationship('Devolucion', back_populates='prestamo', uselist=False,
                              cascade="all, delete-orphan")
    multa = relationship('Multa', back_populates='prestamo', uselist=False)

    def __repr__(self):
        return f"<Prestamo(id={self.id}, tipo='{self.tipo}')>"

    def __str__(self):
        return f"Préstamo #{self.id} - {self.ejemplar.libro.titulo} - {self.estado_efectivo}"

    def validar_prestamo(self):
        """Verifica las reglas de negocio usando solo las relaciones del objeto.
        Lanza ReglaNegocioError con el primer problema encontrado."""
        if not self.socio.esta_habilitado():
            raise ReglaNegocioError(f"El socio {self.socio.nro_socio} no está habilitado")
        if not self.ejemplar.esta_disponible():
            raise ReglaNegocioError(f"El ejemplar {self.ejemplar.codigo_inventario} no está disponible")
        if self.ejemplar.sede is not self.sede_origen:
            raise ReglaNegocioError("El ejemplar no pertenece a la sede de origen del préstamo")
        if not self.sede_origen.esta_activa():
            raise ReglaNegocioError(f"La sede de origen {self.sede_origen.nombre} está dada de baja")
        if not self.sede_destino.esta_activa():
            raise ReglaNegocioError(f"La sede de destino {self.sede_destino.nombre} está dada de baja")
        if self.tipo == TipoPrestamo.LOCAL and self.sede_origen is not self.sede_destino:
            raise ReglaNegocioError("Un préstamo local debe tener la misma sede de origen y destino")
        if self.tipo == TipoPrestamo.INTERBIBLIOTECARIO and self.sede_origen is self.sede_destino:
            raise ReglaNegocioError("Un préstamo interbibliotecario debe tener sedes de origen y destino distintas")

    @property
    def esta_vencido(self):
        """VENCIDO no se guarda: se calcula sobre un préstamo ACTIVO."""
        if self.estado != EstadoPrestamo.ACTIVO:
            return False
        return date.today() > self.fecha_vencimiento

    @property
    def estado_efectivo(self):
        """Estado para mostrar: VENCIDO si corresponde, si no el guardado."""
        if self.esta_vencido:
            return EstadoPrestamo.VENCIDO
        return self.estado

    def activar(self, estrategia):
        """Pasa el préstamo a ACTIVO. La estrategia la elige el DAO y llega
        por parámetro (selección externa del patrón Strategy)."""
        self.fecha_prestamo = date.today()
        self.fecha_vencimiento = estrategia.calcular_vencimiento(self.fecha_prestamo)
        self.estado = EstadoPrestamo.ACTIVO
        self.ejemplar.cambiar_estado(EstadoEjemplar.PRESTADO)


class Devolucion(Base):
    """Cierre de un préstamo, con el estado físico del material."""
    __tablename__ = 'devoluciones'

    id = Column(Integer, primary_key=True)
    prestamo_id = Column(Integer, ForeignKey('prestamos.id'), unique=True, nullable=False)
    fecha_devolucion = Column(Date, default=date.today, nullable=False)
    estado_fisico = Column(String(LARGO_ESTADO), nullable=False)
    observaciones = Column(String(LARGO_OBSERVACIONES))

    prestamo = relationship('Prestamo', back_populates='devolucion')

    def __repr__(self):
        return f"<Devolucion(prestamo_id={self.prestamo_id})>"

    def __str__(self):
        return f"Devolución del {self.fecha_devolucion:%d/%m/%Y} - {self.estado_fisico}"


class Multa(Base):
    """Multa por atraso en la devolución. Solo se registra su estado (no se cobra)."""
    __tablename__ = 'multas'

    id = Column(Integer, primary_key=True)
    prestamo_id = Column(Integer, ForeignKey('prestamos.id'), unique=True, nullable=False)
    dias_atraso = Column(Integer, nullable=False)
    monto = Column(Float, nullable=False, default=0.0)
    estado = Column(String(LARGO_ESTADO), nullable=False, default=EstadoMulta.PENDIENTE)

    prestamo = relationship('Prestamo', back_populates='multa')

    def __repr__(self):
        return f"<Multa(prestamo_id={self.prestamo_id}, monto={self.monto})>"

    def __str__(self):
        return f"${self.monto:.2f} ({self.dias_atraso} días) - {self.estado}"

    def calcular_monto(self, estrategia):
        """La estrategia llega por parámetro: la Multa no la elige."""
        self.monto = round(estrategia.calcular_multa(self.dias_atraso), 2)
        return self.monto
