"""Acceso a datos de socios."""

from config import LARGO_NOMBRE_PERSONA
from constantes import EstadoPrestamo, EstadoSocio
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.socio import Socio
from validadores import (validar_nro_socio, validar_dni, validar_solo_letras,
                         validar_email, validar_telefono)

PRESTAMOS_EN_CURSO = [EstadoPrestamo.SOLICITADO, EstadoPrestamo.APROBADO,
                      EstadoPrestamo.EN_ENVIO, EstadoPrestamo.ACTIVO]


def validar_datos_socio(nro_socio, dni, nombre, apellido, email, telefono):
    nro_socio = validar_nro_socio(nro_socio)
    dni = validar_dni(dni)
    nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_PERSONA)
    apellido = validar_solo_letras(apellido, "apellido", 2, LARGO_NOMBRE_PERSONA)
    email = validar_email(email, obligatorio=False)
    telefono = validar_telefono(telefono)
    return nro_socio, dni, nombre, apellido, email, telefono


class SocioDAO:
    """Operaciones de acceso a datos sobre socios."""

    def verificar_duplicados(self, session, nro_socio, dni, id_actual=None):
        socio = session.query(Socio).filter_by(nro_socio=nro_socio).first()
        if socio is not None and socio.id != id_actual:
            raise ReglaNegocioError(f"Ya existe un socio con el número {nro_socio}")
        socio = session.query(Socio).filter_by(dni=dni).first()
        if socio is not None and socio.id != id_actual:
            raise ReglaNegocioError(f"Ya existe un socio con el DNI {dni}")

    def crear(self, nro_socio, dni, nombre, apellido, email, telefono):
        datos = validar_datos_socio(nro_socio, dni, nombre, apellido, email, telefono)
        nro_socio, dni, nombre, apellido, email, telefono = datos
        with obtener_session() as session:
            self.verificar_duplicados(session, nro_socio, dni)
            session.add(Socio(nro_socio=nro_socio, dni=dni, nombre=nombre, apellido=apellido,
                              email=email, telefono=telefono, estado=EstadoSocio.ACTIVO))

    def modificar(self, id, nro_socio, dni, nombre, apellido, email, telefono):
        datos = validar_datos_socio(nro_socio, dni, nombre, apellido, email, telefono)
        nro_socio, dni, nombre, apellido, email, telefono = datos
        with obtener_session() as session:
            socio = buscar_por_id(session, Socio, id, "el socio")
            self.verificar_duplicados(session, nro_socio, dni, id_actual=socio.id)
            socio.nro_socio = nro_socio
            socio.dni = dni
            socio.nombre = nombre
            socio.apellido = apellido
            socio.email = email
            socio.telefono = telefono

    def inhabilitar(self, id):
        with obtener_session() as session:
            buscar_por_id(session, Socio, id, "el socio").inhabilitar()

    def habilitar(self, id):
        """Vuelve a ACTIVO un socio inhabilitado. Un socio de baja no vuelve."""
        with obtener_session() as session:
            socio = buscar_por_id(session, Socio, id, "el socio")
            if socio.estado != EstadoSocio.INHABILITADO:
                raise ReglaNegocioError(f"Solo se puede habilitar un socio inhabilitado (está {socio.estado})")
            socio.estado = EstadoSocio.ACTIVO

    def dar_de_baja(self, id):
        """Baja lógica, solo sin préstamos en curso (supuesto del grupo)."""
        with obtener_session() as session:
            socio = buscar_por_id(session, Socio, id, "el socio")
            if socio.estado == EstadoSocio.BAJA:
                raise ReglaNegocioError("El socio ya está dado de baja")
            for prestamo in socio.prestamos:
                if prestamo.estado in PRESTAMOS_EN_CURSO:
                    raise ReglaNegocioError("No se puede dar de baja: el socio tiene préstamos en curso")
            socio.estado = EstadoSocio.BAJA

    def listar(self):
        with obtener_session() as session:
            socios = session.query(Socio).order_by(Socio.nro_socio).all()
            return [
                {
                    'id': socio.id,
                    'nro_socio': socio.nro_socio,
                    'dni': socio.dni,
                    'nombre': socio.nombre,
                    'apellido': socio.apellido,
                    'email': socio.email or "",
                    'telefono': socio.telefono or "",
                    'fecha_alta': socio.fecha_alta.strftime("%d/%m/%Y"),
                    'estado': socio.estado,
                }
                for socio in socios
            ]

    def opciones(self, solo_habilitados=True):
        with obtener_session() as session:
            socios = session.query(Socio).order_by(Socio.apellido).all()
            return [(socio.id, str(socio)) for socio in socios
                    if socio.esta_habilitado() or not solo_habilitados]
