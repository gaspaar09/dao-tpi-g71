# TP Integrador DAO — Biblioteca: Sistema de Préstamos Interbibliotecarios

UTN-FRC · Desarrollo de Aplicaciones con Objetos · Grupo 71 · Tema 1 (Biblioteca).
El TP se **defiende oralmente, con código**, y los profes prueban todos los campos con datos inválidos (negativos, letras en campos numéricos, fechas pasadas, vacíos, duplicados, etc.).
Respondé siempre en español.

## Regla principal: implementar solo con lo visto en clase
`docs/APUNTES.md` reúne todo lo que se dio durante el año y es la **referencia obligatoria de cómo se implementa**. El grupo tiene que poder justificar cada línea del TP con algo visto en clase.

1. Antes de implementar cada parte, buscá en `APUNTES.md` cómo se hizo ahí y copiá ese estilo. **No lo leas entero** (pesa ~370 KB): usá grep por título (tabla de abajo).
2. No uses otra librería, sintaxis o técnica si existe una equivalente en los apuntes.
3. Si algo es *realmente necesario* y no está en los apuntes: **pará y preguntá**, explicando por qué es necesario y qué alternativa vista descartaste. No lo agregues en silencio.
4. Al terminar cada fase, listá qué capítulos de los apuntes usaste y dónde, para que el grupo prepare la defensa.

**Modelo a seguir:** el capítulo "ORM con SQLAlchemy", sección *Ejemplo completo: Sistema de biblioteca*. Tiene modelos con `declarative_base`, un DAO por entidad, `obtener_session()` como context manager, reglas de negocio con excepciones y la interacción con el usuario separada del acceso a datos.

### Dónde buscar en APUNTES.md (títulos para grep)
| Tema | Título |
|---|---|
| Excepciones propias (`class X(Exception)`) | "Excepciones definidas por el programador" |
| Clases, propiedades, `__str__` | "Encapsulamiento", "Propiedades", "Métodos mágicos" |
| Composición, herencia, clases abstractas | "Composición", "Herencia", "Polimorfismo", "Clases y métodos abstractos" |
| Tests | "Testing unitario", "Pytest" |
| Acceso a datos | "Patrón DAO", "ORM con SQLAlchemy", "Relaciones entre tablas", "Context managers y gestión de sesiones" |
| State y Strategy | "Patrones State y Strategy" |
| Interfaz gráfica | "Interfaces graficas en python", "Validar texto", "Eventos en Tkinter", "Clase TTK" y los ejercicios de formularios del final |

### No visto en clase → qué usar en cambio
| No usar | Usar |
|---|---|
| Flask / web | Tkinter + ttk |
| `enum.Enum` | Clases de constantes de texto (`class EstadoRemito: EMPAQUETADO = "EMPAQUETADO"`) y columnas `String`, como `estado = Column(String(20))` en los apuntes |
| `Decimal` | `Float` + `round(x, 2)` |
| `re` (regex) | Métodos de `str` (`strip`, `split`, `replace`, `isalpha`, `isnumeric`, `in`, `len`) y `try: int(...) except ValueError` |
| SQLAlchemy 2.0 (`Mapped[]`, `DeclarativeBase`, `select()`) | `declarative_base()`, `Column`, `session.query()` (estilo clásico de los apuntes) |
| `func.count`, `group_by` | Traer filas con `query` y relaciones, y agrupar en Python con diccionarios, `sorted(..., key=lambda ...)`, `sum`, `len` |
| `strptime` | `date(anio, mes, dia)` armado con `split("/")`; lanza `ValueError` en fechas imposibles como 30/02 |
| `dataclasses`, `typing` | Clases normales |
| `pytest.mark.parametrize`, fixtures | Clases `TestXxx`, bucles `for` con `pytest.raises` y funciones auxiliares |
| `unittest`, `mock` | Solo `pytest` |
| `StringVar`, `tkcalendar`, `customtkinter` | Un `ttk.Notebook` con pestañas, `entry.get()`, fechas como `ttk.Combobox` editable (lista de días recientes y texto dd/mm/aaaa) |
| `logging`, `os`, `pathlib`, `argparse` | No usar |

