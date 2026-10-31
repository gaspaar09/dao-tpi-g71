Desarrollo de Aplicaciones con Objetos 

FRC – UTN 

# **Trabajo práctico integrador** 

Documento de referencia de desarrollo 

## **1. Grupo** 

|Número de grupo:|71                            Tema: Biblioteca|
|---|---|
|Integrantes:||
|Legajo|Nombre|
|404034|Ferreyra, Martín|
|400137|Silberstein, Gaspar|
|403596|Germano, Francisco|



## **2. Propuesta** 

### **Objetivos del sistema** 

**Objetivo general.** Desarrollar un sistema orientado a objetos que permita a una red de bibliotecas públicas administrar sus sedes, socios, catálogo y ejemplares, y gestionar los préstamos locales e interbibliotecarios, incluido el envío de ejemplares entre sedes con trazabilidad mediante remito, reemplazando las tareas manuales actuales por un control centralizado y confiable. 

#### **Objetivos específicos** 

- Centralizar la administración de sedes, socios, catálogo y ejemplares físicos, evitando duplicados y registros inconsistentes. 

- Controlar el ciclo completo del préstamo, desde la solicitud (local o interbibliotecaria) hasta la devolución, validando disponibilidad del ejemplar, habilitación del socio, vencimientos y pertenencia del ejemplar a la sede de origen. 

- Garantizar la trazabilidad de cada ejemplar enviado entre sedes mediante remitos con historial de estados (empaquetado, despachado, en tránsito, recibido). 

- Facilitar al personal y a los socios la consulta de disponibilidad del catálogo por sede y la gestión de reservas. 

- Registrar las devoluciones junto con el estado físico del material y calcular las multas por vencimiento. 

- Proveer reportes de gestión sobre préstamos, material en tránsito, demanda de títulos y movimientos entre sedes que apoyen la toma de decisiones de la red. 

- Construir el sistema sobre un diseño orientado a objetos extensible, aplicando patrones de diseño, de modo que los procesos opcionales puedan incorporarse sin rehacer el modelo. 

Desarrollo de Aplicaciones con Objetos 

FRC – UTN 

### **Alcances** 

#### **Procesos obligatorios incluidos** 

- **Sedes:** alta, modificación y baja lógica de sedes (dirección, datos de contacto, horarios y estado activa/baja). 

- **Socios:** alta, modificación, baja e inhabilitación de socios, con control de duplicados por DNI y número de socio. 

- **Catálogo y ejemplares:** administración de libros y otros materiales de consulta, y de sus ejemplares físicos, cada uno asignado a la sede a la que pertenece. 

- **Solicitudes de préstamo:** registro de préstamos locales e interbibliotecarios, indicando sede origen y sede destino. 

- **Logística de ejemplares:** empaquetado, despacho y recepción de ejemplares con asignación de remito y trazabilidad por estados a lo largo del trayecto. 

- **Disponibilidad:** consulta de disponibilidad de ejemplares por título y por sede. 

- **Reservas:** alta, cancelación, vencimiento y asignación de un ejemplar cuando queda disponible. 

- **Devoluciones:** registro de la devolución y del estado físico del material devuelto, con generación de multa si corresponde. 

#### **Validaciones de negocio** 

- No prestar ejemplares que no estén disponibles. 

- No prestar material a socios inhabilitados. 

- Controlar las fechas de vencimiento de los préstamos. 

- Mantener la trazabilidad del remito durante todo el trayecto (cada cambio de estado queda registrado). 

- Evitar duplicados de socios, catálogo y ejemplares. 

- No prestar ejemplares que no pertenezcan a la sede de origen del préstamo. 

- No iniciar préstamos, reservas ni envíos desde o hacia una sede dada de baja. 

#### **Ciclo de vida del remito** 

EMPAQUETADO → DESPACHADO → EN_TRÁNSITO → RECIBIDO. Un remito puede pasar a CANCELADO solo antes del despacho y a EXTRAVIADO desde EN_TRÁNSITO. Las transiciones no permitidas se rechazan, y cada cambio genera un movimiento con fecha, estado anterior, estado nuevo y empleado responsable. La devolución de un préstamo interbibliotecario genera un remito de tipo DEVOLUCIÓN hacia la sede propietaria. 

#### **Reportes previstos** 

- Préstamos activos y material en tránsito. 

- Préstamos vencidos y multas acumuladas por socio. 

- Libros más solicitados para préstamos inter-sedes. 

- Disponibilidad de catálogo por sede. 

- Tasa de envíos exitosos e incidencias. 

- Movimiento de ejemplares entre sedes: envíos por sede origen/destino y tiempo promedio de tránsito. 

