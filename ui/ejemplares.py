"""Pestaña de Ejemplares (copias físicas de los libros)."""

from constantes import EstadoFisico
from dao.ejemplar_dao import EjemplarDAO
from dao.libro_dao import LibroDAO
from dao.sede_dao import SedeDAO
from ui.base import PestaniaBase, ICONO_EDITAR, ICONO_BAJA
from validadores import validar_codigo_inventario

CAMPOS = ['codigo_inventario', 'libro', 'sede', 'estado_fisico']
# Identifican la copia: no se modifican (ver EjemplarDAO.modificar)
CAMPOS_FIJOS = ['codigo_inventario', 'libro', 'sede']


class PestaniaEjemplares(PestaniaBase):
    TITULO_NUEVO = "Nuevo ejemplar"
    TITULO_EDITAR = "Cambiar estado físico"

    def __init__(self, padre):
        super().__init__(padre)
        self.dao = EjemplarDAO()
        self.crear_encabezado("Ejemplares", "Copias físicas de cada título, cada una en una sede",
                              [("Nuevo ejemplar", self.nuevo, True)])
        self.crear_barra_seleccion("Con el ejemplar elegido:", [])
        self.crear_tabla_principal(self, [
            ('codigo_inventario', "Código", 120), ('libro', "Libro", 300), ('sede', "Sede", 190),
            ('estado', "Estado", 120), ('estado_fisico', "Estado físico", 120)],
            doble_clic=self.editar_seleccionado,
            iconos=[(ICONO_EDITAR, self.editar_seleccionado), (ICONO_BAJA, self.dar_de_baja)]).pack(fill="both", expand=True)
        self.refrescar()

    def armar_formulario(self, contenedor):
        self.crear_campo(contenedor, 'codigo_inventario', "Código de inventario:", 0, validar_codigo_inventario)
        self.crear_combo(contenedor, 'libro', "Libro:", 1, LibroDAO().opciones, ancho=45)
        self.crear_combo(contenedor, 'sede', "Sede:", 2, SedeDAO().opciones)
        self.crear_combo(contenedor, 'estado_fisico', "Estado físico:", 3,
                         lambda: [(estado, estado) for estado in EstadoFisico.TODOS])
        if self.id_editando is None:
            self.ayuda(contenedor, "El código es el que está impreso en el ejemplar y no se puede repetir.", 4)
        else:
            self.ayuda(contenedor, "Código, libro y sede identifican la copia: solo cambia el estado físico.", 4)

    def campos_formulario(self):
        if self.id_editando is None:
            return CAMPOS
        return ['estado_fisico']

    def crear(self):
        self.dao.crear(self.valor('codigo_inventario'), self.valor('libro'), self.valor('sede'),
                       self.valor('estado_fisico'))

    def modificar(self, id):
        self.dao.modificar(id, self.valor('estado_fisico'))

    def cargar_formulario(self, fila):
        # Se muestran los datos fijos, pero deshabilitados
        self.poner('codigo_inventario', fila['codigo_inventario'])
        self.campos['libro']['widget'].set(fila['libro'])
        self.campos['sede']['widget'].set(fila['sede'])
        self.poner('estado_fisico', fila['estado_fisico'])
        for nombre in CAMPOS_FIJOS:
            self.campos[nombre]['widget'].config(state="disabled")

    def dar_de_baja(self):
        self.accion_sobre_seleccion(self.dao.dar_de_baja, "¿Dar de baja el ejemplar seleccionado?",
                                    "Ejemplar dado de baja")

    def refrescar(self):
        self.filas = self.dao.listar()
        self.cargar_tabla(self.tabla, self.filas)
