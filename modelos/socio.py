"""Modelo de Socio."""

from datetime import date

from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship

from config import LARGO_NOMBRE_PERSONA, LARGO_EMAIL, LARGO_TELEFONO, LARGO_PREFIJO, LARGO_ESTADO
from constantes import EstadoSocio, PaisTelefono
from database import Base
from excepciones import ReglaNegocioError


class Socio(Base):
    """Socio de la red de bibliotecas."""
    __tablename__ = 'socios'

    id = Column(Integer, primary_key=True)
    nro_socio = Column(Integer, unique=True, nullable=False)
    dni = Column(String(8), unique=True, nullable=False)
    nombre = Column(String(LARGO_NOMBRE_PERSONA), nullable=False)
    apellido = Column(String(LARGO_NOMBRE_PERSONA), nullable=False)
    email = Column(String(LARGO_EMAIL))
    prefijo_pais = Column(String(LARGO_PREFIJO), nullable=False, default=PaisTelefono.ARGENTINA)
    telefono = Column(String(LARGO_TELEFONO), nullable=False)
    fecha_alta = Column(Date, default=date.today, nullable=False)
    estado = Column(String(LARGO_ESTADO), nullable=False, default=EstadoSocio.ACTIVO)

    prestamos = relationship('Prestamo', back_populates='socio')
    reservas = relationship('Reserva', back_populates='socio')

    def __repr__(self):
        return f"<Socio(nro_socio={self.nro_socio})>"

    def __str__(self):
        return f"{self.nombre} {self.apellido} (N° {self.nro_socio})"

    def esta_habilitado(self):
        """Solo un socio ACTIVO puede pedir préstamos y reservas."""
        return self.estado == EstadoSocio.ACTIVO

    def inhabilitar(self):
        if not self.esta_habilitado():
            raise ReglaNegocioError(f"El socio {self.nro_socio} no está activo, no se puede inhabilitar")
        self.estado = EstadoSocio.INHABILITADO