#### **Decisiones de diseño** 

- **Patrón State:** para el ciclo de vida del remito (y del préstamo), donde cada estado define qué transiciones admite. 

- **Patrón Strategy:** para el cálculo de multas y plazos de vencimiento según el tipo de préstamo. 

- **Patrón Factory Method (a confirmar):** para crear préstamos locales e interbibliotecarios con sus reglas propias. 

#### **Supuestos** 

- Cada ejemplar pertenece a una única sede; en un préstamo interbibliotecario viaja a la sede destino, donde lo retira el socio, y vuelve a su sede propietaria con un remito de devolución. 

- Un remito puede agrupar varios ejemplares entre el mismo par de sedes. 

- La reserva se realiza sobre un título y una sede de retiro, y se asigna a un ejemplar concreto cuando hay uno disponible. 

Desarrollo de Aplicaciones con Objetos 

FRC – UTN 

- Usuarios del sistema: el personal (empleados con rol) opera los procesos; los socios consultan disponibilidad y catálogo. 

#### **Fuera del alcance inicial** 

Los procesos opcionales (envío de notificaciones, historial de lecturas, recomendaciones, inventario con códigos y revisión detallada de la recepción por extravío, daño o destrucción) no se incluyen en la versión base y se evaluarán según el tiempo disponible. El modelo ya contempla puntos de extensión: el código de inventario del ejemplar, el estado físico y las incidencias de envío. Tampoco se incluyen el cobro de multas ni la autenticación avanzada: solo se registra el estado de la multa. 

### **DER o Diagrama de Clases UML** 



<!-- Start of picture text -->
Seonemtstone ioestoSmctacon<br>stan Etadasoce tetaera Tooter<br>nab ‘ be<br>tipo: Tipotnvio [idReserva [Autor] .<br>{fechaDespachoetotneon sareelestado:caerEstadoReserva| ‘mtor|ore ——(etepor]Saco[nombre<br>[fechaRecepcion asignarEjemplar()<br>YA x<br>|ven ibe:2Tpoincdenca Jereccen (_ae<br>etaoneerr ettons ameansote ae<br>estaoneer bes eon “<br>esacome eeerecon Sten: tase =<br>[darDeBaja() a<br>4 .<br>ajo=. sstcroen icontne _|saseman5Sates repos | eta:coarsestadeerar eters<br>[a Roto eaciere stadeponie)comarca)<br>teearene tocresam | os<br>ecarestomo<br>fears<br>okie)<br>etaverio<br>Hee<br>=<br><!-- End of picture text -->

**Figura 1.** Diagrama de clases UML del sistema. Las asociaciones sedeOrigen y sedeDestino de Préstamo y Remito apuntan a la misma clase Sede. 

**Enumeraciones** 

- **EstadoSede:** ACTIVA, BAJA 

Desarrollo de Aplicaciones con Objetos 

FRC – UTN 

- **EstadoSocio:** ACTIVO, INHABILITADO, BAJA 

- **TipoMaterial:** LIBRO, REVISTA, MATERIAL_CONSULTA 

- **EstadoEjemplar:** DISPONIBLE, RESERVADO, PRESTADO, EN_TRANSITO, DANADO, EXTRAVIADO, BAJA 

- **EstadoFisico:** NUEVO, BUENO, REGULAR, DANADO, DESTRUIDO 

- **TipoPrestamo:** LOCAL, INTERBIBLIOTECARIO 

- **EstadoPrestamo:** SOLICITADO, APROBADO, EN_ENVIO, ACTIVO, VENCIDO, DEVUELTO, CANCELADO 

- **EstadoReserva:** PENDIENTE, DISPONIBLE, CUMPLIDA, CANCELADA, VENCIDA 

- **EstadoMulta:** PENDIENTE, PAGADA 

- **TipoEnvio:** IDA, DEVOLUCION 

- **EstadoRemito:** EMPAQUETADO, DESPACHADO, EN_TRANSITO, RECIBIDO, CANCELADO, EXTRAVIADO 

- **TipoIncidencia:** EXTRAVIO, DANIO, DEMORA 

- **RolEmpleado:** BIBLIOTECARIO, ADMINISTRADOR 

#### **Notas del modelo** 

- Libro representa el título del catálogo y Ejemplar la copia física; la disponibilidad se controla sobre el ejemplar. 

- La regla de pertenencia se valida comparando la sede del ejemplar con la sedeOrigen del préstamo. 

- ItemRemito vincula cada ejemplar enviado con el préstamo que lo originó, y MovimientoRemito guarda el historial de estados del remito. 

