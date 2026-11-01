"""Punto de entrada: crea las tablas y abre la ventana principal."""

import tkinter as tk
from tkinter import ttk, messagebox

from database import crear_tablas
# Se importan los modelos para que Base los conozca antes de crear las tablas
import modelos.sede
import modelos.empleado
import modelos.socio
import modelos.catalogo
import modelos.ejemplar
import modelos.prestamo
import modelos.reserva
import modelos.remito
from dao.empleado_dao import EmpleadoDAO
from datos_ejemplo import cargar_datos_ejemplo
from ui.sedes import PestaniaSedes
from ui.empleados import PestaniaEmpleados
from ui.socios import PestaniaSocios
from ui.catalogo import PestaniaCatalogo
from ui.ejemplares import PestaniaEjemplares

# Pestañas que todavía no tienen su clase en ui/ (se completan en las fases 4 a 7)
PESTANIAS_PENDIENTES = [
    "Préstamos",
    "Reservas",
    "Remitos",
    "Consulta de disponibilidad",
    "Reportes",
]


def main():
    crear_tablas()

    ventana = tk.Tk()
    ventana.title("Biblioteca - Préstamos interbibliotecarios")
    ventana.geometry("1150x750")
    ttk.Style().theme_use("clam")

    # Empleado actual: no hay login, así que se elige acá quién opera.
    # Lo usan las operaciones que registran quién las hizo (fases 4 a 6).
    marco_superior = ttk.Frame(ventana, padding=10)
    marco_superior.pack(fill="x")
    ttk.Label(marco_superior, text="Empleado actual:").pack(side="left")
    combo_empleado = ttk.Combobox(marco_superior, state="readonly", width=40)
    combo_empleado.pack(side="left", padx=5)

    def cargar_empleados():
        combo_empleado.config(values=[texto for id, texto in EmpleadoDAO().opciones()])
    cargar_empleados()
    # Se recarga al entrar, para que aparezcan los empleados recién dados de alta
    combo_empleado.bind("<FocusIn>", lambda evento: cargar_empleados())

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    pestanias = [
        (PestaniaSedes(notebook), "Sedes"),
        (PestaniaEmpleados(notebook), "Empleados"),
        (PestaniaSocios(notebook), "Socios"),
        (PestaniaCatalogo(notebook), "Catálogo"),
        (PestaniaEjemplares(notebook), "Ejemplares"),
    ]
    for pestania, nombre in pestanias:
        notebook.add(pestania, text=nombre)
    for nombre in PESTANIAS_PENDIENTES:
        notebook.add(ttk.Frame(notebook), text=nombre)

    def cargar_ejemplo():
        if cargar_datos_ejemplo():
            for pestania, nombre in pestanias:
                pestania.refrescar()
            cargar_empleados()
            messagebox.showinfo("Datos de ejemplo", "Se cargaron los datos de ejemplo")
        else:
            messagebox.showinfo("Datos de ejemplo", "La base ya tiene datos: no se cargó nada")

    ttk.Button(marco_superior, text="Cargar datos de ejemplo", command=cargar_ejemplo).pack(side="right")

    ventana.mainloop()


if __name__ == "__main__":
    main()
