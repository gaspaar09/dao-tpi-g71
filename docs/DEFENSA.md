# Guion para la defensa

Preparación del grupo para la defensa oral con código. Hay seis partes: la demo, los datos inválidos que van a probar los profes, los dos patrones, de qué capítulo de los apuntes sale cada técnica, lo que usamos y no estaba en los apuntes, y preguntas probables.

Antes de empezar:
1. Borrar `biblioteca.db` y abrir con `python main.py`.
2. Tocar **Cargar datos de ejemplo**.
3. Tener abierta una terminal con `python -m pytest`.

---

## 1. Demo (10 minutos)

| Paso | Dónde | Qué mostrar |
|---|---|---|
| 1 | Arriba | Sin elegir el empleado actual, intentar aprobar un préstamo: aparece "Seleccione el empleado actual". Elegir a Laura Gómez. |
| 2 | Socios | Alta con DNI `1.000000`: se rechaza por los puntos mal ubicados. Al tipear `40111222`, los puntos aparecen solos. |
| 3 | Préstamos | Solicitar un préstamo LOCAL de MOR-003 en Sede Norte: el destino se completa solo y queda bloqueado. Aprobarlo: queda ACTIVO con vencimiento a 31 días (Strategy). |
| 4 | Préstamos | Solicitar uno INTERBIBLIOTECARIO de REV-001 de Central a Sur y aprobarlo: el ejemplar queda RESERVADO. |
| 5 | Remitos | Elegir Central → Sur, marcar ese préstamo y crear el remito: queda EMPAQUETADO y el préstamo pasa a EN_ENVIO. Avanzarlo tres veces y mirar el historial: el préstamo queda ACTIVO a 38 días (State + Strategy). |
| 6 | Remitos | Sobre REM-000002 (DESPACHADO): Cancelar se rechaza (TransicionInvalidaError). Sobre REM-000003 (EN_TRANSITO): Dar por extraviado sin observación pide el motivo; con motivo, queda EXTRAVIADO con su incidencia. |
| 7 | Préstamos | Devolver RAY-001 (vencido): se genera una multa de $300. Marcarla pagada. |
| 8 | Reservas | Retirar la reserva DISPONIBLE de la revista en Sur: se crea un préstamo local. |
| 9 | Consulta | Buscar "borges" y filtrar por sede. |
| 10 | Reportes | Recorrer los 6. En el 5, mostrar la tasa de éxito con el extraviado del paso 6. |
| 11 | Terminal | `python -m pytest`: todos los tests en verde. |

---

## 2. Datos inválidos que van a probar (guion de VALIDACIONES.md)

La regla general: **el DAO valida todo** con `validadores.py`. La pantalla solo ayuda: el error en rojo al salir del campo y el bloqueo de letras en los campos numéricos. Por eso las mismas reglas se prueban sin interfaz.

