"""Reporte 3: libros más solicitados para préstamos interbibliotecarios."""

from constantes import EstadoPrestamo, TipoPrestamo
from database import obtener_session
from modelos.prestamo import Prestamo
from reportes.comun import numerar, porcentaje

COLUMNAS = [('libro', "Libro", 230), ('solicitudes', "Solicitudes", 90), ('completados', "Completados", 90),
            ('cancelados', "Cancelados", 90), ('efectividad', "% completado", 100),
            ('ruta', "Ruta más pedida", 260)]


def libros_mas_solicitados_interbibliotecarios():
    """Cuenta todas las solicitudes interbibliotecarias por título (también
    las canceladas: miden la demanda). Completado = llegó al socio (ACTIVO o DEVUELTO)."""
    with obtener_session() as session:
        prestamos = session.query(Prestamo).filter_by(tipo=TipoPrestamo.INTERBIBLIOTECARIO).all()
        por_libro = {}  # título -> {'solicitudes', 'completados', 'cancelados', 'rutas': {ruta: cantidad}}
        for prestamo in prestamos:
            titulo = prestamo.ejemplar.libro.titulo
            if titulo not in por_libro:
                por_libro[titulo] = {'solicitudes': 0, 'completados': 0, 'cancelados': 0, 'rutas': {}}
            datos = por_libro[titulo]
            datos['solicitudes'] += 1
            if prestamo.estado in [EstadoPrestamo.ACTIVO, EstadoPrestamo.DEVUELTO]:
                datos['completados'] += 1
            elif prestamo.estado == EstadoPrestamo.CANCELADO:
                datos['cancelados'] += 1
            ruta = f"{prestamo.sede_origen.nombre} -> {prestamo.sede_destino.nombre}"
            datos['rutas'][ruta] = datos['rutas'].get(ruta, 0) + 1

        filas = []
        for titulo, datos in por_libro.items():
            # La ruta con más pedidos (ante un empate, la primera en orden alfabético)
            ruta, cantidad = sorted(datos['rutas'].items(), key=lambda par: (-par[1], par[0]))[0]
            filas.append({
                'libro': titulo,
                'solicitudes': datos['solicitudes'],
                'completados': datos['completados'],
                'cancelados': datos['cancelados'],
                'efectividad': porcentaje(datos['completados'], datos['solicitudes']),
                'ruta': f"{ruta} ({cantidad})",
            })
        filas = sorted(filas, key=lambda fila: (-fila['solicitudes'], fila['libro']))
        return COLUMNAS, numerar(filas)
