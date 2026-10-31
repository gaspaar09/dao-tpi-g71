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
Instala `sqlalchemy` y `pytest`.

### 5. Ejecutar el sistema
```
python main.py
```
Se abre la ventana principal. La primera vez se crea el archivo `biblioteca.db` en la raíz del proyecto. No se sube al repositorio y se puede borrar para empezar con la base vacía.

### 6. Ejecutar los tests
```
python -m pytest
```
Hay que ejecutarlo desde la raíz del proyecto, así pytest encuentra los módulos. Mientras no haya tests, pytest informa "no tests ran"; no es un error.

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

## Estado
Fase 0 (setup) terminada: la ventana abre con las pestañas vacías. Las siguientes fases están en `CLAUDE.md`, sección "Plan de trabajo".