| # | Prueba | Qué pasa | Dónde está | Test |
|---|---|---|---|---|
| 1 | DNI `abc`, `-5`, `1234567890123`, repetido, con espacios | El campo no deja escribir letras. Los demás casos se rechazan con mensaje: "solo números", "entre 1.000.000 y 99.999.999", "Ya existe un socio con ese DNI" | [validadores.py:161](../validadores.py#L161) | `test_validadores.py`, `test_entradas_invalidas.py` |
| 2 | Nombre vacío, con números o de 200 caracteres | "obligatorio", "solo puede tener letras…", "no puede superar…" | [validadores.py:80](../validadores.py#L80) | idem |
| 3 | Año `-1`, `3000`, `dos mil`; ISBN repetido | Rango 1450 hasta el año actual; `int()` dentro de `try` para el texto; ISBN normalizado sin guiones | [validadores.py:113](../validadores.py#L113), [validadores.py:212](../validadores.py#L212) | `test_catalogo_dao.py` |
| 4 | Teléfono con letras, email sin `@`, cierre antes de la apertura | Teléfono: solo dígitos, 6 a 15. Email: una sola `@` y un punto en el dominio. Horario: los desplegables solo ofrecen un cierre posterior a la apertura (y viceversa) y el DAO igual valida `apertura < cierre` por día | [validadores.py:195](../validadores.py#L195), [validadores.py:179](../validadores.py#L179), [validadores.py:278](../validadores.py#L278) | `test_sede_dao.py` |
| 5 | Préstamo de un ejemplar PRESTADO, de un socio INHABILITADO, de otra sede o hacia una sede de BAJA | `Prestamo.validar_prestamo()` (método del diagrama) | [modelos/prestamo.py:46](../modelos/prestamo.py#L46) | `test_prestamo.py`, `test_prestamo_dao.py` |
| 6 | Préstamo LOCAL con origen distinto del destino | La pantalla lo impide (el destino queda bloqueado) y el modelo también lo rechaza | idem | idem |
| 7 | Devolver dos veces, con fecha futura, dañado sin observaciones | Transición DEVUELTO→DEVUELTO no permitida; fecha no futura; observaciones obligatorias si está DAÑADO o DESTRUIDO | [dao/devolucion_dao.py:24](../dao/devolucion_dao.py#L24) | `test_devolucion_dao.py` |
| 8 | Remito: cancelar uno DESPACHADO, saltar de EMPAQUETADO a RECIBIDO, extraviar uno que no está EN_TRANSITO | No se puede saltar: "Avanzar" solo pasa al siguiente. Lo demás lo rechaza el estado actual con `TransicionInvalidaError` | [patrones/estado_remito.py:33](../patrones/estado_remito.py#L33) | `test_estado_remito.py` (recorre la tabla completa con un `for`) |
| 9 | Reserva en una sede de baja; reserva repetida | "dada de baja" / "ya tiene una reserva PENDIENTE" | [dao/reserva_dao.py](../dao/reserva_dao.py) | `test_reserva_dao.py` |
| 10 | Letras en un campo numérico, Ctrl+V, doble clic en Guardar | `validate="key"` rechaza cualquier carácter que no sea un dígito, también al pegar, pero acepta el campo vacío. Doble clic: el cuadro de diálogo bloquea la ventana y el segundo intento choca con el control de duplicados (también en las solicitudes de préstamo) | [ui/base.py:178](../ui/base.py#L178), [dao/prestamo_dao.py:65](../dao/prestamo_dao.py#L65) | `test_prestamo_dao.py` |
| 11 | Cancelar un préstamo EN_ENVIO con el remito despachado; reserva vencida | `quitar_item` solo lo admite EMPAQUETADO. `procesar_vencimientos()` vence la reserva y libera el ejemplar | [dao/reserva_dao.py:73](../dao/reserva_dao.py#L73) | `test_remito_dao.py`, `test_reserva_dao.py` |
| 12 | Operar sin empleado actual | "Seleccione el empleado actual…" | [ui/base.py:408](../ui/base.py#L408) | (interfaz) |

Además, `tests/test_entradas_invalidas.py` prueba todos los valores raros del checklist (vacío, espacios, emojis, `1e5`, `1,5`, números enormes, `30/02`, ids que no existen) contra cada alta y operación de los DAO. Siempre tienen que terminar en uno de nuestros dos errores, nunca en un error de la base.

---

## 3. Patrones de diseño

### State: ciclo de vida del remito
- **Contexto:** `Remito`. Tiene `estado_actual` ([modelos/remito.py:48](../modelos/remito.py#L48)), que convierte el texto guardado en la instancia del estado, y `cambiar_estado` ([modelos/remito.py:52](../modelos/remito.py#L52)): sale del estado anterior, registra el `MovimientoRemito` y entra al nuevo. Es igual a `Semaforo.cambiar_estado` de los apuntes.
- **Estados:** `EstadoRemitoBase(ABC)` y una clase por estado ([patrones/estado_remito.py](../patrones/estado_remito.py)).
  - En la base, `avanzar`, `cancelar`, `extraviar` y `quitar_item` lanzan `TransicionInvalidaError`. Cada estado sobrescribe solo lo que admite.
  - **El estado decide la transición:** `RemitoEmpaquetado.avanzar` llama a `remito.cambiar_estado(DESPACHADO)`, como `Rojo.siguiente` llama a `cambiar_estado(Verde())`.
- **Efectos al entrar a un estado (`entrar`):**
  - DESPACHADO: guarda la fecha de despacho y pone los ejemplares EN_TRANSITO;
  - RECIBIDO: guarda la fecha de recepción y, si es una devolución, el ejemplar vuelve a circular;
  - CANCELADO o EXTRAVIADO: libera o pierde los ejemplares.
- **Por qué no un `if/elif`:** las reglas de cada estado están en una sola clase. Agregar un estado no obliga a tocar el `Remito`, y una transición no permitida no se escapa por un `else` olvidado.
- **Persistencia:** se guarda solo el texto del estado. Los estados no tienen datos propios, así que alcanza con una instancia de cada uno en `ESTADOS_REMITO`.
- **Los estados no importan los modelos ni las estrategias:** reciben el remito por parámetro, y así no hay imports circulares.

### Strategy: plazo y multa según el tipo de préstamo
- `EstrategiaPrestamo(ABC)` define `calcular_vencimiento` y `calcular_multa`.
  - `EstrategiaPrestamoLocal`: 31 días y $100 por día de atraso.
  - `EstrategiaPrestamoInterbibliotecario`: 38 días y $150 por día. Más plazo, porque el ejemplar tiene que volver a su sede.
- **La elección es externa**, como `CalculadorEnvio(estrategia)` en los apuntes. El DAO busca en `ESTRATEGIAS[prestamo.tipo]` y se la pasa por parámetro al modelo: `prestamo.activar(estrategia)` y `multa.calcular_monto(estrategia)`. Ni el préstamo ni la multa eligen.
  - [dao/prestamo_dao.py:87](../dao/prestamo_dao.py#L87): préstamo local, al aprobarlo.
  - [dao/remito_dao.py:141](../dao/remito_dao.py#L141): interbibliotecario, al recibir el remito de ida. Es el único punto de contacto entre los dos patrones.
  - [dao/devolucion_dao.py:51](../dao/devolucion_dao.py#L51): la multa.
- **Por qué no un `if/elif`:** sumar un tipo de préstamo nuevo es sumar una clase y una entrada en el diccionario. No hay que tocar `Prestamo` ni `Multa`.

### El estado del préstamo **no** usa patrón (y por qué)
Las transiciones del préstamo son pocas y no tienen comportamiento propio en cada estado. Alcanza con un diccionario de transiciones permitidas ([dao/prestamo_dao.py:24](../dao/prestamo_dao.py#L24)). Usar State en los dos lugares hubiera sido agregar clases sin necesidad.

---

## 4. De qué capítulo de APUNTES.md sale cada cosa

| Técnica | Capítulo | Dónde |
|---|---|---|
| `declarative_base`, `Column`, `relationship(back_populates)`, `__repr__` / `__str__` | ORM con SQLAlchemy, "Ejemplo completo: Sistema de biblioteca" | `modelos/` |
| Tabla de asociación Libro–Autor y Association Object (`ItemRemito`) | Relaciones entre tablas | `modelos/catalogo.py`, `modelos/remito.py` |
| `obtener_session()` con commit o rollback, `expire_on_commit=False` | Context managers y gestión de sesiones | [database.py:26](../database.py#L26) |
| Un DAO por entidad, que no interactúa con el usuario | Patrón DAO | `dao/` |
| `class ValidacionError(Exception)` con `super().__init__` | Excepciones definidas por el programador | `excepciones.py` |
| Clases abstractas con `ABC` y `@abstractmethod` | Clases y métodos abstractos | `patrones/` |
| Herencia de la clase base de las pestañas | Herencia, Polimorfismo | `ui/base.py`; `avisar_cambios_a` en Catálogo es polimorfismo |
| `@property` (`esta_vencido`, `estado_efectivo`, `estado_actual`) | Propiedades | `modelos/prestamo.py`, `modelos/remito.py` |
| State y Strategy | Patrones State y Strategy | `patrones/` |
| `ttk.Notebook`, `Treeview`, `Combobox`, `Scrollbar`, `Checkbutton` (con los temas de ttkbootstrap) | Clase TTK | `main.py`, `ui/` |
| `validate="key"` con `%P`, `<FocusOut>`, `<FocusIn>`, `<Return>` | Validar texto, Eventos en Tkinter | `ui/base.py` |
| `Listbox` y `curselection()` | Manejo de eventos de listbox | autores del libro, préstamos del remito |
| Clases `TestXxx`, `pytest.raises(match=…)`, bucles `for` | Testing unitario, Pytest | `tests/` |
| Agrupar con diccionarios, `sorted(key=lambda …)`, `sum`, `len` | Python básico | `reportes/` |

---

## 5. Lo que usamos y no está en los apuntes (y por qué)

| Qué | Por qué es necesario | Alternativa vista que descartamos |
|---|---|---|
| `foreign_keys=[…]` en `relationship` | `Prestamo` y `Remito` tienen dos claves hacia `Sede`, y SQLAlchemy exige indicar cuál usa cada relación | Ninguna: sin esto el modelo no arranca |
| `tkinter.messagebox` (`showerror`, `showinfo`, `askyesno`) | Los ejercicios piden "cuadro de diálogo"; `askyesno` confirma antes de bajas y cancelaciones | Un `Label` de estado no detiene al usuario |
| `Combobox(state="readonly")` | Evita texto libre en los desplegables | Combobox editable, que permite escribir cualquier cosa |
| `Listbox(selectmode="multiple")` | Un libro tiene varios autores y un remito agrupa varios préstamos | Un Combobox por autor |
| `<<ComboboxSelected>>` | Acomodar el formulario apenas se elige una opción (destino de un préstamo local, préstamos para enviar) | `<FocusOut>` recién actúa al salir del campo |
| `<ButtonRelease-1>` en una tabla | Mostrar el detalle (horarios, historial del remito) al hacer clic | Un botón "Ver detalle" extra |
| `<KeyRelease>` en el DNI | Poner los puntos automáticamente después de cada tecla | `<Key>` corre antes de que el carácter entre al campo |
| Combobox de fecha **sin** `readonly` | La fecha se elige de una lista o se escribe | `tkcalendar` (librería externa, excluida) |
| `ttkbootstrap` (temas modernos para ttk) | Decisión del grupo para que la interfaz se vea actual. Solo cambia la apariencia: los widgets son los mismos de ttk (`import ttkbootstrap as ttk`), con `bootstyle` para el color de los botones y mensajes. Arriba de la ventana se elige el tema | `ttk.Style().theme_use("clam")`, que se ve anticuado |
| Ventanas modales (`ttk.Toplevel`, `transient`, `grab_set`) | Decisión del grupo para ordenar la pantalla: los formularios se abren en una ventana aparte, con Cancelar y la acción al pie, y la tabla ocupa la pestaña. Mientras el modal está abierto no se puede tocar el resto de la app | Formularios fijos arriba de cada tabla, con los botones mezclados |
| Íconos ✏ y 🗑 en cada fila de los ABM (`identify_row`, `identify_column`, `bbox`, `font.measure`) | Decisión del grupo: el `Treeview` no admite botones dentro de las filas, así que la última columna muestra los íconos como texto y un clic se ubica con `identify_row`/`identify_column` y el ancho de cada ícono. Solo en los ABM simples (editar y dar de baja); en préstamos, reservas y remitos todas las acciones son botones de la barra, con "Cancelar" en rojo a la derecha de todo | Botones Editar y Eliminar arriba de la tabla |
| `ttk.Checkbutton` sin variable (`instate(["selected"])`) | Marcar los días de apertura de la sede; está en los apuntes, pero sin `IntVar`, que no usamos | Un Combobox de un solo día |

---

## 6. Preguntas probables

- **¿Por qué VENCIDO no se guarda?** Depende de la fecha de hoy: guardado, mañana estaría mal. Se calcula con un `@property` (`estado_efectivo`), igual que `esta_vencido` en los apuntes. En la base el préstamo sigue ACTIVO.
- **¿Y por qué VENCIDA en la reserva sí se guarda?** Porque vencer una reserva modifica otros datos: libera el ejemplar y se lo asigna a la siguiente reserva. Lo hace `procesar_vencimientos()`, que corre al abrir la app, en la pestaña Reservas y en la Consulta.
- **¿Dónde se valida, en la pantalla o en el backend?** En los dos lugares, pero la fuente de verdad es el DAO. La pantalla solo da aviso temprano. Los tests llaman directamente a los DAO, sin interfaz.
- **¿Se puede hacer inyección SQL escribiendo `' OR 1=1 --`?** No. Nunca armamos SQL con texto: el ORM manda los valores como parámetros. Por eso un título puede llevar comillas sin problema.
- **¿Qué pasa si falla algo en mitad de una operación?** `obtener_session()` hace rollback de todo. Por ejemplo, al recibir un remito de ida, el cambio de estado, el movimiento y la activación de los préstamos van en un solo commit.
- **¿Por qué el préstamo interbibliotecario empieza a contar al recibirse el remito?** Para que el tiempo de viaje no le consuma el plazo al socio. `fecha_prestamo` y `fecha_vencimiento` se fijan cuando el préstamo pasa a ACTIVO.
- **¿Por qué `DevolucionDAO` está aparte?** Usa el diccionario de transiciones de `PrestamoDAO` y el armado de remitos de `RemitoDAO`. Si estuviera en uno de los dos, los módulos se importarían entre sí.
- **¿Cómo se evita prestar el mismo ejemplar dos veces?** Al aprobar se vuelve a validar que siga DISPONIBLE. En los interbibliotecarios pasa a RESERVADO apenas se aprueba, así otra solicitud ya no lo encuentra libre.
- **¿Qué es la "asignación en el momento" de las reservas?** Cada operación que libera un ejemplar (devolver, cancelar, recibir una devolución, vencer una reserva) se lo asigna, en la misma sesión, a la reserva PENDIENTE más antigua de ese título y sede (`asignar_a_reserva_pendiente` en [dao/comun.py:24](../dao/comun.py#L24)).
- **¿Por qué no usaron Enum, regex, `strptime` o `group_by`?** No se vieron en clase. Usamos las alternativas de los apuntes: clases de constantes, métodos de `str`, `date(año, mes, día)` dentro de `try` y agrupación en Python. Están detalladas en `CLAUDE.md`.
