"""Pestaña de Consulta de disponibilidad (para el personal y para los socios)."""

# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk

from dao.consulta_dao import ConsultaDAO
from dao.reserva_dao import ReservaDAO
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase

TODAS_LAS_SEDES = "(todas las sedes)"


def opciones_de_sede():
    """Las sedes (también las dadas de baja: sus ejemplares existen) más la
    opción de no filtrar, que tiene id None."""
    return [(None, TODAS_LAS_SEDES)] + SedeDAO().opciones(solo_activas=False)


class PestaniaConsulta(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = ConsultaDAO()
        self.crear_encabezado("Consulta de disponibilidad",
                              "Cuántos ejemplares de cada título hay en cada sede y en qué estado")

        # Barra de filtros en una sola línea, sobre la tabla
        filtros = ttk.Frame(self)
        filtros.pack(fill="x", pady=(0, 8))
        texto = ttk.Frame(filtros)
        texto.pack(side="left")
        self.crear_campo(texto, 'texto', "Buscar título, autor o ISBN:", 0, ancho=36)
        sede = ttk.Frame(filtros)
        sede.pack(side="left", padx=(12, 0))
        self.crear_combo(sede, 'sede', "Sede:", 0, opciones_de_sede, ancho=24)
        self.poner('sede', None)
        # Enter en el campo de búsqueda equivale a apretar Buscar
        self.campos['texto']['widget'].bind("<Return>", lambda evento: self.refrescar())
        self.campos['sede']['widget'].bind("<<ComboboxSelected>>", lambda evento: self.refrescar())
        ttk.Button(filtros, text="Buscar", bootstyle="primary", command=self.refrescar).pack(
            side="left", padx=(12, 0), anchor="n", pady=(5, 0))
        ttk.Button(filtros, text="Limpiar filtros", bootstyle="secondary-outline", command=self.limpiar).pack(
            side="left", padx=(6, 0), anchor="n", pady=(5, 0))
        self.resumen = ttk.Label(filtros, text="", bootstyle="secondary")
        self.resumen.pack(side="right", anchor="n", pady=(8, 0))

        marco, self.tabla = self.crear_tabla(self, [
            ('titulo', "Título", 250), ('autores', "Autores", 230), ('tipo', "Tipo", 140), ('sede', "Sede", 150),
            ('disponibles', "Disponibles", 100), ('prestados', "Prestados", 90), ('reservados', "Reservados", 95),
            ('en_transito', "En tránsito", 95), ('fuera_de_circulacion', "Fuera de circ.", 110),
            ('total', "Total", 60)], alto=18)
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def limpiar(self):
        self.campos['texto']['widget'].delete(0, "end")
        self.poner('sede', None)
        self.refrescar()

    def refrescar(self):
        # Al consultar se vencen primero las reservas cuyo plazo pasó, así
        # los ejemplares que liberan ya figuran como disponibles
        ReservaDAO().procesar_vencimientos()
        self.filas = self.dao.disponibilidad(self.valor('texto'), self.valor('sede'))
        self.cargar_tabla(self.tabla, self.filas)
        disponibles = sum([fila['disponibles'] for fila in self.filas])
        self.resumen.config(text=f"{len(self.filas)} filas, {disponibles} ejemplares disponibles")