### Excepciones ya aprobadas (necesarias y mínimas)
- `foreign_keys=[...]` en `relationship()` cuando una clase tiene dos claves foráneas a `Sede` (`sede_origen` y `sede_destino`): SQLAlchemy lo exige. Dejar un comentario en el código.
- `tkinter.messagebox` para los cuadros de diálogo (los ejercicios de formularios de los apuntes piden "cuadro de diálogo" y "ventana emergente").
- `ttk.Combobox(..., state="readonly")`: es una opción del widget visto y evita texto libre en los desplegables.
- Módulos que sí aparecen en los apuntes: `contextlib.contextmanager`, `abc`, `datetime` (`date`, `datetime`, `time`, `timedelta`).

## Cómo trabajar en este repo
- Cada integrante tiene que **entender y poder explicar** todo el código. Priorizá código simple y claro sobre código "ingenioso". Nada de abstracciones que el enunciado no pide.
- Trabajá **por fases** (ver "Plan de trabajo"). Al terminar cada una: resumen corto de qué hiciste y por qué, qué probar a mano y qué supuestos tomaste. No pases a la fase siguiente sin que el usuario lo confirme.
- Si el enunciado, la propuesta y el diagrama se contradicen, o falta un dato de negocio: **preguntá**, no decidas solo.
- Comentarios y docstrings en español, breves, explicando el *por qué* (estilo de los apuntes).
- No hagas commit ni push salvo que te lo pidan. Cuando te lo pidan: commits en español, formato Conventional Commits (`feat:`, `fix:`, `docs:`, `test:`, `refactor:`).

## Fuentes de verdad
Orden de precedencia: `TPI_ENUNCIADO.md` > este archivo > `diagrama-clases.mmd` > `PROPUESTA.md`.

| Archivo | Para qué |
|---|---|
| `docs/TPI_ENUNCIADO.md` | Consigna oficial: procesos obligatorios, validaciones, reportes, mínimo 2 patrones y 4 reportes. |
| `docs/PROPUESTA.md` | Propuesta del grupo: objetivos, alcances, ciclo de vida del remito, supuestos, enumeraciones y notas del modelo. **Leela completa antes de empezar** (es corta). Está actualizada con las decisiones de este archivo. |
| `docs/diagrama-clases.mmd` (+ `.png`) | **Modelo de clases vigente** (dominio, enumeraciones y patrones). |
| `docs/TP-Biblioteca-Propuesta.pdf` | PDF original de la propuesta. |
| `docs/VALIDACIONES.md` | Checklist de validaciones por entidad. **Leelo antes de escribir DAOs, validadores o formularios.** |
| `docs/APUNTES.md` | Apuntes de la cátedra: ver "Regla principal". |

## Stack
- **Python 3.10+**, entorno virtual `.venv`. `requirements.txt`: `sqlalchemy`, `pytest`, `ttkbootstrap`.
- **Persistencia:** SQLite + SQLAlchemy ORM, estilo clásico de los apuntes.
- **Interfaz:** Tkinter + ttk, de escritorio.
- **Tests:** pytest. Ejecutar con `python -m pytest` desde la raíz, así encuentra los módulos del proyecto.
- Se ejecuta con `python main.py`.

## Arquitectura
```
main.py                  # crea las tablas y abre la ventana principal (como el main() del ejemplo de biblioteca)
config.py                # constantes: DB_URL, plazos y multas, largos máximos
database.py              # engine, Base, Session, obtener_session(), crear_tablas()
constantes.py            # "enumeraciones" del diagrama como clases de constantes de texto
excepciones.py           # ValidacionError, ReglaNegocioError, TransicionInvalidaError
validadores.py           # funciones de validación de formato: texto, números, fechas, email, teléfono, etc.
modelos/                 # entidades SQLAlchemy (una clase por entidad del diagrama)
patrones/
  estado_remito.py       # State
  estrategia_prestamo.py # Strategy
dao/                     # un DAO por entidad principal: CRUD + reglas de negocio
reportes/                # una función por reporte
ui/                      # ventana principal con ttk.Notebook y un Frame por módulo
tests/
docs/
```
Cada carpeta de código lleva un `__init__.py` vacío.

