"""Constantes de configuración del sistema.

Se juntan acá para no repetir números sueltos en el código y poder
cambiarlos en un solo lugar.
"""

# Base de datos (SQLite, como en el ejemplo de biblioteca de los apuntes)
DB_URL = "sqlite:///biblioteca.db"

# Plazos y multas por tipo de préstamo (los usa el patrón Strategy).
# Valores confirmados por el grupo.
DIAS_PRESTAMO_LOCAL = 31
MULTA_DIARIA_LOCAL = 100.0
DIAS_PRESTAMO_INTERBIBLIOTECARIO = 38
MULTA_DIARIA_INTERBIBLIOTECARIO = 150.0

# Plazos de la reserva: espera mientras está PENDIENTE y días para
# retirar el ejemplar una vez que pasa a DISPONIBLE.
DIAS_ESPERA_RESERVA = 45
DIAS_RETIRO_RESERVA = 2

# Largos máximos de los campos de texto (docs/VALIDACIONES.md).
# Se usan en las columnas String(n) y en los validadores.
LARGO_NOMBRE_SEDE = 80
LARGO_DIRECCION = 120
LARGO_EMAIL = 100
LARGO_TELEFONO = 15  # solo dígitos, sin el código de país
LARGO_PREFIJO = 3     # código de país, por ejemplo "54" o "598"
LARGO_LEGAJO = 20
LARGO_NOMBRE_EMPLEADO = 80
LARGO_NOMBRE_PERSONA = 50
LARGO_ISBN = 20
LARGO_TITULO = 150
LARGO_EDITORIAL = 80
LARGO_IDIOMA = 30
LARGO_CODIGO_INVENTARIO = 20
LARGO_OBSERVACIONES = 300
LARGO_OBSERVACION_MOVIMIENTO = 200
LARGO_DESCRIPCION_INCIDENCIA = 300
LARGO_ESTADO = 20

# Límites numéricos de los validadores
MAXIMO_ENTERO = 999999999  # evita que un número enorme desborde el entero de SQLite
ANIO_MINIMO_EDICION = 1450  # imprenta de Gutenberg
DNI_MINIMO = 1000000
DNI_MAXIMO = 99999999
