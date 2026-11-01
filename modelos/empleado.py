"""Modelo de Empleado."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config import LARGO_LEGAJO, LARGO_NOMBRE_EMPLEADO, LARGO_ESTADO
from database import Base


class Empleado(Base):
    """Personal de la red. Pertenece a una sede y registra las operaciones."""
    __tablename__ = 'empleados'

    id = Column(Integer, primary_key=True)
    legajo = Column(String(LARGO_LEGAJO), unique=True, nullable=False)
    nombre = Column(String(LARGO_NOMBRE_EMPLEADO), nullable=False)
    rol = Column(String(LARGO_ESTADO), nullable=False)
    sede_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)

    sede = relationship('Sede', back_populates='empleados')

    def __repr__(self):
        return f"<Empleado(legajo='{self.legajo}')>"

    def __str__(self):
        return f"{self.nombre} (Legajo {self.legajo})"
