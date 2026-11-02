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
from dao.reserva_dao import ReservaDAO
from datos_ejemplo import cargar_datos_ejemplo
from ui.sedes import PestaniaSedes
from ui.empleados import PestaniaEmpleados
from ui.socios import PestaniaSocios
from ui.catalogo import PestaniaCatalogo
from ui.ejemplares import PestaniaEjemplares
from ui.prestamos import PestaniaPrestamos
from ui.reservas import PestaniaReservas
from ui.remitos import PestaniaRemitos
from ui.consulta import PestaniaConsulta
from ui.reportes import PestaniaReportes
from ui.estilos import aplicar_estilos


def main():
    crear_tablas()
    # Las reservas cuyo plazo pasó se vencen al abrir la app (y liberan su ejemplar)
    ReservaDAO().procesar_vencimientos()

    ventana = tk.Tk()
    ventana.title("Biblioteca - Préstamos interbibliotecarios")
    # El contenido de las pestañas pide unos 1370x960: se abre con ese tamaño,
    # sin pasarse de la pantalla (en pantallas chicas conviene maximizar)
    ancho = min(1380, ventana.winfo_screenwidth())
    alto = min(960, ventana.winfo_screenheight() - 80)
    ventana.geometry(f"{ancho}x{alto}+0+0")
    aplicar_estilos(ventana)

    # Empleado actual: no hay login, así que se elige acá quién opera.
    # Lo usan las operaciones que registran quién las hizo (préstamos, reservas, devoluciones y remitos).
    marco_superior = ttk.Frame(ventana, padding=(16, 10), style="Header.TFrame")
    marco_superior.pack(fill="x")
    ttk.Label(marco_superior, text="Biblioteca · Préstamos interbibliotecarios",
              style="HeaderTitle.TLabel").pack(side="left", padx=(0, 30))
    ttk.Label(marco_superior, text="Empleado actual:", style="Header.TLabel").pack(side="left")
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
    notebook.pack(fill="both", expand=True, padx=10, pady=(4, 10))
    pestanias = [
        (PestaniaSedes(notebook), "Sedes"),
        (PestaniaEmpleados(notebook), "Empleados"),
        (PestaniaSocios(notebook), "Socios"),
        (PestaniaCatalogo(notebook), "Catálogo"),
        (PestaniaEjemplares(notebook), "Ejemplares"),
        (PestaniaPrestamos(notebook, empleado_actual), "Préstamos"),
        (PestaniaReservas(notebook, empleado_actual), "Reservas"),
        (PestaniaRemitos(notebook, empleado_actual), "Remitos"),
        (PestaniaConsulta(notebook), "Consulta de disponibilidad"),
        (PestaniaReportes(notebook), "Reportes"),
    ]
    for pestania, nombre in pestanias:
        notebook.add(pestania, text=nombre)

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
