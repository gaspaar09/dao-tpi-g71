"""Acceso a datos de remitos: armado, cambios de estado e incidencias.

Las transiciones las decide el estado actual del remito (patrón State); este
DAO solo busca los objetos, llama al método del remito y se ocupa de los
préstamos. Es el único lugar donde se tocan los dos patrones: al recibir un
remito de IDA elige la estrategia en ESTRATEGIAS y se la pasa a
prestamo.activar(). Todo ocurre en una sola sesión: si algo falla,
obtener_session() deshace el cambio de estado completo.
"""

from config import LARGO_OBSERVACION_MOVIMIENTO, LARGO_DESCRIPCION_INCIDENCIA
from constantes import EstadoPrestamo, EstadoRemito, TipoEnvio, TipoIncidencia, TipoPrestamo
from dao.comun import buscar_por_id
from dao.prestamo_dao import verificar_transicion, formatear_fecha
from database import obtener_session
from excepciones import ValidacionError, ReglaNegocioError
from modelos.empleado import Empleado
from modelos.prestamo import Prestamo
from modelos.remito import Remito, ItemRemito, IncidenciaEnvio
from modelos.sede import Sede
from patrones.estrategia_prestamo import ESTRATEGIAS
from validadores import (validar_texto, validar_texto_opcional, validar_opcion, validar_fecha,
                         validar_fecha_no_futura)

MINIMO_OBSERVACION = 5
MINIMO_DESCRIPCION = 5


def validar_observacion_obligatoria(observacion):
    """Cancelar o dar por extraviado un envío exige explicar el motivo."""
    return validar_texto(observacion, "observación", LARGO_OBSERVACION_MOVIMIENTO, MINIMO_OBSERVACION)


def cancelar_prestamos(remito):
    """Un remito de IDA que no llega (cancelado o extraviado) cancela sus
    préstamos. En uno de DEVOLUCION los préstamos ya están DEVUELTO."""
    if remito.tipo == TipoEnvio.IDA:
        for item in remito.items:
            verificar_transicion(item.prestamo, EstadoPrestamo.CANCELADO)
            item.prestamo.estado = EstadoPrestamo.CANCELADO


