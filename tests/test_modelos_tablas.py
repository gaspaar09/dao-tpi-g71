from sqlalchemy import create_engine

from database import Base
import tests.auxiliares  # importa todos los modelos para que Base los conozca

TABLAS_ESPERADAS = [
    'sedes', 'horarios_sede', 'empleados', 'socios', 'autores', 'categorias',
    'libros', 'libro_autor', 'ejemplares', 'prestamos', 'devoluciones', 'multas',
    'reservas', 'remitos', 'items_remito', 'movimientos_remito', 'incidencias_envio',
]


class TestCreacionDeTablas:
    def test_crea_todas_las_tablas_en_memoria(self):
        engine = create_engine('sqlite:///:memory:')
        Base.metadata.create_all(engine)
        for tabla in TABLAS_ESPERADAS:
            assert tabla in Base.metadata.tables

    def test_libro_autor_tiene_solo_las_dos_claves(self):
        columnas = [c.name for c in Base.metadata.tables['libro_autor'].columns]
        assert columnas == ['libro_id', 'autor_id']
