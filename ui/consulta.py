"""Pestaña de Consulta de disponibilidad (para el personal y para los socios)."""

from tkinter import ttk

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

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_campo(formulario, 'texto', "Título, autor o ISBN (vacío = todos):", 0, ancho=40)
        self.crear_combo(formulario, 'sede', "Sede:", 1, opciones_de_sede)
        self.poner('sede', None)
        # Enter en el campo de búsqueda equivale a apretar Buscar
        self.campos['texto']['widget'].bind("<Return>", lambda evento: self.refrescar())

        botones = ttk.Frame(self)
        botones.pack(anchor="w", pady=10)
        ttk.Button(botones, text="Buscar", command=self.refrescar).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        self.resumen = ttk.Label(botones, text="")
        self.resumen.pack(side="left", padx=20)

        marco, self.tabla = self.crear_tabla(self, [
            ('titulo', "Título", 230), ('autores', "Autores", 200), ('tipo', "Tipo", 120), ('sede', "Sede", 130),
            ('disponibles', "Disponibles", 80), ('prestados', "Prestados", 75), ('reservados', "Reservados", 80),
            ('en_transito', "En tránsito", 80), ('fuera_de_circulacion', "Fuera de circ.", 90),
            ('total', "Total", 50)], alto=18)
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def limpiar(self):
        self.limpiar_campos(['texto'])
        self.poner('sede', None)
        self.refrescar()

    def refrescar(self):
        # Al consultar se vencen primero las reservas cuyo plazo pasó, así
        # los ejemplares que liberan ya figuran como disponibles
        ReservaDAO().procesar_vencimientos()
        self.filas = self.dao.disponibilidad(self.valor('texto'), self.valor('sede'))
        self.cargar_tabla(self.tabla, self.filas)
        disponibles = sum([fila['disponibles'] for fila in self.filas])
        self.resumen.config(text=f"{len(self.filas)} filas - {disponibles} ejemplares disponibles")
