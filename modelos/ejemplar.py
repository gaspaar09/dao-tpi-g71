"""Modelo de Ejemplar (copia física de un libro)."""

from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from config import LARGO_CODIGO_INVENTARIO, LARGO_ESTADO
from constantes import EstadoEjemplar, EstadoFisico
from database import Base
from excepciones import ValidacionError


class Ejemplar(Base):
    """Copia física de un libro. Pertenece a una única sede y la
    disponibilidad se controla sobre el ejemplar, no sobre el libro."""
    __tablename__ = 'ejemplares'

    id = Column(Integer, primary_key=True)
    codigo_inventario = Column(String(LARGO_CODIGO_INVENTARIO), unique=True, nullable=False)
    estado = Column(String(LARGO_ESTADO), nullable=False, default=EstadoEjemplar.DISPONIBLE)
    estado_fisico = Column(String(LARGO_ESTADO), nullable=False, default=EstadoFisico.NUEVO)
    libro_id = Column(Integer, ForeignKey('libros.id'), nullable=False)
    sede_id = Column(Integer, ForeignKey('sedes.id'), nullable=False)

    libro = relationship('Libro', back_populates='ejemplares')
    sede = relationship('Sede', back_populates='ejemplares')
    prestamos = relationship('Prestamo', back_populates='ejemplar')

    def __repr__(self):
        return f"<Ejemplar(codigo_inventario='{self.codigo_inventario}')>"

    def __str__(self):
        return f"{self.codigo_inventario} - {self.estado}"

    def esta_disponible(self):
        return self.estado == EstadoEjemplar.DISPONIBLE

    def cambiar_estado(self, nuevo):
        if nuevo not in EstadoEjemplar.TODOS:
            raise ValidacionError(f"Estado de ejemplar inválido: {nuevo}")
        self.estado = nuevo

    def volver_a_circular(self):
        """Al volver a su sede (devolución), el estado depende de cómo llegó:
        dañado queda fuera de circulación y destruido se da de baja."""
        if self.estado_fisico == EstadoFisico.DANADO:
            self.cambiar_estado(EstadoEjemplar.DANADO)
        elif self.estado_fisico == EstadoFisico.DESTRUIDO:
            self.cambiar_estado(EstadoEjemplar.BAJA)
        else:
            self.cambiar_estado(EstadoEjemplar.DISPONIBLE)
