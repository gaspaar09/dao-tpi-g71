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
from ui.prestamos import PestaniaPrestamos

# Pestañas que todavía no tienen su clase en ui/ (se completan en las fases 5 a 7)
PESTANIAS_PENDIENTES = [
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

    empleados = {}  # texto mostrado -> id

    def cargar_empleados():
        empleados.clear()
        for id, texto in EmpleadoDAO().opciones():
            empleados[texto] = id
        combo_empleado.config(values=list(empleados.keys()))
        if combo_empleado.get() not in empleados:
            combo_empleado.set("")

    def empleado_actual():
        """Id del empleado elegido, o None. Lo usan las pestañas que registran operaciones."""
        texto = combo_empleado.get()
        if texto in empleados:
            return empleados[texto]
        return None

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
        (PestaniaPrestamos(notebook, empleado_actual), "Préstamos"),
    ]
    for pestania, nombre in pestanias:
        notebook.add(pestania, text=nombre)
    for nombre in PESTANIAS_PENDIENTES:
        notebook.add(ttk.Frame(notebook), text=nombre)

    def refrescar_todas():
        """Recarga las tablas de todas las pestañas y la lista de empleados."""
        for pestania, nombre in pestanias:
            pestania.refrescar()
        cargar_empleados()

    # Cualquier operación exitosa refresca todo, porque puede cambiar datos que
    # muestra otra pestaña (aprobar un préstamo cambia el estado del ejemplar)
    for pestania, nombre in pestanias:
        pestania.avisar_cambios_a(refrescar_todas)

    def cargar_ejemplo():
        if cargar_datos_ejemplo():
            refrescar_todas()
            messagebox.showinfo("Datos de ejemplo", "Se cargaron los datos de ejemplo")
        else:
            messagebox.showinfo("Datos de ejemplo", "La base ya tiene datos: no se cargó nada")

    ttk.Button(marco_superior, text="Cargar datos de ejemplo", command=cargar_ejemplo).pack(side="right")

    ventana.mainloop()


if __name__ == "__main__":
    main()
