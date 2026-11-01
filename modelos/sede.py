"""Modelos de Sede y sus horarios."""

from sqlalchemy import Column, Integer, String, Time, ForeignKey
from sqlalchemy.orm import relationship

from config import LARGO_NOMBRE_SEDE, LARGO_DIRECCION, LARGO_TELEFONO, LARGO_PREFIJO, LARGO_EMAIL, LARGO_ESTADO
from constantes import EstadoSede, PaisTelefono
from database import Base
from excepciones import ReglaNegocioError


class Sede(Base):
    """Representa una sede (biblioteca) de la red."""
    __tablename__ = 'sedes'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(LARGO_NOMBRE_SEDE), unique=True, nullable=False)
    direccion = Column(String(LARGO_DIRECCION), nullable=False)
    prefijo_pais = Column(String(LARGO_PREFIJO), nullable=False, default=PaisTelefono.ARGENTINA)
    telefono = Column(String(LARGO_TELEFONO), nullable=False)
    email = Column(String(LARGO_EMAIL))
    estado = Column(String(LARGO_ESTADO), nullable=False, default=EstadoSede.ACTIVA)

    # Composición: los horarios no existen sin su sede
    horarios = relationship('HorarioSede', back_populates='sede', cascade="all, delete-orphan")
    empleados = relationship('Empleado', back_populates='sede')
    ejemplares = relationship('Ejemplar', back_populates='sede')

    def __repr__(self):
        return f"<Sede(nombre='{self.nombre}')>"

    def __str__(self):
        return self.nombre

    def esta_activa(self):
        """Indica si la sede puede operar (no está dada de baja)."""
        return self.estado == EstadoSede.ACTIVA

    def dar_de_baja(self):
        """Baja lógica. Los controles que requieren consultar otras filas
        (préstamos activos, remitos en curso) los hace el DAO."""
        if not self.esta_activa():
            raise ReglaNegocioError(f"La sede {self.nombre} ya está dada de baja")
        self.estado = EstadoSede.BAJA

    def reactivar(self):
        """Vuelve a dar de alta una sede dada de baja (la baja es lógica, así
        que la sede conserva sus horarios, empleados y ejemplares)."""
        if self.esta_activa():
            raise ReglaNegocioError(f"La sede {self.nombre} ya está activa")
        self.estado = EstadoSede.ACTIVA


class HorarioSede(Base):
    """Horario de atención de una sede para un día de la semana."""
    __tablename__ = 'horarios_sede'

    id = Column(Integer, primary_key=True)
    sede_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)
    dia_semana = Column(String(9), nullable=False)  # constante de DiaSemana; "MIERCOLES" es la más larga
    hora_apertura = Column(Time, nullable=False)
    hora_cierre = Column(Time, nullable=False)

    sede = relationship('Sede', back_populates='horarios')

    def __repr__(self):
        return f"<HorarioSede(dia_semana='{self.dia_semana}')>"

    def __str__(self):
        return f"{self.dia_semana} {self.hora_apertura:%H:%M} a {self.hora_cierre:%H:%M}"
