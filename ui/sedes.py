"""Pestaña de Sedes: alta, modificación, baja y horarios."""

from tkinter import ttk, messagebox

from config import LARGO_NOMBRE_SEDE, LARGO_DIRECCION
from constantes import DiaSemana, PaisTelefono
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase
from validadores import validar_nombre_con_numeros, validar_direccion, validar_telefono, validar_email

CAMPOS_SEDE = ['nombre', 'direccion', 'prefijo', 'telefono', 'email']
# Horarios que ofrecen los desplegables: cada 30 minutos, de 06:00 a 23:30
HORAS = [f"{hora:02d}:{minuto:02d}" for hora in range(6, 24) for minuto in [0, 30]]


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

        # Semana de la sede: se marcan los días que abre y cada uno tiene su horario
        semana = ttk.Frame(formulario)
        semana.pack(side="left", anchor="n", padx=20)
        ttk.Label(semana, text="Días y horarios de apertura").grid(row=0, column=0, columnspan=3, sticky="w", padx=5)
        ttk.Label(semana, text="Apertura").grid(row=1, column=1, sticky="w", padx=5)
        ttk.Label(semana, text="Cierre").grid(row=1, column=2, sticky="w", padx=5)
        # día -> {'marcado': Checkbutton, 'apertura': Combobox, 'cierre': Combobox}
        self.dias = {}
        for fila, dia in enumerate(DiaSemana.TODOS, start=2):
            marcado = ttk.Checkbutton(semana, text=dia, command=lambda d=dia: self.cambio_dia(d))
            marcado.grid(row=fila, column=0, sticky="w", padx=5, pady=2)
            apertura = ttk.Combobox(semana, values=HORAS, state="disabled", width=7)
            apertura.grid(row=fila, column=1, sticky="w", padx=5, pady=2)
            cierre = ttk.Combobox(semana, values=HORAS, state="disabled", width=7)
            cierre.grid(row=fila, column=2, sticky="w", padx=5, pady=2)
            apertura.bind("<<ComboboxSelected>>", lambda evento, d=dia: self.acomodar_horas(d))
            cierre.bind("<<ComboboxSelected>>", lambda evento, d=dia: self.acomodar_horas(d))
            self.dias[dia] = {'marcado': marcado, 'apertura': apertura, 'cierre': cierre}
        ttk.Button(semana, text="Copiar el horario del primer día marcado a los demás",
                   command=self.copiar_horario).grid(row=len(DiaSemana.TODOS) + 2, column=0, columnspan=3,
                                                     sticky="w", padx=5, pady=5)
        self.limpiar_semana()

        self.crear_botones(self, [("Dar de baja", self.dar_de_baja),
                                  ("Volver a dar de alta", self.reactivar)]).pack(anchor="w", pady=10)

        marco, self.tabla = self.crear_tabla(self, [
            ('nombre', "Nombre", 180), ('direccion', "Dirección", 220), ('telefono_completo', "Teléfono", 140),
            ('email', "Email", 180), ('estado', "Estado", 80)], alto=7)
        marco.pack(fill="both", expand=True)
        # Al hacer clic en una sede se muestran sus horarios abajo
        self.tabla.bind("<ButtonRelease-1>", lambda evento: self.mostrar_horarios())

        self.titulo_horarios = ttk.Label(self, text="Horarios: haga clic en una sede (para cambiarlos, Editar seleccionado)")
        self.titulo_horarios.pack(anchor="w", pady=(10, 0))
        marco, self.tabla_horarios = self.crear_tabla(self, [
            ('dia', "Día", 120), ('apertura', "Apertura", 100), ('cierre', "Cierre", 100)], alto=5)
        marco.pack(fill="x")

        self.poner('prefijo', PaisTelefono.ARGENTINA)
        self.refrescar()

    def campos_formulario(self):
        return CAMPOS_SEDE

    def crear(self):
        self.dao.crear(self.valor('nombre'), self.valor('direccion'), self.valor('prefijo'), self.valor('telefono'),
                       self.valor('email'), self.horarios_marcados())

    def modificar(self, id):
        self.dao.modificar(id, self.valor('nombre'), self.valor('direccion'), self.valor('prefijo'), self.valor('telefono'),
                           self.valor('email'), self.horarios_marcados())

    def cargar_formulario(self, fila):
        for nombre in CAMPOS_SEDE:
            self.poner(nombre, fila[nombre])
        for horario in self.dao.listar_horarios(fila['id']):
            self.marcar_dia(horario['dia'], True)
            self.dias[horario['dia']]['apertura'].set(horario['apertura'])
            self.dias[horario['dia']]['cierre'].set(horario['cierre'])
            self.acomodar_horas(horario['dia'])

    def limpiar(self):
        super().limpiar()
        self.limpiar_semana()
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

    def esta_marcado(self, dia):
        return self.dias[dia]['marcado'].instate(['selected'])

    def marcar_dia(self, dia, marcado):
        """Marca o desmarca el día. Los horarios de un día sin marcar no se
        pueden elegir (la sede no abre ese día)."""
        widgets = self.dias[dia]
        # Sin variable asociada, el Checkbutton nace "a medias" (alternate): se limpia
        widgets['marcado'].state(['!alternate', 'selected' if marcado else '!selected'])
        for nombre in ['apertura', 'cierre']:
            if marcado:
                widgets[nombre].config(state="readonly")
            else:
                widgets[nombre].set("")
                widgets[nombre].config(state="disabled", values=HORAS)

    def cambio_dia(self, dia):
        self.marcar_dia(dia, self.esta_marcado(dia))

    def acomodar_horas(self, dia):
        """Cada desplegable ofrece solo horas coherentes con el otro: el
        cierre, posteriores a la apertura; la apertura, anteriores al cierre.
        Así no se puede elegir un cierre anterior a la apertura ni al revés."""
        apertura = self.dias[dia]['apertura']
        cierre = self.dias[dia]['cierre']
        # "HH:MM" con ceros adelante se compara bien como texto
        if apertura.get():
            cierre.config(values=[hora for hora in HORAS if hora > apertura.get()])
        if cierre.get():
            apertura.config(values=[hora for hora in HORAS if hora < cierre.get()])

    def limpiar_semana(self):
        for dia in DiaSemana.TODOS:
            self.marcar_dia(dia, False)

    def horarios_marcados(self):
        """[(día, apertura, cierre)] de los días marcados, para el DAO."""
        return [(dia, self.dias[dia]['apertura'].get(), self.dias[dia]['cierre'].get())
                for dia in DiaSemana.TODOS if self.esta_marcado(dia)]

    def copiar_horario(self):
        """Mismo horario para toda la semana: copia el del primer día marcado
        a los demás días marcados."""
        marcados = [dia for dia in DiaSemana.TODOS if self.esta_marcado(dia)]
        if not marcados:
            messagebox.showwarning("Atención", "Marque los días de apertura")
            return
        modelo = self.dias[marcados[0]]
        for dia in marcados[1:]:
            self.dias[dia]['apertura'].config(values=HORAS)
            self.dias[dia]['cierre'].config(values=HORAS)
            self.dias[dia]['apertura'].set(modelo['apertura'].get())
            self.dias[dia]['cierre'].set(modelo['cierre'].get())
            self.acomodar_horas(dia)

    def mostrar_horarios(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            return
        self.sede_horarios = int(seleccion[0])
        self.titulo_horarios.config(text=f"Horarios de {self.buscar_fila(self.sede_horarios)['nombre']}")
        self.cargar_tabla(self.tabla_horarios, self.dao.listar_horarios(self.sede_horarios))