class RemitoDAO:
    """Operaciones de acceso a datos sobre remitos."""

    def crear_ida(self, sede_origen_id, sede_destino_id, prestamos_ids, empleado_id):
        """Arma un remito EMPAQUETADO con préstamos interbibliotecarios
        aprobados entre el mismo par de sedes. Los préstamos pasan a EN_ENVIO."""
        if not prestamos_ids:
            raise ValidacionError("Seleccione al menos un préstamo para enviar")
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, empleado_id, "el empleado actual")
            origen = buscar_por_id(session, Sede, sede_origen_id, "la sede de origen")
            destino = buscar_por_id(session, Sede, sede_destino_id, "la sede de destino")
            if origen is destino:
                raise ReglaNegocioError("Las sedes de origen y destino del remito deben ser distintas")
            for sede in [origen, destino]:
                if not sede.esta_activa():
                    raise ReglaNegocioError(f"La sede {sede.nombre} está dada de baja")

            # Los remitos nunca se borran: el siguiente número es la cantidad + 1
            numero = session.query(Remito).count() + 1
            remito = Remito(nro_remito=f"REM-{numero:06d}", tipo=TipoEnvio.IDA,
                            sede_origen=origen, sede_destino=destino)
            for prestamo_id in prestamos_ids:
                prestamo = buscar_por_id(session, Prestamo, prestamo_id, "el préstamo")
                if prestamo.tipo != TipoPrestamo.INTERBIBLIOTECARIO:
                    raise ReglaNegocioError(f"El préstamo #{prestamo.id} es local: no viaja con remito")
                if prestamo.sede_origen is not origen or prestamo.sede_destino is not destino:
                    raise ReglaNegocioError(f"El préstamo #{prestamo.id} no va de {origen.nombre} a {destino.nombre}")
                # Solo un préstamo APROBADO puede pasar a EN_ENVIO
                verificar_transicion(prestamo, EstadoPrestamo.EN_ENVIO)
                prestamo.estado = EstadoPrestamo.EN_ENVIO
                remito.items.append(ItemRemito(ejemplar=prestamo.ejemplar, prestamo=prestamo))
            # El remito nace con su primer movimiento
            remito.cambiar_estado(EstadoRemito.EMPAQUETADO, empleado, "Remito creado")
            session.add(remito)

    def avanzar(self, id, empleado_id, observacion):
        """Pasa al estado siguiente (lo decide el estado actual). Si un remito
        de IDA queda RECIBIDO, sus préstamos se activan con su estrategia."""
        observacion = validar_texto_opcional(observacion, "observación", LARGO_OBSERVACION_MOVIMIENTO)
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, empleado_id, "el empleado actual")
            remito = buscar_por_id(session, Remito, id, "el remito")
            remito.avanzar_estado(empleado, observacion)
            if remito.estado == EstadoRemito.RECIBIDO and remito.tipo == TipoEnvio.IDA:
                for item in remito.items:
                    verificar_transicion(item.prestamo, EstadoPrestamo.ACTIVO)
                    # Selección externa de la estrategia (patrón Strategy)
                    item.prestamo.activar(ESTRATEGIAS[item.prestamo.tipo])

    def cancelar(self, id, empleado_id, observacion):
        observacion = validar_observacion_obligatoria(observacion)
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, empleado_id, "el empleado actual")
            remito = buscar_por_id(session, Remito, id, "el remito")
            remito.cancelar(empleado, observacion)
            cancelar_prestamos(remito)

    def extraviar(self, id, empleado_id, observacion):
        """Da el envío por perdido: queda registrada una incidencia de extravío."""
        observacion = validar_observacion_obligatoria(observacion)
        with obtener_session() as session:
            empleado = buscar_por_id(session, Empleado, empleado_id, "el empleado actual")
            remito = buscar_por_id(session, Remito, id, "el remito")
            remito.extraviar(empleado, observacion)
            remito.incidencias.append(IncidenciaEnvio(tipo=TipoIncidencia.EXTRAVIO, descripcion=observacion))
            cancelar_prestamos(remito)

    def registrar_incidencia(self, id, tipo, fecha, descripcion):
        tipo = validar_opcion(tipo, TipoIncidencia.TODOS, "tipo de incidencia")
        fecha = validar_fecha_no_futura(validar_fecha(fecha, "fecha"), "fecha")
        descripcion = validar_texto(descripcion, "descripción", LARGO_DESCRIPCION_INCIDENCIA, MINIMO_DESCRIPCION)
        with obtener_session() as session:
            remito = buscar_por_id(session, Remito, id, "el remito")
            if fecha < remito.fecha_creacion:
                raise ReglaNegocioError("La fecha de la incidencia no puede ser anterior a la creación del remito")
            remito.incidencias.append(IncidenciaEnvio(tipo=tipo, fecha=fecha, descripcion=descripcion))

    # ------------------------------------------------------------ consultas

    def prestamos_para_enviar(self, sede_origen_id, sede_destino_id):
        """[(id, texto)] de los préstamos interbibliotecarios aprobados entre
        ese par de sedes: son los que todavía esperan su remito de ida."""
        if sede_origen_id is None or sede_destino_id is None:
            return []
        with obtener_session() as session:
            prestamos = session.query(Prestamo).filter_by(
                tipo=TipoPrestamo.INTERBIBLIOTECARIO, estado=EstadoPrestamo.APROBADO,
                sede_origen_id=sede_origen_id, sede_destino_id=sede_destino_id).order_by(Prestamo.id).all()
            return [(prestamo.id, f"#{prestamo.id} - {prestamo.ejemplar.codigo_inventario} - "
                                  f"{prestamo.ejemplar.libro.titulo} - {prestamo.socio}")
                    for prestamo in prestamos]

    def listar(self):
        """Remitos listos para mostrar, los más nuevos primero."""
        with obtener_session() as session:
            remitos = session.query(Remito).order_by(Remito.id.desc()).all()
            return [
                {
                    'id': remito.id,
                    'nro_remito': remito.nro_remito,
                    'tipo': remito.tipo,
                    'origen': remito.sede_origen.nombre,
                    'destino': remito.sede_destino.nombre,
                    'estado': remito.estado,
                    'ejemplares': ", ".join([item.ejemplar.codigo_inventario for item in remito.items]),
                    'fecha_creacion': formatear_fecha(remito.fecha_creacion),
                    'fecha_despacho': formatear_fecha(remito.fecha_despacho),
                    'fecha_recepcion': formatear_fecha(remito.fecha_recepcion),
                }
                for remito in remitos
            ]

    def listar_movimientos(self, id):
        """Historial de estados del remito, en orden."""
        with obtener_session() as session:
            remito = buscar_por_id(session, Remito, id, "el remito")
            return [
                {
                    'id': movimiento.id,
                    'fecha_hora': movimiento.fecha_hora.strftime("%d/%m/%Y %H:%M"),
                    'estado_anterior': movimiento.estado_anterior or "",
                    'estado_nuevo': movimiento.estado_nuevo,
                    'empleado': str(movimiento.empleado),
                    'observacion': movimiento.observacion or "",
                }
                for movimiento in remito.movimientos
            ]

    def listar_incidencias(self, id):
        with obtener_session() as session:
            remito = buscar_por_id(session, Remito, id, "el remito")
            return [
                {
                    'id': incidencia.id,
                    'tipo': incidencia.tipo,
                    'fecha': formatear_fecha(incidencia.fecha),
                    'descripcion': incidencia.descripcion,
                }
                for incidencia in remito.incidencias
            ]