**Capas: `ui → dao → modelos`.**
- Los DAO **no** usan `input`/`print` ni importan `tkinter` (los apuntes: "No interactúan con el usuario"). Devuelven objetos (`obtener_por_...`) o diccionarios "listos para mostrar", materializados dentro de la sesión para evitar `DetachedInstanceError`. La sesión se crea con `expire_on_commit=False`, igual que en los apuntes.
- Todo método que figure en el diagrama de clases se implementa en esa clase del modelo, y el DAO lo llama. Ejemplos: `Prestamo.validar_prestamo()` revisa socio habilitado, ejemplar disponible, que el ejemplar pertenezca a la sede de origen y que ambas sedes estén activas, usando solo las relaciones del objeto; `Reserva.asignar_ejemplar(ejemplar)` y `Reserva.cancelar()` cambian el estado de la reserva y del ejemplar. El DAO se ocupa de consultar (por ejemplo, buscar un ejemplar disponible), llamar al método del modelo, manejar la sesión y persistir. Las reglas que necesitan consultar otras filas (DNI o ISBN repetidos, reserva duplicada) quedan en el DAO. Esto mantiene el código coherente con el diagrama que se defiende.
- Los DAO validan **siempre** con `validadores.py` antes de tocar la base: así el backend es la fuente de verdad y se puede probar sin interfaz.
- La UI solo captura `ValidacionError` y `ReglaNegocioError`, y muestra el mensaje.
- Excepciones propias definidas como en los apuntes: heredan de `Exception`, con `__init__(self, mensaje)` y `super().__init__(mensaje)`. `TransicionInvalidaError` hereda de `ReglaNegocioError`.
- Para tests, `database.py` permite apuntar a `sqlite:///:memory:` (aparece en los apuntes).

## Interfaz (Tkinter + ttk)
- **Apariencia (decisión del grupo, más allá de los apuntes):** `ttkbootstrap`. Las pestañas importan `import ttkbootstrap as ttk` (mismos widgets ttk, con temas modernos); los botones principales llevan `bootstyle="primary"`, los destructivos `"danger-outline"`, los errores `bootstyle="danger"` y las ayudas `"secondary"`. El tema se elige arriba de la ventana (`TEMAS` en `main.py`).
- **Organización de cada pestaña (decisión del grupo):** encabezado con título y descripción; debajo, una barra que empieza a la izquierda con la acción principal ("Nuevo socio") y sigue con las acciones sobre la fila elegida (desactivadas hasta elegir una; las destructivas aparte, a la derecha y en rojo); y la tabla con el resto del espacio. En los ABM simples (sedes, empleados, socios, catálogo, ejemplares) editar y dar de baja son los íconos ✏ y 🗑 de la última columna de cada fila (`crear_tabla_principal(..., iconos=...)`). En Préstamos, Reservas y Remitos, "Cancelar" es un botón rojo lleno a la derecha de todo de la barra (el DAO decide si se puede cancelar). Las columnas toman el ancho de su texto más largo (título o celda) y la letra es 2 puntos más grande que la de Tk. Los formularios (alta, edición, devolución, incidencia, cancelar o extraviar un remito) se abren en una ventana modal (`ttk.Toplevel` con `grab_set`) con Cancelar y la acción al pie. Todo esto vive en `PestaniaBase` (`crear_encabezado`, `crear_barra_seleccion`, `abrir_modal`, `abrir_formulario`).
- `main.py` crea `ttk.Window(themename=...)` y arma un `ttk.Notebook` con una pestaña por módulo: Sedes, Empleados, Socios, Catálogo (libros, autores, categorías), Ejemplares, Préstamos, Reservas, Remitos, Consulta de disponibilidad y Reportes. Cada pestaña es una subclase de `ttk.Frame` en `ui/`. Para no repetir código entre pestañas, usar una clase base en `ui/base.py` con lo común (armado de campos, etiqueta de error en rojo, limpiar formulario) y que cada pestaña herede de ella (herencia, vista en clase).
- Listados en `ttk.Treeview`; selecciones con `ttk.Combobox` (y validar igualmente que el valor esté entre las opciones); campos de texto con `ttk.Entry`.
- Validación en la interfaz, según los apuntes ("Validar texto" y ejercicios 1 a 6): `validate="key"` con `validatecommand` para impedir caracteres imposibles en campos numéricos, y evento `<FocusOut>` para mostrar una advertencia **en rojo debajo del campo**. Al enviar, `messagebox.showerror` con la lista de errores.
- **Ojo con el ejemplo de los apuntes:** `new_value.isnumeric() and int(new_value) >= 0` rechaza la cadena vacía y el usuario no puede borrar el campo. La validación en vivo debe aceptar `""`; la verificación estricta ocurre al enviar.
- Fechas ingresadas: `ttk.Combobox` **sin** `state="readonly"` (`PestaniaBase.crear_campo_fecha`): se despliega con hoy y los días anteriores, y también se escribe en formato dd/mm/aaaa (como el ejercicio 4). Siempre que se pueda, las fechas las pone el sistema.
- **Usuarios** (de la propuesta): el personal opera los procesos; los socios consultan disponibilidad y catálogo, para lo cual hay una pestaña de consulta. La autenticación está fuera de alcance.
- **Empleado actual.** No hay login: arriba de la ventana principal un `Combobox` de empleado actual define quién registra los `MovimientoRemito` y las demás operaciones. Mientras no haya uno elegido, las operaciones se bloquean con un mensaje.

