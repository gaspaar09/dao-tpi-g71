"""Pestaña de Sedes: alta, modificación, baja y horarios."""

from tkinter import ttk

from config import LARGO_NOMBRE_SEDE, LARGO_DIRECCION
from constantes import DiaSemana, PaisTelefono
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase
from validadores import validar_nombre_con_numeros, validar_direccion, validar_telefono, validar_email, validar_hora

CAMPOS_SEDE = ['nombre', 'direccion', 'prefijo', 'telefono', 'email']
CAMPOS_HORARIO = ['dia', 'apertura', 'cierre']


class PestaniaSedes(PestaniaBase):

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = SedeDAO()
        self.sede_horarios = None  # sede cuyos horarios se están mostrando

        formulario = ttk.Frame(self)
        formulario.pack(fill="x")
        datos = ttk.Frame(formulario)
        datos.pack(side="left", anchor="n")
        self.crear_campo(datos, 'nombre', "Nombre:", 0,
                         lambda v: validar_nombre_con_numeros(v, "nombre", 2, LARGO_NOMBRE_SEDE))
        self.crear_campo(datos, 'direccion', "Dirección:", 1,
                         lambda v: validar_direccion(v, "dirección", LARGO_DIRECCION))
        # El código de país no se escribe: se elige el país y el número va sin "+"
        self.crear_combo(datos, 'prefijo', "País (teléfono):", 2,
                         lambda: [(codigo, f"{pais} (+{codigo})") for pais, codigo in PaisTelefono.PAISES])
        self.crear_campo(datos, 'telefono', "Teléfono (solo números):", 3, validar_telefono, numerico=True)
        self.crear_campo(datos, 'email', "Email (opcional):", 4,
                         lambda v: validar_email(v, obligatorio=False))

        # El horario sirve para el alta (la sede nace con uno) y para agregar más
        horario = ttk.Frame(formulario)
        horario.pack(side="left", anchor="n", padx=20)
        ttk.Label(horario, text="Horario (al dar de alta o para agregar)").grid(row=0, column=0, columnspan=2,
                                                                                 sticky="w", padx=5)
        marco_campos = ttk.Frame(horario)
        marco_campos.grid(row=1, column=0, columnspan=2, sticky="w")
        self.crear_combo(marco_campos, 'dia', "Día:", 0,
                         lambda: [(dia, dia) for dia in DiaSemana.TODOS], ancho=15)
        self.crear_campo(marco_campos, 'apertura', "Apertura (HH:MM):", 1,
                         lambda v: validar_hora(v, "hora de apertura"), ancho=10)
        self.crear_campo(marco_campos, 'cierre', "Cierre (HH:MM):", 2,
                         lambda v: validar_hora(v, "hora de cierre"), ancho=10)

        self.crear_botones(self, [("Dar de baja", self.dar_de_baja),
                                  ("Volver a dar de alta", self.reactivar)]).pack(anchor="w", pady=10)

        marco, self.tabla = self.crear_tabla(self, [
            ('nombre', "Nombre", 180), ('direccion', "Dirección", 220), ('telefono_completo', "Teléfono", 140),
            ('email', "Email", 180), ('estado', "Estado", 80)], alto=7)
        marco.pack(fill="both", expand=True)
        # Al hacer clic en una sede se muestran sus horarios abajo
        self.tabla.bind("<ButtonRelease-1>", lambda evento: self.mostrar_horarios())

        self.titulo_horarios = ttk.Label(self, text="Horarios: haga clic en una sede")
        self.titulo_horarios.pack(anchor="w", pady=(10, 0))
        marco, self.tabla_horarios = self.crear_tabla(self, [
            ('dia', "Día", 120), ('apertura', "Apertura", 100), ('cierre', "Cierre", 100)], alto=5)
        marco.pack(fill="x")
        botones = ttk.Frame(self)
        botones.pack(anchor="w", pady=5)
        ttk.Button(botones, text="Agregar horario a la sede", command=self.agregar_horario).pack(side="left", padx=5)
        ttk.Button(botones, text="Quitar horario seleccionado", command=self.quitar_horario).pack(side="left", padx=5)

        self.poner('prefijo', PaisTelefono.ARGENTINA)
        self.refrescar()

    def campos_formulario(self):
        # En el alta se pide el primer horario; al modificar, solo los datos de la sede
        if self.id_editando is None:
            return CAMPOS_SEDE + CAMPOS_HORARIO
        return CAMPOS_SEDE

    def crear(self):
        self.dao.crear(self.valor('nombre'), self.valor('direccion'), self.valor('prefijo'), self.valor('telefono'),
                       self.valor('email'), self.valor('dia'), self.valor('apertura'), self.valor('cierre'))

    def modificar(self, id):
        self.dao.modificar(id, self.valor('nombre'), self.valor('direccion'), self.valor('prefijo'), self.valor('telefono'),
                           self.valor('email'))

    def cargar_formulario(self, fila):
        for nombre in CAMPOS_SEDE:
            self.poner(nombre, fila[nombre])

    def limpiar(self):
        super().limpiar()
        self.limpiar_campos(CAMPOS_HORARIO)
        self.poner('prefijo', PaisTelefono.ARGENTINA)

    def dar_de_baja(self):
        self.accion_sobre_seleccion(self.dao.dar_de_baja, "¿Dar de baja la sede seleccionada?",
                                    "Sede dada de baja")

    def reactivar(self):
        self.accion_sobre_seleccion(self.dao.reactivar, "¿Volver a dar de alta la sede seleccionada?",
                                    "Sede activa nuevamente")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
        if self.sede_horarios is not None:
            self.cargar_tabla(self.tabla_horarios, self.dao.listar_horarios(self.sede_horarios))

    # ---------------------------------------------------------- horarios

    def mostrar_horarios(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        self.sede_horarios = int(seleccion[0])
        self.titulo_horarios.config(text=f"Horarios de {self.buscar_fila(self.sede_horarios)['nombre']}")
        self.cargar_tabla(self.tabla_horarios, self.dao.listar_horarios(self.sede_horarios))

    def agregar_horario(self):
        if self.sede_horarios is None:
            self.id_seleccionado(self.tabla, "Haga clic en la sede a la que quiere agregar el horario")
            return
        if not self.validar_campos(CAMPOS_HORARIO):
            return
        if self.ejecutar(lambda: self.dao.agregar_horario(self.sede_horarios, self.valor('dia'),
                                                          self.valor('apertura'), self.valor('cierre')),
                         "Horario agregado"):
            self.limpiar_campos(CAMPOS_HORARIO)

    def quitar_horario(self):
        id = self.id_seleccionado(self.tabla_horarios, "Seleccione el horario a quitar")
        if id is not None:
            self.ejecutar(lambda: self.dao.quitar_horario(id), "Horario quitado")
