"""Configuración de la base de datos.

Copia la configuración del ejemplo "Sistema de biblioteca" de los apuntes
(ORM con SQLAlchemy): motor, clase base, fábrica de sesiones y un context
manager que confirma o deshace la transacción.
"""

from contextlib import contextmanager

from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import DB_URL

# Configuración de la base de datos
engine = create_engine(DB_URL, echo=False)
Base = declarative_base()

# expire_on_commit=False: los objetos devueltos por los DAO mantienen sus
# atributos cargados legibles al cerrarse la sesión. Las relaciones lazy,
# en cambio, solo pueden consultarse con la sesión abierta.
Session = sessionmaker(bind=engine, expire_on_commit=False)


@contextmanager
def obtener_session():
    """Context manager para gestionar sesiones de SQLAlchemy."""
    session = Session()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def crear_tablas():
    """Crea todas las tablas en la base de datos.

    Los modelos tienen que estar importados antes de llamarla,
    si no Base no los conoce y no crea sus tablas.
    """
    Base.metadata.create_all(engine)
