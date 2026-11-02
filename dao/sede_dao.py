"""Acceso a datos de sedes y sus horarios."""

from config import LARGO_NOMBRE_SEDE, LARGO_DIRECCION
from constantes import DiaSemana, EstadoPrestamo, EstadoRemito, EstadoReserva, EstadoSede
from dao.comun import buscar_por_id
from database import obtener_session
from excepciones import ReglaNegocioError, ValidacionError
from modelos.sede import Sede, HorarioSede
from modelos.prestamo import Prestamo
from modelos.remito import Remito
from modelos.reserva import Reserva
from validadores import (validar_nombre_con_numeros, validar_direccion, validar_telefono, validar_prefijo_pais, validar_email, validar_opcion,
                         validar_hora, validar_rango_horario)

# Estados que impiden dar de baja una sede porque la operación sigue abierta
PRESTAMOS_EN_CURSO = [EstadoPrestamo.SOLICITADO, EstadoPrestamo.APROBADO,
                      EstadoPrestamo.EN_ENVIO, EstadoPrestamo.ACTIVO]
REMITOS_EN_CURSO = [EstadoRemito.EMPAQUETADO, EstadoRemito.DESPACHADO, EstadoRemito.EN_TRANSITO]
RESERVAS_EN_CURSO = [EstadoReserva.PENDIENTE, EstadoReserva.DISPONIBLE]


def validar_datos_sede(nombre, direccion, prefijo, telefono, email):
    """Valida el formato de los datos de la sede y los devuelve normalizados."""
    nombre = validar_nombre_con_numeros(nombre, "nombre", 2, LARGO_NOMBRE_SEDE)
    direccion = validar_direccion(direccion, "dirección", LARGO_DIRECCION)
    prefijo = validar_prefijo_pais(prefijo)
    telefono = validar_telefono(telefono)
    email = validar_email(email, obligatorio=False)
    return nombre, direccion, prefijo, telefono, email


def validar_datos_horario(dia, apertura, cierre):
    dia = validar_opcion(dia, DiaSemana.TODOS, "día")
    if not apertura or not cierre:
        raise ValidacionError(f"Elija la hora de apertura y la de cierre del {dia}")
    apertura = validar_hora(apertura, f"hora de apertura del {dia}")
    cierre = validar_hora(cierre, f"hora de cierre del {dia}")
    validar_rango_horario(apertura, cierre, dia)
    return dia, apertura, cierre


def validar_horarios(horarios):
    """horarios es la semana de la sede: [(día, apertura, cierre)], uno por
    cada día que abre, cada uno con su propio horario. Mínimo un día y sin
    repetir días. Devuelve la lista validada (con objetos time)."""
    if not horarios:
        raise ValidacionError("Marque al menos un día de apertura")
    validados = []
    dias = []
    for dia, apertura, cierre in horarios:
        dia, apertura, cierre = validar_datos_horario(dia, apertura, cierre)
        if dia in dias:
            raise ValidacionError(f"El día {dia} está repetido")
        dias.append(dia)
        validados.append((dia, apertura, cierre))
    return validados


class SedeDAO:
    """Operaciones de acceso a datos sobre sedes y horarios."""

    def verificar_nombre_unico(self, session, nombre, id_actual=None):
        # unique=True de SQLite distingue mayúsculas: se compara en minúsculas
        for sede in session.query(Sede).all():
            if sede.nombre.lower() == nombre.lower() and sede.id != id_actual:
                raise ReglaNegocioError(f"Ya existe una sede llamada {sede.nombre}")

    def poner_horarios(self, sede, horarios):
        """Reemplaza la semana de la sede. Por la composición (cascade
        delete-orphan), los horarios que salen de la lista se borran."""
        sede.horarios = [HorarioSede(dia_semana=dia, hora_apertura=apertura, hora_cierre=cierre)
                         for dia, apertura, cierre in horarios]

    def crear(self, nombre, direccion, prefijo, telefono, email, horarios):
        """Da de alta una sede con sus días y horarios de apertura (mínimo uno)."""
        datos = validar_datos_sede(nombre, direccion, prefijo, telefono, email)
        nombre, direccion, prefijo, telefono, email = datos
        horarios = validar_horarios(horarios)
        with obtener_session() as session:
            self.verificar_nombre_unico(session, nombre)
            sede = Sede(nombre=nombre, direccion=direccion, prefijo_pais=prefijo, telefono=telefono, email=email,
                        estado=EstadoSede.ACTIVA)
            self.poner_horarios(sede, horarios)
            session.add(sede)

    def modificar(self, id, nombre, direccion, prefijo, telefono, email, horarios):
        """Modifica los datos de la sede y reemplaza su semana de horarios."""
        datos = validar_datos_sede(nombre, direccion, prefijo, telefono, email)
        nombre, direccion, prefijo, telefono, email = datos
        horarios = validar_horarios(horarios)
        with obtener_session() as session:
            sede = buscar_por_id(session, Sede, id, "la sede")
            self.verificar_nombre_unico(session, nombre, id_actual=sede.id)
            sede.nombre = nombre
            sede.direccion = direccion
            sede.prefijo_pais = prefijo
            sede.telefono = telefono
            sede.email = email
            self.poner_horarios(sede, horarios)

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

    def reactivar(self, id):
        with obtener_session() as session:
            sede = buscar_por_id(session, Sede, id, "la sede")
            sede.reactivar()

    def listar(self):
        """Devuelve las sedes con los datos listos para mostrar."""
        with obtener_session() as session:
            sedes = session.query(Sede).order_by(Sede.nombre).all()
            return [
                {
                    'id': sede.id,
                    'nombre': sede.nombre,
                    'direccion': sede.direccion,
                    'prefijo': sede.prefijo_pais,
                    'telefono': sede.telefono,
                    'telefono_completo': f"+{sede.prefijo_pais} {sede.telefono}",
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