## Patrones de diseño (exactamente dos)
Se aplican **State** y **Strategy**, siguiendo el capítulo "Patrones State y Strategy" de los apuntes. **No implementar Singleton, Observer ni Factory Method.** (DAO y Unit of Work son organización del acceso a datos, no son los patrones declarados.)

### State — ciclo de vida del Remito
- Contexto: `Remito` (modelo). Estados en `patrones/estado_remito.py`: `EstadoRemitoBase` (clase abstracta con `ABC`) y `RemitoEmpaquetado`, `RemitoDespachado`, `RemitoEnTransito`, `RemitoRecibido`, `RemitoCancelado`, `RemitoExtraviado`.
- Mismo esquema que el semáforo de los apuntes: el contexto tiene `cambiar_estado()`, cada estado tiene `entrar/salir`, y **el estado actual decide la transición** (`avanzar` equivale al `siguiente` del semáforo).
- En la clase base, `avanzar`, `cancelar`, `extraviar` y `quitar_item` lanzan `TransicionInvalidaError`; cada estado concreto sobrescribe solo las que admite.
- Persistencia: el remito guarda solo el texto del estado (`estado = Column(String(20))`). `Remito.estado_actual` (`@property`) devuelve la instancia desde un diccionario `{EstadoRemito.EMPAQUETADO: RemitoEmpaquetado(), ...}`. Los estados no guardan datos propios. Los estados no importan el modelo (reciben el remito por parámetro), para evitar imports circulares.
- Prohibido decidir transiciones con `if/elif` sobre `remito.estado` fuera de esas clases.

| Estado | `avanzar` | `cancelar` | `extraviar` | `quitar_item` |
|---|---|---|---|---|
| EMPAQUETADO | → DESPACHADO | → CANCELADO | ✗ | saca el ítem; si era el único → CANCELADO |
| DESPACHADO | → EN_TRANSITO | ✗ | ✗ | ✗ |
| EN_TRANSITO | → RECIBIDO | ✗ | → EXTRAVIADO | ✗ |
| RECIBIDO / CANCELADO / EXTRAVIADO | ✗ (finales) | ✗ | ✗ | ✗ |

- Cada cambio crea un `MovimientoRemito` (fecha-hora, estado anterior, estado nuevo, empleado, observación). El remito nace con su primer movimiento (EMPAQUETADO).
- Devolver un préstamo interbibliotecario genera un remito `DEVOLUCION` hacia la sede propietaria.
- **Reparto de los efectos:** los estados (`entrar`) tocan el remito y sus ejemplares; los préstamos los actualiza `RemitoDAO` con `verificar_transicion` de `PrestamoDAO`, así el diccionario de transiciones del préstamo queda en un solo lugar.
- **Efectos colaterales (confirmados por el grupo):** DESPACHADO → `fecha_despacho` = hoy y ejemplares EN_TRANSITO. RECIBIDO → `fecha_recepcion` = hoy; si es IDA, el préstamo pasa a ACTIVO (lo hace `RemitoDAO`, ver abajo); si es DEVOLUCION, cada ejemplar vuelve a circular con `Ejemplar.volver_a_circular()`: DISPONIBLE, o DAÑADO / BAJA si el socio lo devolvió dañado o destruido (el préstamo ya quedó DEVUELTO cuando el socio devolvió), y se asigna a la reserva que lo espere. CANCELADO → si es IDA, ejemplares DISPONIBLE y préstamo CANCELADO; si es DEVOLUCION, el préstamo sigue DEVUELTO y el ejemplar no cambia (espera un nuevo remito de devolución). EXTRAVIADO → ejemplares EXTRAVIADO, se crea una `IncidenciaEnvio` de tipo EXTRAVIO y, si es IDA, el préstamo pasa a CANCELADO.
- **Activación del préstamo interbibliotecario (EN_ENVIO → ACTIVO).** Los estados del remito **no conocen ni importan** `EstrategiaPrestamo` ni `ESTRATEGIAS`, y la firma de `avanzar(empleado, observacion)` no cambia. Después de `avanzar()`, si el remito quedó RECIBIDO y es de tipo IDA, `RemitoDAO` recorre sus ítems y por cada préstamo llama a `prestamo.activar(ESTRATEGIAS[prestamo.tipo])`. Todo ocurre en la misma sesión que el cambio de estado, con un solo commit: si algo falla, `obtener_session()` hace rollback de todo. Los demás efectos colaterales siguen como se describen arriba.

