"""Pestaña de Socios: alta, modificación, inhabilitación y baja."""

import tkinter as tk
from tkinter import messagebox

from config import LARGO_NOMBRE_PERSONA
from constantes import PaisTelefono
from dao.socio_dao import SocioDAO
from ui.base import PestaniaBase, ICONO_EDITAR, ICONO_BAJA
from validadores import (validar_dni, formatear_dni, solo_digitos, validar_solo_letras,
                         validar_email, validar_telefono)

# El número de socio no se carga: lo asigna el sistema al dar de alta
CAMPOS = ['dni', 'nombre', 'apellido', 'email', 'prefijo', 'telefono']


class PestaniaSocios(PestaniaBase):
    TITULO_NUEVO = "Nuevo socio"
    TITULO_EDITAR = "Editar socio"

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = SocioDAO()
        self.crear_encabezado("Socios", "Personas que pueden pedir préstamos y reservas",
                              [("Nuevo socio", self.nuevo, True)])
        self.crear_barra_seleccion("Con el socio elegido:",
                                   [("Habilitar", self.habilitar)], [("Inhabilitar", self.inhabilitar)])
        self.crear_tabla_principal(self, [
            ('nro_socio', "N° socio", 80), ('dni_formateado', "DNI", 110), ('apellido', "Apellido", 150),
            ('nombre', "Nombre", 150), ('email', "Email", 220), ('telefono_completo', "Teléfono", 150),
            ('fecha_alta', "Alta", 100), ('estado', "Estado", 110)],
            doble_clic=self.editar_seleccionado,
            iconos=[(ICONO_EDITAR, self.editar_seleccionado), (ICONO_BAJA, self.dar_de_baja)]).pack(fill="both", expand=True)
        self.refrescar()

    def armar_formulario(self, contenedor):
        entry_dni = self.crear_campo(contenedor, 'dni', "DNI:", 0, validar_dni)
        # En vivo: solo dígitos (los puntos los pone el sistema) y como máximo 8
        vcmd = self.register(self.dni_permitido)
        entry_dni.config(validate="key", validatecommand=(vcmd, "%P"))
        # Al soltar cada tecla se reacomodan los puntos de miles
        entry_dni.bind("<KeyRelease>", lambda evento: self.poner_puntos_dni())
        self.crear_campo(contenedor, 'nombre', "Nombre:", 1,
                         lambda v: validar_solo_letras(v, "nombre", 2, LARGO_NOMBRE_PERSONA))
        self.crear_campo(contenedor, 'apellido', "Apellido:", 2,
                         lambda v: validar_solo_letras(v, "apellido", 2, LARGO_NOMBRE_PERSONA))
        self.crear_campo(contenedor, 'email', "Email (opcional):", 3, lambda v: validar_email(v, obligatorio=False))
        # El código de país no se escribe: se elige el país y el número va sin "+"
        self.crear_combo(contenedor, 'prefijo', "País (teléfono):", 4,
                         lambda: [(codigo, f"{pais} (+{codigo})") for pais, codigo in PaisTelefono.PAISES])
        self.crear_campo(contenedor, 'telefono', "Teléfono (solo números):", 5, validar_telefono, numerico=True)
        self.poner('prefijo', PaisTelefono.ARGENTINA)
        if self.id_editando is None:
            self.ayuda(contenedor, "El número de socio lo asigna el sistema al dar de alta.", 6)

    def dni_permitido(self, nuevo_valor):
        """Acepta "" (para poder borrar) o dígitos con puntos, hasta 8 dígitos."""
        digitos = nuevo_valor.replace(".", "")
        return nuevo_valor == "" or (solo_digitos(digitos) and len(digitos) <= 8)

    def poner_puntos_dni(self):
        entry = self.campos['dni']['widget']
        texto = entry.get()
        con_puntos = formatear_dni(texto)
        if con_puntos != texto:
            entry.delete(0, tk.END)
            entry.insert(0, con_puntos)

    def campos_formulario(self):
        return CAMPOS

    def crear(self):
        self.nro_asignado = self.dao.crear(*[self.valor(nombre) for nombre in CAMPOS])

    def guardar(self):
        """Como el número lo pone el sistema, después del alta se informa cuál quedó."""
        self.nro_asignado = None
        correcto = super().guardar()
        if correcto and self.nro_asignado is not None:
            messagebox.showinfo("Número de socio", f"Se asignó el número de socio {self.nro_asignado}",
                                parent=self.ventana_actual())
        return correcto

    def modificar(self, id):
        self.dao.modificar(id, *[self.valor(nombre) for nombre in CAMPOS])

    def cargar_formulario(self, fila):
        for nombre in CAMPOS:
            self.poner(nombre, fila[nombre])
        self.poner('dni', fila['dni_formateado'])

    def inhabilitar(self):
        self.accion_sobre_seleccion(self.dao.inhabilitar, "¿Inhabilitar el socio seleccionado?", "Socio inhabilitado")

    def habilitar(self):
        self.accion_sobre_seleccion(self.dao.habilitar, "¿Volver a habilitar el socio seleccionado?",
                                    "Socio habilitado")

    def dar_de_baja(self):
        self.accion_sobre_seleccion(self.dao.dar_de_baja, "¿Dar de baja el socio seleccionado?",
                                    "Socio dado de baja")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
