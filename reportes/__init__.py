"""Reportes: una función por reporte. Cada una devuelve (columnas, filas)
listas para mostrar en un Treeview, igual que los listar() de los DAO."""

from reportes.prestamos_activos import prestamos_activos_y_transito
from reportes.vencidos_y_multas import vencidos_y_multas_por_socio
from reportes.mas_solicitados import libros_mas_solicitados_interbibliotecarios
from reportes.disponibilidad_por_sede import disponibilidad_por_sede
from reportes.envios_e_incidencias import tasa_envios_e_incidencias
from reportes.movimiento_entre_sedes import movimiento_entre_sedes

# Nombre que se muestra en el desplegable -> función que arma el reporte
REPORTES = {
    "1. Préstamos activos y material en tránsito": prestamos_activos_y_transito,
    "2. Préstamos vencidos y multas por socio": vencidos_y_multas_por_socio,
    "3. Libros más solicitados (interbibliotecarios)": libros_mas_solicitados_interbibliotecarios,
    "4. Disponibilidad de catálogo por sede": disponibilidad_por_sede,
    "5. Tasa de envíos exitosos e incidencias": tasa_envios_e_incidencias,
    "6. Movimiento de ejemplares entre sedes": movimiento_entre_sedes,
}
