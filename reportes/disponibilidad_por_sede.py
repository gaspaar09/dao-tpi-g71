"""Reporte 4: disponibilidad del catálogo por sede."""

from dao.consulta_dao import sumar_ejemplar
from database import obtener_session
from modelos.sede import Sede
from reportes.comun import numerar, porcentaje

COLUMNAS = [('sede', "Sede", 160), ('estado_sede', "Estado", 70), ('titulos', "Títulos", 70),
            ('total', "Ejemplares", 80), ('disponibles', "Disponibles", 85), ('prestados', "Prestados", 80),
            ('reservados', "Reservados", 85), ('en_transito', "En tránsito", 85),
            ('fuera_de_circulacion', "Fuera de circ.", 95), ('porcentaje', "% disponible", 95)]


def disponibilidad_por_sede():
    """Resumen de cada sede: cuántos títulos y ejemplares tiene y en qué estado."""
    with obtener_session() as session:
        filas = []
        for sede in session.query(Sede).order_by(Sede.nombre).all():
            fila = {'sede': sede.nombre, 'estado_sede': sede.estado, 'disponibles': 0, 'prestados': 0,
                    'reservados': 0, 'en_transito': 0, 'fuera_de_circulacion': 0, 'total': 0}
            titulos = set()
            for ejemplar in sede.ejemplares:
                titulos.add(ejemplar.libro_id)
                sumar_ejemplar(fila, ejemplar)  # mismo conteo que la Consulta de disponibilidad
            fila['titulos'] = len(titulos)
            fila['porcentaje'] = porcentaje(fila['disponibles'], fila['total'])
            filas.append(fila)
        return COLUMNAS, numerar(filas)
