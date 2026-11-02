# Checklist de validaciones

Los profes van a probar cada campo con datos inválidos durante la defensa. Este documento es la lista de qué validar y qué probar. Los valores marcados como *(supuesto)* son propuestas del grupo, no vienen del enunciado.

Todo se implementa con lo visto en clase (ver `CLAUDE.md`): métodos de `str`, `try: int(...) except ValueError`, `date(anio, mes, dia)` y excepciones propias. Sin regex.

## Principios
1. **Defensa en capas.**
   - *En vivo (UI):* `validate="key"` + `validatecommand` solo para impedir caracteres imposibles en campos numéricos. Siempre debe aceptar la cadena vacía, si no el usuario no puede borrar el campo.
   - *Al perder el foco (`<FocusOut>`):* advertencia en rojo debajo del campo.
   - *Al enviar:* la UI llama al DAO y muestra los errores con `messagebox.showerror`.
   - **El DAO valida todo otra vez con `validadores.py`.** Esa es la fuente de verdad y permite probar sin interfaz.
   - *Base de datos:* `unique=True`, `nullable=False`.
2. **Normalizar antes de validar:** `strip()`, espacios repetidos, DNI sin puntos (se quitan y se guardan solo los dígitos). Para los campos únicos (nombre de sede, DNI, ISBN/ISSN, código de inventario) el DAO compara el valor normalizado, porque `unique=True` en SQLite distingue mayúsculas.
3. **Helpers en `validadores.py`** (lanzan `ValidacionError` con el nombre del campo y un mensaje claro): texto obligatorio con largo máximo, solo letras, entero positivo, número no negativo, fecha dd/mm/aaaa, email, teléfono, valor perteneciente a una lista de constantes, existencia de una entidad por id.
4. Primero formato → `ValidacionError`. Después reglas de negocio → `ReglaNegocioError`. Transición de estado inválida → `TransicionInvalidaError`.
5. Si el sistema puede generar un dato (fechas de alta, solicitud, despacho; `nro_remito`; vencimientos; multas), **no se le pide al usuario**.
6. Los desplegables se arman con `Combobox`, pero igual se valida que el valor esté entre las opciones.
7. Los montos son `Float` redondeados a 2 decimales.

## Cómo validar sin regex
- **Entero positivo:** `try: n = int(texto)` / `except ValueError` y luego `n > 0`. Cubre letras, decimales, `1e5` y vacío.
- **Solo letras:** `texto.replace(" ", "").replace("-", "").replace("'", "").isalpha()`, más largo mínimo y máximo.
- **Email:** una sola `@`, texto antes de la `@`, y un `.` después de la `@` que no sea el último carácter; sin espacios.
- **Teléfono:** número plano, solo dígitos (`isdigit` sobre cada carácter), entre 6 y 15; el código de país se elige aparte en un desplegable (Sudamérica, sin "+").
- **Fecha dd/mm/aaaa:** `partes = texto.split("/")`, tres partes numéricas, `date(anio, mes, dia)` (lanza `ValueError` ante 30/02).
- **Código de inventario:** recorrer los caracteres y aceptar letras mayúsculas, dígitos y guiones.

## Casos a probar en *todos* los campos
- **Texto:** vacío, solo espacios, más largo que el máximo, emojis, `<script>alert(1)</script>`, `' OR 1=1 --`, mayúsculas/minúsculas y espacios distintos en un duplicado.
- **Números:** negativo, cero, decimal donde va entero, letras, `1e5`, coma en vez de punto, número enorme, pegar texto con Ctrl+V.
- **Fechas:** pasada, futura, formato inválido, `30/02`, fin anterior al inicio.
- **Desplegables:** sin selección; valor inexistente en el DAO.
- **Estado:** entidad dada de baja, doble clic en el botón de enviar, entidad eliminada mientras otra pestaña la mostraba.

## Por entidad

### Sede
| Campo | Regla |
|---|---|
| nombre | Obligatorio, 2–80 caracteres, letras y números (al menos una letra, por ejemplo "7 Soles"), espacios, apóstrofo y guion; se guarda capitalizado; único sin distinguir mayúsculas *(supuesto)* |
| direccion | Obligatoria, hasta 120; letras, números, espacios, apóstrofo y guion, con al menos una letra (sin puntos ni comas) |
| prefijo (país) | Obligatorio, ∈ `PaisTelefono.TODOS` (desplegable de países de Sudamérica; por defecto Argentina, 54) |
| telefono | Obligatorio; número plano, solo dígitos, entre 6 y 15 (sin espacios, guiones ni "+") |
| email | Opcional; si se carga, formato `usuario@dominio.com`, hasta 100, se guarda en minúsculas |
| estado | Constante de `EstadoSede`; solo cambia con `dar_de_baja()` |
| baja | No permitir con préstamos activos, remitos en curso o reservas pendientes *(supuesto)* |
| volver a dar de alta | Solo una sede dada de baja; vuelve a ACTIVA con sus horarios, empleados y ejemplares |

