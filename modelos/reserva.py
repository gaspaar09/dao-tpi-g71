"""Modelo de Reserva."""

from datetime import date, timedelta

from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship

from config import DIAS_RETIRO_RESERVA, LARGO_ESTADO
from constantes import EstadoEjemplar, EstadoReserva
from database import Base
from excepciones import ReglaNegocioError


class Reserva(Base):
    """Reserva de un título para retirar en una sede. Cuando se libera un
    ejemplar de esa sede se le asigna. La fecha de vencimiento inicial
    (hoy + DIAS_ESPERA_RESERVA) la fija el DAO al darla de alta."""
    __tablename__ = 'reservas'

    id = Column(Integer, primary_key=True)
    fecha_reserva = Column(Date, default=date.today, nullable=False)
    fecha_vencimiento = Column(Date, nullable=False)
    estado = Column(String(LARGO_ESTADO), nullable=False, default=EstadoReserva.PENDIENTE)
    socio_id = Column(Integer, ForeignKey('socios.id'), nullable=False)
    libro_id = Column(Integer, ForeignKey('libros.id'), nullable=False)
    sede_retiro_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)
    ejemplar_id = Column(Integer, ForeignKey('ejemplares.id'))  # 0..1: se asigna después

    socio = relationship('Socio', back_populates='reservas')
    libro = relationship('Libro', back_populates='reservas')
    sede_retiro = relationship('Sede')
    ejemplar = relationship('Ejemplar')

    def __repr__(self):
        return f"<Reserva(id={self.id}, estado='{self.estado}')>"

    def __str__(self):
        return f"Reserva #{self.id} - {self.libro.titulo} - {self.estado}"

    def asignar_ejemplar(self, ejemplar):
        """Asigna un ejemplar disponible. Desde ahora el socio tiene
        DIAS_RETIRO_RESERVA días para retirarlo."""
        if self.estado != EstadoReserva.PENDIENTE:
            raise ReglaNegocioError(f"Solo se asigna ejemplar a una reserva PENDIENTE (está {self.estado})")
        if not ejemplar.esta_disponible():
            raise ReglaNegocioError(f"El ejemplar {ejemplar.codigo_inventario} no está disponible")
        ejemplar.cambiar_estado(EstadoEjemplar.RESERVADO)
        self.ejemplar = ejemplar
        self.estado = EstadoReserva.DISPONIBLE
        self.fecha_vencimiento = date.today() + timedelta(days=DIAS_RETIRO_RESERVA)

    def esta_en_curso(self):
        return self.estado in [EstadoReserva.PENDIENTE, EstadoReserva.DISPONIBLE]

    def liberar_ejemplar(self):
        """El ejemplar apartado vuelve a estar disponible (sigue registrado
        en la reserva para el historial)."""
        if self.estado == EstadoReserva.DISPONIBLE:
            self.ejemplar.cambiar_estado(EstadoEjemplar.DISPONIBLE)

    def cancelar(self):
        if not self.esta_en_curso():
            raise ReglaNegocioError(f"No se puede cancelar una reserva {self.estado}")
        self.liberar_ejemplar()
        self.estado = EstadoReserva.CANCELADA

    def vencer(self):
        """Pasó el plazo de espera o de retiro: el ejemplar se libera."""
        if not self.esta_en_curso():
            raise ReglaNegocioError(f"No puede vencer una reserva {self.estado}")
        self.liberar_ejemplar()
        self.estado = EstadoReserva.VENCIDA

    def cumplir(self):
        """El socio retira el ejemplar. Queda DISPONIBLE solo un instante: el
        DAO arma el préstamo local en la misma sesión."""
        if self.estado != EstadoReserva.DISPONIBLE:
            raise ReglaNegocioError(f"Solo se retira una reserva DISPONIBLE (está {self.estado})")
        self.liberar_ejemplar()
        self.estado = EstadoReserva.CUMPLIDA
