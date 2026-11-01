"""Patrón State: ciclo de vida del Remito.

Mismo esquema que el semáforo de los apuntes: el Remito es el contexto,
tiene cambiar_estado() y delega en su estado actual. Es el estado el que
decide la transición (avanzar equivale al siguiente() del semáforo).

En la clase base, las acciones lanzan TransicionInvalidaError; cada estado
concreto sobrescribe solo las que admite:

    EMPAQUETADO -> avanzar: DESPACHADO, cancelar: CANCELADO
    DESPACHADO  -> avanzar: EN_TRANSITO
    EN_TRANSITO -> avanzar: RECIBIDO, extraviar: EXTRAVIADO
    RECIBIDO, CANCELADO, EXTRAVIADO: estados finales

Los estados no importan los modelos (reciben el remito por parámetro), así
no hay imports circulares. Tampoco conocen préstamos ni estrategias: los
préstamos los actualiza RemitoDAO.
"""

from abc import ABC, abstractmethod
from datetime import date

from constantes import EstadoEjemplar, EstadoRemito, TipoEnvio
from excepciones import TransicionInvalidaError


def cambiar_estado_ejemplares(remito, nuevo_estado):
    """Efecto colateral común: todos los ejemplares del remito pasan a nuevo_estado."""
    for item in remito.items:
        item.ejemplar.cambiar_estado(nuevo_estado)


class EstadoRemitoBase(ABC):
    """Contrato común. Por defecto ninguna acción está permitida."""

    @abstractmethod
    def codigo(self):
        """Constante de EstadoRemito que se guarda en la base."""
        pass

    def entrar(self, remito, empleado, observacion):
        """Efectos al llegar a este estado. Por defecto, ninguno."""
        pass

    def salir(self, remito):
        """Efectos al dejar este estado. Por defecto, ninguno."""
        pass

    def avanzar(self, remito, empleado, observacion):
        raise TransicionInvalidaError(f"Un remito {self.codigo()} no puede avanzar de estado")

    def cancelar(self, remito, empleado, observacion):
        raise TransicionInvalidaError(f"Un remito {self.codigo()} no se puede cancelar")

    def extraviar(self, remito, empleado, observacion):
        raise TransicionInvalidaError(f"Un remito {self.codigo()} no se puede dar por extraviado")

    def quitar_item(self, remito, item, empleado, observacion):
        raise TransicionInvalidaError(
            f"Un remito {self.codigo()} ya salió: no se le pueden quitar ejemplares")


class RemitoEmpaquetado(EstadoRemitoBase):
    def codigo(self):
        return EstadoRemito.EMPAQUETADO

    def avanzar(self, remito, empleado, observacion):
        remito.cambiar_estado(EstadoRemito.DESPACHADO, empleado, observacion)

    def cancelar(self, remito, empleado, observacion):
        remito.cambiar_estado(EstadoRemito.CANCELADO, empleado, observacion)

    def quitar_item(self, remito, item, empleado, observacion):
        """Mientras no se despachó se puede sacar un ejemplar. Si era el
        único, se cancela el remito entero (el ítem queda para el historial)."""
        if len(remito.items) == 1:
            remito.cambiar_estado(EstadoRemito.CANCELADO, empleado, observacion)
        else:
            remito.items.remove(item)


class RemitoDespachado(EstadoRemitoBase):
    def codigo(self):
        return EstadoRemito.DESPACHADO

    def entrar(self, remito, empleado, observacion):
        remito.fecha_despacho = date.today()
        cambiar_estado_ejemplares(remito, EstadoEjemplar.EN_TRANSITO)

    def avanzar(self, remito, empleado, observacion):
        remito.cambiar_estado(EstadoRemito.EN_TRANSITO, empleado, observacion)


class RemitoEnTransito(EstadoRemitoBase):
    def codigo(self):
        return EstadoRemito.EN_TRANSITO

    def avanzar(self, remito, empleado, observacion):
        remito.cambiar_estado(EstadoRemito.RECIBIDO, empleado, observacion)

    def extraviar(self, remito, empleado, observacion):
        remito.cambiar_estado(EstadoRemito.EXTRAVIADO, empleado, observacion)


class RemitoRecibido(EstadoRemitoBase):
    """Estado final. En un remito de IDA el ejemplar pasa a PRESTADO cuando
    RemitoDAO activa el préstamo; en uno de DEVOLUCION vuelve a circular."""

    def codigo(self):
        return EstadoRemito.RECIBIDO

    def entrar(self, remito, empleado, observacion):
        remito.fecha_recepcion = date.today()
        if remito.tipo == TipoEnvio.DEVOLUCION:
            # Disponible, o fuera de circulación si el socio lo devolvió dañado
            for item in remito.items:
                item.ejemplar.volver_a_circular()


class RemitoCancelado(EstadoRemitoBase):
    """Estado final. En una IDA los ejemplares no salieron: vuelven a estar
    disponibles. En una DEVOLUCION el ejemplar sigue esperando un nuevo
    remito que lo lleve a su sede, así que no cambia."""

    def codigo(self):
        return EstadoRemito.CANCELADO

    def entrar(self, remito, empleado, observacion):
        if remito.tipo == TipoEnvio.IDA:
            cambiar_estado_ejemplares(remito, EstadoEjemplar.DISPONIBLE)


class RemitoExtraviado(EstadoRemitoBase):
    """Estado final: los ejemplares quedan fuera de circulación."""

    def codigo(self):
        return EstadoRemito.EXTRAVIADO

    def entrar(self, remito, empleado, observacion):
        cambiar_estado_ejemplares(remito, EstadoEjemplar.EXTRAVIADO)


# El remito guarda solo el texto del estado; este diccionario da la instancia.
# Los estados no guardan datos propios, así que alcanza con una de cada uno.
ESTADOS_REMITO = {
    EstadoRemito.EMPAQUETADO: RemitoEmpaquetado(),
    EstadoRemito.DESPACHADO: RemitoDespachado(),
    EstadoRemito.EN_TRANSITO: RemitoEnTransito(),
    EstadoRemito.RECIBIDO: RemitoRecibido(),
    EstadoRemito.CANCELADO: RemitoCancelado(),
    EstadoRemito.EXTRAVIADO: RemitoExtraviado(),
}