**HorarioSede:** la sede se carga con su semana: se marcan los días que abre (mínimo uno) y cada día tiene su propio horario; el día no se repite en la misma sede. Apertura y cierre se eligen de un desplegable (cada 30 minutos, 06:00 a 23:30, solo con horas coherentes: el cierre, posteriores a la apertura, y viceversa) o se escriben: en vivo solo se aceptan dígitos y `:` hasta `HH:MM`, y al salir del campo se avisa en rojo una hora inválida o un cierre que no es posterior a la apertura; el DAO igual valida formato `HH:MM` (`time(hora, minuto)`) y `hora_apertura < hora_cierre` por día. Al modificar la sede se reemplaza la semana completa.

### Empleado
`legajo` lo asigna el sistema según el rol: `B` + número para BIBLIOTECARIO y `A` + número para ADMINISTRADOR, correlativo al último de esa letra (B1, B2…). Si al modificar cambia el rol, recibe un legajo nuevo con la otra letra. `nombre` obligatorio, solo letras, 2–80. `rol` ∈ `RolEmpleado`. `sede_id` obligatorio: la sede debe existir y estar ACTIVA al dar de alta. En un `MovimientoRemito` no se exige que el empleado pertenezca a la sede del remito; solo se guarda su sede.

### Socio
| Campo | Regla |
|---|---|
| nro_socio | Lo asigna el sistema al dar de alta: el más alto registrado + 1; no se modifica |
| dni | Entre 1.000.000 y 99.999.999, sin 0 adelante; se admiten puntos solo bien ubicados (la UI los pone sola al tipear); se guardan solo los dígitos; único |
| nombre, apellido | Solo letras, espacios, tildes, apóstrofo y guion; 2–50 |
| email | Opcional; si se carga, formato válido, hasta 100 |
| prefijo, telefono | Igual que Sede (teléfono obligatorio) |
| fecha_alta | La pone el sistema (hoy); si fuera editable, no puede ser futura |
| baja / inhabilitar | Baja solo sin préstamos activos *(supuesto)* |

### Libro, Autor, Categoría
| Campo | Regla |
|---|---|
| isbn (ISBN o ISSN) | Tras quitar guiones y espacios debe tener 8 (ISSN), 10 o 13 caracteres; todos dígitos salvo que ISSN e ISBN-10 pueden terminar en `X`; único. Validar el dígito verificador es un plus |
| titulo | Obligatorio, hasta 150, con al menos una letra (texto libre: admite signos) |
| editorial | Obligatoria, hasta 80, con al menos una letra |
| idioma | Obligatorio, solo letras, 2–30 |
| anio_edicion | Entero entre 1450 y el año actual |
| tipo_material | ∈ `TipoMaterial` |
| autores | Al menos uno, todos existentes |
| categoria | Existente |
| Autor | nombre y apellido solo letras; duplicado = mismo nombre y apellido normalizados |
| Categoría | nombre solo letras, 2–50, único sin distinguir mayúsculas |

*Decidido:* el campo `isbn` acepta ISBN (10 o 13) e ISSN (8), porque el catálogo incluye revistas y otros materiales de consulta.

### Ejemplar
`codigo_inventario` obligatorio, único, 3–20 caracteres entre mayúsculas, dígitos y guiones. `libro` y `sede` existentes y la sede ACTIVA. Estado inicial DISPONIBLE. `estado_fisico` ∈ `EstadoFisico`. No dar de baja un ejemplar PRESTADO, RESERVADO o EN_TRANSITO.

### Préstamo
- Socio existente y ACTIVO. Ejemplar existente y DISPONIBLE.
- El mismo socio no puede tener dos solicitudes SOLICITADO o APROBADO del mismo ejemplar (evita el doble clic). Socios distintos sí pueden pedir el mismo ejemplar: se lo lleva el primero que se aprueba.
- `ejemplar.sede == sede_origen`. Ambas sedes existentes y ACTIVAS.
- LOCAL → `origen == destino`. INTERBIBLIOTECARIO → `origen != destino`.
- `fecha_solicitud` = hoy (sistema). `fecha_prestamo` y `fecha_vencimiento` las fija el sistema cuando el préstamo pasa a ACTIVO; el vencimiento lo calcula la estrategia (31 días local, 38 interbibliotecario) y es siempre posterior a `fecha_prestamo`. El usuario no las ingresa.
- Transiciones de estado solo las permitidas. VENCIDO no se guarda: se calcula.
- Al aprobar, el ejemplar debe seguir DISPONIBLE. Interbibliotecario: pasa a RESERVADO hasta que el remito IDA se recibe; al cancelar vuelve a DISPONIBLE. Local: el préstamo se activa en la misma aprobación y el ejemplar pasa directo a PRESTADO.
- Cancelar desde EN_ENVIO solo si el remito está EMPAQUETADO: el ejemplar sale del remito (si era el único, se cancela el remito). Si ya fue despachado o está en tránsito, se rechaza.