### Strategy — plazo y multa según el tipo de préstamo
- `patrones/estrategia_prestamo.py`: `EstrategiaPrestamo(ABC)` con `calcular_vencimiento(fecha_prestamo)` y `calcular_multa(dias_atraso)` abstractos, y las implementaciones `EstrategiaPrestamoLocal` y `EstrategiaPrestamoInterbibliotecario`.
- Selección **externa**, como enseñan los apuntes (el contexto no elige): un diccionario `ESTRATEGIAS = {TipoPrestamo.LOCAL: ..., TipoPrestamo.INTERBIBLIOTECARIO: ...}` que usan los DAO al activar el préstamo (para calcular el vencimiento) y al calcular la multa.
- La estrategia se **inyecta por parámetro**, como `CalculadorEnvio(estrategia)` en los apuntes: el DAO (`PrestamoDAO`, o `RemitoDAO` al recibir un remito IDA) obtiene `ESTRATEGIAS[prestamo.tipo]` y se la pasa a `prestamo.activar(estrategia)` (fija `fecha_prestamo` = hoy, `fecha_vencimiento = estrategia.calcular_vencimiento(fecha_prestamo)` y pasa el ejemplar a PRESTADO) y a `multa.calcular_monto(estrategia)`. Ni `Prestamo` ni `Multa` eligen la estrategia: ese es el argumento de "selección externa" para la defensa.
- El usuario **nunca ingresa** el vencimiento: lo calcula la estrategia. `fecha_prestamo` y `fecha_vencimiento` se fijan **cuando el préstamo pasa a ACTIVO** (en el interbibliotecario, al recibirse el remito de ida), para que el tránsito no consuma el plazo.
- Valores confirmados por el grupo, en `config.py`: Local 31 días y $100 por día de atraso; Interbibliotecario 38 días y $150 por día. Montos con `Float` y `round(x, 2)`.
- `dias_atraso = max(0, (fecha_devolucion - fecha_vencimiento).days)`, con `fecha_devolucion` = el día en que el **socio** devolvió (no la fecha del remito de vuelta); si es 0 no se genera multa.

### Estado del Préstamo (sin patrón)
Constantes de texto + un diccionario de transiciones permitidas validado en `PrestamoDAO` (confirmado por el grupo): SOLICITADO→{APROBADO, CANCELADO}; APROBADO→{EN_ENVIO (interbibliotecario), ACTIVO (local), CANCELADO}; EN_ENVIO→{ACTIVO, CANCELADO}; ACTIVO→{DEVUELTO}.

- **Activación (dos caminos; en ambos el DAO elige la estrategia).** Local: el préstamo pasa de APROBADO a ACTIVO sin remito, así que `PrestamoDAO.aprobar()` llama a `prestamo.activar(ESTRATEGIAS[prestamo.tipo])` en la propia aprobación. Interbibliotecario: `RemitoDAO` llama a `activar()` cuando el remito IDA queda RECIBIDO (ver State).

- **VENCIDO no se guarda.** En la base el préstamo sigue ACTIVO y un `@property` (`estado_efectivo`, como `esta_vencido` en los apuntes) devuelve VENCIDO si está ACTIVO y `fecha_vencimiento < hoy`. Los reportes filtran `estado == ACTIVO` con vencimiento anterior a hoy. Un préstamo vencido se devuelve igual que uno vigente.
- **Reserva del ejemplar.**
  - *Interbibliotecario:* al aprobar, el ejemplar pasa a RESERVADO (así dos préstamos aprobados no pueden pedir el mismo). Pasa a PRESTADO cuando el remito IDA queda RECIBIDO y se llama a `activar()`. Si el préstamo se cancela, vuelve a DISPONIBLE.
  - *Local:* `PrestamoDAO.aprobar()` valida que el ejemplar esté DISPONIBLE y llama a `activar(estrategia)` en la misma operación. El ejemplar pasa directo a PRESTADO, sin pasar por RESERVADO. El estado APROBADO del local es transitorio, pero se mantiene en el diccionario de transiciones para que el flujo sea igual en los dos tipos.
