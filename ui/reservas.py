"""Pestaña de Reservas: alta, retiro (crea el préstamo), cancelación y vencimientos."""

from tkinter import messagebox

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
        self.crear_encabezado("Reservas", "Títulos apartados para que un socio los retire en una sede",
                              [("Procesar vencimientos", self.procesar, False),
                               ("Nueva reserva", self.nueva_reserva, True)])
        self.crear_barra_seleccion("Con la reserva elegida:", [("Retirar (crea el préstamo)", self.retirar)],
                                   [("Cancelar", self.cancelar, True)])
        self.crear_tabla_principal(self, [
            ('id', "N°", 50), ('socio', "Socio", 200), ('libro', "Libro", 250), ('sede', "Sede de retiro", 160),
            ('ejemplar', "Ejemplar", 100), ('estado', "Estado", 110), ('fecha_reserva', "Reservada", 100),
            ('fecha_vencimiento', "Vence", 100)]).pack(fill="both", expand=True)
        self.refrescar()

    def nueva_reserva(self):
        if self.hay_empleado():
            self.abrir_modal("Nueva reserva", self.armar_reserva, self.reservar, "Reservar")

    def armar_reserva(self, contenedor):
        self.crear_combo(contenedor, 'socio', "Socio (solo habilitados):", 0, SocioDAO().opciones, ancho=45)
        self.crear_combo(contenedor, 'libro', "Libro:", 1, LibroDAO().opciones, ancho=45)
        self.crear_combo(contenedor, 'sede_retiro', "Sede de retiro:", 2, SedeDAO().opciones)
        self.ayuda(contenedor, "Si hay un ejemplar libre en esa sede se aparta en el acto y el socio tiene "
                               "2 días para retirarlo; si no, la reserva espera hasta 45 días.", 3)

    def reservar(self):
        if not self.validar_campos(CAMPOS):
            return False
        return self.ejecutar(lambda: self.dao.crear(self.valor('socio'), self.valor('libro'),
                                                    self.valor('sede_retiro')), "Reserva registrada")

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

    def refrescar(self):
        # Antes de mostrar se vencen las reservas cuyo plazo pasó (modifica datos)
        self.dao.procesar_vencimientos()
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