### Reserva
Socio ACTIVO. Libro existente. `sede_retiro` ACTIVA. `fecha_reserva` = hoy. `fecha_vencimiento` la calcula el sistema: hoy + 45 días mientras está PENDIENTE; al asignarle un ejemplar se reescribe como hoy + 2 días (plazo de retiro). No duplicar una reserva PENDIENTE/DISPONIBLE del mismo socio y libro *(supuesto)*. Si hay un ejemplar DISPONIBLE del título en la sede, se asigna en el acto. Cancelar solo si está PENDIENTE o DISPONIBLE. Retirar solo si está DISPONIBLE: crea un préstamo LOCAL activo, con las mismas reglas que cualquier préstamo (socio habilitado, sede activa).

### Devolución y multa
- El préstamo debe estar ACTIVO (vencido o no, porque VENCIDO no se guarda); no se devuelve dos veces. Si es interbibliotecario, se crea el remito DEVOLUCION.
- `fecha_devolucion` no futura y ≥ `fecha_prestamo`.
- `estado_fisico` ∈ `EstadoFisico`. `observaciones` hasta 300; **obligatorias** si es DANADO o DESTRUIDO.
- Multa: la calcula el sistema; `dias_atraso` entero ≥ 0, `monto` ≥ 0 con 2 decimales; estado solo PENDIENTE → PAGADA.

### Remito, movimientos e incidencias
- `nro_remito` lo genera el sistema (único, p. ej. `REM-000001`).
- `sede_origen != sede_destino`, ambas ACTIVAS.
- Al menos un ítem; cada ejemplar asociado a un préstamo en estado correcto (APROBADO para IDA; para DEVOLUCION, un préstamo interbibliotecario ya DEVUELTO cuyo ejemplar todavía no volvió a su sede) y que no esté en otro remito abierto.
- Transición inválida (p. ej. cancelar un remito DESPACHADO) → `TransicionInvalidaError`.
- Movimiento: empleado obligatorio y existente; observación hasta 200, obligatoria al cancelar o dar por extraviado.
- Incidencia: `tipo` ∈ `TipoIncidencia`; `fecha` no futura y ≥ `fecha_creacion` del remito; descripción 5–300.

**Textos libres** (título, editorial, observaciones, descripciones): aceptan signos como `<`, `'` o `--` a propósito. No hay riesgo de inyección SQL porque el ORM pasa los valores como parámetros (nunca se arma SQL con texto), y Tkinter muestra el texto tal cual, sin interpretarlo.

**Cobertura automática:** `tests/test_entradas_invalidas.py` recorre los "casos a probar en todos los campos" contra cada alta y operación de los DAO, y comprueba que siempre terminen en `ValidacionError` o `ReglaNegocioError` (nunca en un error de la base).

## Guion de pruebas manuales (ensayo de defensa)
1. Alta de socio con DNI `abc`, `-5`, `1234567890123`, repetido y con espacios.
2. Alta de socio con nombre vacío, con números, y con 200 caracteres.
3. Libro con año `-1`, `3000`, `dos mil` y con ISBN repetido.
4. Sede con teléfono de letras, email sin `@`, horario con cierre antes de la apertura.
5. Préstamo de un ejemplar PRESTADO, de un socio INHABILITADO, de otra sede, hacia una sede de BAJA.
6. Préstamo LOCAL con origen distinto de destino.
7. Devolución dos veces del mismo préstamo; con fecha futura; dañado sin observaciones.
8. Remito: cancelar uno ya DESPACHADO, saltar de EMPAQUETADO a RECIBIDO, extraviar uno que no está EN_TRANSITO.
9. Reserva sobre sede de baja; segunda reserva idéntica.
10. En cada formulario: escribir letras en un campo numérico, pegar texto con Ctrl+V y apretar el botón de enviar dos veces seguidas.
11. Cancelar un préstamo EN_ENVIO cuyo remito ya está DESPACHADO; dejar una reserva PENDIENTE pasada su espera y ver que queda VENCIDA y libera el ejemplar.
12. Intentar operar sin elegir el empleado actual.
