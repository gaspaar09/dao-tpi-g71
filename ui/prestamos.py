"""Pestaña de Préstamos: solicitud, aprobación, cancelación, devolución y multas."""

from datetime import date
from tkinter import ttk

from config import LARGO_OBSERVACIONES
from constantes import EstadoFisico, TipoPrestamo
from dao.devolucion_dao import DevolucionDAO
from dao.ejemplar_dao import EjemplarDAO
from dao.prestamo_dao import PrestamoDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from ui.base import PestaniaBase
from validadores import validar_fecha, validar_fecha_no_futura, validar_texto_opcional

CAMPOS = ['tipo', 'socio', 'sede_origen', 'sede_destino', 'ejemplar']
CAMPOS_DEVOLUCION = ['fecha_devolucion', 'estado_fisico', 'observaciones']


class PestaniaPrestamos(PestaniaBase):

    def __init__(self, padre, empleado_actual):
        super().__init__(padre, empleado_actual)
        self.dao = PrestamoDAO()
        self.devolucion_dao = DevolucionDAO()

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
            ('fecha_prestamo', "Préstamo", 80), ('fecha_vencimiento', "Vence", 80),
            ('multa', "Multa", 170)], alto=7)
        marco.pack(fill="both", expand=True)

        # --- Devolución del préstamo seleccionado en la tabla
        ttk.Label(self, text="DEVOLUCIÓN DEL PRÉSTAMO SELECCIONADO").pack(anchor="w", pady=(10, 0), padx=5)
        devolucion = ttk.Frame(self)
        devolucion.pack(fill="x")
        self.crear_campo_fecha(devolucion, 'fecha_devolucion', "Fecha (elegir o dd/mm/aaaa):", 0,
                               lambda v: validar_fecha_no_futura(validar_fecha(v, "fecha de devolución"),
                                                                 "fecha de devolución"))
        self.crear_combo(devolucion, 'estado_fisico', "Estado físico:", 1,
                         lambda: [(estado, estado) for estado in EstadoFisico.TODOS], ancho=20)
        self.crear_campo(devolucion, 'observaciones', "Observaciones:", 2,
                         lambda v: validar_texto_opcional(v, "observaciones", LARGO_OBSERVACIONES), ancho=50)
        ttk.Label(devolucion, text="Obligatorias si el ejemplar volvió dañado o destruido.",
                  foreground="gray").grid(row=6, column=1, sticky="w", padx=5)
        botones = ttk.Frame(devolucion)
        botones.grid(row=0, column=2, rowspan=3, sticky="n", padx=20)
        ttk.Button(botones, text="Registrar devolución", command=self.devolver).pack(fill="x", pady=2)
        ttk.Button(botones, text="Marcar multa pagada", command=self.pagar_multa).pack(fill="x", pady=2)
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
            # Si está en envío hace falta el empleado: puede cancelarse su remito
            self.accion_sobre_seleccion(lambda id: self.dao.cancelar(id, self.empleado_actual()),
                                        "¿Cancelar el préstamo seleccionado?", "Préstamo cancelado")

    def devolver(self):
        if not self.hay_empleado() or not self.validar_campos(CAMPOS_DEVOLUCION):
            return
        self.accion_sobre_seleccion(
            lambda id: self.devolucion_dao.registrar(id, self.valor('fecha_devolucion'), self.valor('estado_fisico'),
                                                     self.valor('observaciones'), self.empleado_actual()),
            "¿Registrar la devolución del préstamo seleccionado?",
            "Devolución registrada. Si hubo atraso se generó la multa; si es interbibliotecario, "
            "se creó el remito de devolución.")

    def pagar_multa(self):
        self.accion_sobre_seleccion(self.dao.pagar_multa, "¿Marcar como pagada la multa del préstamo seleccionado?",
                                    "Multa marcada como pagada")

    def limpiar(self):
        # No hay modificación de préstamos: solo se vacía el formulario
        self.campos['sede_destino']['widget'].config(state="readonly")
        self.limpiar_campos(CAMPOS + CAMPOS_DEVOLUCION)
        self.poner('fecha_devolucion', date.today().strftime("%d/%m/%Y"))
        self.tabla.selection_remove(self.tabla.selection())

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
