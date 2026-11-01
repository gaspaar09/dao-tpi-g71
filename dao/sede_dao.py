"""Acceso a datos de sedes y sus horarios."""

from config import LARGO_NOMBRE_SEDE, LARGO_DIRECCION
from constantes import DiaSemana, EstadoPrestamo, EstadoRemito, EstadoReserva, EstadoSede
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError
from modelos.sede import Sede, HorarioSede
from modelos.prestamo import Prestamo
from modelos.remito import Remito
from modelos.reserva import Reserva
from validadores import (validar_texto, validar_telefono, validar_email, validar_opcion,
                         validar_hora, validar_rango_horario)

# Estados que impiden dar de baja una sede porque la operación sigue abierta
PRESTAMOS_EN_CURSO = [EstadoPrestamo.SOLICITADO, EstadoPrestamo.APROBADO,
                      EstadoPrestamo.EN_ENVIO, EstadoPrestamo.ACTIVO]
REMITOS_EN_CURSO = [EstadoRemito.EMPAQUETADO, EstadoRemito.DESPACHADO, EstadoRemito.EN_TRANSITO]
RESERVAS_EN_CURSO = [EstadoReserva.PENDIENTE, EstadoReserva.DISPONIBLE]


def validar_datos_sede(nombre, direccion, telefono, email):
    """Valida el formato de los datos de la sede y los devuelve normalizados."""
    nombre = validar_texto(nombre, "nombre", LARGO_NOMBRE_SEDE, minimo=2)
    direccion = validar_texto(direccion, "dirección", LARGO_DIRECCION)
    telefono = validar_telefono(telefono)
    email = validar_email(email, obligatorio=False)
    return nombre, direccion, telefono, email


def validar_datos_horario(dia, apertura, cierre):
    dia = validar_opcion(dia, DiaSemana.TODOS, "día")
    apertura = validar_hora(apertura, "hora de apertura")
    cierre = validar_hora(cierre, "hora de cierre")
    validar_rango_horario(apertura, cierre)
    return dia, apertura, cierre


class SedeDAO:
    """Operaciones de acceso a datos sobre sedes y horarios."""

    def verificar_nombre_unico(self, session, nombre, id_actual=None):
        # unique=True de SQLite distingue mayúsculas: se compara en minúsculas
        for sede in session.query(Sede).all():
            if sede.nombre.lower() == nombre.lower() and sede.id != id_actual:
                raise ReglaNegocioError(f"Ya existe una sede llamada {sede.nombre}")

    def crear(self, nombre, direccion, telefono, email, dia, apertura, cierre):
        """Da de alta una sede junto con su primer horario (mínimo uno)."""
        nombre, direccion, telefono, email = validar_datos_sede(nombre, direccion, telefono, email)
        dia, apertura, cierre = validar_datos_horario(dia, apertura, cierre)
        with obtener_session() as session:
            self.verificar_nombre_unico(session, nombre)
            sede = Sede(nombre=nombre, direccion=direccion, telefono=telefono, email=email,
                        estado=EstadoSede.ACTIVA)
            sede.horarios.append(HorarioSede(dia_semana=dia, hora_apertura=apertura, hora_cierre=cierre))
            session.add(sede)

    def modificar(self, id, nombre, direccion, telefono, email):
        nombre, direccion, telefono, email = validar_datos_sede(nombre, direccion, telefono, email)
        with obtener_session() as session:
            sede = buscar_por_id(session, Sede, id, "la sede")
            self.verificar_nombre_unico(session, nombre, id_actual=sede.id)
            sede.nombre = nombre
            sede.direccion = direccion
            sede.telefono = telefono
            sede.email = email

    def agregar_horario(self, sede_id, dia, apertura, cierre):
        dia, apertura, cierre = validar_datos_horario(dia, apertura, cierre)
        with obtener_session() as session:
            sede = buscar_por_id(session, Sede, sede_id, "la sede")
            for horario in sede.horarios:
                if horario.dia_semana == dia:
                    raise ReglaNegocioError(f"La sede ya tiene un horario para el día {dia}")
            sede.horarios.append(HorarioSede(dia_semana=dia, hora_apertura=apertura, hora_cierre=cierre))

    def quitar_horario(self, horario_id):
        with obtener_session() as session:
            horario = buscar_por_id(session, HorarioSede, horario_id, "el horario")
            if len(horario.sede.horarios) == 1:
                raise ReglaNegocioError("La sede debe tener al menos un horario")
            session.delete(horario)

    def dar_de_baja(self, id):
        """Baja lógica. No se permite con operaciones en curso (supuesto del grupo)."""
        with obtener_session() as session:
            sede = buscar_por_id(session, Sede, id, "la sede")
            prestamos = (session.query(Prestamo).filter_by(sede_origen_id=sede.id).all()
                         + session.query(Prestamo).filter_by(sede_destino_id=sede.id).all())
            for prestamo in prestamos:
                if prestamo.estado in PRESTAMOS_EN_CURSO:
                    raise ReglaNegocioError("No se puede dar de baja: la sede tiene préstamos en curso")
            remitos = (session.query(Remito).filter_by(sede_origen_id=sede.id).all()
                       + session.query(Remito).filter_by(sede_destino_id=sede.id).all())
            for remito in remitos:
                if remito.estado in REMITOS_EN_CURSO:
                    raise ReglaNegocioError("No se puede dar de baja: la sede tiene remitos en curso")
            for reserva in session.query(Reserva).filter_by(sede_retiro_id=sede.id).all():
                if reserva.estado in RESERVAS_EN_CURSO:
                    raise ReglaNegocioError("No se puede dar de baja: la sede tiene reservas pendientes")
            sede.dar_de_baja()

    def listar(self):
        """Devuelve las sedes con los datos listos para mostrar."""
        with obtener_session() as session:
            sedes = session.query(Sede).order_by(Sede.nombre).all()
            return [
                {
                    'id': sede.id,
                    'nombre': sede.nombre,
                    'direccion': sede.direccion,
                    'telefono': sede.telefono,
                    'email': sede.email or "",
                    'estado': sede.estado,
                }
                for sede in sedes
            ]

    def listar_horarios(self, sede_id):
        with obtener_session() as session:
            sede = buscar_por_id(session, Sede, sede_id, "la sede")
            # Se ordenan por día de la semana, no alfabéticamente
            horarios = sorted(sede.horarios, key=lambda h: DiaSemana.TODOS.index(h.dia_semana))
            return [
                {
                    'id': horario.id,
                    'dia': horario.dia_semana,
                    'apertura': horario.hora_apertura.strftime("%H:%M"),
                    'cierre': horario.hora_cierre.strftime("%H:%M"),
                }
                for horario in horarios
            ]

    def opciones(self, solo_activas=True):
        """Lista de (id, texto) para llenar un Combobox."""
        with obtener_session() as session:
            sedes = session.query(Sede).order_by(Sede.nombre).all()
            return [(sede.id, sede.nombre) for sede in sedes
                    if sede.esta_activa() or not solo_activas]
