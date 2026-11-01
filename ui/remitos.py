"""Pestaña de Remitos: armado del envío, cambios de estado, historial e incidencias."""

import tkinter as tk
from datetime import date
from tkinter import ttk

from config import LARGO_OBSERVACION_MOVIMIENTO, LARGO_DESCRIPCION_INCIDENCIA
from constantes import TipoIncidencia
from dao.remito_dao import RemitoDAO
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase
from validadores import validar_texto, validar_texto_opcional, validar_fecha, validar_fecha_no_futura

CAMPOS_INCIDENCIA = ['tipo_incidencia', 'fecha', 'descripcion']


def validar_fecha_incidencia(valor):
    return validar_fecha_no_futura(validar_fecha(valor, "fecha"), "fecha")


class PestaniaRemitos(PestaniaBase):

    def __init__(self, padre, empleado_actual):
        super().__init__(padre, empleado_actual)
        self.dao = RemitoDAO()
        self.prestamos_ids = []     # id de cada renglón del Listbox de préstamos
        self.remito_detalle = None  # remito cuyo historial se está mostrando

        superior = ttk.Frame(self)
        superior.pack(fill="x")

        # --- Nuevo remito de ida
        bloque = ttk.Frame(superior)
        bloque.pack(side="left", anchor="n")
        ttk.Label(bloque, text="NUEVO REMITO DE IDA").pack(anchor="w", padx=5)
        nuevo = ttk.Frame(bloque)
        nuevo.pack(anchor="w")
        self.crear_combo(nuevo, 'sede_origen', "Sede de origen:", 0, SedeDAO().opciones, ancho=25)
        self.crear_combo(nuevo, 'sede_destino', "Sede de destino:", 1, SedeDAO().opciones, ancho=25)
        # Al cambiar las sedes cambian los préstamos que se pueden enviar
        for nombre in ['sede_origen', 'sede_destino']:
            self.campos[nombre]['widget'].bind("<<ComboboxSelected>>", lambda evento: self.recargar_prestamos())
        ttk.Label(nuevo, text="Préstamos aprobados (clic para marcar):").grid(row=4, column=0, columnspan=2,
                                                                             sticky="w", padx=5)
        # Igual que los autores de un libro: Listbox de selección múltiple
        self.lista_prestamos = tk.Listbox(nuevo, selectmode="multiple", height=4, width=60,
                                          exportselection=False)
        self.lista_prestamos.grid(row=5, column=0, columnspan=2, sticky="w", padx=5)
        self.lista_prestamos.bind("<FocusIn>", lambda evento: self.recargar_prestamos())
        ttk.Button(nuevo, text="Crear remito", command=self.crear_remito).grid(row=6, column=0, sticky="w",
                                                                               padx=5, pady=5)

        # --- Incidencia del remito elegido
        bloque = ttk.Frame(superior)
        bloque.pack(side="left", anchor="n", padx=20)
        ttk.Label(bloque, text="INCIDENCIA DEL REMITO ELEGIDO").pack(anchor="w", padx=5)
        incidencia = ttk.Frame(bloque)
        incidencia.pack(anchor="w")
        self.crear_combo(incidencia, 'tipo_incidencia', "Tipo:", 0,
                         lambda: [(tipo, tipo) for tipo in TipoIncidencia.TODOS], ancho=20)
        self.crear_campo_fecha(incidencia, 'fecha', "Fecha (elegir o dd/mm/aaaa):", 1, validar_fecha_incidencia)
        self.crear_campo(incidencia, 'descripcion', "Descripción:", 2,
                         lambda v: validar_texto(v, "descripción", LARGO_DESCRIPCION_INCIDENCIA, 5), ancho=30)
        ttk.Button(incidencia, text="Registrar incidencia", command=self.registrar_incidencia).grid(
            row=6, column=0, sticky="w", padx=5, pady=5)

        # --- Cambios de estado del remito seleccionado
        acciones = ttk.Frame(self)
        acciones.pack(fill="x", pady=5)
        self.crear_campo(acciones, 'observacion', "Observación:", 0,
                         lambda v: validar_texto_opcional(v, "observación", LARGO_OBSERVACION_MOVIMIENTO), ancho=50)
        botones = ttk.Frame(acciones)
        botones.grid(row=0, column=2, sticky="w")
        ttk.Button(botones, text="Avanzar estado", command=self.avanzar).pack(side="left", padx=5)
        ttk.Button(botones, text="Cancelar", command=self.cancelar).pack(side="left", padx=5)
        ttk.Button(botones, text="Dar por extraviado", command=self.extraviar).pack(side="left", padx=5)
        ttk.Label(acciones, text="La observación es obligatoria para cancelar o dar por extraviado.",
                  foreground="gray").grid(row=2, column=1, sticky="w", padx=5)

        marco, self.tabla = self.crear_tabla(self, [
            ('nro_remito', "N° remito", 90), ('tipo', "Tipo", 90), ('origen', "Origen", 110),
            ('destino', "Destino", 110), ('estado', "Estado", 100), ('ejemplares', "Ejemplares", 160),
            ('fecha_creacion', "Creación", 80), ('fecha_despacho', "Despacho", 80),
            ('fecha_recepcion', "Recepción", 80)], alto=6)
        marco.pack(fill="both", expand=True)
        # Al hacer clic en un remito se muestran su historial y sus incidencias
        self.tabla.bind("<ButtonRelease-1>", lambda evento: self.mostrar_detalle())

        # --- Detalle: historial de estados e incidencias
        self.titulo_detalle = ttk.Label(self, text="Historial e incidencias: haga clic en un remito")
        self.titulo_detalle.pack(anchor="w", pady=(10, 0))
        detalle = ttk.Frame(self)
        detalle.pack(fill="x")
        marco, self.tabla_movimientos = self.crear_tabla(detalle, [
            ('fecha_hora', "Fecha y hora", 110), ('estado_anterior', "Anterior", 100),
            ('estado_nuevo', "Nuevo", 100), ('empleado', "Empleado", 150), ('observacion', "Observación", 180)],
            alto=5)
        marco.pack(side="left", fill="x", expand=True)
        marco, self.tabla_incidencias = self.crear_tabla(detalle, [
            ('tipo', "Tipo", 80), ('fecha', "Fecha", 80), ('descripcion', "Descripción", 200)], alto=5)
        marco.pack(side="left", fill="x", padx=(10, 0))

        self.refrescar()

    # ------------------------------------------------------- nuevo remito

    def recargar_prestamos(self):
        self.lista_prestamos.delete(0, tk.END)
        self.prestamos_ids = []
        for id, texto in self.dao.prestamos_para_enviar(self.valor('sede_origen'), self.valor('sede_destino')):
            self.lista_prestamos.insert(tk.END, texto)
            self.prestamos_ids.append(id)

    def prestamos_seleccionados(self):
        return [self.prestamos_ids[indice] for indice in self.lista_prestamos.curselection()]

    def crear_remito(self):
        if not self.hay_empleado() or not self.validar_campos(['sede_origen', 'sede_destino']):
            return
        if self.ejecutar(lambda: self.dao.crear_ida(self.valor('sede_origen'), self.valor('sede_destino'),
                                                    self.prestamos_seleccionados(), self.empleado_actual()),
                         "Remito creado: quedó EMPAQUETADO y sus préstamos EN_ENVIO"):
            self.recargar_prestamos()

    # --------------------------------------------------- cambios de estado

    def accion_con_observacion(self, accion, pregunta, mensaje_ok):
        """accion(id, empleado, observacion) sobre el remito seleccionado."""
        if not self.hay_empleado() or not self.validar_campos(['observacion']):
            return
        observacion = self.valor('observacion')
        self.accion_sobre_seleccion(lambda id: accion(id, self.empleado_actual(), observacion),
                                    pregunta, mensaje_ok)

    def avanzar(self):
        self.accion_con_observacion(self.dao.avanzar, "¿Pasar el remito seleccionado a su estado siguiente?",
                                    "Estado del remito actualizado")

    def cancelar(self):
        self.accion_con_observacion(self.dao.cancelar, "¿Cancelar el remito seleccionado?",
                                    "Remito cancelado: sus ejemplares volvieron a estar disponibles")

    def extraviar(self):
        self.accion_con_observacion(self.dao.extraviar, "¿Dar por extraviado el remito seleccionado?",
                                    "Remito extraviado: se registró la incidencia")

    # ------------------------------------------------- detalle e incidencias

    def mostrar_detalle(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        self.remito_detalle = int(seleccion[0])
        self.cargar_detalle()

    def cargar_detalle(self):
        fila = self.buscar_fila(self.remito_detalle)
        if fila is None:
            return
        self.titulo_detalle.config(text=f"Historial e incidencias del remito {fila['nro_remito']}")
        self.cargar_tabla(self.tabla_movimientos, self.dao.listar_movimientos(self.remito_detalle))
        self.cargar_tabla(self.tabla_incidencias, self.dao.listar_incidencias(self.remito_detalle))

    def registrar_incidencia(self):
        if not self.hay_empleado():
            return
        if self.remito_detalle is None:
            self.id_seleccionado(self.tabla, "Haga clic en el remito al que corresponde la incidencia")
            return
        if not self.validar_campos(CAMPOS_INCIDENCIA):
            return
        if self.ejecutar(lambda: self.dao.registrar_incidencia(self.remito_detalle, self.valor('tipo_incidencia'),
                                                               self.valor('fecha'), self.valor('descripcion')),
                         "Incidencia registrada"):
            self.limpiar_campos(CAMPOS_INCIDENCIA)
            self.poner('fecha', date.today().strftime("%d/%m/%Y"))

    # ---------------------------------------------------------------- comunes

    def limpiar(self):
        # Después de un cambio de estado se borra la observación usada
        self.limpiar_campos(['observacion'])
        self.tabla.selection_remove(self.tabla.selection())

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
        self.recargar_prestamos()
        if self.remito_detalle is not None:
            self.cargar_detalle()
