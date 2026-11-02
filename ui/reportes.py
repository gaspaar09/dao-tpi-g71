"""Pestaña de Reportes: un desplegable para elegir el reporte y una tabla
con el resultado."""

from tkinter import ttk

from reportes import REPORTES
from ui.base import PestaniaBase


class PestaniaReportes(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_combo(formulario, 'reporte', "Reporte:", 0,
                         lambda: [(nombre, nombre) for nombre in REPORTES], ancho=50)
        self.campos['reporte']['widget'].bind("<<ComboboxSelected>>", lambda evento: self.generar())

        botones = ttk.Frame(self)
        botones.pack(anchor="w", pady=10)
        ttk.Button(botones, text="Generar", command=self.generar, style="Accent.TButton").pack(side="left", padx=5)
        self.resumen = ttk.Label(botones, text="Elija un reporte")
        self.resumen.pack(side="left", padx=20)

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
