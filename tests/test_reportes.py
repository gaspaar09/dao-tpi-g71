from datetime import date, timedelta

from constantes import EstadoFisico, EstadoPrestamo, TipoIncidencia, TipoPrestamo
from dao.devolucion_dao import DevolucionDAO
from dao.prestamo_dao import PrestamoDAO
from dao.remito_dao import RemitoDAO
from database import obtener_session
from datos_ejemplo import cargar_datos_ejemplo
from modelos.remito import Remito
from reportes import REPORTES
from reportes.disponibilidad_por_sede import disponibilidad_por_sede
from reportes.envios_e_incidencias import tasa_envios_e_incidencias
from reportes.mas_solicitados import libros_mas_solicitados_interbibliotecarios
from reportes.movimiento_entre_sedes import movimiento_entre_sedes
from reportes.prestamos_activos import prestamos_activos_y_transito
from reportes.vencidos_y_multas import vencidos_y_multas_por_socio
from tests.auxiliares import preparar_base_en_memoria
from tests.test_devolucion_dao import correr_fechas, prestamo_local_activo
from tests.test_remito_dao import preparar, aprobar_inter, crear_remito

prestamos = PrestamoDAO()
remitos = RemitoDAO()
HOY = date.today().strftime("%d/%m/%Y")


def filas(reporte):
    return reporte()[1]


def recibir(remito_id, ids):
    for _ in range(3):
        remitos.avanzar(remito_id, ids['empleado'], "")


class TestTodosLosReportes:
    def test_base_vacia(self):
        """Sin datos no fallan (ni dividen por cero)."""
        preparar_base_en_memoria()
        for nombre, reporte in REPORTES.items():
            columnas, resultado = reporte()
            assert len(columnas) > 0
            for fila in resultado:
                assert 'id' in fila

    def test_cada_fila_tiene_todas_sus_columnas(self):
        preparar_base_en_memoria()
        cargar_datos_ejemplo()
        for nombre, reporte in REPORTES.items():
            columnas, resultado = reporte()
            assert len(resultado) > 0, nombre
            for fila in resultado:
                for clave, titulo, ancho in columnas:
                    assert clave in fila, (nombre, clave)


class TestPrestamosActivosYTransito:
    def test_activos_vencidos_y_en_transito(self):
        ids = preparar()
        local = prestamo_local_activo(ids, 0)
        correr_fechas(local, 40)
        remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][1])])
        remitos.avanzar(remito_id, ids['empleado'], "")
        resultado = filas(prestamos_activos_y_transito)
        assert [(fila['ejemplar'], fila['estado']) for fila in resultado] == [
            ("EJ-001", EstadoPrestamo.VENCIDO), ("EJ-002", "DESPACHADO")]
        assert resultado[1]['remito'] == "REM-000001"
        assert resultado[1]['categoria'] == "En tránsito (ida)"


class TestVencidosYMultas:
    def test_ordena_por_deuda(self):
        ids = preparar()
        con_multa = prestamo_local_activo(ids, 0)
        correr_fechas(con_multa, 41)  # 10 días de atraso: $1000
        DevolucionDAO().registrar(con_multa, HOY, EstadoFisico.BUENO, "", ids['empleado'])
        vencido = prestamo_local_activo(ids, 1)
        correr_fechas(vencido, 35)
        resultado = filas(vencidos_y_multas_por_socio)
        assert len(resultado) == 1  # los dos son del mismo socio
        fila = resultado[0]
        assert (fila['vencidos'], fila['multas'], fila['pendiente'], fila['pagado']) == (1, 1, "$1000.00", "$0.00")
        prestamos.pagar_multa(con_multa)
        assert filas(vencidos_y_multas_por_socio)[0]['pagado'] == "$1000.00"

    def test_sin_vencidos_ni_multas_no_aparece(self):
        ids = preparar()
        prestamo_local_activo(ids)
        assert filas(vencidos_y_multas_por_socio) == []


