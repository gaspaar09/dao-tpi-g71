"""Excepciones propias del sistema.

Definidas como en los apuntes ("Excepciones definidas por el programador"):
heredan de Exception y guardan el mensaje. La interfaz captura
ValidacionError y ReglaNegocioError y muestra el mensaje al usuario.
"""


class ValidacionError(Exception):
    """Se dispara cuando un dato ingresado tiene un formato inválido."""

    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class ReglaNegocioError(Exception):
    """Se dispara cuando una operación viola una regla de negocio."""

    def __init__(self, mensaje):
        self.mensaje = mensaje
        super().__init__(self.mensaje)


class TransicionInvalidaError(ReglaNegocioError):
    """Se dispara cuando un estado no admite la transición pedida (patrón State).

    Hereda de ReglaNegocioError para que la interfaz la capture igual.
    """

    def __init__(self, mensaje):
        super().__init__(mensaje)
