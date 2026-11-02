"""Apariencia de la interfaz: paleta de colores y estilos ttk.

Solo cambia cómo se ve la ventana, no lo que hace. Se aplica una vez al
inicio y todos los widgets ttk de todas las pestañas toman estos estilos.

Los apuntes muestran ttk.Style().theme_use("clam") y colores con bg/fg.
Para cambiar el aspecto de los widgets ttk se usan además configure() y
map() de la misma clase ttk.Style (excepción aprobada por el grupo).

Esquinas redondeadas: el tema "clam" dibuja todo con rectángulos y ttk no
tiene una opción de radio. Por eso se dibujan imágenes redondeadas con
PhotoImage (visto en los apuntes) y se registran como elementos nuevos con
ttk.Style().element_create(), que reemplazan el borde de botones, campos y
pestañas (excepción aprobada por el grupo).
"""

import tkinter as tk
from tkinter import ttk


class Colores:
    """Paleta moderna clara: fondo gris suave, paneles blancos y acento índigo."""
    FONDO = "#f4f6fb"
    PANEL = "#ffffff"
    ACENTO = "#4f46e5"
    ACENTO_OSCURO = "#4338ca"
    ACENTO_CLARO = "#e0e7ff"
    TEXTO = "#1f2937"
    TEXTO_SECUNDARIO = "#6b7280"
    BORDE = "#e5e7eb"
    CUADRICULA = "#d1d5db"
    FILA_PAR = "#f9fafb"
    ERROR = "#dc2626"


FUENTE = ("Helvetica", 10)
FUENTE_NEGRITA = ("Helvetica", 10, "bold")
FUENTE_TITULO = ("Helvetica", 11, "bold")
FUENTE_ENCABEZADO = ("Helvetica", 14, "bold")

# Color del texto de una fila según su estado. Solo se resaltan los estados
# que piden atención: el resto queda en negro
ESTADOS_ROJOS = ["VENCIDO", "VENCIDA", "EXTRAVIADO", "CANCELADO", "CANCELADA", "BAJA", "INHABILITADO",
                 "DAÑADO"]
ESTADOS_AZULES = ["EN_TRANSITO", "EN_ENVIO", "DESPACHADO", "EMPAQUETADO", "PENDIENTE", "SOLICITADO",
                  "APROBADO"]