class TestMasSolicitados:
    def test_cuenta_solicitudes_y_completados(self):
        ids = preparar()
        recibido = aprobar_inter(ids, ids['ejemplares'][0])
        recibir(crear_remito(ids, [recibido]), ids)
        prestamos.cancelar(aprobar_inter(ids, ids['ejemplares'][1]))
        prestamos.solicitar(TipoPrestamo.LOCAL, ids['socio'], ids['ejemplares'][1], ids['central'], None)
        fila = filas(libros_mas_solicitados_interbibliotecarios)[0]
        # El préstamo local no cuenta
        assert (fila['libro'], fila['solicitudes'], fila['completados'], fila['cancelados']) == ("Rayuela", 2, 1, 1)
        assert fila['efectividad'] == "50.0%"
        assert fila['ruta'] == "Central -> Norte (2)"


class TestDisponibilidadPorSede:
    def test_conteo_y_porcentaje(self):
        ids = preparar()
        prestamo_local_activo(ids, 0)
        por_sede = dict((fila['sede'], fila) for fila in filas(disponibilidad_por_sede))
        central = por_sede['Central']
        assert (central['titulos'], central['total'], central['disponibles'], central['prestados']) == (1, 2, 1, 1)
        assert central['porcentaje'] == "50.0%"
        assert por_sede['Norte']['porcentaje'] == "—"  # sin ejemplares


class TestEnviosEIncidencias:
    def test_tasa_de_exito(self):
        ids = preparar()
        recibir(crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])]), ids)
        perdido = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][1])])
        remitos.avanzar(perdido, ids['empleado'], "")
        remitos.avanzar(perdido, ids['empleado'], "")
        remitos.registrar_incidencia(perdido, TipoIncidencia.DEMORA, HOY, "Retraso del transporte")
        remitos.extraviar(perdido, ids['empleado'], "No llegó a destino")
        por_concepto = dict((fila['concepto'], fila) for fila in filas(tasa_envios_e_incidencias))
        ida = por_concepto["Remitos IDA"]
        assert (ida['remitos'], ida['despachados'], ida['recibidos'], ida['extraviados']) == (2, 2, 1, 1)
        assert ida['tasa'] == "50.0%"
        assert ida['incidencias'] == 2
        assert por_concepto["Remitos DEVOLUCION"]['tasa'] == "—"
        assert por_concepto["Incidencias: EXTRAVIO"]['incidencias'] == 1
        assert por_concepto["Incidencias: DEMORA"]['incidencias'] == 1

    def test_cancelado_no_baja_la_tasa(self):
        ids = preparar()
        recibir(crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])]), ids)
        remitos.cancelar(crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][1])]), ids['empleado'],
                         "El socio desistió")
        total = [fila for fila in filas(tasa_envios_e_incidencias) if fila['concepto'] == "Total"][0]
        assert (total['cancelados'], total['tasa']) == (1, "100.0%")


class TestMovimientoEntreSedes:
    def test_promedio_de_transito(self):
        ids = preparar()
        for indice, dias in [(0, 2), (1, 5)]:
            remito_id = crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][indice])])
            recibir(remito_id, ids)
            with obtener_session() as session:
                session.query(Remito).filter_by(id=remito_id).first().fecha_despacho = \
                    date.today() - timedelta(days=dias)
        fila = filas(movimiento_entre_sedes)[0]
        assert (fila['origen'], fila['destino'], fila['remitos'], fila['ejemplares']) == ("Central", "Norte", 2, 2)
        assert fila['promedio'] == 3.5

    def test_sin_recibidos_y_cancelados(self):
        ids = preparar()
        crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][0])])
        remitos.cancelar(crear_remito(ids, [aprobar_inter(ids, ids['ejemplares'][1])]), ids['empleado'],
                         "El socio desistió")
        resultado = filas(movimiento_entre_sedes)
        assert len(resultado) == 1
        assert (resultado[0]['remitos'], resultado[0]['recibidos'], resultado[0]['promedio']) == (1, 0, "—")
