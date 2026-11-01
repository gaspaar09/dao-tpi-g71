"""Reporte 1: préstamos activos y material en tránsito."""

from constantes import EstadoPrestamo, EstadoRemito
from database import obtener_session
from modelos.prestamo import Prestamo
from modelos.remito import Remito
from reportes.comun import formatear_fecha, numerar

COLUMNAS = [('categoria', "Categoría", 150), ('ejemplar', "Ejemplar", 80), ('libro', "Libro", 200),
            ('socio', "Socio", 170), ('origen', "Origen", 120), ('destino', "Destino", 120),
            ('estado', "Estado", 100), ('fecha', "Vence / Despachado", 120), ('remito', "Remito", 100)]


def prestamos_activos_y_transito():
    """Lo que está fuera de su estante: préstamos ACTIVO (VENCIDO si pasó la
    fecha, que se calcula y no se guarda) y ejemplares viajando en remitos."""
    with obtener_session() as session:
        filas = []
        prestamos = session.query(Prestamo).filter_by(estado=EstadoPrestamo.ACTIVO).all()
        for prestamo in sorted(prestamos, key=lambda p: p.fecha_vencimiento):
            filas.append({
                'categoria': "Préstamo " + prestamo.tipo.lower(),
                'ejemplar': prestamo.ejemplar.codigo_inventario,
                'libro': prestamo.ejemplar.libro.titulo,
                'socio': str(prestamo.socio),
                'origen': prestamo.sede_origen.nombre,
                'destino': prestamo.sede_destino.nombre,
                'estado': prestamo.estado_efectivo,
                'fecha': formatear_fecha(prestamo.fecha_vencimiento),
                'remito': "",
            })
        # Un ejemplar viaja mientras su remito está DESPACHADO o EN_TRANSITO
        remitos = [remito for remito in session.query(Remito).order_by(Remito.id).all()
                   if remito.estado in [EstadoRemito.DESPACHADO, EstadoRemito.EN_TRANSITO]]
        for remito in remitos:
            for item in remito.items:
                filas.append({
                    'categoria': "En tránsito (" + remito.tipo.lower() + ")",
                    'ejemplar': item.ejemplar.codigo_inventario,
                    'libro': item.ejemplar.libro.titulo,
                    'socio': str(item.prestamo.socio),
                    'origen': remito.sede_origen.nombre,
                    'destino': remito.sede_destino.nombre,
                    'estado': remito.estado,
                    'fecha': formatear_fecha(remito.fecha_despacho),
                    'remito': remito.nro_remito,
                })
        return COLUMNAS, numerar(filas)