- **Cancelación.** Desde SOLICITADO o APROBADO no hay remito: solo se libera el ejemplar. Desde EN_ENVIO solo se permite si el remito sigue EMPAQUETADO (lo decide el estado con `quitar_item`): el ítem del préstamo sale del remito y, si era el único, se cancela el remito entero (el ítem queda para el historial). El ejemplar vuelve a DISPONIBLE. Si el remito ya fue despachado, se rechaza con `TransicionInvalidaError`.
- **Devolución.** Al registrarla, el préstamo pasa a DEVUELTO ese día y se calcula la multa con esa fecha. La registra `DevolucionDAO` (módulo propio porque usa `PrestamoDAO` y `RemitoDAO`). Local: el ejemplar vuelve a circular en el acto. Si es interbibliotecario, además se crea solo el remito DEVOLUCION (uno por devolución); el ejemplar **sigue PRESTADO** hasta que ese remito se despacha (pasa a EN_TRANSITO) y vuelve a circular cuando se recibe en la sede propietaria. Si ese remito se cancela, `RemitoDAO.crear_devolucion()` arma uno nuevo. La multa solo se marca PAGADA (`PrestamoDAO.pagar_multa`); el préstamo la muestra en la columna `multa`.

## Reglas de negocio (obligatorias)
- No prestar ejemplares que no estén DISPONIBLE.
- No prestar a socios que no estén ACTIVO (inhabilitados o de baja).
- Controlar vencimientos: un préstamo ACTIVO pasado de `fecha_vencimiento` se considera VENCIDO (se calcula al consultar y **no se guarda**, con un `@property` como `esta_vencido` en los apuntes).
- No prestar un ejemplar cuya sede no sea la `sede_origen` del préstamo.
- No iniciar préstamos, reservas ni envíos desde o hacia una sede dada de BAJA.
- Préstamo LOCAL: `sede_origen == sede_destino`. INTERBIBLIOTECARIO: `sede_origen != sede_destino`.
- Evitar duplicados: socios (DNI), catálogo (ISBN o ISSN) y ejemplares (`codigo_inventario`).
- **Identificadores que asigna el sistema (decisión del grupo):** `nro_socio` = el más alto + 1; `legajo` = letra del rol (`B` bibliotecario, `A` administrador, en `RolEmpleado.PREFIJO_LEGAJO`) + número correlativo, y un cambio de rol le da un legajo nuevo; `nro_remito` = `REM-` + número. Los `id` los autoincrementa SQLite. `isbn` y `codigo_inventario` siguen manuales.
- **Horarios de la sede:** se carga la semana completa (días marcados, cada uno con su horario, desde desplegables cada 30 minutos); `SedeDAO.crear/modificar` reciben `[(día, apertura, cierre)]` y modificar reemplaza la semana.
- `codigo_inventario` lo ingresa el personal (es el código impreso del ejemplar), es obligatorio y único: es lo que permite detectar la carga doble de un mismo ejemplar físico. El proceso opcional de inventario (escaneo, auditorías) queda fuera de alcance. El campo `isbn` acepta ISBN (10 o 13) e ISSN (8), porque el catálogo incluye revistas y material de consulta.
- Trazabilidad del remito: cada cambio de estado deja un `MovimientoRemito`; las transiciones no permitidas se rechazan. Un remito puede agrupar varios ejemplares entre el mismo par de sedes.
- Reserva sobre un título y una sede de retiro; cuando queda un ejemplar disponible se asigna (ejemplar RESERVADO, reserva DISPONIBLE). Estados: PENDIENTE → DISPONIBLE → CUMPLIDA / CANCELADA / VENCIDA.
- **Reservas (confirmado por el grupo).** Se puede reservar aunque haya un ejemplar libre en esa sede: se asigna en el acto. La asignación es **en el momento**: toda operación que deja un ejemplar DISPONIBLE (devolución local, recepción de una DEVOLUCION, cancelación de préstamo, remito IDA o reserva, vencimiento) llama en la misma sesión a `asignar_a_reserva_pendiente()` (`dao/comun.py`), que se lo da a la reserva PENDIENTE más antigua de ese título y sede. **Retirar** una reserva DISPONIBLE la pasa a CUMPLIDA (`Reserva.cumplir()`) y crea un préstamo LOCAL en la sede de retiro, activo en el acto.
- Plazos de la reserva (confirmados, constantes en `config.py`): una reserva PENDIENTE espera **45 días** a que se libere un ejemplar; al pasar a DISPONIBLE el socio tiene **2 días** para retirarlo (al asignar el ejemplar, `fecha_vencimiento` se reescribe como hoy + 2 días).
- Una reserva vencida (en cualquiera de las dos etapas) pasa a VENCIDA; si tenía ejemplar asignado, este se libera y se le asigna a la siguiente reserva PENDIENTE del mismo título y sede. Como esto **modifica datos**, el estado sí se guarda: `ReservaDAO.procesar_vencimientos()` (usa `Reserva.vencer()`) se ejecuta al abrir la app, cada vez que se refrescan las pestañas de Reservas y de Consulta de disponibilidad, y con el botón "Procesar vencimientos".
- Devolución: registra `estado_fisico`; DANADO o DESTRUIDO deja el ejemplar fuera de circulación (DANADO / BAJA) y exige observaciones.
- Un libro (título) puede tener 0 ejemplares; la disponibilidad de un título sin ejemplares es 0.
- Cada ejemplar pertenece a una única sede. La disponibilidad se controla sobre el ejemplar, no sobre el libro (a diferencia del contador `ejemplares_disponibles` del ejemplo de los apuntes).

