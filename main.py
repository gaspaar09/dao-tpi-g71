"""Punto de entrada: crea las tablas y abre la ventana principal."""

import tkinter as tk
from tkinter import ttk

from database import crear_tablas

# Una pestaña por módulo. En la Fase 3 cada Frame vacío se reemplaza
# por su clase de la carpeta ui/.
PESTANIAS = [
    "Sedes",
    "Empleados",
    "Socios",
    "Catálogo",
    "Ejemplares",
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
    ventana.geometry("1000x650")
    ttk.Style().theme_use("clam")

    # Empleado actual: no hay login, así que se elige acá quién opera.
    # Se llena con los empleados cuando exista EmpleadoDAO (Fase 3).
    marco_empleado = ttk.Frame(ventana, padding=10)
    marco_empleado.pack(fill="x")
    ttk.Label(marco_empleado, text="Empleado actual:").pack(side="left")
    combo_empleado = ttk.Combobox(marco_empleado, state="readonly", width=40)
    combo_empleado.pack(side="left", padx=5)

    notebook = ttk.Notebook(ventana)
    notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))
    for nombre in PESTANIAS:
        frame = ttk.Frame(notebook)
        notebook.add(frame, text=nombre)

    ventana.mainloop()


if __name__ == "__main__":
    main()
