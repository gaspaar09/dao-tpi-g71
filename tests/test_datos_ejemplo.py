from dao.ejemplar_dao import EjemplarDAO
from dao.empleado_dao import EmpleadoDAO
from dao.libro_dao import LibroDAO
from dao.prestamo_dao import PrestamoDAO
from dao.remito_dao import RemitoDAO
from dao.reserva_dao import ReservaDAO
from dao.sede_dao import SedeDAO
from dao.socio_dao import SocioDAO
from constantes import EstadoEjemplar, EstadoPrestamo, EstadoRemito, EstadoReserva, TipoEnvio
from datos_ejemplo import cargar_datos_ejemplo
from tests.auxiliares import preparar_base_en_memoria


class TestDatosEjemplo:
    def test_carga_una_sola_vez(self):
        preparar_base_en_memoria()
        assert cargar_datos_ejemplo() is True
        assert cargar_datos_ejemplo() is False
        assert len(SedeDAO().listar()) == 3

    def test_datos_coherentes(self):
        preparar_base_en_memoria()
        cargar_datos_ejemplo()
        assert len(EmpleadoDAO().listar()) == 3
        assert len(SocioDAO().listar()) == 4
        assert len(SocioDAO().opciones()) == 3  # uno está inhabilitado
        assert len(LibroDAO().listar()) == 5
        assert len(EjemplarDAO().listar()) == 15

    def test_hay_un_caso_por_estado(self):
        """Para probar cada botón hace falta un préstamo y un remito en cada estado."""
        preparar_base_en_memoria()
        cargar_datos_ejemplo()
        estados_prestamos = [fila['estado'] for fila in PrestamoDAO().listar()]
        for estado in [EstadoPrestamo.SOLICITADO, EstadoPrestamo.APROBADO, EstadoPrestamo.EN_ENVIO,
                       EstadoPrestamo.ACTIVO, EstadoPrestamo.VENCIDO, EstadoPrestamo.CANCELADO]:
            assert estado in estados_prestamos
        assert set([fila['estado'] for fila in RemitoDAO().listar()]) == set(EstadoRemito.TODOS)
        assert set([fila['estado'] for fila in ReservaDAO().listar()]) == set(EstadoReserva.TODOS)
        assert EstadoPrestamo.DEVUELTO in estados_prestamos
        assert "$900.00 (9 días) - PENDIENTE" in [fila['multa'] for fila in PrestamoDAO().listar()]
        assert TipoEnvio.DEVOLUCION in [fila['tipo'] for fila in RemitoDAO().listar()]
        # Quedan ejemplares libres en las tres sedes para probar préstamos nuevos
        libres = [fila['sede'] for fila in EjemplarDAO().listar() if fila['estado'] == EstadoEjemplar.DISPONIBLE]
        assert len(set(libres)) == 3
        estados_ejemplares = [fila['estado'] for fila in EjemplarDAO().listar()]
        for estado in [EstadoEjemplar.RESERVADO, EstadoEjemplar.PRESTADO, EstadoEjemplar.EN_TRANSITO,
                       EstadoEjemplar.EXTRAVIADO]:
            assert estado in estados_ejemplares