## Validaciones de entrada
Detalle por campo en `docs/VALIDACIONES.md`. Principios:
1. **El backend es la fuente de verdad**: los DAO validan todo con `validadores.py`. La validación en vivo de la UI es solo ayuda.
2. Primero formato (`ValidacionError`), después reglas de negocio (`ReglaNegocioError`).
3. Defensa en profundidad: `UNIQUE`, `NOT NULL` y `nullable=False` también en las columnas.
4. Mensajes en español y concretos: "El DNI debe tener 7 u 8 dígitos", no "valor inválido".
5. **Normalizar antes de comparar duplicados.** `unique=True` en SQLite distingue mayúsculas y espacios, así que el DAO normaliza (`strip`, minúsculas, ISBN sin guiones, DNI solo dígitos) y consulta antes de insertar; la restricción `unique` queda como red de seguridad.

## Convenciones de código
- PEP 8, `snake_case` para atributos y funciones (`fecha_vencimiento`, `nro_socio`) y `PascalCase` para clases. El paso desde el camelCase del diagrama es mecánico para los atributos comunes; las claves primarias y foráneas se rigen por la regla de abajo. Anotaciones simples como las de los apuntes (`peso_kg: float`), sin importar `typing`.
- **Claves primarias y foráneas.** Todas las tablas de entidades tienen `id = Column(Integer, primary_key=True)`, como en el "Ejemplo completo: Sistema de biblioteca" de los apuntes. Las tablas de asociación simples (`libro_autor`) llevan solo sus dos claves foráneas, como en los apuntes. `ItemRemito` es una entidad y lleva `id`. Los atributos naturales (`nro_socio`, `dni`, `isbn`, `legajo`, `codigo_inventario`, `nro_remito`) son `unique=True, nullable=False`. En el diagrama, `idSede`, `idPrestamo`, `idReserva`, `idAutor` e `idCategoria` se implementan como `id`. Las claves foráneas se llaman `<entidad>_id` (`sede_id`, `libro_id`, `socio_id`, `ejemplar_id`), igual que `cliente_id` y `libro_id` en los apuntes; por ejemplo, el empleado pertenece a una sede mediante `sede_id` (obligatorio). Cuando una clase tiene más de una clave a la misma tabla, o la clave cumple un rol, se nombra `<rol>_id`: `sede_origen_id` y `sede_destino_id` (`Prestamo` y `Remito`) y `sede_retiro_id` (`Reserva`).
- Modelos: `Base`, `Column`, `relationship(back_populates=...)`, `__repr__` y `__str__`, como en el ejemplo de biblioteca. Muchos a muchos sin atributos (Libro–Autor): tabla de asociación. Con atributos (`ItemRemito`): *Association Object*, como en los apuntes.
- Fechas con `date`, `datetime` y `time`; columnas `Date`, `DateTime` y `Time`; `default=date.today`.
- Nunca armar SQL con f-strings: usar el ORM.

## Tests (pytest, como en "Testing unitario")
- Clases `TestXxx`, `assert` y `pytest.raises(..., match=...)`. Un archivo por clase o DAO, `test_nombre.py`.
- Remito: transiciones válidas e inválidas (recorrer la tabla de arriba con un `for`) y que cada cambio cree su movimiento.
- Strategy: vencimiento y multa de cada estrategia, incluido atraso 0.
- Cada regla de negocio, con su caso feliz y su caso de rechazo.
- Validadores: los valores inválidos de `docs/VALIDACIONES.md`, recorridos con `for`.

