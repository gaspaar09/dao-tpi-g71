"""Modelos del catálogo: Libro (título), Autor y Categoría."""

from sqlalchemy import Column, Integer, String, ForeignKey, Table
from sqlalchemy.orm import relationship

from config import (LARGO_ISBN, LARGO_TITULO, LARGO_EDITORIAL, LARGO_IDIOMA,
                    LARGO_NOMBRE_PERSONA, LARGO_ESTADO)
from database import Base

# Tabla de asociación muchos a muchos: libros y autores (sin atributos propios)
libro_autor = Table(
    'libro_autor', Base.metadata,
    Column('libro_id', Integer, ForeignKey('libros.id')),
    Column('autor_id', Integer, ForeignKey('autores.id'))
)


class Autor(Base):
    """Autor de libros."""
    __tablename__ = 'autores'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(LARGO_NOMBRE_PERSONA), nullable=False)
    apellido = Column(String(LARGO_NOMBRE_PERSONA), nullable=False)

    libros = relationship('Libro', secondary=libro_autor, back_populates='autores')

    def __repr__(self):
        return f"<Autor(nombre='{self.nombre} {self.apellido}')>"

    def __str__(self):
        return f"{self.nombre} {self.apellido}"


class Categoria(Base):
    """Categoría temática del catálogo."""
    __tablename__ = 'categorias'

    id = Column(Integer, primary_key=True)
    nombre = Column(String(LARGO_NOMBRE_PERSONA), unique=True, nullable=False)

    libros = relationship('Libro', back_populates='categoria')

    def __repr__(self):
        return f"<Categoria(nombre='{self.nombre}')>"

    def __str__(self):
        return self.nombre


class Libro(Base):
    """Título del catálogo. La copia física es el Ejemplar."""
    __tablename__ = 'libros'

    id = Column(Integer, primary_key=True)
    isbn = Column(String(LARGO_ISBN), unique=True, nullable=False)  # ISBN o ISSN
    titulo = Column(String(LARGO_TITULO), nullable=False)
    editorial = Column(String(LARGO_EDITORIAL), nullable=False)
    anio_edicion = Column(Integer, nullable=False)
    idioma = Column(String(LARGO_IDIOMA), nullable=False)
    tipo_material = Column(String(LARGO_ESTADO), nullable=False)
    categoria_id = Column(Integer, ForeignKey('categorias.id'), nullable=False)

    autores = relationship('Autor', secondary=libro_autor, back_populates='libros')
    categoria = relationship('Categoria', back_populates='libros')
    ejemplares = relationship('Ejemplar', back_populates='libro')
    reservas = relationship('Reserva', back_populates='libro')

    def __repr__(self):
        return f"<Libro(titulo='{self.titulo}')>"

    def __str__(self):
        autores_str = ', '.join([str(autor) for autor in self.autores])
        return f"{self.titulo} - {autores_str} ({self.anio_edicion})"