def aplicar_estilos(ventana):
    estilo = ttk.Style()
    estilo.theme_use("clam")
    ventana.configure(bg=Colores.FONDO)

    # Base común a todos los widgets ttk
    estilo.configure(".", background=Colores.FONDO, foreground=Colores.TEXTO, font=FUENTE,
                     bordercolor=Colores.BORDE, focuscolor=Colores.ACENTO)
    estilo.configure("TFrame", background=Colores.FONDO)
    estilo.configure("TLabel", background=Colores.FONDO, foreground=Colores.TEXTO)
    estilo.configure("Muted.TLabel", foreground=Colores.TEXTO_SECUNDARIO)
    estilo.configure("Error.TLabel", foreground=Colores.ERROR)
    estilo.configure("Title.TLabel", foreground=Colores.ACENTO, font=FUENTE_TITULO)

    # Barra superior
    estilo.configure("Header.TFrame", background=Colores.ACENTO)
    estilo.configure("Header.TLabel", background=Colores.ACENTO, foreground="white", font=FUENTE_NEGRITA)
    estilo.configure("HeaderTitle.TLabel", background=Colores.ACENTO, foreground="white",
                     font=FUENTE_ENCABEZADO)

    # Pestañas (letra normal y poco relleno para que entren los diez nombres)
    estilo.configure("TNotebook", background=Colores.FONDO, borderwidth=0, tabmargins=(0, 6, 0, 0))
    estilo.configure("TNotebook.Tab", background=Colores.FONDO, foreground=Colores.TEXTO_SECUNDARIO,
                     padding=(8, 6), borderwidth=0, font=FUENTE)
    estilo.map("TNotebook.Tab",
               background=[("selected", Colores.PANEL), ("active", Colores.ACENTO_CLARO)],
               foreground=[("selected", Colores.ACENTO)])

    # Botones: secundarios blancos y principal índigo
    estilo.configure("TButton", background=Colores.PANEL, foreground=Colores.TEXTO, padding=(10, 5),
                     borderwidth=1, relief="flat")
    estilo.map("TButton",
               background=[("pressed", Colores.ACENTO_CLARO), ("active", Colores.ACENTO_CLARO)],
               bordercolor=[("active", Colores.ACENTO)])
    estilo.configure("Accent.TButton", background=Colores.ACENTO, foreground="white",
                     bordercolor=Colores.ACENTO, font=FUENTE_NEGRITA)
    estilo.map("Accent.TButton",
               background=[("pressed", Colores.ACENTO_OSCURO), ("active", Colores.ACENTO_OSCURO)],
               foreground=[("active", "white")])

    # Campos de texto y desplegables: borde índigo al tener el foco
    for nombre in ["TEntry", "TCombobox"]:
        estilo.configure(nombre, fieldbackground=Colores.PANEL, bordercolor=Colores.BORDE,
                         lightcolor=Colores.BORDE, darkcolor=Colores.BORDE, padding=2)
        estilo.map(nombre, bordercolor=[("focus", Colores.ACENTO)], lightcolor=[("focus", Colores.ACENTO)])
    estilo.map("TCombobox", fieldbackground=[("readonly", Colores.PANEL)],
               selectbackground=[("readonly", Colores.PANEL)], selectforeground=[("readonly", Colores.TEXTO)])
    estilo.configure("TCheckbutton", background=Colores.FONDO)
    estilo.configure("TRadiobutton", background=Colores.FONDO)

    # Tablas con cuadrícula: borde alrededor y cada encabezado con su recuadro.
    # Treeview no dibuja líneas entre filas; las filas alternadas las separan.
    estilo.configure("Treeview", background=Colores.PANEL, fieldbackground=Colores.PANEL,
                     foreground=Colores.TEXTO, rowheight=22, borderwidth=1, bordercolor=Colores.CUADRICULA)
    estilo.map("Treeview", background=[("selected", Colores.ACENTO)], foreground=[("selected", "white")])
    # Encabezado en letra normal: en negrita no entra en los anchos de columna y se corta
    estilo.configure("Treeview.Heading", background=Colores.BORDE, foreground=Colores.TEXTO,
                     font=FUENTE, relief="solid", borderwidth=1, bordercolor=Colores.CUADRICULA,
                     lightcolor=Colores.BORDE, darkcolor=Colores.CUADRICULA, padding=(2, 4))
    estilo.map("Treeview.Heading", background=[("active", Colores.ACENTO_CLARO)])

    estilo.configure("Vertical.TScrollbar", background=Colores.BORDE, troughcolor=Colores.FONDO,
                     bordercolor=Colores.FONDO, arrowcolor=Colores.TEXTO_SECUNDARIO)

    redondear_esquinas(estilo)


# ------------------------------------------------------- esquinas redondeadas

RADIO = 6
# Las imágenes se guardan acá: si nadie las referencia, Python las borra y desaparecen de la ventana
imagenes = []


def imagen_redondeada(relleno, borde, ancho=24, alto=24):
    """Rectángulo con esquinas redondeadas pintado pixel por pixel.
    Los pixeles de afuera no se pintan y quedan transparentes."""
    imagen = tk.PhotoImage(width=ancho, height=alto)
    for y in range(alto):
        for x in range(ancho):
            # Distancia al centro de la esquina más cercana (0 si no está en una esquina)
            centro_x = min(max(x + 0.5, RADIO), ancho - RADIO)
            centro_y = min(max(y + 0.5, RADIO), alto - RADIO)
            distancia = ((x + 0.5 - centro_x) ** 2 + (y + 0.5 - centro_y) ** 2) ** 0.5
            if distancia <= RADIO - 1:
                imagen.put(relleno, (x, y))
            elif distancia <= RADIO:
                imagen.put(borde, (x, y))
    imagenes.append(imagen)
    return imagen


def crear_elemento(estilo, nombre, normal, por_estado):
    """Registra un elemento de imagen. por_estado = [(estado, relleno, borde)].
    border=RADIO + 1 indica cuánto de cada borde no se estira (las esquinas)."""
    estados = []
    for estado, relleno, borde in por_estado:
        estados.append((estado, imagen_redondeada(relleno, borde)))
    estilo.element_create(nombre, "image", imagen_redondeada(normal[0], normal[1]), *estados,
                          border=RADIO + 1, sticky="nsew")


