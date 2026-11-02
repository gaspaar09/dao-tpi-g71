"""Pestaña de Reservas: alta, retiro (crea el préstamo), cancelación y vencimientos."""

from tkinter import ttk, messagebox

from dao.libro_dao import LibroDAO
from dao.reserva_dao import ReservaDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from ui.base import PestaniaBase

CAMPOS = ['socio', 'libro', 'sede_retiro']


class PestaniaReservas(PestaniaBase):

    def __init__(self, padre, empleado_actual):
        super().__init__(padre, empleado_actual)
        self.dao = ReservaDAO()

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_combo(formulario, 'socio', "Socio (solo habilitados):", 0, SocioDAO().opciones, ancho=45)
        self.crear_combo(formulario, 'libro', "Libro:", 1, LibroDAO().opciones, ancho=45)
        self.crear_combo(formulario, 'sede_retiro', "Sede de retiro:", 2, SedeDAO().opciones)
        ttk.Label(formulario, text="Si hay un ejemplar libre en esa sede se aparta en el acto (2 días para "
                                   "retirarlo); si no, la reserva espera hasta 45 días.",
                  style="Muted.TLabel").grid(row=6, column=1, sticky="w", padx=5)

        botones = ttk.Frame(self)
        botones.pack(anchor="w", pady=10)
        ttk.Button(botones, text="Reservar", command=self.reservar, style="Accent.TButton").pack(side="left", padx=5)
        ttk.Button(botones, text="Retirar seleccionada", command=self.retirar).pack(side="left", padx=5)
        ttk.Button(botones, text="Cancelar seleccionada", command=self.cancelar).pack(side="left", padx=5)
        ttk.Button(botones, text="Procesar vencimientos", command=self.procesar).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        marco, self.tabla = self.crear_tabla(self, [
            ('id', "N°", 40), ('socio', "Socio", 190), ('libro', "Libro", 200), ('sede', "Sede de retiro", 130),
            ('ejemplar', "Ejemplar", 80), ('estado', "Estado", 90), ('fecha_reserva', "Reservada", 80),
            ('fecha_vencimiento', "Vence", 80)])
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def reservar(self):
        if not self.hay_empleado() or not self.validar_campos(CAMPOS):
            return
        if self.ejecutar(lambda: self.dao.crear(self.valor('socio'), self.valor('libro'), self.valor('sede_retiro')),
                         "Reserva registrada"):
            self.limpiar()

    def retirar(self):
        if self.hay_empleado():
            self.accion_sobre_seleccion(self.dao.retirar, "¿El socio retira el ejemplar de la reserva seleccionada?",
                                        "Reserva cumplida: se creó el préstamo local, ya activo")

    def cancelar(self):
        if self.hay_empleado():
            self.accion_sobre_seleccion(self.dao.cancelar, "¿Cancelar la reserva seleccionada?",
                                        "Reserva cancelada. Si tenía ejemplar, pasó a la siguiente en espera.")

    def procesar(self):
        vencidas = self.dao.procesar_vencimientos()
        messagebox.showinfo("Vencimientos", f"Reservas vencidas en este proceso: {vencidas}")
        if self.refrescar_todo is not None:
            self.refrescar_todo()

    def limpiar(self):
        self.limpiar_campos(CAMPOS)
        self.tabla.selection_remove(self.tabla.selection())

    def refrescar(self):
        # Antes de mostrar se vencen las reservas cuyo plazo pasó (modifica datos)
        self.dao.procesar_vencimientos()
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
