"""Reporte 6: movimiento de ejemplares entre sedes y tiempo promedio de tránsito."""

from constantes import EstadoRemito
from database import obtener_session
from modelos.remito import Remito
from reportes.comun import numerar

COLUMNAS = [('origen', "Origen", 160), ('destino', "Destino", 160), ('remitos', "Remitos", 70),
            ('ejemplares', "Ejemplares enviados", 120), ('recibidos', "Remitos recibidos", 120),
            ('promedio', "Tránsito promedio (días)", 160)]


def movimiento_entre_sedes():
    """Por par origen -> destino. El tiempo de tránsito es fecha_recepcion -
    fecha_despacho y se promedia solo sobre los remitos ya recibidos.
    Los cancelados no se cuentan: no movieron ningún ejemplar."""
    with obtener_session() as session:
        por_ruta = {}  # (origen, destino) -> {'remitos', 'ejemplares', 'dias': [días de cada recibido]}
        for remito in session.query(Remito).all():
            if remito.estado == EstadoRemito.CANCELADO:
                continue
            ruta = (remito.sede_origen.nombre, remito.sede_destino.nombre)
            if ruta not in por_ruta:
                por_ruta[ruta] = {'remitos': 0, 'ejemplares': 0, 'dias': []}
            por_ruta[ruta]['remitos'] += 1
            por_ruta[ruta]['ejemplares'] += len(remito.items)
            if remito.estado == EstadoRemito.RECIBIDO:
                por_ruta[ruta]['dias'].append((remito.fecha_recepcion - remito.fecha_despacho).days)

        filas = []
        for ruta in sorted(por_ruta.keys()):
            datos = por_ruta[ruta]
            promedio = "—"
            if len(datos['dias']) > 0:
                promedio = round(sum(datos['dias']) / len(datos['dias']), 2)
            filas.append({'origen': ruta[0], 'destino': ruta[1], 'remitos': datos['remitos'],
                          'ejemplares': datos['ejemplares'], 'recibidos': len(datos['dias']),
                          'promedio': promedio})
        return COLUMNAS, numerar(filas)
