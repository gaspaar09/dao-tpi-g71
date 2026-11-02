"""Acceso a datos de socios."""

from config import LARGO_NOMBRE_PERSONA
from constantes import EstadoPrestamo, EstadoSocio
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.socio import Socio
from validadores import (validar_dni, formatear_dni, validar_solo_letras,
                         validar_email, validar_prefijo_pais, validar_telefono)

PRESTAMOS_EN_CURSO = [EstadoPrestamo.SOLICITADO, EstadoPrestamo.APROBADO,
                      EstadoPrestamo.EN_ENVIO, EstadoPrestamo.ACTIVO]


def validar_datos_socio(dni, nombre, apellido, email, prefijo, telefono):
    dni = validar_dni(dni)
    nombre = validar_solo_letras(nombre, "nombre", 2, LARGO_NOMBRE_PERSONA)
    apellido = validar_solo_letras(apellido, "apellido", 2, LARGO_NOMBRE_PERSONA)
    email = validar_email(email, obligatorio=False)
    prefijo = validar_prefijo_pais(prefijo)
    telefono = validar_telefono(telefono)
    return dni, nombre, apellido, email, prefijo, telefono


class SocioDAO:
    """Operaciones de acceso a datos sobre socios."""

    def verificar_dni_unico(self, session, dni, id_actual=None):
        socio = session.query(Socio).filter_by(dni=dni).first()
        if socio is not None and socio.id != id_actual:
            raise ReglaNegocioError(f"Ya existe un socio con el DNI {dni}")

    def siguiente_nro_socio(self, session):
        """El número de socio lo asigna el sistema: el último registrado + 1.
        Se usa el máximo y no la cantidad, así no se repite aunque falte alguno."""
        numeros = [socio.nro_socio for socio in session.query(Socio).all()]
        return max(numeros, default=0) + 1

    def crear(self, dni, nombre, apellido, email, prefijo, telefono):
        """Da de alta el socio y devuelve el número de socio asignado."""
        dni, nombre, apellido, email, prefijo, telefono = validar_datos_socio(dni, nombre, apellido, email,
                                                                              prefijo, telefono)
        with obtener_session() as session:
            self.verificar_dni_unico(session, dni)
            nro_socio = self.siguiente_nro_socio(session)
            session.add(Socio(nro_socio=nro_socio, dni=dni, nombre=nombre, apellido=apellido,
                              email=email, prefijo_pais=prefijo, telefono=telefono,
                              estado=EstadoSocio.ACTIVO))
            return nro_socio

    def modificar(self, id, dni, nombre, apellido, email, prefijo, telefono):
        """El número de socio no se modifica: lo asignó el sistema en el alta."""
        dni, nombre, apellido, email, prefijo, telefono = validar_datos_socio(dni, nombre, apellido, email,
                                                                              prefijo, telefono)
        with obtener_session() as session:
            socio = buscar_por_id(session, Socio, id, "el socio")
            self.verificar_dni_unico(session, dni, id_actual=socio.id)
            socio.dni = dni
            socio.nombre = nombre
            socio.apellido = apellido
            socio.email = email
            socio.prefijo_pais = prefijo
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
                    'dni_formateado': formatear_dni(socio.dni),
                    'nombre': socio.nombre,
                    'apellido': socio.apellido,
                    'email': socio.email or "",
                    'prefijo': socio.prefijo_pais,
                    'telefono': socio.telefono,
                    'telefono_completo': f"+{socio.prefijo_pais} {socio.telefono}",
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
