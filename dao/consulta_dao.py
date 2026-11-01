"""Consulta de disponibilidad: cuántos ejemplares de cada título hay en cada
sede y en qué estado. La usan el personal y los socios (solo lectura).

La disponibilidad se cuenta sobre los ejemplares, no sobre el libro. Se
agrupa en Python con diccionarios, como en los apuntes (sin group_by).
"""

from constantes import EstadoEjemplar
from database import obtener_session
from modelos.catalogo import Libro
from modelos.sede import Sede
from validadores import normalizar_texto

# Estados que sacan al ejemplar de circulación
FUERA_DE_CIRCULACION = [EstadoEjemplar.DANADO, EstadoEjemplar.EXTRAVIADO, EstadoEjemplar.BAJA]
SIN_EJEMPLARES = "(sin ejemplares)"


def coincide(libro, texto):
    """True si el texto aparece en el título, en un autor o en el ISBN/ISSN."""
    if texto == "":
        return True
    donde_buscar = [libro.titulo, libro.isbn] + [str(autor) for autor in libro.autores]
    for valor in donde_buscar:
        if texto in valor.lower():
            return True
    return False


def fila_vacia(libro, nombre_sede):
    """Fila de un título con todos los contadores en 0."""
    return {
        'titulo': libro.titulo,
        'autores': ", ".join([str(autor) for autor in libro.autores]),
        'tipo': libro.tipo_material,
        'sede': nombre_sede,
        'disponibles': 0,
        'prestados': 0,
        'reservados': 0,
        'en_transito': 0,
        'fuera_de_circulacion': 0,
        'total': 0,
    }


def sumar_ejemplar(fila, ejemplar):
    fila['total'] += 1
    if ejemplar.estado == EstadoEjemplar.DISPONIBLE:
        fila['disponibles'] += 1
    elif ejemplar.estado == EstadoEjemplar.PRESTADO:
        fila['prestados'] += 1
    elif ejemplar.estado == EstadoEjemplar.RESERVADO:
        fila['reservados'] += 1
    elif ejemplar.estado == EstadoEjemplar.EN_TRANSITO:
        fila['en_transito'] += 1
    elif ejemplar.estado in FUERA_DE_CIRCULACION:
        fila['fuera_de_circulacion'] += 1


class ConsultaDAO:

    def disponibilidad(self, texto="", sede_id=None):
        """Una fila por título y sede. texto filtra por título, autor o ISBN
        (sin distinguir mayúsculas); sede_id None = todas las sedes.

        Un título que no tiene ejemplares (o no los tiene en la sede elegida)
        aparece igual, con disponibilidad 0."""
        texto = normalizar_texto(texto).lower()
        with obtener_session() as session:
            sede_elegida = None
            if sede_id is not None:
                sede_elegida = session.query(Sede).filter_by(id=sede_id).first()
            filas = []
            for libro in session.query(Libro).order_by(Libro.titulo).all():
                if not coincide(libro, texto):
                    continue
                por_sede = {}  # nombre de la sede -> fila con sus contadores
                for ejemplar in libro.ejemplares:
                    if sede_elegida is not None and ejemplar.sede is not sede_elegida:
                        continue
                    if ejemplar.sede.nombre not in por_sede:
                        por_sede[ejemplar.sede.nombre] = fila_vacia(libro, ejemplar.sede.nombre)
                    sumar_ejemplar(por_sede[ejemplar.sede.nombre], ejemplar)
                if len(por_sede) == 0:
                    nombre = sede_elegida.nombre if sede_elegida is not None else SIN_EJEMPLARES
                    por_sede[nombre] = fila_vacia(libro, nombre)
                for nombre in sorted(por_sede.keys()):
                    filas.append(por_sede[nombre])
            # Cada fila necesita un id para el Treeview
            for numero in range(len(filas)):
                filas[numero]['id'] = numero + 1
            return filas
