"""Clase base de las pestañas: todo lo que se repite entre formularios.

Cada pestaña hereda de PestaniaBase y solo define sus campos y qué DAO
llama. Así el armado de campos, el mensaje de error en rojo, las tablas y
el manejo de errores se escriben una sola vez (herencia, vista en clase).
"""

import tkinter as tk
from datetime import date, timedelta
from tkinter import ttk, messagebox

from excepciones import ValidacionError, ReglaNegocioError
from validadores import solo_digitos


class PestaniaBase(ttk.Frame):

    def __init__(self, padre, empleado_actual=None):
        """empleado_actual es una función que devuelve el id del empleado
        elegido arriba de la ventana (o None). La reciben solo las pestañas
        cuyas operaciones quedan registradas a nombre de un empleado."""
        super().__init__(padre, padding=10)
        self.empleado_actual = empleado_actual
        # nombre -> {'widget', 'error', 'validador', 'etiqueta'}
        self.campos = {}
        # nombre del combo -> {texto mostrado: id}
        self.opciones_combo = {}
        self.filas = []            # última lista que devolvió el DAO
        self.id_editando = None    # None = alta; un id = modificación
        # Función que refresca todas las pestañas (la asigna main.py). Una
        # operación puede cambiar datos que muestra otra pestaña: por ejemplo,
        # aprobar un préstamo cambia el estado del ejemplar.
        self.refrescar_todo = None

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
        error = ttk.Label(contenedor, text="", foreground="red")
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
        error = ttk.Label(contenedor, text="", foreground="red")
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
        error = ttk.Label(contenedor, text="", foreground="red")
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
            messagebox.showerror("Revise los datos", "\n".join(errores))
            return False
        return True

    def limpiar_campos(self, nombres):
        for nombre in nombres:
            widget = self.campos[nombre]['widget']
            if self.es_combo(nombre):
                widget.set("")
            else:
                widget.delete(0, tk.END)
            self.campos[nombre]['error'].config(text="")

    # ------------------------------------------------------------ tablas

    def crear_tabla(self, contenedor, columnas, alto=10):
        """Treeview con barra de desplazamiento. columnas = [(clave, título, ancho)]."""
        marco = ttk.Frame(contenedor)
        tabla = ttk.Treeview(marco, columns=[c[0] for c in columnas], show="headings", height=alto)
        for clave, titulo, ancho in columnas:
            tabla.heading(clave, text=titulo)
            tabla.column(clave, width=ancho)
        barra = ttk.Scrollbar(marco, orient="vertical", command=tabla.yview)
        tabla.config(yscrollcommand=barra.set)
        tabla.pack(side="left", fill="both", expand=True)
        barra.pack(side="right", fill="y")
        tabla.columnas = [c[0] for c in columnas]
        return marco, tabla

    def cargar_tabla(self, tabla, filas):
        """Reemplaza el contenido. Cada fila es un diccionario del DAO con su 'id'."""
        for item in tabla.get_children():
            tabla.delete(item)
        for fila in filas:
            tabla.insert("", tk.END, iid=str(fila['id']), values=[fila[clave] for clave in tabla.columnas])

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
            messagebox.showerror("No se pudo completar la operación", str(error))
            return False
        messagebox.showinfo("Listo", mensaje_ok)
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
            if self.ejecutar(lambda: accion(id), mensaje_ok):
                self.limpiar()

    # ------------------------------------------- flujo de alta/modificación
    # Las subclases definen: self.tabla, campos_formulario(), crear(),
    # modificar(id), cargar_formulario(fila) y refrescar().

    def crear_botones(self, contenedor, extras=None):
        """Botones comunes (Guardar, Editar seleccionado, Limpiar) más los propios."""
        marco = ttk.Frame(contenedor)
        self.boton_guardar = ttk.Button(marco, text="Guardar", command=self.guardar)
        self.boton_guardar.pack(side="left", padx=5)
        ttk.Button(marco, text="Editar seleccionado", command=self.editar_seleccionado).pack(side="left", padx=5)
        ttk.Button(marco, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)
        for texto, comando in extras or []:
            ttk.Button(marco, text=texto, command=comando).pack(side="left", padx=5)
        return marco

    def guardar(self):
        """Alta si no se está editando; si no, modificación del registro elegido."""
        if not self.validar_campos(self.campos_formulario()):
            return
        if self.id_editando is None:
            correcto = self.ejecutar(self.crear, "Registro dado de alta")
        else:
            correcto = self.ejecutar(lambda: self.modificar(self.id_editando), "Cambios guardados")
        if correcto:
            self.limpiar()

    def editar_seleccionado(self):
        id = self.id_seleccionado(self.tabla, "Seleccione en la tabla el registro a modificar")
        if id is None:
            return
        self.limpiar()
        self.id_editando = id
        self.cargar_formulario(self.buscar_fila(id))
        self.boton_guardar.config(text="Guardar cambios")

    def limpiar(self):
        self.limpiar_campos(self.campos_formulario())
        self.id_editando = None
        self.boton_guardar.config(text="Guardar")
        self.tabla.selection_remove(self.tabla.selection())

    def refrescar(self):
        """Cada pestaña recarga su tabla. Se redefine en las subclases."""
        pass
