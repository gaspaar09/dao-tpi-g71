"""Funciones que comparten los reportes."""


def formatear_monto(valor):
    return f"${valor:.2f}"


def formatear_fecha(fecha):
    if fecha is None:
        return ""
    return fecha.strftime("%d/%m/%Y")


def numerar(filas):
    """El Treeview necesita un id por fila: se numeran en orden."""
    for numero in range(len(filas)):
        filas[numero]['id'] = numero + 1
    return filas


def porcentaje(parte, total):
    """Porcentaje con un decimal, o "—" si no hay nada que medir (evita dividir por 0)."""
    if total == 0:
        return "—"
    return f"{round(parte * 100 / total, 1)}%"
