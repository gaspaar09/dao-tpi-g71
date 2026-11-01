"""Reporte 5: tasa de envíos logísticos exitosos e incidencias."""

from constantes import EstadoRemito, TipoEnvio, TipoIncidencia
from database import obtener_session
from modelos.remito import Remito
from reportes.comun import numerar, porcentaje

COLUMNAS = [('concepto', "Concepto", 190), ('remitos', "Remitos", 70), ('despachados', "Despachados", 90),
            ('recibidos', "Recibidos", 80), ('extraviados', "Extraviados", 85), ('cancelados', "Cancelados", 85),
            ('en_curso', "En curso", 75), ('tasa', "Tasa de éxito", 95), ('incidencias', "Incidencias", 85)]

EN_CURSO = [EstadoRemito.EMPAQUETADO, EstadoRemito.DESPACHADO, EstadoRemito.EN_TRANSITO]


def resumir(concepto, remitos):
    """Una fila con los contadores de una lista de remitos.

    Tasa de éxito = recibidos / (recibidos + extraviados): solo cuentan los
    envíos que terminaron su viaje. Un remito cancelado nunca salió."""
    recibidos = len([r for r in remitos if r.estado == EstadoRemito.RECIBIDO])
    extraviados = len([r for r in remitos if r.estado == EstadoRemito.EXTRAVIADO])
    return {
        'concepto': concepto,
        'remitos': len(remitos),
        'despachados': len([r for r in remitos if r.fecha_despacho is not None]),
        'recibidos': recibidos,
        'extraviados': extraviados,
        'cancelados': len([r for r in remitos if r.estado == EstadoRemito.CANCELADO]),
        'en_curso': len([r for r in remitos if r.estado in EN_CURSO]),
        'tasa': porcentaje(recibidos, recibidos + extraviados),
        'incidencias': sum([len(r.incidencias) for r in remitos]),
    }


def tasa_envios_e_incidencias():
    """Una fila por tipo de remito, el total y después las incidencias por tipo."""
    with obtener_session() as session:
        remitos = session.query(Remito).all()
        filas = []
        for tipo in TipoEnvio.TODOS:
            filas.append(resumir(f"Remitos {tipo}", [r for r in remitos if r.tipo == tipo]))
        filas.append(resumir("Total", remitos))
        for tipo in TipoIncidencia.TODOS:
            cantidad = 0
            for remito in remitos:
                cantidad += len([i for i in remito.incidencias if i.tipo == tipo])
            # Las demás columnas no aplican a estas filas: quedan vacías
            fila = {}
            for clave, titulo, ancho in COLUMNAS:
                fila[clave] = ""
            fila['concepto'] = f"Incidencias: {tipo}"
            fila['incidencias'] = cantidad
            filas.append(fila)
        return COLUMNAS, numerar(filas)
