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
- **Teléfono:** recorrer los caracteres y aceptar dígitos, espacios, `+`, `-` y paréntesis; contar entre 6 y 15 dígitos.
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
| nombre | Obligatorio, 2–80 caracteres, único sin distinguir mayúsculas *(supuesto)* |
| direccion | Obligatoria, hasta 120 |
| telefono | Obligatorio; solo dígitos, espacios, `+`, `-`, `()`; entre 6 y 15 dígitos |
| email | Formato válido, hasta 100 |
| estado | Constante de `EstadoSede`; solo cambia con `dar_de_baja()` |
| baja | No permitir con préstamos activos, remitos en curso o reservas pendientes *(supuesto)* |

**HorarioSede:** mínimo un horario por sede; día entre lunes y domingo y sin repetirse en la misma sede; formato `HH:MM` (`time(hora, minuto)`); `hora_apertura < hora_cierre`.

### Empleado
`legajo` obligatorio, único, letras y dígitos, hasta 20. `nombre` obligatorio, solo letras, 2–80. `rol` ∈ `RolEmpleado`. `sede_id` obligatorio: la sede debe existir y estar ACTIVA al dar de alta. En un `MovimientoRemito` no se exige que el empleado pertenezca a la sede del remito; solo se guarda su sede.

### Socio
| Campo | Regla |
|---|---|
| nro_socio | Entero > 0, único |
| dni | Solo dígitos (se admiten puntos y se quitan), 7 u 8 dígitos, único |
| nombre, apellido | Solo letras, espacios, tildes, apóstrofo y guion; 2–50 |
| email | Formato válido, hasta 100 |
| telefono | Igual que Sede |
| fecha_alta | La pone el sistema (hoy); si fuera editable, no puede ser futura |
| baja / inhabilitar | Baja solo sin préstamos activos *(supuesto)* |

### Libro, Autor, Categoría
| Campo | Regla |
|---|---|
| isbn (ISBN o ISSN) | Tras quitar guiones y espacios debe tener 8 (ISSN), 10 o 13 caracteres; todos dígitos salvo que ISSN e ISBN-10 pueden terminar en `X`; único. Validar el dígito verificador es un plus |
| titulo | Obligatorio, hasta 150 |
| editorial, idioma | Obligatorios, hasta 80 y 30 |
| anio_edicion | Entero entre 1450 y el año actual |
| tipo_material | ∈ `TipoMaterial` |
| autores | Al menos uno, todos existentes |
| categoria | Existente |
| Autor | nombre y apellido solo letras; duplicado = mismo nombre y apellido normalizados |
| Categoría | nombre obligatorio, único |

*Decidido:* el campo `isbn` acepta ISBN (10 o 13) e ISSN (8), porque el catálogo incluye revistas y otros materiales de consulta.

### Ejemplar
`codigo_inventario` obligatorio, único, 3–20 caracteres entre mayúsculas, dígitos y guiones. `libro` y `sede` existentes y la sede ACTIVA. Estado inicial DISPONIBLE. `estado_fisico` ∈ `EstadoFisico`. No dar de baja un ejemplar PRESTADO, RESERVADO o EN_TRANSITO.

### Préstamo
- Socio existente y ACTIVO. Ejemplar existente y DISPONIBLE.
- `ejemplar.sede == sede_origen`. Ambas sedes existentes y ACTIVAS.
- LOCAL → `origen == destino`. INTERBIBLIOTECARIO → `origen != destino`.
- `fecha_solicitud` = hoy (sistema). `fecha_prestamo` y `fecha_vencimiento` las fija el sistema cuando el préstamo pasa a ACTIVO; el vencimiento lo calcula la estrategia (31 días local, 38 interbibliotecario) y es siempre posterior a `fecha_prestamo`. El usuario no las ingresa.
- Transiciones de estado solo las permitidas. VENCIDO no se guarda: se calcula.
- Al aprobar, el ejemplar debe seguir DISPONIBLE. Interbibliotecario: pasa a RESERVADO hasta que el remito IDA se recibe; al cancelar vuelve a DISPONIBLE. Local: el préstamo se activa en la misma aprobación y el ejemplar pasa directo a PRESTADO.
- Cancelar desde EN_ENVIO solo si el remito está EMPAQUETADO; si ya fue despachado o está en tránsito, se rechaza.

### Reserva
Socio ACTIVO. Libro existente. `sede_retiro` ACTIVA. `fecha_reserva` = hoy. `fecha_vencimiento` la calcula el sistema: hoy + 45 días mientras está PENDIENTE; al asignarle un ejemplar se reescribe como hoy + 2 días (plazo de retiro). No duplicar una reserva PENDIENTE/DISPONIBLE del mismo socio y libro *(supuesto)*. Cancelar solo si está PENDIENTE o DISPONIBLE.

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
