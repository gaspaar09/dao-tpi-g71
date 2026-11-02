# Biblioteca: Sistema de Préstamos Interbibliotecarios

TP Integrador de Desarrollo de Aplicaciones con Objetos (UTN-FRC), Grupo 71.
Aplicación de escritorio en Python con Tkinter, SQLite y SQLAlchemy.

## Requisitos
- **Python 3.10 o superior** con Tkinter (viene incluido en el instalador oficial de python.org).
- Git.

Para verificar la versión:
```
python --version
```
En macOS o Linux puede ser `python3` en lugar de `python`.

## Primera ejecución

### 1. Clonar el repositorio
```
git clone https://github.com/gaspaar09/dao-tpi-g71.git
cd dao-tpi-g71
```

### 2. Crear el entorno virtual
```
python -m venv .venv
```

### 3. Activar el entorno virtual
| Sistema | Comando |
|---|---|
| Windows (PowerShell) | `.venv\Scripts\Activate.ps1` |
| Windows (cmd) | `.venv\Scripts\activate.bat` |
| Windows (Git Bash) | `source .venv/Scripts/activate` |
| macOS / Linux | `source .venv/bin/activate` |

Cuando está activo, la consola muestra `(.venv)` al principio de la línea. Hay que activarlo cada vez que se abre una consola nueva.

> Si PowerShell dice que "la ejecución de scripts está deshabilitada", ejecutá una vez
> `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned` y volvé a intentar.

### 4. Instalar las dependencias
```
pip install -r requirements.txt
```
Instala `sqlalchemy`, `pytest` y `ttkbootstrap` (los temas de la interfaz). Si ya tenías el entorno armado, volvé a correr este comando.

### 5. Ejecutar el sistema
```
python main.py
```
Se abre la ventana principal. La primera vez se crea el archivo `biblioteca.db` en la raíz del proyecto. No se sube al repositorio y se puede borrar para empezar con la base vacía.

### 6. Ejecutar los tests
```
python -m pytest
```
Hay que ejecutarlo desde la raíz del proyecto, así pytest encuentra los módulos.

## Primer recorrido
1. Arriba de la ventana, tocá **Cargar datos de ejemplo** (solo carga si la base está vacía). Trae sedes, socios, catálogo y ejemplares, y además préstamos, remitos y reservas en cada uno de sus estados.
2. Elegí el **Empleado actual**: sin él no se pueden registrar préstamos, reservas, devoluciones ni remitos.
3. Todas las pestañas se usan igual: a la izquierda de la barra de botones está la acción principal (**Nuevo socio**, **Nueva solicitud**...), que abre un formulario en una ventana aparte; para operar sobre un registro, elegilo en la tabla y usá los botones que siguen en esa barra (doble clic en una fila también la edita). En Sedes, Empleados, Socios, Catálogo y Ejemplares, cada fila tiene al final los íconos ✏ (editar) y 🗑 (dar de baja o eliminar). En Préstamos, Reservas y Remitos, **Cancelar** es el botón rojo a la derecha de todo de la barra. Lo que borra o bloquea está a la derecha, en rojo.
   - **Sedes, Empleados, Socios, Catálogo, Ejemplares:** altas, modificaciones y bajas.
   - **Préstamos:** solicitar, aprobar, cancelar, registrar la devolución y marcar multas pagadas.
   - **Reservas:** reservar un título en una sede, retirar (crea el préstamo) y cancelar.
   - **Remitos:** armar el envío, avanzar su estado, cancelar, dar por extraviado, historial e incidencias.
   - **Consulta de disponibilidad:** buscar por título, autor o ISBN y filtrar por sede; no pide empleado.
   - **Reportes:** elegir uno de los 6 reportes en el desplegable; se actualiza solo después de cada operación.

## En VS Code
1. Abrí la carpeta del proyecto.
2. `Ctrl+Shift+P` → **Python: Select Interpreter** → elegí el que está en `.venv`.
3. Las terminales nuevas activan el entorno solas.

## Problemas frecuentes
| Problema | Solución |
|---|---|
| `ModuleNotFoundError: No module named 'sqlalchemy'` | El entorno virtual no está activo o faltó el paso 4. |
| `ModuleNotFoundError: No module named 'tkinter'` | En Linux: `sudo apt install python3-tk`. En Windows o macOS, reinstalar Python desde python.org. |
| Error raro en la base después de cambiar los modelos | Cerrá la aplicación, borrá `biblioteca.db` y volvé a ejecutar `python main.py`. |
| `python` no se reconoce | Probá con `py` (Windows) o `python3` (macOS/Linux). |

## Estructura
```
main.py          punto de entrada: crea las tablas y abre la ventana
config.py        constantes: base de datos, plazos, multas, largos máximos
database.py      motor, sesiones y obtener_session()
constantes.py    enumeraciones del diagrama como constantes de texto
excepciones.py   ValidacionError, ReglaNegocioError, TransicionInvalidaError
modelos/         entidades SQLAlchemy
patrones/        State (remito) y Strategy (préstamo)
dao/             acceso a datos y reglas de negocio
reportes/        reportes de gestión
ui/              pestañas de la interfaz
tests/           tests con pytest
docs/            enunciado, propuesta, diagrama, validaciones y apuntes
```

## Documentación
- `CLAUDE.md`: reglas de implementación, arquitectura y plan de trabajo por fases.
- `docs/TPI_ENUNCIADO.md`: consigna oficial.
- `docs/PROPUESTA.md`: propuesta del grupo.
- `docs/diagrama-clases.mmd`: diagrama de clases vigente.
- `docs/VALIDACIONES.md`: checklist de validaciones y guion de pruebas para la defensa.
- `docs/DEFENSA.md`: guion de la defensa (demo, casos inválidos, patrones, capítulos de los apuntes y preguntas probables).

## Estado
Fases 0 a 8 terminadas: todos los procesos obligatorios, los dos patrones (State y Strategy), los 6 reportes y la pasada por el checklist de validaciones. Para preparar la defensa, ver `docs/DEFENSA.md`.
