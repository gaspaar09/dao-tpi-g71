"""Punto de entrada: crea las tablas y abre la ventana principal."""

import tkinter.font as tkfont
from tkinter import messagebox

# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk


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
from ui.base import aplicar_estilo_tablas
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

# Temas de ttkbootstrap para elegir arriba de la ventana; el primero es el que abre
TEMAS = ["bootstrap-light", "minty-light", "pulse-light", "nord-light", "sandstone-light",
         "bootstrap-dark", "nord-dark"]


def main():
    crear_tablas()
    # Las reservas cuyo plazo pasó se vencen al abrir la app (y liberan su ejemplar)
    ReservaDAO().procesar_vencimientos()

    # ttkbootstrap: ventana de Tkinter con temas modernos para todos los widgets ttk
    ventana = ttk.Window(themename=TEMAS[0])
    # Letra 2 puntos más grande en toda la app: se agrandan las fuentes con
    # nombre que usan los widgets (texto, campos y títulos de las tablas)
    for nombre in ["TkDefaultFont", "TkTextFont", "TkHeadingFont", "TkMenuFont"]:
        fuente = tkfont.nametofont(nombre)
        fuente.configure(size=fuente.cget("size") + 2)
    ventana.title("Biblioteca - Préstamos interbibliotecarios")
    # Tamaño al salir de maximizada: unos 1380x1000, sin pasarse de la pantalla
    ancho = min(1380, ventana.winfo_screenwidth())
    alto = min(1000, ventana.winfo_screenheight() - 80)
    ventana.geometry(f"{ancho}x{alto}+0+0")
    # Se abre maximizada: la tabla de Préstamos necesita todo el ancho para
    # mostrar la columna Acciones sin desplazarse
    ventana.state("zoomed")

    # Empleado actual: no hay login, así que se elige acá quién opera.
    # Lo usan las operaciones que registran quién las hizo (préstamos, reservas, devoluciones y remitos).
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

    # Selector de tema: cambia el aspecto de toda la ventana en el momento
    combo_tema = ttk.Combobox(marco_superior, state="readonly", values=TEMAS, width=18)
    combo_tema.set(TEMAS[0])
    combo_tema.pack(side="right", padx=(5, 20))
    ttk.Label(marco_superior, text="Tema:").pack(side="right")
    def cambiar_tema():
        ttk.Style().theme_use(combo_tema.get())
        # Los estilos de las tablas dependen del tema: se vuelven a aplicar
        aplicar_estilo_tablas()

    combo_tema.bind("<<ComboboxSelected>>", lambda evento: cambiar_tema())

    ventana.mainloop()


if __name__ == "__main__":
    main()