## Reportes (mínimo 4 no triviales; apuntar a los 6)
Cada uno como función en `reportes/`: consulta con `session.query` y relaciones, y agregación en Python (ver tabla "No visto"). Se muestran en la pestaña Reportes: un `Combobox` para elegir y un `Treeview` para el resultado.
1. Préstamos activos y material en tránsito.
2. Préstamos vencidos y multas acumuladas por socio.
3. Libros más solicitados para préstamos interbibliotecarios.
4. Disponibilidad de catálogo por sede.
5. Tasa de envíos exitosos e incidencias.
6. Movimiento de ejemplares entre sedes: envíos por par origen/destino y tiempo promedio de tránsito (`fecha_recepcion - fecha_despacho`).

**Implementación (supuestos del grupo).** Cada función devuelve `(columnas, filas)`; `reportes/__init__.py` las reúne en `REPORTES` para el desplegable. La pestaña vuelve a generar el reporte elegido después de cada operación.
- (2) Solo aparecen socios con algún préstamo vencido hoy o alguna multa; se ordena por deuda pendiente.
- (3) Cuentan todas las solicitudes interbibliotecarias, también las canceladas (miden la demanda); "completado" = ACTIVO o DEVUELTO. Muestra la ruta más pedida.
- (4) Usa el mismo conteo por estado que la Consulta de disponibilidad (`sumar_ejemplar` de `dao/consulta_dao.py`).
- (5) Tasa de éxito = recibidos / (recibidos + extraviados): un remito cancelado nunca salió y no cuenta como envío fallido. "—" si no hay envíos terminados.
- (6) Se excluyen los remitos cancelados; el promedio es solo sobre los recibidos, con 2 decimales, y "—" si no hay.

**Consulta de disponibilidad** (`dao/consulta_dao.py`, pestaña sin empleado): una fila por título y sede con los ejemplares por estado; filtra por texto (título, autor o ISBN, sin distinguir mayúsculas) y por sede. Un título sin ejemplares aparece con 0. Antes de mostrar corre `procesar_vencimientos()`.

## Plan de trabajo (fases; cada una incluye su pestaña de la UI para poder mostrarla)
0. **Setup:** `.venv`, `requirements.txt`, `.gitignore` (`.venv/`, `__pycache__/`, `*.db`, `.pytest_cache/`, `.DS_Store`), estructura de carpetas, `database.py` (copiando la configuración de los apuntes), `constantes.py`, `excepciones.py` y ventana principal vacía.
1. **Modelos:** entidades SQLAlchemy según el diagrama y creación de tablas. Además, los modelos implementan los métodos del diagrama: `Socio.esta_habilitado()` e `inhabilitar()`, `Ejemplar.esta_disponible()` y `cambiar_estado(nuevo)` (valida que `nuevo` sea una constante de `EstadoEjemplar`), `Sede.dar_de_baja()` y `esta_activa()`, `Reserva.cancelar()`, y los de `Prestamo` y `Multa`. Los métodos de State del `Remito` (`estado_actual`, `cambiar_estado`, `avanzar_estado`, `cancelar`, `extraviar`) se agregan en la Fase 5, junto con `patrones/estado_remito.py`.
2. **Validadores** y sus tests.
3. **ABM:** sedes (con horarios), empleados, socios, autores y categorías, libros y ejemplares, con sus DAO y pestañas.
4. **Préstamos** + Strategy (vencimiento y multas).
5. **Remitos** + State (empaquetar, despachar, recibir, cancelar, extraviar, incidencias, historial). `RemitoDAO` importa `ESTRATEGIAS` de `patrones/estrategia_prestamo.py` para activar los préstamos al recibir un remito IDA: es la única dependencia entre ambos patrones y vive en el DAO, no en las clases de State.
6. **Reservas y devoluciones** (incluye el remito de devolución, la multa y `procesar_vencimientos()` de reservas).
7. **Consulta de disponibilidad y reportes.**
8. **Pasada completa por el checklist de validaciones** y ensayo de la defensa (guion de `docs/VALIDACIONES.md`).

## Fuera de alcance
Notificaciones, historial de lecturas, recomendaciones, revisión detallada de la recepción, cobro de multas (solo se registra su estado) y autenticación avanzada. Dejar los puntos de extensión del modelo (`codigo_inventario`, `estado_fisico`, `IncidenciaEnvio`).
