"""Clase base de las pestañas: todo lo que se repite entre formularios.

Cada pestaña hereda de PestaniaBase y solo define sus campos y qué DAO
llama. Así el armado de campos, el mensaje de error en rojo, las tablas y
el manejo de errores se escriben una sola vez (herencia, vista en clase).

Todas las pestañas se ordenan igual, de arriba hacia abajo:
1. Encabezado: título, para qué sirve la pantalla y la acción principal
   ("Nuevo socio") a la derecha.
2. Barra de acciones sobre la fila elegida en la tabla. Sus botones están
   desactivados hasta que se elige una fila; las acciones que quitan o
   bloquean algo van aparte, a la derecha y en rojo.
3. La tabla, que ocupa el resto de la pantalla.
Los formularios (alta, edición, devolución...) se abren en una ventana
modal, con los botones Cancelar y Guardar al pie.
"""

import tkinter as tk
import tkinter.font as tkfont
from datetime import date, timedelta
from tkinter import messagebox

# Los widgets ttk se toman de ttkbootstrap: son los mismos, con los temas modernos
import ttkbootstrap as ttk

from excepciones import ValidacionError, ReglaNegocioError
from validadores import solo_digitos

# Margen a la izquierda de cada celda y de cada título (ttk no tiene padding por celda)
MARGEN = "  "
FUENTE_TITULO = ("Segoe UI", 17, "bold")
FUENTE_MODAL = ("Segoe UI", 14, "bold")
# Espacio extra de cada columna además del texto más largo
RELLENO_COLUMNA = 20
# Íconos de la columna Acciones de los ABM, y el espacio entre uno y otro
ICONO_EDITAR = "✏"
ICONO_BAJA = "🗑"
SEPARACION_ICONOS = "     "


def aplicar_estilo_tablas():
    """Bordes, filas más altas y franjas alternadas en todas las tablas.
    ttk no dibuja líneas entre celdas: las franjas separan las filas. Los
    colores salen del tema, por eso se vuelve a llamar al cambiar de tema."""
    estilo = ttk.Style()
    colores = estilo.colors
    estilo.configure("Treeview", rowheight=32, borderwidth=1, relief="solid", bordercolor=colores.border)
    estilo.configure("Treeview.Heading", padding=(0, 8), borderwidth=1, relief="solid",
                     bordercolor=colores.border)
    # Franja: el fondo un poco más oscuro (tema claro) o más claro (tema oscuro)
    cambio = 0.06 if estilo.theme_mode == "dark" else -0.04
    franja = colores.update_hsv(colores.bg, vd=cambio)
    # Reportes vuelve a crear su tabla: las que ya se destruyeron se descartan
    PestaniaBase.tablas = [tabla for tabla in PestaniaBase.tablas if tabla.winfo_exists()]
    for tabla in PestaniaBase.tablas:
        tabla.tag_configure("franja", background=franja)


