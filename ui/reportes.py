"""Pestaña de Reportes: un desplegable para elegir el reporte y una tabla
con el resultado."""

# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk

from reportes import REPORTES
from ui.base import PestaniaBase


class PestaniaReportes(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)
        self.crear_encabezado("Reportes", "Información de gestión que se actualiza después de cada operación")

        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))
        selector = ttk.Frame(barra)
        selector.pack(side="left")
        self.crear_combo(selector, 'reporte', "Reporte:", 0,
                         lambda: [(nombre, nombre) for nombre in REPORTES], ancho=55)
        # Al elegir un reporte se genera en el momento
        self.campos['reporte']['widget'].bind("<<ComboboxSelected>>", lambda evento: self.generar())
        ttk.Button(barra, text="Generar", bootstyle="primary", command=self.generar).pack(
            side="left", padx=(12, 0), anchor="n", pady=(5, 0))
        self.resumen = ttk.Label(barra, text="Elegí un reporte de la lista", bootstyle="secondary")
        self.resumen.pack(side="right", anchor="n", pady=(8, 0))

        # Cada reporte tiene sus propias columnas: la tabla se arma de nuevo
        # al generar, dentro de este contenedor
        self.contenedor = ttk.Frame(self)
        self.contenedor.pack(fill="both", expand=True)
        self.marco_tabla = None
        self.tabla = None

    def generar(self):
        if not self.validar_campos(['reporte']):
            return
        self.mostrar(self.valor('reporte'))

    def mostrar(self, nombre):
        columnas, filas = REPORTES[nombre]()
        if self.marco_tabla is not None:
            self.marco_tabla.destroy()
        self.marco_tabla, self.tabla = self.crear_tabla(self.contenedor, columnas, alto=20)
        self.marco_tabla.pack(fill="both", expand=True)
        self.filas = filas
        self.cargar_tabla(self.tabla, filas)
        self.resumen.config(text=f"{len(filas)} filas" if filas else "Sin datos para este reporte")

    def refrescar(self):
        # Después de cualquier operación se vuelve a generar el reporte elegido
        if self.valor('reporte') is not None:
            self.mostrar(self.valor('reporte'))
