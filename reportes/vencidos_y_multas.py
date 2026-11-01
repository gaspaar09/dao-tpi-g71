"""Reporte 2: préstamos vencidos y multas acumuladas por socio."""

from constantes import EstadoMulta
from database import obtener_session
from modelos.socio import Socio
from reportes.comun import formatear_monto, numerar

COLUMNAS = [('socio', "Socio", 200), ('estado_socio', "Estado del socio", 110),
            ('vencidos', "Préstamos vencidos", 120), ('multas', "Multas", 70),
            ('pendiente', "Deuda pendiente", 110), ('pagado', "Pagado", 90), ('total', "Total multas", 100)]


def vencidos_y_multas_por_socio():
    """Por socio: préstamos vencidos hoy y montos de sus multas. Solo los
    socios con algún vencido o alguna multa, primero los que más deben."""
    with obtener_session() as session:
        filas = []
        for socio in session.query(Socio).all():
            vencidos = len([prestamo for prestamo in socio.prestamos if prestamo.esta_vencido])
            multas = [prestamo.multa for prestamo in socio.prestamos if prestamo.multa is not None]
            if vencidos == 0 and len(multas) == 0:
                continue
            pendiente = sum([multa.monto for multa in multas if multa.estado == EstadoMulta.PENDIENTE])
            pagado = sum([multa.monto for multa in multas if multa.estado == EstadoMulta.PAGADA])
            filas.append({
                'socio': str(socio),
                'estado_socio': socio.estado,
                'vencidos': vencidos,
                'multas': len(multas),
                'pendiente': round(pendiente, 2),
                'pagado': round(pagado, 2),
                'total': round(pendiente + pagado, 2),
            })
        filas = sorted(filas, key=lambda fila: (-fila['pendiente'], -fila['vencidos'], fila['socio']))
        # Los montos se formatean recién después de ordenar por número
        for fila in filas:
            for clave in ['pendiente', 'pagado', 'total']:
                fila[clave] = formatear_monto(fila[clave])
        return COLUMNAS, numerar(filas)