class PestaniaBase(ttk.Frame):
    # Todas las tablas creadas, para volver a pintar las franjas al cambiar de tema
    tablas = []

    def __init__(self, padre, empleado_actual=None):
        """empleado_actual es una función que devuelve el id del empleado
        elegido arriba de la ventana (o None). La reciben solo las pestañas
        cuyas operaciones quedan registradas a nombre de un empleado."""
        super().__init__(padre, padding=(16, 12))
        self.empleado_actual = empleado_actual
        # nombre -> {'widget', 'error', 'validador', 'etiqueta'}
        self.campos = {}
        # nombre del combo -> {texto mostrado: id}
        self.opciones_combo = {}
        self.filas = []            # última lista que devolvió el DAO
        self.id_editando = None    # None = alta; un id = modificación
        self.modal = None          # ventana del formulario abierto, si hay una
        # Botones que actúan sobre la fila elegida: se activan al elegir una
        self.botones_seleccion = []
        self.acciones_generales = []  # las de crear_encabezado
        # Función que refresca todas las pestañas (la asigna main.py). Una
        # operación puede cambiar datos que muestra otra pestaña: por ejemplo,
        # aprobar un préstamo cambia el estado del ejemplar.
        self.refrescar_todo = None

    # ---------------------------------------------------- estructura común

    def crear_encabezado(self, titulo, descripcion, acciones=None):
        """Título y descripción. acciones = [(texto, comando, principal)] son
        las que no dependen de una fila ("Nuevo socio"): se guardan para que
        crear_barra_seleccion las ponga a la izquierda de la barra."""
        encabezado = ttk.Frame(self)
        encabezado.pack(fill="x", pady=(0, 10))
        textos = ttk.Frame(encabezado)
        textos.pack(side="left")
        ttk.Label(textos, text=titulo, font=FUENTE_TITULO).pack(anchor="w")
        ttk.Label(textos, text=descripcion, bootstyle="secondary").pack(anchor="w")
        self.acciones_generales = acciones or []
        return encabezado

    def crear_barra_seleccion(self, texto, acciones, destructivas=None):
        """Barra de botones: primero las acciones generales del encabezado
        (la principal en color); después, las acciones sobre la fila elegida.
        acciones y destructivas son [(texto, comando)]; las destructivas van
        a la derecha, en rojo. La última destructiva queda a la derecha de
        todo; con una tercera parte True va en rojo lleno (Cancelar)."""
        barra = ttk.Frame(self)
        barra.pack(fill="x", pady=(0, 8))
        destructivas = destructivas or []
        # La principal primero, a la izquierda de todo
        generales = sorted(self.acciones_generales, key=lambda accion: not accion[2])
        for texto_boton, comando, principal in generales:
            ttk.Button(barra, text=texto_boton, bootstyle="primary" if principal else "primary-outline",
                       command=comando).pack(side="left", padx=(0, 6))
        # En los ABM editar y dar de baja están en cada fila: puede no quedar
        # ninguna acción sobre la fila elegida, y entonces no se muestra el texto
        if not acciones and not destructivas:
            return barra
        if generales:
            ttk.Separator(barra, orient="vertical").pack(side="left", fill="y", padx=(8, 14))
        ttk.Label(barra, text=texto, bootstyle="secondary").pack(side="left", padx=(0, 8))
        for texto_boton, comando in acciones:
            boton = ttk.Button(barra, text=texto_boton, bootstyle="secondary-outline", command=comando)
            boton.pack(side="left", padx=(0, 6))
            self.botones_seleccion.append(boton)
        for destructiva in reversed(destructivas):
            texto_boton, comando = destructiva[0], destructiva[1]
            lleno = len(destructiva) > 2 and destructiva[2]
            boton = ttk.Button(barra, text=texto_boton, bootstyle="danger" if lleno else "danger-outline",
                               command=comando)
            boton.pack(side="right", padx=(6, 0))
            self.botones_seleccion.append(boton)
        return barra

    def activar_botones_seleccion(self):
        """Los botones de la barra solo se pueden usar con una fila elegida."""
        estado = "normal" if self.tabla.selection() else "disabled"
        for boton in self.botones_seleccion:
            boton.config(state=estado)

    # ------------------------------------------------------------ modales

    def abrir_modal(self, titulo, armar, aceptar, texto_aceptar="Guardar"):
        """Ventana modal con un formulario: armar(cuerpo) crea los campos y
        aceptar() devuelve True si la operación salió bien (entonces se
        cierra). Mientras está abierta no se puede usar el resto de la app."""
        self.cerrar_modal()
        principal = self.winfo_toplevel()
        modal = ttk.Toplevel(title=titulo, transient=principal, resizable=(False, False))
        self.modal = modal
        cuerpo = ttk.Frame(modal, padding=(24, 20, 24, 8))
        cuerpo.pack(fill="both", expand=True)
        ttk.Label(cuerpo, text=titulo, font=FUENTE_MODAL).grid(row=0, column=0, columnspan=3, sticky="w",
                                                               pady=(0, 12))
        campos = ttk.Frame(cuerpo)
        campos.grid(row=1, column=0, columnspan=3, sticky="nsew")
        armar(campos)
        # Pie: Cancelar y la acción, abajo a la derecha como en todo diálogo
        ttk.Separator(modal).pack(fill="x")
        pie = ttk.Frame(modal, padding=(24, 12))
        pie.pack(fill="x")
        ttk.Button(pie, text=texto_aceptar, bootstyle="primary",
                   command=lambda: self.aceptar_modal(aceptar)).pack(side="right")
        ttk.Button(pie, text="Cancelar", bootstyle="secondary-outline",
                   command=self.cerrar_modal).pack(side="right", padx=(0, 8))
        modal.bind("<Escape>", lambda evento: self.cerrar_modal())
        modal.protocol("WM_DELETE_WINDOW", self.cerrar_modal)
        # Centrada sobre la ventana principal
        modal.update_idletasks()
        x = principal.winfo_rootx() + (principal.winfo_width() - modal.winfo_reqwidth()) // 2
        y = principal.winfo_rooty() + (principal.winfo_height() - modal.winfo_reqheight()) // 3
        modal.geometry(f"+{max(x, 0)}+{max(y, 0)}")
        modal.grab_set()
        return modal

    def aceptar_modal(self, aceptar):
        if aceptar():
            self.cerrar_modal()

    def cerrar_modal(self):
        if self.modal is not None and self.modal.winfo_exists():
            self.modal.grab_release()
            self.modal.destroy()
        self.modal = None

    def ayuda(self, contenedor, texto, fila):
        """Texto de ayuda en gris debajo de los campos del formulario."""
        ttk.Label(contenedor, text=texto, bootstyle="secondary", wraplength=420, justify="left").grid(
            row=fila * 2, column=1, sticky="w", padx=5, pady=(4, 0))

    # ------------------------------------------------------------ campos

    def solo_numeros(self, nuevo_valor):
        """Validación en vivo (validate="key"). Acepta "" para que el
        usuario pueda borrar el campo; el control estricto es al guardar."""
        return nuevo_valor == "" or solo_digitos(nuevo_valor)

    def crear_campo(self, contenedor, nombre, etiqueta, fila, validador=None, numerico=False, ancho=35):
        """Etiqueta + Entry + mensaje de error en rojo debajo del campo."""
        ttk.Label(contenedor, text=etiqueta).grid(row=fila * 2, column=0, sticky="w", padx=5, pady=(5, 0))
        entry = ttk.Entry(contenedor, width=ancho)
        entry.grid(row=fila * 2, column=1, sticky="w", padx=5, pady=(5, 0))
        if numerico:
            vcmd = self.register(self.solo_numeros)
            entry.config(validate="key", validatecommand=(vcmd, "%P"))
        error = ttk.Label(contenedor, text="", bootstyle="danger")
        error.grid(row=fila * 2 + 1, column=1, sticky="w", padx=5)
        self.campos[nombre] = {'widget': entry, 'error': error, 'validador': validador, 'etiqueta': etiqueta}
        # Al salir del campo se avisa el error sin esperar a guardar
        entry.bind("<FocusOut>", lambda evento: self.validar_campo(nombre))
        return entry

    def caracteres_de_fecha(self, nuevo_valor):
        """Validación en vivo de una fecha: solo dígitos y "/", hasta dd/mm/aaaa.
        Acepta "" para poder borrar; el control estricto es al guardar."""
        if len(nuevo_valor) > 10:
            return False
        return nuevo_valor == "" or solo_digitos(nuevo_valor.replace("/", ""))

    def crear_campo_fecha(self, contenedor, nombre, etiqueta, fila, validador, dias=30):
        """Fecha que se elige o se escribe: un Combobox sin state="readonly"
        se despliega con hoy y los días anteriores, y también acepta texto
        dd/mm/aaaa. Para el resto del formulario es un campo de texto más."""
        ttk.Label(contenedor, text=etiqueta).grid(row=fila * 2, column=0, sticky="w", padx=5, pady=(5, 0))
        fechas = [(date.today() - timedelta(days=atras)).strftime("%d/%m/%Y") for atras in range(dias + 1)]
        combo = ttk.Combobox(contenedor, values=fechas, width=12)
        combo.grid(row=fila * 2, column=1, sticky="w", padx=5, pady=(5, 0))
        vcmd = self.register(self.caracteres_de_fecha)
        combo.config(validate="key", validatecommand=(vcmd, "%P"))
        combo.set(fechas[0])  # por defecto, hoy
        error = ttk.Label(contenedor, text="", bootstyle="danger")
        error.grid(row=fila * 2 + 1, column=1, sticky="w", padx=5)
        self.campos[nombre] = {'widget': combo, 'error': error, 'validador': validador, 'etiqueta': etiqueta}
        combo.bind("<FocusOut>", lambda evento: self.validar_campo(nombre))
        # Al elegir una fecha de la lista se borra el error que hubiera
        combo.bind("<<ComboboxSelected>>", lambda evento: self.validar_campo(nombre))
        return combo

    def crear_combo(self, contenedor, nombre, etiqueta, fila, cargar_opciones, ancho=33):
        """Combobox de solo lectura. cargar_opciones devuelve [(id, texto)].
        Se recarga al entrar al campo, así aparecen los datos dados de alta
        en otra pestaña."""
        ttk.Label(contenedor, text=etiqueta).grid(row=fila * 2, column=0, sticky="w", padx=5, pady=(5, 0))
        combo = ttk.Combobox(contenedor, state="readonly", width=ancho)
        combo.grid(row=fila * 2, column=1, sticky="w", padx=5, pady=(5, 0))
        error = ttk.Label(contenedor, text="", bootstyle="danger")
        error.grid(row=fila * 2 + 1, column=1, sticky="w", padx=5)
        self.campos[nombre] = {'widget': combo, 'error': error, 'validador': None, 'etiqueta': etiqueta,
                               'cargar': cargar_opciones}
        self.recargar_combo(nombre)
        combo.bind("<FocusIn>", lambda evento: self.recargar_combo(nombre))
        return combo

    def recargar_combo(self, nombre):
        combo = self.campos[nombre]['widget']
        self.opciones_combo[nombre] = {}
        for id, texto in self.campos[nombre]['cargar']():
            self.opciones_combo[nombre][texto] = id
        combo.config(values=list(self.opciones_combo[nombre].keys()))
        # Si la opción elegida ya no existe (por ejemplo, sede dada de baja), se borra
        if combo.get() not in self.opciones_combo[nombre]:
            combo.set("")

    def es_combo(self, nombre):
        return nombre in self.opciones_combo

    def valor(self, nombre):
        """Texto de un Entry, o id de la opción elegida en un Combobox."""
        texto = self.campos[nombre]['widget'].get()
        if self.es_combo(nombre):
            if texto in self.opciones_combo[nombre]:
                return self.opciones_combo[nombre][texto]
            return None
        return texto

    def poner(self, nombre, valor):
        """Carga un valor en el campo (para modificar un registro)."""
        widget = self.campos[nombre]['widget']
        if self.es_combo(nombre):
            self.recargar_combo(nombre)
            widget.set("")
            for texto, id in self.opciones_combo[nombre].items():
                if id == valor:
                    widget.set(texto)
        else:
            widget.delete(0, tk.END)
            widget.insert(0, str(valor))

    # -------------------------------------------------------- validación

    def validar_campo(self, nombre):
        """Valida un campo y muestra el error en rojo. Devuelve el mensaje o None."""
        campo = self.campos[nombre]
        mensaje = None
        if self.es_combo(nombre):
            if campo['widget'].get() == "":
                mensaje = f"Seleccione {campo['etiqueta'].lower().rstrip(':')}"
        elif campo['validador'] is not None:
            try:
                campo['validador'](campo['widget'].get())
            except ValidacionError as error:
                mensaje = str(error)
        campo['error'].config(text=mensaje or "")
        return mensaje

    def validar_campos(self, nombres):
        """Valida los campos indicados y muestra la lista de errores en un
        cuadro de diálogo. Devuelve True si está todo bien."""
        errores = []
        for nombre in nombres:
            mensaje = self.validar_campo(nombre)
            if mensaje:
                errores.append("- " + mensaje)
        if errores:
            messagebox.showerror("Revise los datos", "\n".join(errores), parent=self.ventana_actual())
            return False
        return True

    def ventana_actual(self):
        """Los cuadros de diálogo se muestran sobre el modal si hay uno abierto."""
        if self.modal is not None and self.modal.winfo_exists():
            return self.modal
        return self.winfo_toplevel()

    # ------------------------------------------------------------ tablas

    def crear_tabla(self, contenedor, columnas, alto=10):
        """Treeview con barras de desplazamiento vertical y horizontal (las
        tablas con muchas columnas pueden ser más anchas que la ventana).
        columnas = [(clave, título, ancho)]."""
        marco = ttk.Frame(contenedor)
        tabla = ttk.Treeview(marco, columns=[c[0] for c in columnas], show="headings", height=alto)
        for clave, titulo, ancho in columnas:
            # Título y celdas alineados a la izquierda, con el mismo margen.
            # Las columnas mantienen su ancho (si no entran, aparece la barra);
            # solo la última se estira para ocupar el espacio que sobre
            tabla.heading(clave, text=MARGEN + titulo, anchor="w")
            tabla.column(clave, width=ancho, minwidth=40, anchor="w", stretch=clave == columnas[-1][0])
        vertical = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        horizontal = ttk.Scrollbar(marco, orient="horizontal", command=tabla.xview)
        tabla.config(yscrollcommand=vertical.set, xscrollcommand=horizontal.set)
        tabla.grid(row=0, column=0, sticky="nsew")
        vertical.grid(row=0, column=1, sticky="ns")
        horizontal.grid(row=1, column=0, sticky="ew")
        marco.rowconfigure(0, weight=1)
        marco.columnconfigure(0, weight=1)
        tabla.columnas = [c[0] for c in columnas]
        tabla.titulos = {c[0]: c[1] for c in columnas}
        tabla.iconos = []  # [(ícono, comando[, condicion])] de la columna Acciones, si la tiene
        PestaniaBase.tablas.append(tabla)
        aplicar_estilo_tablas()
        self.ajustar_columnas(tabla, [])
        return marco, tabla

    def ajustar_columnas(self, tabla, filas):
        """Cada columna toma el ancho de su texto más largo, sea el título o
        alguna celda. measure() da el ancho en píxeles de un texto."""
        fuente = tkfont.nametofont("TkDefaultFont")
        fuente_titulo = tkfont.nametofont("TkHeadingFont")
        for clave in tabla.columnas:
            ancho = fuente_titulo.measure(MARGEN + tabla.titulos[clave])
            for fila in filas:
                ancho = max(ancho, fuente.measure(MARGEN + self.texto_celda(tabla, fila, clave)))
            # minwidth: la última columna se estira, pero nunca queda más angosta que su texto
            tabla.column(clave, width=ancho + RELLENO_COLUMNA, minwidth=ancho + RELLENO_COLUMNA)
        # Volver a indicar las columnas visibles hace que la tabla pida su nuevo ancho
        tabla.configure(displaycolumns=tabla.columnas)

    def crear_tabla_principal(self, contenedor, columnas, alto=10, doble_clic=None, iconos=None):
        """La tabla de la pestaña: al elegir una fila se activan los botones
        de la barra de selección; doble_clic es la acción del doble clic
        sobre una fila (por ejemplo, editarla). iconos = [(ícono, comando)]
        agrega al final la columna Acciones: un clic en un ícono elige
        esa fila y llama a su comando (los ABM: editar y dar de baja). Un
        ícono puede llevar una tercera parte, condicion(fila), y entonces solo
        aparece en las filas donde tiene sentido (Cancelar en un préstamo
        que todavía no está activo). El DAO valida igual al ejecutar."""
        if iconos:
            columnas = columnas + [('acciones', "Acciones", 0)]
        marco, self.tabla = self.crear_tabla(contenedor, columnas, alto)
        if iconos:
            self.tabla.iconos = iconos
            self.ajustar_columnas(self.tabla, [])
            self.tabla.bind("<Button-1>", self.clic_en_icono)
            # La manito indica que el ícono se puede tocar
            self.tabla.bind("<Motion>", self.cursor_sobre_icono)
        self.tabla.bind("<<TreeviewSelect>>", lambda evento: self.activar_botones_seleccion())
        if doble_clic is not None:
            self.tabla.bind("<Double-1>", lambda evento: doble_clic())
        self.activar_botones_seleccion()
        return marco

    def iconos_de_fila(self, tabla, fila):
        """Los (ícono, comando) que corresponden a esa fila."""
        iconos = []
        for icono in tabla.iconos:
            if len(icono) < 3 or icono[2](fila):
                iconos.append((icono[0], icono[1]))
        return iconos

    def texto_celda(self, tabla, fila, clave):
        if clave == 'acciones':
            return SEPARACION_ICONOS.join([icono for icono, comando in self.iconos_de_fila(tabla, fila)])
        return str(fila[clave])

    def icono_en(self, evento):
        """La fila y el comando del ícono que está bajo el mouse, o None.
        Treeview no tiene botones por celda: identify_row e identify_column
        dicen en qué fila y columna cayó el mouse, y measure() dónde termina
        cada ícono."""
        fila = self.tabla.identify_row(evento.y)
        # Acciones es la última columna: "#n", con n la cantidad de columnas
        if not fila or self.tabla.identify_column(evento.x) != f"#{len(self.tabla.columnas)}":
            return None, None
        x = evento.x - self.tabla.bbox(fila, 'acciones')[0]
        fuente = tkfont.nametofont("TkDefaultFont")
        medio_espacio = fuente.measure(SEPARACION_ICONOS) // 2
        de_la_fila = self.iconos_de_fila(self.tabla, self.buscar_fila(int(fila)))
        for posicion in range(len(de_la_fila)):
            iconos = [icono for icono, comando in de_la_fila[:posicion + 1]]
            if x <= fuente.measure(MARGEN + SEPARACION_ICONOS.join(iconos)) + medio_espacio:
                return fila, de_la_fila[posicion][1]
        return None, None

    def clic_en_icono(self, evento):
        fila, comando = self.icono_en(evento)
        if comando is None:
            return None
        self.tabla.selection_set(fila)
        self.tabla.focus(fila)
        comando()
        # "break" evita que el clic siga su curso normal después del comando
        return "break"

    def cursor_sobre_icono(self, evento):
        fila, comando = self.icono_en(evento)
        self.tabla.config(cursor="hand2" if comando is not None else "")

    def cargar_tabla(self, tabla, filas):
        """Reemplaza el contenido. Cada fila es un diccionario del DAO con su 'id'."""
        for item in tabla.get_children():
            tabla.delete(item)
        for posicion, fila in enumerate(filas):
            # Una fila sí y una no lleva la franja, para separar las filas a la vista
            tags = ["franja"] if posicion % 2 == 1 else []
            tabla.insert("", tk.END, iid=str(fila['id']), tags=tags,
                         values=[MARGEN + self.texto_celda(tabla, fila, clave) for clave in tabla.columnas])
        self.ajustar_columnas(tabla, filas)
        if tabla is getattr(self, 'tabla', None):
            self.activar_botones_seleccion()

    def id_seleccionado(self, tabla, aviso="Seleccione una fila de la tabla"):
        """Como curselection() del Listbox: devuelve el id de la fila elegida."""
        seleccion = tabla.selection()
        if not seleccion:
            messagebox.showwarning("Atención", aviso)
            return None
        return int(seleccion[0])

    def buscar_fila(self, id):
        for fila in self.filas:
            if fila['id'] == id:
                return fila
        return None

    # ---------------------------------------------------------- acciones

    def ejecutar(self, accion, mensaje_ok):
        """Llama al DAO y muestra el resultado. La UI solo captura los
        errores de validación y de negocio, como pide la arquitectura."""
        try:
            accion()
        except (ValidacionError, ReglaNegocioError) as error:
            messagebox.showerror("No se pudo completar la operación", str(error), parent=self.ventana_actual())
            return False
        messagebox.showinfo("Listo", mensaje_ok, parent=self.ventana_actual())
        if self.refrescar_todo is not None:
            self.refrescar_todo()
        else:
            self.refrescar()
        return True

    def hay_empleado(self):
        """Las operaciones que registran quién las hizo no se permiten sin
        empleado actual elegido."""
        if self.empleado_actual is None or self.empleado_actual() is None:
            messagebox.showerror("Falta el empleado", "Seleccione el empleado actual arriba de la ventana")
            return False
        return True

    def avisar_cambios_a(self, funcion):
        """main.py indica qué función llamar para refrescar todas las pestañas."""
        self.refrescar_todo = funcion

    def accion_sobre_seleccion(self, accion, pregunta, mensaje_ok):
        """Para bajas y eliminaciones: pide confirmación y llama accion(id)."""
        id = self.id_seleccionado(self.tabla)
        if id is not None and messagebox.askyesno("Confirmar", pregunta):
            self.ejecutar(lambda: accion(id), mensaje_ok)

    # ------------------------------------------- flujo de alta/modificación
    # Las pestañas de ABM definen: TITULO_NUEVO y TITULO_EDITAR (por ejemplo
    # "Nueva sede" y "Editar sede"), self.tabla, armar_formulario(contenedor),
    # campos_formulario(), crear(), modificar(id), cargar_formulario(fila) y refrescar().

    def nuevo(self):
        self.abrir_formulario(None)

    def editar_seleccionado(self):
        id = self.id_seleccionado(self.tabla, "Seleccione en la tabla el registro a modificar")
        if id is not None:
            self.abrir_formulario(id)

    def abrir_formulario(self, id):
        """Alta (id None) o modificación del registro id, en una ventana modal."""
        self.id_editando = id
        titulo = self.TITULO_NUEVO if id is None else self.TITULO_EDITAR
        self.abrir_modal(titulo, self.armar_formulario, self.guardar,
                         "Dar de alta" if id is None else "Guardar cambios")
        if id is not None:
            self.cargar_formulario(self.buscar_fila(id))

    def guardar(self):
        """Alta si no se está editando; si no, modificación del registro elegido."""
        if not self.validar_campos(self.campos_formulario()):
            return False
        if self.id_editando is None:
            return self.ejecutar(self.crear, "Registro dado de alta")
        return self.ejecutar(lambda: self.modificar(self.id_editando), "Cambios guardados")

    def refrescar(self):
        """Cada pestaña recarga su tabla. Se redefine en las subclases."""
        pass