def redondear_esquinas(estilo):
    # Botón común: blanco con borde gris; índigo claro al pasar el mouse
    crear_elemento(estilo, "Redondo.boton", (Colores.PANEL, Colores.CUADRICULA),
                   [("pressed", Colores.ACENTO_CLARO, Colores.ACENTO),
                    ("active", Colores.ACENTO_CLARO, Colores.ACENTO)])
    # Botón principal: índigo, más oscuro al pasar el mouse
    crear_elemento(estilo, "Redondo.principal", (Colores.ACENTO, Colores.ACENTO),
                   [("pressed", Colores.ACENTO_OSCURO, Colores.ACENTO_OSCURO),
                    ("active", Colores.ACENTO_OSCURO, Colores.ACENTO_OSCURO)])
    # Campos: borde gris que pasa a índigo con el foco
    crear_elemento(estilo, "Redondo.campo", (Colores.PANEL, Colores.CUADRICULA),
                   [("focus", Colores.PANEL, Colores.ACENTO)])
    # Pestañas: la elegida en blanco, la que está bajo el mouse en índigo claro
    crear_elemento(estilo, "Redondo.pestania", (Colores.FONDO, Colores.FONDO),
                   [("selected", Colores.PANEL, Colores.PANEL),
                    ("active", Colores.ACENTO_CLARO, Colores.ACENTO_CLARO)])

    # El layout dice qué elementos forman cada widget: se cambia solo el borde
    # exterior por la imagen redondeada y se conservan los de adentro
    def boton(elemento):
        return [(elemento, {"sticky": "nsew", "children": [
            ("Button.padding", {"sticky": "nsew", "children": [
                ("Button.label", {"sticky": "nsew"})]})]})]

    estilo.layout("TButton", boton("Redondo.boton"))
    estilo.layout("Accent.TButton", boton("Redondo.principal"))
    estilo.layout("TEntry", [("Redondo.campo", {"sticky": "nsew", "children": [
        ("Entry.padding", {"sticky": "nsew", "children": [
            ("Entry.textarea", {"sticky": "nsew"})]})]})])
    estilo.layout("TCombobox", [("Redondo.campo", {"sticky": "nsew", "children": [
        ("Combobox.downarrow", {"side": "right", "sticky": "ns"}),
        ("Combobox.padding", {"expand": "1", "sticky": "nsew", "children": [
            ("Combobox.textarea", {"sticky": "nsew"})]})]})])
    estilo.layout("TNotebook.Tab", [("Redondo.pestania", {"sticky": "nsew", "children": [
        ("Notebook.padding", {"side": "top", "sticky": "nsew", "children": [
            ("Notebook.label", {"side": "top", "sticky": ""})]})]})])
    # Los campos y botones dejan un margen interno para que el texto no pise la curva
    estilo.configure("TEntry", padding=(6, 2))
    estilo.configure("TCombobox", padding=(6, 2), arrowsize=12, background=Colores.PANEL)
    estilo.configure("TButton", padding=(12, 4))


def configurar_tags_tabla(tabla):
    """Filas alternadas y color de texto por estado."""
    tabla.tag_configure("par", background=Colores.FILA_PAR)
    tabla.tag_configure("rojo", foreground=Colores.ERROR)
    tabla.tag_configure("azul", foreground=Colores.ACENTO)


def tags_de_fila(fila, posicion):
    """Tags visuales de una fila del DAO (no cambian sus datos)."""
    tags = []
    if posicion % 2 == 1:
        tags.append("par")
    estado = fila.get('estado')
    if estado in ESTADOS_ROJOS:
        tags.append("rojo")
    elif estado in ESTADOS_AZULES:
        tags.append("azul")
    return tags


def estilo_listbox(listbox):
    """tk.Listbox no es ttk: se le ponen los colores con bg/fg, como en los apuntes."""
    listbox.config(bg=Colores.PANEL, fg=Colores.TEXTO, selectbackground=Colores.ACENTO,
                   selectforeground="white", highlightthickness=1, highlightbackground=Colores.BORDE,
                   highlightcolor=Colores.ACENTO, relief="flat", font=FUENTE)
