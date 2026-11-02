"""Pestaña de Sedes: alta, modificación, baja y horarios."""

from tkinter import messagebox

# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk

from config import LARGO_NOMBRE_SEDE, LARGO_DIRECCION
from constantes import DiaSemana, PaisTelefono
from dao.sede_dao import SedeDAO, validar_datos_horario
from excepciones import ValidacionError
from ui.base import PestaniaBase, ICONO_EDITAR, ICONO_BAJA, FUENTE_MODAL
from validadores import (validar_nombre_con_numeros, validar_direccion, validar_telefono, validar_email,
                         validar_hora, solo_digitos)

CAMPOS_SEDE = ['nombre', 'direccion', 'prefijo', 'telefono', 'email']
# Horarios que ofrecen los desplegables: cada 30 minutos, de 06:00 a 23:30
HORAS = [f"{hora:02d}:{minuto:02d}" for hora in range(6, 24) for minuto in [0, 30]]


class PestaniaSedes(PestaniaBase):
    TITULO_NUEVO = "Nueva sede"
    TITULO_EDITAR = "Editar sede"

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = SedeDAO()
        self.dias = {}  # día -> {'marcado', 'apertura', 'cierre'} del formulario abierto

        self.crear_encabezado("Sedes", "Bibliotecas de la red, con sus datos de contacto y horarios",
                              [("Nueva sede", self.nuevo, True)])
        self.crear_barra_seleccion("Con la sede elegida:",
                                   [("Volver a dar de alta", self.reactivar)])

        # Tabla a la izquierda; a la derecha, los horarios de la sede elegida
        cuerpo = ttk.Frame(self)
        cuerpo.pack(fill="both", expand=True)
        marco_sedes = self.crear_tabla_principal(cuerpo, [
            ('nombre', "Nombre", 180), ('direccion', "Dirección", 230), ('telefono_completo', "Teléfono", 150),
            ('email', "Email", 190), ('estado', "Estado", 90)],
            doble_clic=self.editar_seleccionado,
            iconos=[(ICONO_EDITAR, self.editar_seleccionado), (ICONO_BAJA, self.dar_de_baja)])
        # El panel se ubica primero, así toma el ancho que necesita y la tabla el resto
        panel = ttk.Frame(cuerpo, padding=(16, 0, 0, 0))
        panel.pack(side="right", anchor="n")
        self.titulo_horarios = ttk.Label(panel, text="Horarios", font=FUENTE_MODAL)
        self.titulo_horarios.pack(anchor="w")
        self.aviso_horarios = ttk.Label(panel, text="Elegí una sede para ver sus días de apertura",
                                        bootstyle="secondary", wraplength=280)
        self.aviso_horarios.pack(anchor="w", pady=(0, 6))
        marco, self.tabla_horarios = self.crear_tabla(panel, [
            ('dia', "Día", 110), ('apertura', "Apertura", 85), ('cierre', "Cierre", 85)], alto=7)
        # Una semana tiene a lo sumo 7 días: la tabla no se estira más que eso
        marco.pack(anchor="w")
        marco_sedes.pack(side="left", fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", lambda evento: self.al_elegir_sede())

        self.refrescar()

    # ------------------------------------------------------------ formulario

    def armar_formulario(self, contenedor):
        datos = ttk.Frame(contenedor)
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
        self.poner('prefijo', PaisTelefono.ARGENTINA)

        # Semana de la sede: se marcan los días que abre y cada uno tiene su horario
        semana = ttk.Frame(contenedor)
        semana.pack(side="left", anchor="n", padx=(24, 0))
        ttk.Label(semana, text="Días de apertura").grid(row=0, column=0, sticky="w", padx=5)
        ttk.Label(semana, text="Apertura").grid(row=0, column=1, sticky="w", padx=5)
        ttk.Label(semana, text="Cierre").grid(row=0, column=2, sticky="w", padx=5)
        self.dias = {}
        # Las horas se eligen de la lista o se escriben (como las fechas): en vivo
        # solo se aceptan dígitos y ":"; el formato completo se revisa al salir
        vcmd = self.register(self.caracteres_de_hora)
        for fila, dia in enumerate(DiaSemana.TODOS, start=1):
            marcado = ttk.Checkbutton(semana, text=dia, command=lambda d=dia: self.cambio_dia(d))
            marcado.grid(row=fila, column=0, sticky="w", padx=5, pady=2)
            apertura = ttk.Combobox(semana, values=HORAS, state="disabled", width=7,
                                    validate="key", validatecommand=(vcmd, "%P"))
            apertura.grid(row=fila, column=1, sticky="w", padx=5, pady=2)
            cierre = ttk.Combobox(semana, values=HORAS, state="disabled", width=7,
                                  validate="key", validatecommand=(vcmd, "%P"))
            cierre.grid(row=fila, column=2, sticky="w", padx=5, pady=2)
            for combo in [apertura, cierre]:
                combo.bind("<<ComboboxSelected>>", lambda evento, d=dia: self.revisar_dia(d))
                combo.bind("<FocusOut>", lambda evento, d=dia: self.revisar_dia(d))
            self.dias[dia] = {'marcado': marcado, 'apertura': apertura, 'cierre': cierre}
        fin = len(DiaSemana.TODOS) + 1
        ttk.Button(semana, text="Mismo horario para todos los días marcados", bootstyle="link",
                   command=self.copiar_horario).grid(row=fin, column=0, columnspan=3, sticky="w", pady=(4, 0))
        # Aviso en rojo debajo de la grilla, como el de los demás campos
        self.error_semana = ttk.Label(semana, text="", bootstyle="danger", wraplength=330)
        self.error_semana.grid(row=fin + 1, column=0, columnspan=3, sticky="w", padx=5)
        self.limpiar_semana()

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

    # ---------------------------------------------------------- acciones

    def dar_de_baja(self):
        self.accion_sobre_seleccion(self.dao.dar_de_baja, "¿Dar de baja la sede seleccionada?",
                                    "Sede dada de baja")

    def reactivar(self):
        self.accion_sobre_seleccion(self.dao.reactivar, "¿Volver a dar de alta la sede seleccionada?",
                                    "Sede activa nuevamente")

    def al_elegir_sede(self):
        self.activar_botones_seleccion()
        self.mostrar_horarios()

    def mostrar_horarios(self):
        seleccion = self.tabla.selection()
        if not seleccion:
            self.titulo_horarios.config(text="Horarios")
            self.aviso_horarios.config(text="Elegí una sede para ver sus días de apertura")
            self.cargar_tabla(self.tabla_horarios, [])
            return
        sede_id = int(seleccion[0])
        self.titulo_horarios.config(text=f"Horarios de {self.buscar_fila(sede_id)['nombre']}")
        self.aviso_horarios.config(text="Para cambiarlos: Editar datos y horarios")
        self.cargar_tabla(self.tabla_horarios, self.dao.listar_horarios(sede_id))

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
        self.mostrar_horarios()

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
                widgets[nombre].config(state="normal")
            else:
                widgets[nombre].set("")
                widgets[nombre].config(state="disabled", values=HORAS)

    def cambio_dia(self, dia):
        self.marcar_dia(dia, self.esta_marcado(dia))

    def caracteres_de_hora(self, nuevo_valor):
        """Validación en vivo de una hora: dígitos y un solo ":", hasta HH:MM.
        Acepta "" para poder borrar; el control estricto es al salir y al guardar."""
        if len(nuevo_valor) > 5 or nuevo_valor.count(":") > 1:
            return False
        return nuevo_valor == "" or solo_digitos(nuevo_valor.replace(":", ""))

    def hora_escrita(self, combo):
        """La hora del campo como "HH:MM", o None si está vacía o mal escrita."""
        try:
            return validar_hora(combo.get(), "hora").strftime("%H:%M")
        except ValidacionError:
            return None

    def acomodar_horas(self, dia):
        """Cada desplegable ofrece solo horas coherentes con el otro: el
        cierre, posteriores a la apertura; la apertura, anteriores al cierre."""
        apertura = self.hora_escrita(self.dias[dia]['apertura'])
        cierre = self.hora_escrita(self.dias[dia]['cierre'])
        # "HH:MM" con ceros adelante se compara bien como texto
        if apertura:
            self.dias[dia]['cierre'].config(values=[hora for hora in HORAS if hora > apertura])
        if cierre:
            self.dias[dia]['apertura'].config(values=[hora for hora in HORAS if hora < cierre])

    def revisar_dia(self, dia):
        """Al elegir o escribir una hora: acomoda las listas y avisa en rojo si
        la hora está mal escrita o si el cierre no es posterior a la apertura
        (lo mismo que valida el DAO al guardar)."""
        self.acomodar_horas(dia)
        apertura = self.dias[dia]['apertura'].get()
        cierre = self.dias[dia]['cierre'].get()
        mensaje = ""
        try:
            if apertura and cierre:
                validar_datos_horario(dia, apertura, cierre)
            elif apertura:
                validar_hora(apertura, f"hora de apertura del {dia}")
            elif cierre:
                validar_hora(cierre, f"hora de cierre del {dia}")
        except ValidacionError as error:
            mensaje = str(error)
        self.error_semana.config(text=mensaje)

    def limpiar_semana(self):
        for dia in DiaSemana.TODOS:
            self.marcar_dia(dia, False)
        self.error_semana.config(text="")

    def horarios_marcados(self):
        """[(día, apertura, cierre)] de los días marcados, para el DAO."""
        return [(dia, self.dias[dia]['apertura'].get(), self.dias[dia]['cierre'].get())
                for dia in DiaSemana.TODOS if self.esta_marcado(dia)]

    def copiar_horario(self):
        """Mismo horario para toda la semana: copia el del primer día marcado
        a los demás días marcados."""
        marcados = [dia for dia in DiaSemana.TODOS if self.esta_marcado(dia)]
        if not marcados:
            messagebox.showwarning("Atención", "Marque los días de apertura", parent=self.ventana_actual())
            return
        modelo = self.dias[marcados[0]]
        for dia in marcados[1:]:
            self.dias[dia]['apertura'].config(values=HORAS)
            self.dias[dia]['cierre'].config(values=HORAS)
            self.dias[dia]['apertura'].set(modelo['apertura'].get())
            self.dias[dia]['cierre'].set(modelo['cierre'].get())
            self.acomodar_horas(dia)
