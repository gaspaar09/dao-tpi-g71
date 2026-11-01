from constantes import TipoMaterial, TipoPrestamo
from dao.autor_dao import AutorDAO
from dao.categoria_dao import CategoriaDAO
from dao.consulta_dao import ConsultaDAO, SIN_EJEMPLARES
from dao.libro_dao import LibroDAO
from dao.prestamo_dao import PrestamoDAO
from tests.test_remito_dao import preparar

dao = ConsultaDAO()


def contadores(fila):
    return (fila['disponibles'], fila['prestados'], fila['reservados'], fila['en_transito'],
            fila['fuera_de_circulacion'], fila['total'])


class TestDisponibilidad:
    def test_cuenta_por_estado(self):
        ids = preparar()  # Rayuela: EJ-001 y EJ-002 en Central
        PrestamoDAO().solicitar(TipoPrestamo.LOCAL, ids['socio'], ids['ejemplares'][0], ids['central'], None)
        PrestamoDAO().aprobar(PrestamoDAO().listar()[0]['id'])
        filas = dao.disponibilidad()
        assert len(filas) == 1
        assert (filas[0]['titulo'], filas[0]['sede'], filas[0]['autores']) == ("Rayuela", "Central", "Julio Cortázar")
        assert contadores(filas[0]) == (1, 1, 0, 0, 0, 2)

    def test_filtro_por_texto_sin_distinguir_mayusculas(self):
        preparar()
        for texto in ["rayu", "CORTÁZAR", "9789500700011", "  julio  "]:
            assert [fila['titulo'] for fila in dao.disponibilidad(texto)] == ["Rayuela"]
        assert dao.disponibilidad("borges") == []

    def test_filtro_por_sede(self):
        ids = preparar()
        assert contadores(dao.disponibilidad("", ids['central'])[0]) == (2, 0, 0, 0, 0, 2)
        # En Norte no hay ejemplares: el título aparece igual, con 0
        fila = dao.disponibilidad("", ids['norte'])[0]
        assert (fila['sede'], contadores(fila)) == ("Norte", (0, 0, 0, 0, 0, 0))

    def test_titulo_sin_ejemplares(self):
        preparar()
        LibroDAO().crear("9789500700042", "La invención de Morel", "Losada", "1940", "Español", TipoMaterial.LIBRO,
                         CategoriaDAO().opciones()[0][0], [AutorDAO().opciones()[0][0]])
        fila = dao.disponibilidad("morel")[0]
        assert (fila['sede'], fila['total']) == (SIN_EJEMPLARES, 0)
