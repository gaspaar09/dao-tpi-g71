"""Pestaña de Préstamos: solicitud, aprobación, cancelación, devolución y multas."""

# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk

from config import LARGO_OBSERVACIONES
from constantes import EstadoFisico, TipoPrestamo
from dao.devolucion_dao import DevolucionDAO
from dao.ejemplar_dao import EjemplarDAO
from dao.prestamo_dao import PrestamoDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from ui.base import PestaniaBase
from validadores import validar_fecha, validar_fecha_no_futura, validar_texto_opcional

# Estados en los que se ofrece Cancelar en la fila (un préstamo en envío solo
# se cancela si su remito sigue empaquetado: eso lo controla el DAO)
CAMPOS = ['tipo', 'socio', 'sede_origen', 'sede_destino', 'ejemplar']
CAMPOS_DEVOLUCION = ['fecha_devolucion', 'estado_fisico', 'observaciones']


class PestaniaPrestamos(PestaniaBase):

    def __init__(self, padre, empleado_actual):
        super().__init__(padre, empleado_actual)
        self.dao = PrestamoDAO()
        self.devolucion_dao = DevolucionDAO()

        self.crear_encabezado("Préstamos", "Solicitudes, aprobación, devoluciones y multas",
                              [("Nueva solicitud", self.nueva_solicitud, True)])
        self.crear_barra_seleccion("Con el préstamo elegido:",
                                   [("Aprobar", self.aprobar), ("Registrar devolución", self.abrir_devolucion),
                                    ("Marcar multa pagada", self.pagar_multa)],
                                   [("Cancelar", self.cancelar, True)])
        self.crear_tabla_principal(self, [
            ('id', "N°", 50), ('socio_nombre', "Socio", 180), ('libro', "Libro", 230), ('ejemplar', "Ejemplar", 90),
            ('tipo', "Tipo", 150), ('ruta', "Origen → destino", 260), ('estado', "Estado", 110),
            ('fecha_prestamo', "Préstamo", 100), ('fecha_vencimiento', "Vence", 100),
            ('multa_corta', "Multa", 200)]).pack(fill="both", expand=True)
        self.refrescar()

    # -------------------------------------------------------- solicitud

    def nueva_solicitud(self):
        if self.hay_empleado():
            self.abrir_modal("Nueva solicitud de préstamo", self.armar_solicitud, self.registrar,
                             "Registrar solicitud")

    def armar_solicitud(self, contenedor):
        self.crear_combo(contenedor, 'tipo', "Tipo de préstamo:", 0,
                         lambda: [(tipo, tipo) for tipo in TipoPrestamo.TODOS])
        self.crear_combo(contenedor, 'socio', "Socio (solo habilitados):", 1, SocioDAO().opciones, ancho=45)
        self.crear_combo(contenedor, 'sede_origen', "Sede de origen (del ejemplar):", 2, SedeDAO().opciones)
        self.crear_combo(contenedor, 'sede_destino', "Sede de destino (retiro):", 3, SedeDAO().opciones)
        # Solo los ejemplares disponibles de la sede de origen elegida
        self.crear_combo(contenedor, 'ejemplar', "Ejemplar:", 4,
                         lambda: EjemplarDAO().opciones_disponibles(self.valor('sede_origen')), ancho=45)
        self.ayuda(contenedor, "En un préstamo local la sede de destino es la misma que la de origen. "
                               "La solicitud queda pendiente hasta que se aprueba.", 5)
        # Al elegir una opción se acomoda el formulario. <<ComboboxSelected>> no
        # está en los apuntes; con <FocusOut> el cambio recién se vería al salir
        # del desplegable.
        self.campos['tipo']['widget'].bind("<<ComboboxSelected>>", lambda evento: self.acomodar_destino())
        self.campos['sede_origen']['widget'].bind("<<ComboboxSelected>>", lambda evento: self.cambio_origen())

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
        if not self.validar_campos(CAMPOS):
            return False
        return self.ejecutar(lambda: self.dao.solicitar(self.valor('tipo'), self.valor('socio'), self.valor('ejemplar'),
                                                        self.valor('sede_origen'), self.valor('sede_destino')),
                             "Solicitud registrada. Apruébela para prestar el ejemplar.")

    # -------------------------------------------------------- devolución

    def abrir_devolucion(self):
        id = self.id_seleccionado(self.tabla)
        if id is None or not self.hay_empleado():
            return
        fila = self.buscar_fila(id)
        self.prestamo_devolucion = id
        self.abrir_modal(f"Registrar devolución del préstamo {id}",
                         lambda contenedor: self.armar_devolucion(contenedor, fila), self.devolver,
                         "Registrar devolución")

    def armar_devolucion(self, contenedor, fila):
        ttk.Label(contenedor, text=f"{fila['libro']} ({fila['ejemplar']}), prestado a {fila['socio']}. "
                                   f"Vence: {fila['fecha_vencimiento'] or '-'}",
                  bootstyle="secondary", wraplength=460).grid(row=0, column=0, columnspan=2, sticky="w",
                                                             padx=5, pady=(0, 6))
        self.crear_campo_fecha(contenedor, 'fecha_devolucion', "Fecha de devolución:", 1,
                               lambda v: validar_fecha_no_futura(validar_fecha(v, "fecha de devolución"),
                                                                 "fecha de devolución"))
        self.crear_combo(contenedor, 'estado_fisico', "Estado físico:", 2,
                         lambda: [(estado, estado) for estado in EstadoFisico.TODOS], ancho=20)
        self.crear_campo(contenedor, 'observaciones', "Observaciones:", 3,
                         lambda v: validar_texto_opcional(v, "observaciones", LARGO_OBSERVACIONES), ancho=45)
        self.ayuda(contenedor, "Las observaciones son obligatorias si el ejemplar volvió dañado o destruido. "
                               "Si hubo atraso se calcula la multa.", 4)

    def devolver(self):
        if not self.validar_campos(CAMPOS_DEVOLUCION):
            return False
        return self.ejecutar(
            lambda: self.devolucion_dao.registrar(self.prestamo_devolucion, self.valor('fecha_devolucion'),
                                                  self.valor('estado_fisico'), self.valor('observaciones'),
                                                  self.empleado_actual()),
            "Devolución registrada. Si hubo atraso se generó la multa; si es interbibliotecario, "
            "se creó el remito de devolución.")

    # -------------------------------------------------- acciones directas

    def aprobar(self):
        if self.hay_empleado():
            self.accion_sobre_seleccion(self.dao.aprobar, "¿Aprobar el préstamo seleccionado?",
                                        "Préstamo aprobado. Si es local, ya quedó activo con su vencimiento.")

    def cancelar(self):
        if self.hay_empleado():
            # Si está en envío hace falta el empleado: puede cancelarse su remito
            self.accion_sobre_seleccion(lambda id: self.dao.cancelar(id, self.empleado_actual()),
                                        "¿Cancelar el préstamo seleccionado?", "Préstamo cancelado")

    def pagar_multa(self):
        self.accion_sobre_seleccion(self.dao.pagar_multa, "¿Marcar como pagada la multa del préstamo seleccionado?",
                                    "Multa marcada como pagada")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
