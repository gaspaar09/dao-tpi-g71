"""Pestaña de Remitos: armado del envío, cambios de estado, historial e incidencias."""

import tkinter as tk
# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk

from config import LARGO_OBSERVACION_MOVIMIENTO, LARGO_DESCRIPCION_INCIDENCIA
from constantes import TipoIncidencia
from dao.remito_dao import RemitoDAO
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase, FUENTE_MODAL
from validadores import validar_texto, validar_texto_opcional, validar_fecha, validar_fecha_no_futura

CAMPOS_INCIDENCIA = ['tipo_incidencia', 'fecha', 'descripcion']


def validar_fecha_incidencia(valor):
    return validar_fecha_no_futura(validar_fecha(valor, "fecha"), "fecha")


class PestaniaRemitos(PestaniaBase):

    def __init__(self, padre, empleado_actual):
        super().__init__(padre, empleado_actual)
        self.dao = RemitoDAO()
        self.prestamos_ids = []  # id de cada renglón del Listbox de préstamos

        self.crear_encabezado("Remitos", "Envíos de ejemplares entre sedes y su recorrido",
                              [("Remito de devolución", self.nuevo_remito_devolucion, False),
                               ("Nuevo remito", self.nuevo_remito, True)])
        self.crear_barra_seleccion("Con el remito elegido:",
                                   [("Avanzar estado", self.abrir_avanzar),
                                    ("Registrar incidencia", self.abrir_incidencia)],
                                   [("Dar por extraviado", self.abrir_extraviar), ("Cancelar", self.abrir_cancelar, True)])
        self.crear_tabla_principal(self, [
            ('nro_remito', "N° remito", 110), ('tipo', "Tipo", 110), ('origen', "Origen", 150),
            ('destino', "Destino", 150), ('estado', "Estado", 120), ('ejemplares', "Ejemplares", 200),
            ('fecha_creacion', "Creación", 100), ('fecha_despacho', "Despacho", 100),
            ('fecha_recepcion', "Recepción", 100)], alto=8).pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda evento: self.al_elegir_remito())

        # Detalle del remito elegido: historial de estados e incidencias, lado a lado
        detalle = ttk.Frame(self, padding=(0, 14, 0, 0))
        detalle.pack(fill="x")
        izquierda = ttk.Frame(detalle)
        izquierda.pack(side="left", fill="both", expand=True)
        self.titulo_detalle = ttk.Label(izquierda, text="Historial", font=FUENTE_MODAL)
        self.titulo_detalle.pack(anchor="w")
        self.aviso_detalle = ttk.Label(izquierda, text="Elegí un remito para ver sus cambios de estado",
                                       bootstyle="secondary")
        self.aviso_detalle.pack(anchor="w", pady=(0, 6))
        marco, self.tabla_movimientos = self.crear_tabla(izquierda, [
            ('fecha_hora', "Fecha y hora", 130), ('estado_anterior', "Anterior", 120),
            ('estado_nuevo', "Nuevo", 120), ('empleado', "Empleado", 190), ('observacion', "Observación", 220)],
            alto=5)
        marco.pack(fill="x")
        derecha = ttk.Frame(detalle, padding=(16, 0, 0, 0))
        derecha.pack(side="left", fill="both")
        ttk.Label(derecha, text="Incidencias", font=FUENTE_MODAL).pack(anchor="w")
        ttk.Label(derecha, text="Extravíos, daños y demoras del envío", bootstyle="secondary").pack(
            anchor="w", pady=(0, 6))
        marco, self.tabla_incidencias = self.crear_tabla(derecha, [
            ('tipo', "Tipo", 100), ('fecha', "Fecha", 100), ('descripcion', "Descripción", 230)], alto=5)
        marco.pack(fill="x")

        self.refrescar()

    def remito_elegido(self):
        """La fila del remito elegido en la tabla, o None."""
        seleccion = self.tabla.selection()
        if not seleccion:
            return None
        return self.buscar_fila(int(seleccion[0]))

    # ------------------------------------------------------- nuevo remito

    def nuevo_remito(self):
        if self.hay_empleado():
            self.abrir_modal("Nuevo remito de ida", self.armar_remito, self.crear_remito, "Crear remito")

    def armar_remito(self, contenedor):
        self.crear_combo(contenedor, 'sede_origen', "Sede de origen:", 0, SedeDAO().opciones)
        self.crear_combo(contenedor, 'sede_destino', "Sede de destino:", 1, SedeDAO().opciones)
        # Al cambiar las sedes cambian los préstamos que se pueden enviar
        for nombre in ['sede_origen', 'sede_destino']:
            self.campos[nombre]['widget'].bind("<<ComboboxSelected>>", lambda evento: self.recargar_prestamos())
        ttk.Label(contenedor, text="Préstamos a enviar:").grid(row=4, column=0, sticky="nw", padx=5, pady=(8, 0))
        # Igual que los autores de un libro: Listbox de selección múltiple
        self.lista_prestamos = tk.Listbox(contenedor, selectmode="multiple", height=6, width=60,
                                          exportselection=False)
        self.lista_prestamos.grid(row=4, column=1, sticky="w", padx=5, pady=(8, 0))
        self.ayuda(contenedor, "Aparecen los préstamos interbibliotecarios aprobados entre esas dos sedes. "
                               "Marcá uno o varios: viajan juntos en el mismo remito.", 3)
        self.recargar_prestamos()

    def recargar_prestamos(self):
        self.lista_prestamos.delete(0, tk.END)
        self.prestamos_ids = []
        for id, texto in self.dao.prestamos_para_enviar(self.valor('sede_origen'), self.valor('sede_destino')):
            self.lista_prestamos.insert(tk.END, texto)
            self.prestamos_ids.append(id)

    def prestamos_seleccionados(self):
        return [self.prestamos_ids[indice] for indice in self.lista_prestamos.curselection()]

    def crear_remito(self):
        if not self.validar_campos(['sede_origen', 'sede_destino']):
            return False
        return self.ejecutar(lambda: self.dao.crear_ida(self.valor('sede_origen'), self.valor('sede_destino'),
                                                        self.prestamos_seleccionados(), self.empleado_actual()),
                             "Remito creado: quedó EMPAQUETADO y sus préstamos EN_ENVIO")

    def nuevo_remito_devolucion(self):
        if self.hay_empleado():
            self.abrir_modal("Nuevo remito de devolución", self.armar_devolucion, self.crear_devolucion,
                             "Crear remito")

    def armar_devolucion(self, contenedor):
        # Una devolución cuyo remito se canceló necesita uno nuevo
        self.crear_combo(contenedor, 'devolucion', "Devolución sin remito:", 0, self.dao.devoluciones_pendientes,
                         ancho=45)
        self.ayuda(contenedor, "Los remitos de devolución se crean solos al devolver un préstamo "
                               "interbibliotecario. Acá aparecen los que quedaron sin remito porque se "
                               "canceló el anterior.", 1)

    def crear_devolucion(self):
        if not self.validar_campos(['devolucion']):
            return False
        return self.ejecutar(lambda: self.dao.crear_devolucion(self.valor('devolucion'), self.empleado_actual()),
                             "Remito de devolución creado")

    # --------------------------------------------------- cambios de estado

    def abrir_cambio_de_estado(self, titulo, explicacion, accion, texto_boton, mensaje_ok, obligatoria):
        """Modal para avanzar, cancelar o extraviar el remito elegido. La
        observación queda en el historial; al cancelar o extraviar es obligatoria."""
        fila = self.remito_elegido()
        if fila is None or not self.hay_empleado():
            return
        if obligatoria:
            validador = lambda v: validar_texto(v, "observación", LARGO_OBSERVACION_MOVIMIENTO)
            etiqueta = "Observación:"
        else:
            validador = lambda v: validar_texto_opcional(v, "observación", LARGO_OBSERVACION_MOVIMIENTO)
            etiqueta = "Observación (opcional):"

        def armar(contenedor):
            ttk.Label(contenedor, text=f"{fila['nro_remito']}: {fila['origen']} a {fila['destino']}, "
                                       f"hoy {fila['estado']}.", bootstyle="secondary").grid(
                row=0, column=0, columnspan=2, sticky="w", padx=5)
            self.ayuda(contenedor, explicacion, 1)
            self.crear_campo(contenedor, 'observacion', etiqueta, 2, validador, ancho=45)

        def aceptar():
            if not self.validar_campos(['observacion']):
                return False
            observacion = self.valor('observacion')
            return self.ejecutar(lambda: accion(fila['id'], self.empleado_actual(), observacion), mensaje_ok)

        self.abrir_modal(titulo, armar, aceptar, texto_boton)

    def abrir_avanzar(self):
        self.abrir_cambio_de_estado(
            "Avanzar el remito a su estado siguiente",
            "Empaquetado pasa a despachado, despachado a en tránsito y en tránsito a recibido.",
            self.dao.avanzar, "Avanzar estado", "Estado del remito actualizado", obligatoria=False)

    def abrir_cancelar(self):
        self.abrir_cambio_de_estado(
            "Cancelar el remito",
            "Solo se cancela un remito que todavía no salió (empaquetado).",
            self.dao.cancelar, "Cancelar remito",
            "Remito cancelado. Si era de ida, los ejemplares volvieron a estar disponibles; "
            "si era de devolución, esperan un remito nuevo.", obligatoria=True)

    def abrir_extraviar(self):
        self.abrir_cambio_de_estado(
            "Dar el remito por extraviado",
            "Solo un remito en tránsito. Sus ejemplares quedan extraviados y se registra la incidencia.",
            self.dao.extraviar, "Dar por extraviado", "Remito extraviado: se registró la incidencia",
            obligatoria=True)

    # ------------------------------------------------- detalle e incidencias

    def al_elegir_remito(self):
        self.activar_botones_seleccion()
        self.cargar_detalle()

    def cargar_detalle(self):
        fila = self.remito_elegido()
        if fila is None:
            self.titulo_detalle.config(text="Historial")
            self.aviso_detalle.config(text="Elegí un remito para ver sus cambios de estado")
            self.cargar_tabla(self.tabla_movimientos, [])
            self.cargar_tabla(self.tabla_incidencias, [])
            return
        self.titulo_detalle.config(text=f"Historial del remito {fila['nro_remito']}")
        self.aviso_detalle.config(text="Cada cambio de estado, con quién lo registró")
        self.cargar_tabla(self.tabla_movimientos, self.dao.listar_movimientos(fila['id']))
        self.cargar_tabla(self.tabla_incidencias, self.dao.listar_incidencias(fila['id']))

    def abrir_incidencia(self):
        fila = self.remito_elegido()
        if fila is None or not self.hay_empleado():
            return

        def armar(contenedor):
            self.crear_combo(contenedor, 'tipo_incidencia', "Tipo:", 0,
                             lambda: [(tipo, tipo) for tipo in TipoIncidencia.TODOS], ancho=20)
            self.crear_campo_fecha(contenedor, 'fecha', "Fecha:", 1, validar_fecha_incidencia)
            self.crear_campo(contenedor, 'descripcion', "Descripción:", 2,
                             lambda v: validar_texto(v, "descripción", LARGO_DESCRIPCION_INCIDENCIA, 5), ancho=45)

        def aceptar():
            if not self.validar_campos(CAMPOS_INCIDENCIA):
                return False
            return self.ejecutar(lambda: self.dao.registrar_incidencia(fila['id'], self.valor('tipo_incidencia'),
                                                                       self.valor('fecha'), self.valor('descripcion')),
                                 "Incidencia registrada")

        self.abrir_modal(f"Incidencia del remito {fila['nro_remito']}", armar, aceptar, "Registrar incidencia")

    def refrescar(self):
        elegido = self.tabla.selection()
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
        # Se mantiene elegido el remito sobre el que se acaba de operar
        if elegido and self.tabla.exists(elegido[0]):
            self.tabla.selection_set(elegido[0])
        self.cargar_detalle()
