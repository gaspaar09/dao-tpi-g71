"""Pestaña de Préstamos: solicitud, aprobación y cancelación."""

from tkinter import ttk, messagebox

from constantes import TipoPrestamo
from dao.ejemplar_dao import EjemplarDAO
from dao.prestamo_dao import PrestamoDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from ui.base import PestaniaBase

CAMPOS = ['tipo', 'socio', 'sede_origen', 'sede_destino', 'ejemplar']


class PestaniaPrestamos(PestaniaBase):

    def __init__(self, padre, empleado_actual):
        """empleado_actual es una función que devuelve el id del empleado
        elegido arriba de la ventana, o None si no hay ninguno."""
        super().__init__(padre)
        self.dao = PrestamoDAO()
        self.empleado_actual = empleado_actual

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        self.crear_combo(formulario, 'tipo', "Tipo de préstamo:", 0,
                         lambda: [(tipo, tipo) for tipo in TipoPrestamo.TODOS])
        self.crear_combo(formulario, 'socio', "Socio (solo habilitados):", 1, SocioDAO().opciones, ancho=45)
        self.crear_combo(formulario, 'sede_origen', "Sede de origen (del ejemplar):", 2, SedeDAO().opciones)
        self.crear_combo(formulario, 'sede_destino', "Sede de destino (retiro):", 3, SedeDAO().opciones)
        # Solo los ejemplares disponibles de la sede de origen elegida
        self.crear_combo(formulario, 'ejemplar', "Ejemplar:", 4,
                         lambda: EjemplarDAO().opciones_disponibles(self.valor('sede_origen')), ancho=45)
        ttk.Label(formulario, text="En un préstamo local la sede de destino es la misma que la de origen.",
                  foreground="gray").grid(row=10, column=1, sticky="w", padx=5)

        # Al elegir una opción se acomoda el formulario. <<ComboboxSelected>> no
        # está en los apuntes; con <FocusOut> el cambio recién se vería al salir
        # del desplegable.
        self.campos['tipo']['widget'].bind("<<ComboboxSelected>>", lambda evento: self.acomodar_destino())
        self.campos['sede_origen']['widget'].bind("<<ComboboxSelected>>", lambda evento: self.cambio_origen())

        botones = ttk.Frame(self)
        botones.pack(anchor="w", pady=10)
        self.boton_guardar = ttk.Button(botones, text="Registrar solicitud", command=self.registrar)
        self.boton_guardar.pack(side="left", padx=5)
        ttk.Button(botones, text="Aprobar seleccionado", command=self.aprobar).pack(side="left", padx=5)
        ttk.Button(botones, text="Cancelar seleccionado", command=self.cancelar).pack(side="left", padx=5)
        ttk.Button(botones, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        marco, self.tabla = self.crear_tabla(self, [
            ('id', "N°", 40), ('socio', "Socio", 170), ('libro', "Libro", 160), ('ejemplar', "Ejemplar", 80),
            ('tipo', "Tipo", 130), ('origen', "Origen", 110), ('destino', "Destino", 110),
            ('estado', "Estado", 90), ('fecha_solicitud', "Solicitud", 80),
            ('fecha_prestamo', "Préstamo", 80), ('fecha_vencimiento', "Vence", 80)])
        marco.pack(fill="both", expand=True)
        self.refrescar()

    def acomodar_destino(self):
        """LOCAL: el destino es el origen y no se puede cambiar.
        INTERBIBLIOTECARIO: el destino se elige."""
        destino = self.campos['sede_destino']['widget']
        if self.valor('tipo') == TipoPrestamo.LOCAL:
            destino.config(state="readonly")
            destino.set(self.campos['sede_origen']['widget'].get())
            destino.config(state="disabled")
        else:
            if str(destino.cget("state")) == "disabled":
                destino.set("")
            destino.config(state="readonly")
        self.campos['sede_destino']['error'].config(text="")

    def cambio_origen(self):
        # El ejemplar elegido era de la sede anterior
        self.campos['ejemplar']['widget'].set("")
        self.acomodar_destino()

    def hay_empleado(self):
        """Las operaciones de préstamo quedan registradas a nombre de un
        empleado: sin empleado actual elegido no se permiten."""
        if self.empleado_actual() is None:
            messagebox.showerror("Falta el empleado", "Seleccione el empleado actual arriba de la ventana")
            return False
        return True

    def registrar(self):
        if not self.hay_empleado():
            return
        obligatorios = ['tipo', 'socio', 'sede_origen', 'sede_destino', 'ejemplar']
        if not self.validar_campos(obligatorios):
            return
        if self.ejecutar(lambda: self.dao.solicitar(self.valor('tipo'), self.valor('socio'), self.valor('ejemplar'),
                                                    self.valor('sede_origen'), self.valor('sede_destino')),
                         "Solicitud registrada. Apruébela para prestar el ejemplar."):
            self.limpiar()

    def aprobar(self):
        if self.hay_empleado():
            self.accion_sobre_seleccion(self.dao.aprobar, "¿Aprobar el préstamo seleccionado?",
                                        "Préstamo aprobado. Si es local, ya quedó activo con su vencimiento.")

    def cancelar(self):
        if self.hay_empleado():
            self.accion_sobre_seleccion(self.dao.cancelar, "¿Cancelar el préstamo seleccionado?",
                                        "Préstamo cancelado")

    def limpiar(self):
        # No hay modificación de préstamos: solo se vacía el formulario
        self.campos['sede_destino']['widget'].config(state="readonly")
        self.limpiar_campos(CAMPOS)
        self.tabla.selection_remove(self.tabla.selection())

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
