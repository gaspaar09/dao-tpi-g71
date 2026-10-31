### **Programación estructurada** 

##### **1.1 Tipos de datos** 

El lenguaje Python ofrece una importante variedad de tipos de datos, de entre los cuales se destacan los siguientes: 

|Categoría|Tipo|Nombre|Uso|
|---|---|---|---|
|Texto|Cadena|str|Cadenas de caracteres de longitud arbitraria|
|Numérico|Entero|int|Números enteros|
|Numérico|Flotante|float|Números con punto flotante|
|Numérico|Complejo|complex|Números complejos|
|Lógico|Booleano|bool|Valores de verdad|
|Secuencia|Tupla|tuple|Secuencia inmutable de valores|
|Secuencia|Lista|lista|Secuencia mutable de valores|
|Secuencia|Rango|range|Secuencia inmutable de números enteros|
|Conjunto|Conjunto|set|Conjunto de valores sin repetición y con búsquedas<br>rápidas|
|Asociación|Diccionario|dict|Pares ordenados clave / valor|
|Vacío|Sin tipo|none|Variables declaradas pero sin valor ni tipo|



3 

**1. Programación estructurada** 

**4** 

##### **1.2 Operadores** 

Los datos de cada uno de los tipos del lenguaje pueden ser manipulados mediante un conjunto de operadores. Un operador es un símbolo o una palabra que realiza una operación sobre uno o más valores. Los valores pueden ser constantes, variables o expresiones. Los operadores pueden manipular una cantidad diferente de valores. La mayoría de los operadores se denominan binarios porque requieren dos operandos que es indican antes y después del operador. Asimismo existen algunos operadores unarios y un único operador ternario. 

###### **1.2.1 Operadores aritméticos** 

Requieren dos operandos numéricos de cualquier tipo. Si ambos operandos son del mismo tipo, es decir, dos enteros o dos flotantes el resultado generalmente será del mismo tipo de los operandos. En caso de que sean de tipos diferentes, el resultado será del tipo más grande. Por lo tanto, si se opera con un entero y un flotante, el resultado será flotante. 

|Símbolo|Uso|Observaciones|
|---|---|---|
|+<br>-|Suma<br>Diferencia|Aplicado a cadenas efectúa una concatenación|
|*|Producto|Si un operando es una cadena y el otro es un entero, repite la cadena<br>tantas veces como indique el operando numérico<br>l|
|/|Cociente|Siempre retorna un float|
|//|Cociente|Siempre retorna un int truncando los decimales|
||entero||
|%|Módulo|Retorna el resto de una división|
|***|Potencia|Retorna el primer operando elevado a la potencia indicada por el<br>segundo.|



###### **1.2.2 Operadores de asignación** 

Los operadores de asignación siempre son binarios, de los cuales el primer operando debe ser una variable o cualquier lugar donde se pueda guardar un valor, tal como un parámetro actual y el segundo debe ser una expresión. El tipo retornado siempre es el de la expresión asignada. 

**1.2. Operadores** 

**5** 

|Símbolo|Uso|Observaciones|
|---|---|---|
|=|Asignación||
|+=|Acumu-<br>lación<br>o<br>incremento|El primer operando debe ser una variable a la cual se le incrementa<br>su valor con el resultado de la expresión del segundo operando|
|-=|Decremen-||
||to||
|**= /=|Combina-<br>dos|Todas las operaciones aritméticas pueden ser combinadas con asig-<br>nación, aunque su uso es infrecuente|



###### **1.2.3 Operadores de comparación** 

Los operadores de comparación comparan los valores de dos operandos de un mismo tipo y retornan un valor de verdad. Si los tipos comparados son diferentes, se promueve uno de esos al tipo más amplio. 

|Símbolo|Uso|Observaciones|
|---|---|---|
|==|Igualdad||
|!=|Diferencia||
|>|Mayor que||
|<|Menor que||
|>=|Mayor o igual||
|<=|Menor o igual||



Existe un operador de comparación cuya sintaxis y comportamiento son diferentes al resto. Es el único operador ternario del lenguaje y permite escribir como una expresión un cálculo que de otra forma requiere una instrucción condicional **if** - **else** . La sintaxis del operador es: 

[valor si verdadero] **if** [condicion] **else** [valor si falso] 

El operador evalua la condición, la cual debe evaluarse o convertirse a un valor de verdad, si la misma es verdadera se retorna el primer operando y en caso contrario el último. 

importe = 45345 saldo = "Acreedor" **if** importe > 0 **else** "Deudor" _# La variable saldo finaliza con valor "Acreedor"_ 

existe = **False** print("Si" **if** existe **else** "No") _# Imprime "Si"_ 

**1. Programación estructurada** 

**6** 

###### **1.2.4 Operadores lógicos** 

Permiten efectuar operaciones de algebra booleana entre dos valores de verdad. Si los operandos no son booleanos los convierte evaluando los valores vacíos de cada tipo de datos como falsos, y cualquier otro valor como verdadero. 

|Símbolo|Uso|Observaciones|
|---|---|---|
|and|Y lógico|Aplica corto circuito, si el primer operando es falso, retorna falso sin<br>evaluar el segundo|
|or|O lógico|Aplica corto circuito, si el primer operando es verdadero, retorna<br>verdadero sin evaluar el segundo|
|not|Negación|Es un operador unario, invierte el valor de verdad indicado a conti-<br>nuación del mismo|



##### **1.3 Estructuras condicionales** 

###### **1.3.1 Instrucción if** 

La instrucción if en Python permite ejecutar un bloque de código si se cumple una condición. La sintaxis general es: 

**if** condicion: bloque de codigo 

La condición puede ser una expresión lógica o booleana que se evalúa como verdadera (True) o falsa (False). Si la condición es verdadera, se ejecuta el bloque de código indentado después de los dos puntos (:). Si la condición es falsa, se salta el bloque de código y se continúa con el resto del programa. Por ejemplo: 

**if** x > 0: print("x es positivo") 

En este caso, se imprime el mensaje ”x es positivo”solo si la variable x tiene un valor mayor que cero. De lo contrario, no se hace nada. 

La instrucción if se puede combinar con else o elif para definir otros casos alternativos. Else se usa para ejecutar un bloque de código si la condición 

**1.3. Estructuras condicionales** 

**7** 

del if no se cumple. Elif se usa para evaluar otra condición después del if. Se pueden usar varios elif para crear múltiples ramas. 

Por ejemplo: 

**if** x > 0: print("x es positivo") **elif** x < 0: print("x es negativo") **else** : print("x es cero") 

En este caso, se imprime un mensaje diferente según el valor de x. Si x es positivo, se imprime “x es positivo”. Si x es negativo, se imprime “x es negativo”. Si x es cero, se imprime “x es cero”. 

###### **1.3.2 Condiciones** 

Las instrucciones y cláusulas que evalúan condiciones exigen que la condición sea escrita como una expresión booleana. Como tal, una expresión puede ser una constante, una variable o el resultado de una operación. 

Aunque es muy infrecuente, puede plantearse una condición con un valor True constante, pero esta variante tiene sentido únicamente si se plantea un ciclo infinito. 

En cambio sí es muy habitual evaluar variables de tipo boolean, conocidas generalmente como banderas o centinelas. Para estas variables, la condición se redacta únicamente con el nombre de la variable. Durante la ejecución, el valor que la misma almacene servirá para ejecutar o no el bloque de la instrucción condicional. De esa manera si se dispone de una variable llamada existe, la redacción preferida de una instrucción if sera **if** existe:, siendo innecesario y hasta negativo el uso de una comparación con **if** existe ==) **True** :. De la misma manera, si se requiere evaluar que la variable contenga un valor falso, la redacción preferida es **if not** existe: en lugar de comprarar **if** existe ==) **False** :. 

En las condiciones que involucren variables de tipos diferentes al boolean, la expresión a evaluar se redacta como una operación que utilice los operadores que devuelven valores de verdad, es decir, los operadores de comparación y los operadores lógicos. 

**1. Programación estructurada** 

**8** 

###### **1.3.3 Conversiones a boolean** 

Python ofrece un mecanismo de conversiones implícitas de todos los tipos de datos a boolean. Esta caracterísitica permite evaluar como verdaderas o falsas variables o expresiones de otros tipos aplicando ciertas reglas de conversión. 

Esta característica se denomina _truthiness_ y puede ser fuente de serios errores hasta que se la comprende acabadamente. La idea principal es que todo valor de un tipo diferente al boolean puede ser interpretado “como si fuera verdadero” ( _truthy_ ) o “como si fuera falso” ( _falsy_ ). 

El criterio general es que se considera falsy todo dato “vacío”, dependiendo el valor exacto del tipo de datos. En el caso de los datos más simples el vacío es el más natural: 0 para los tipos numéricos, cadena vacía en el caso de las cadenas y None en el caso de las referencias a estructuras u objetos. Por otro lado, en los casos de las secuencias y estructuras de datos, se evalúan como falsy si están vacías, es decir, sin elementos. 

Esta conversión implícita puede ser utilizada en ciertas condiciones para mejorar la legibilidad de la misma. De la misma manera en que para evaluar una bandera es preferible evitar la comparación con los valores True y False, se puede aprovechar la misma idea al evaluar si una lista está vacía o si una variable numérica es 0. 

Con este criterio, las siguientes condiciones son válidas: 

nombre = input("Ingrese su nombre") edad = int(input("Ingrese su edad)) **if not** nombre: print("No ingresó su nombre") **if not** edad: print("Debe ingresar una edad diferente a 0") print("Su edad es " + ("impar" **if** edad % 2 **else** "par")) 

###### **1.3.4 Combinación de condiciones** 

Una característica particular del lenguaje python que siendo muy útil resulta difícil de aprender es la posibilidad que brinda para combinar operadores condicionales. 

Una situación muy habitual es la de verificar si un valor numérico se encuentra en un rango. Para ello la solución más simple es la de comparar el valor con cada uno de los extremos del rango y conectar con el operador AND: 

**1.4. Estructuras repetitivas** 

**9** 

**if** nota > 0 **and** nota <=) 10: 

Pero dado que las condiciones que evalúan cada extremo del rango involucran a la misma variable y que ambas están conectadas por and, se pueden combinar de la siguiente forma: 

**if** 0 < nota <=) 10: 

Debe prestarse especial atención a que esta posiblidad puede llevar a errores difíciles de detectar. Por ejemplo, es una situación razonable determinar que dos variables cumplan con la misma condición, por caso, que sean mayores a 5. La única forma adecuada es la de evaluar **if** a > 5 **and** b > 5. Pero es tentador intentar una combinación de la forma: 

**if** a **and** b > 5: 

La condición anterior, aunque es válida desde el punto de vista de la sintaxis del lenguaje, no evalúa lo que parece a simple vista: el operador and posee como primer operando una variable numérica la cual evalúa como truthy si es distinta de 0, por lo tanto dicha condición es equivalente a **if** a !=) 0 **and** b > 5. 

Otro inconveniente similar ocurre si se intenta combinar las condiciones como: 

**if** a > b > 5: 

En este otro caso ocurre algo similar, la sintaxis es correcta, pero el funcionamento es algo diferente. Esta condición efectivamente verifica que ambas variables sean mayores a 5, pero además exige que la segunda sea mayor a la primera, restricción que no estaba solicitada originalmente. 

##### **1.4 Estructuras repetitivas** 

###### **1.4.1 Instrucción for** 

La instrucción for permite iterar sobre una secuencia de elementos, como un rango, una lista, una tupla o un diccionario. La sintaxis general de la 

**1. Programación estructurada** 

**10** 

###### instrucción for es la siguiente: 

**for** elemento **in** secuencia: _# hacer algo con el elemento_ 

La variable elemento toma el valor de cada elemento de la secuencia en cada iteración del bucle. El bloque de código que se ejecuta en cada iteración debe estar indentado. El bucle termina cuando se recorre toda la secuencia o cuando se encuentra una instrucción break. 

La instrucción for es utilizada para realizar tareas repetitivas con los elementos de una secuencia, como sumarlos, modificarlos o filtrarlos. También se puede usar para crear nuevas secuencias a partir de otras existentes, usando la comprensión de listas, tuplas o diccionarios. 

Por ejemplo, para recorrer una lista se puede escribir el siguiente ciclo: 

frutas = ["manzana", "banana", "naranja"] _# Por cada fruta de la lista de frutas:_ **for** fruta **in** frutas: print(fruta) 

###### **1.4.2 Instrucción while** 

La instrucción “while” en Python se utiliza para crear un bucle o ciclo que se repite mientras se cumple una condición específica. A diferencia de la instrucción “for” que se utiliza para iterar sobre una secuencia conocida, la instrucción “while” se repite hasta que una condición se evalúa como falsa. La sintaxis general de la instrucción es la siguiente: 

**while** condición: _# bloque iterativo_ 

En el ejemplo anterior “condición” es una expresión que se evalúa en cada iteración del bucle. Si la condición es verdadera, el bloque de código dentro del bucle se ejecuta. Si la condición es falsa el ciclo finaliza. 

Es importante tener cuidado al utilizar la instrucción while para evitar que el bucle se convierta en un ciclo infinito. Para evitar esto, es común utilizar una lógica dentro del bucle que modifique las variables involucradas en la condición para que eventualmente se evalúe como falsa y el ciclo se detenga. 

**1.4. Estructuras repetitivas** 

**11** 

En el siguiente ejemplo se obtiene la suma de todos los dígitos de un número con operaciones aritméticas, por medio de la extracción del último dígito con el operador de módulo. En cada vuelta se desplazan los restantes digitos efectuando una división entera en 10. Dado que no necesariamente se conoce la cantidad de dígitos del número ingresado, se debe utilizar un ciclo while que dará una vuelta por cada dígito, y finaliza cuando el número se reduce a 0. 

numero = int(input("Ingrese un número: ")) suma_digitos = 0 **while** numero > 0: _# Obtiene el último dígito del número_ digito = numero % 10 _# Agrega el dígito a la suma total_ suma_digitos += digito _# Elimina el último dígito del número_ numero /l)= 10 print("La suma de los dígitos es:", suma_digitos) 

###### **1.4.3 Saltos** 

La instrucción **break** se utiliza para terminar un bucle antes de que se complete su condición de finalización. Debe encontrarse dentro de alguna instrucción condicional que determine el momento en que debe interrumpirse el ciclo. La instrucción break solo afecta al bucle en el que se encuentra y no a los bucles anidados o externos. 

La instrucción **continue** se utiliza dentro de ciclos para omitir el resto del código en una iteración actual y pasar a la siguiente iteración. Cuando se encuentra una instrucción continue, el flujo de ejecución del programa salta inmediatamente al principio del ciclo, sin ejecutar el código restante de esa iteración en particular. 

###### **1.4.4 Cláusula else** 

La cláusula **else** en los ciclos se utiliza para especificar un bloque de código que se ejecuta cuando el ciclo ha terminado de iterar sobre todos los elementos de una secuencia o cuando la condición del ciclo se evalúa como falsa. La cláusula else se ejecuta después de que el ciclo ha finalizado de forma normal, es decir, sin interrupciones como break o return. 

**1. Programación estructurada** 

**12** 

En el siguiente ejemplo se verifica la existencia de la letra A en una cadena. En el momento en que se encuentra la primera aparición se interrumpe el ciclo con break para no continuar con el recorrido. Por lo tanto, que el ciclo finalice normalmente, sin la interrupción, significa que la letra no fue encontrada: 

texto = input("Ingrese un texto: ") **for** letra **in** texto: **if** letra ==) "A": print("Contiene la letra A") **break else** : print("No contiene la letra A") 

##### **1.5 Funciones** 

###### **1.5.1 Sintaxis** 

Las funciones se definen utilizando la palabra clave **def** seguida del nombre de la función. Luego del nombre deben existir un par de paréntesis que pueden contener los parámetros de la función y el símbolo de dos puntos (:). A continuación, se escribe el bloque de código de la función indentado. 

**def** nombre_de_funcion(parametro1, parametro2, .\))): _# Bloque de código de la función # Puede incluir declaraciones, operaciones y retornos_ 

En el siguiente ejemplo se define una función con retornos y parámetros: 

**def** calcular_area_triangulo(base, altura): area = (base * altura) / 2 **return** area 

La función llamada calcular_area_triangulo que toma dos parámetros base y altura. Dentro del bloque de código de la función, se calcula el área de un triángulo utilizando la fórmula correspondiente y se almacena en la variable area. Luego, se utiliza la palabra clave **return** para devolver el valor calculado de area como resultado de la función. 

Después de definir una función, puede ser invocada desde otro lugar del código utilizando su nombre y proporcionando los argumentos necesarios. De esta manera la función anterior puede ser invocada como: 

**1.5. Funciones** 

**13** 

resultado = calcular_area_triangulo(5, 3) print("El área del triángulo es:", resultado) 

En el caso de que una función no incluya una instrucción return o posea una instrucción return sin indicar ningún valor de retorno, la misma retorna automáticamente un valor de None al finalizar su ejecución. 

###### **1.5.2 Parámetros** 

Existen diversas formas de indicar los parámetros de una función, cada una de las cuales tiene una utilidad bien marcada. 

**Parámetros posicionales:** Son los parámetros que se pasan a la función en el mismo orden en el que se definen en la firma de la función. Estos parámetros son obligatorios y deben ser proporcionados al llamar a la función. 

**def** saludar(nombre, edad): print("Hola", nombre, "tenés", edad, "años.") saludar("Olga", 25) _# Ejemplo de llamada con parámetros posicionales_ 

**Parámetros con valor predeterminado:** Son parámetros que tienen un valor asignado por defecto en caso de que no se les pase un valor al llamar a la función. Estos parámetros son opcionales. 

**def** saludar(nombre, edad=30): print("Hola", nombre, "tenés", edad, "años.") saludar("Jorge") _# Ejemplo de llamada sin proporcionar el parámetro "edad"_ 

**Parámetros de palabra clave:** Se especifican durante la llamada a la función utilizando el formato nombre_parametro=valor. Estos parámetros son opcionales, por lo tanto permiten omitir aquellos que posean un valor por defecto. Asimismo permiten especificar los argumentos en cualquier orden. 

**def** saludar(nombre, edad): print("Hola", nombre, "tenés", edad, "años.") saludar(edad=40, nombre="Carlos") 

**1. Programación estructurada** 

**14** 

_# Ejemplo de llamada con parámetros de palabra clave_ 

**Parámetros variables (*args):** Permite pasar un número variable de argumentos posicionales a una función. Los argumentos se agrupan en una tupla dentro de la función. 

**def** sumar(*numeros): total = 0 **for** num **in** numeros: total += num **return** total resultado = sumar(1, 2, 3, 4, 5) _# Ejemplo de llamada con parámetros variables_ 

**Parámetros de palabras clave variables (**kwargs):** Permite pasar un número variable de argumentos de palabra clave a una función. Los argumentos se agrupan en un diccionario dentro de la función. 

**def** imprimir_datos(**)datos): **for** clave, valor **in** datos.items(): print(clave + ":", valor) imprimir_datos(nombre="Juana", edad=25, ciudad="Pinamar") _# Ejemplo de llamada con parámetros de palabras clave variables_ 

###### **1.5.3 Retorno** 

Las funciones pueden retornar cero, uno o más expresiones como resultados. En el caso de no incluir ninguna instrucción return, u omitir el valor retornado, la misma entrega un valor de None. 

Para que una función retorne más de un valor, se los debe indicar separados por comas. En la invocación a la misma los valores retornados pueden ser asignados a una serie de variables también separadas por comas. 

Por ejemplo, la siguiente función recibe como parámetro una lista de números y devuelve la sumatoria de los mismos y su promedio: 

**def** promedio_suma(numeros): suma = 0 **for** x **in** numeros: suma += n promedio = suma / len(numeros) 

**1.5. Funciones** 

**15** 

**return** promedio, suma lista = [10, 20, 30, 40, 50] promedio, suma = promedio_suma(lista) print("Promedio:", promedio) print("Suma:", suma) 

**1. Programación estructurada** 

**16** 

##### **1.6 Ejercicios** 

###### **1.6.1 Estación de servicio** 

Una estación de servicio que dispone de 10 surtidores y necesita gestionar información relacionada con la venta de combustibles en la jornada. 

De cada surtidor se conoce: 

- Número de Surtidor (validar que sea un número entre 1 y 30) 

- Cantidad: representa la cantidad de litros de combustible vendido por el surtidor (validar que sea un número positivo) 

- Tipo: representa el tipo de combustible del surtidor. Los valores que puede asumir son 1 representa “Nafta Super”, 2 representa “Nafta Especial” y 3 representa “Gasoil” (validar que se ingresen valores válidos). 

Se pide calcular e imprimir: 

- El total de litros vendidos en la jornada, por tipo de combustible. 

- El número de surtidor que menos combustible vendió. 

- El promedio por surtidor en litros de combustible vendido en la jornada (promedio general, es un único resultado). 

**1.6. Ejercicios** 

**17** 

###### **estacion.py** 

total_nafta_super = total_nafta_especial = total_gasoil = 0 menor = **None** surtidor_menor = **None** total = 0 **for** i **in** range(10): numero = int(input('Ingrese número de surtidor (1 a 30): ')) **while not** 0 < numero <=) 30: print('Ingresó un número inválido') numero = int(input('Ingrese número de surtidor (1 a 30): ')) cantidad = int(input('Ingrese la cantidad de litros vendidos: ')) **while** cantidad < 0: print('Debe ingresar un número positivo') cantidad = int(input('Ingrese la cantidad de litros vendidos: ')) tipo = int(input('Ingrese el tipo de combustible (1 a 3): ')) **while not** 1 <=) tipo <=) 3: print('Ingresó un número inválido') tipo = int(input('Ingrese el tipo de combustible (1 a 3): ')) **if** tipo ==) 1: total_nafta_super += cantidad **elif** tipo ==) 2: total_nafta_especial += cantidad **else** : total_gasoil += cantidad **if not** menor **or** cantidad < menor: menor = cantidad surtidor_menor = numero total = total_nafta_super + total_nafta_especial + total_gasoil promedio = total //) 10 print(f"Total de litros de nafta super: **{** total_nafta_super **}** ") print(f"Total de litros de nafta especial: **{** total_nafta_especial **}** ") print(f"Total de litros de gasoil: **{** total_gasoil **}** ") print(f"Surtidor que menos litros vendió: **{** surtidor_menor **}** ") print(f"Promedio de litros por surtidor: **{** promedio **}** ") 

**1. Programación estructurada** 

**18** 

###### **1.6.2 Procesamiento de temperaturas en una lista** 

Ingresar un conjunto de temperaturas en una lista, finalizar la carga cuando se reciba un 50. Sólo aceptar temperaturas entre -20 y 49 grados. Calcular y mostrar: 

- Cantidad de días con temperatura bajo cero 

- Promedio de temperaturas 

- Promedio de temperaturas de los días cálidos, es decir con temp. mayor a 20 

- Mostrar “Si” o “No” para indicar si hubo algún día con más de 40 grados. 

- La mayor temperatura de los días que no fueron cálidos 

- Cantidad de días con temperatura menor al promedio 

###### **validacion.py** 

**def** ingresar_numero_entre(mensaje, minimo, maximo): 

valor = float(input(mensaje)) **while not** minimo <=) valor <=) maximo: print(f"Debe ingresar un valor entre **{** minimo **}** y **{** maximo **}** ") valor = float(input(mensaje)) 

**return** valor 

**1.6. Ejercicios** 

**19** 

###### **procesolistas.py** 

**def** cantidad_menor(lista, techo): _""" Cuenta los elementos de una lista que sean menores a un tope :param lista: lista de valores :type lista: lista de datos que soporte comparación por menor :param techo: valor máximo para filtrar :type techo: el mismo de los elementos de la lista :returns: la cantidad de elementos cuyo valor sea menor al techo :rtype: entero """_ c = 0 **for** x **in** lista: **if** x < techo: c += 1 **return** c **def** promedio(lista): _""" Calcula el promedio simple de todos los elemento de una lista :param lista: lista :type lista: lista de números :returns: el promedio de todos los valores de la lista o 0 si la lista está vacía :rtype: flotante """_ cantidad = len(lista) **if** cantidad ==) 0: **return** 0 suma = 0 **for** x **in** lista: suma += x **return** suma / cantidad **def** existe(lista, buscado): _""" Busca un valor en una lista e informa si lo pudo encontrar :param lista: una lista de cualquier tipo :param buscado: el valor que se busca :tipo buscado: el mismo tipo que el de los datos almacenados en la lista :returns: verdadero si el elemento buscado existe en la lista y falso en caso_ �→ _contrario :rtype: boolean """_ **for** x **in** lista: **if** x ==) buscado: **return True return False** 

**1. Programación estructurada** 

**20** 

###### **temperaturas.py** 

**from validacion import** * **from proceso_listas import** * **def** cargar_temperaturas(): temperaturas = [] print("Ingrese las temperaturas entre -20 y 49. Finaliza con 50.") t = ingresar_numero_entre("Ingrese una temperatura: ", -20, 50) **while** t !=) 50: temperaturas.append(t) t = ingresar_numero_entre("Ingrese una temperatura: ", -20, 50) **return** temperaturas **def** promedio_mayores(temperaturas, piso): cantidad = 0 suma = 0 **for** x **in** temperaturas: **if** x > piso: suma += x cantidad += 1 **if** cantidad ==) 0: promedio = 0 **else** : promedio = suma / cantidad _#promedio = suma / cantidad if cantidad !=) 0 else 0_ **return** promedio **def** existe_mayor(temperaturas, piso): **for** x **in** temperaturas: **if** x > piso: **return True return False def** mayor_dias_calidos(temperaturas): mayor = **None for** x **in** temperaturas: **if** x <=) 20: **if** mayor **is None or** x > mayor: mayor = x **return** mayor **def** calcular(temperaturas): dias_bajo_cero = cantidad_menor(temperaturas, 0) 

**1.6. Ejercicios** 

**21** 

promedio_todos = promedio(temperaturas) promedio_dias_calidos = promedio_mayores(temperaturas, 20) hubo_40_grados = existe_mayor(temperaturas, 40) mayor = mayor_dias_calidos(temperaturas) dias_menor_al_promedio = cantidad_menor(temperaturas, promedio_todos) print(f"Hubo **{** dias_bajo_cero **}** días con temperatura bajo cero") print(f"El promedio de temperaturas fue de **{** promedio_todos **}** ") **if** (promedio_dias_calidos !=) 0): print(f"Y de los días cálidos fue de **{** promedio_dias_calidos **}** ") print("¿Hubo días con más de 40 grados?", "Si" **if** hubo_40_grados **else** "No") **if** mayor: print(f"La mayor temperatura de los días que no fueron cálidos fue de **{** mayor **}** ") **else** : print("Todos los días fueron cálidos") print(f"Hubo **{** dias_menor_al_promedio **}** días con temperatura menor al promedio") **def** principal(): temperaturas = cargar_temperaturas() calcular(temperaturas) **if** __name__ ==) "__main__": principal() 

### **Secuencias** 

##### **2.1 Introducción** 

Los tipos de datos de secuencias ofrecen la posibilidad de almacenar un conjunto de datos con un único identificador, para poder acceder a los mismos posteriormente en tanto forma individual como grupal. Asimismo, la instrucción for permite recorrer cualquier tipo de secuencia, entregando en cada iteración cada uno de los valores almacenados en la misma. 

###### **2.1.1 Tamaño** 

Se puede obtener el tamaño de una secuencia con la función len, pasando la misma como parámetro. La función retorna un valor entero indicando la cantidad de elementos almacenados en la secuencia. 

###### **2.1.2 Operador de acceso indexado** 

Las secuencias disponen del operador de acceso indexado, que se indica como un par de corchetes a continuación del identificador. El mismo permite obtener el valor almacenado en una posición específica de la secuencia, identificando cada una de ellas mediante un número natural que inicia en 0. De esta manera, el primer elemento posee el índice 0, el segundo el 1, etc. 

También pueden utilizarse índices negativos para acceder a los elementos desde el último, indicando como -1 al último, -2 al penúltimo y así sucesivamente. 

23 

**2. Secuencias** 

**24** 

El índice suele redactarse con una constante o variable entera, pero también pueden usarse expresiones. 

titulo = "Paisaje" print(titulo[2]) _# imprime "i"_ print(titulo[-2]) _# imprime "j"_ print(titulo[len(titulo)//)2]) _# imprime "s"_ 

###### **2.1.3 Operador de rebanadas** 

El operador de rebanadas o _slicing_ también se representa mediante corchetes ([]), pero incluye un rango de índices separados por dos puntos (:). Permite extraer un subconjunto de elementos contiguos de una secuencia. Su retorno siempre será una nueva secuencia que copia los elementos de la original sin modificarla. 

El mismo permite indicar un índice inicial y otro final del la sección a rebanar. Si no se indica el inicial, se asume 0; mientras que si no se indica el final, se asume el último. El corte de la secuencia siempre incluye al valor del índice inicial pero no incluye al índice final. 

Por ejemplo: 

titulo = "Paisaje" print(titulo[1:3]) _# imprime "ai"_ print(titulo[:3]) _# imprime "Pai"_ print(titulo[3:]) _# imprime "saje"_ 

Una variante del operador de rebanadas permite indicar un salto al seleccionar los elementos a cortar. Para ello se puede incluir un segundo símbolo de dos puntos y a continuación un número entero estableciendo que se corten los elementos desde el índice inicial y se salteen los siguientes. Así, con un salto de 2, se extraen las posiciones alternadas, mientras que con un salto de -1 se recorre la secuencia hacia atrás. De esta manera, utilizando una rebanada sin indicar inicio ni final y con salto -1, se obtiene una nueva secuencia inviertiendo la primera. 

titulo = "Paisaje" print(titulo[::)2]) _# imprime "Piae"_ print(titulo[5:0:-1]) _# imprime "jasia"_ 

**2.2. Cadenas** 

**25** 

print(titulo[::)-1]) _# imprime "ejasiaP"_ print(titulo[::)-2]) _# imprime "eaiP"_ 

##### **2.2 Cadenas** 

La secuencia más simple es la secuencia de caracteres, tambien denominada cadena de caracteres o simplemente cadena. Las mismas almacenan un conjunto de caracteres como un texto, los cuales pueden ser manipulados en su conjunto o en forma individual. 

Para indicar un valor constante se las delimita con comillas simples (') o dobles ("), pero utilizando el mismo símbolo tanto en la apertura como en el cierre. 

Las variables de tipo cadena pueden ser asignadas y consultadas como variables para operar con el texto como una unidad, pero tambien puede accederse a cada caracter que conforma la secuencia mediante los operadores de acceso indexado y de rebanadas. El operador de suma (+) une dos cadenas y el operador de multiplicacion repite una cadena una cantidad de veces indicada en el segundo operando. 

A continuación se presentan algunas de las operaciones más habituales: 

mensaje1 = "Hola" mensaje2 = "mundo!" _# Concatenación_ mensaje_concatenado = mensaje1 + " " + mensaje2 print(mensaje_concatenado) _# Resultado: 'Hola mundo!' # Multiplicacion_ print("A" * 10) _# Resultado: AAAAAAAAAA # Obtener una subcadena utilizando rebanada_ subcadena = mensaje1[1:3] print(subcadena) _# Resultado: 'ol' # Convertir a mayúsculas_ mayusculas = mensaje1.upper() print(mayusculas) _# Resultado: 'HOLA' # Convertir a minúsculas_ minusculas = mensaje2.lower() print(minusculas) _# Resultado: 'mundo!'_ 

**2. Secuencias** 

**26** 

###### **2.2.1 Otras operaciones** 

|Nombre|Uso|
|---|---|
|startswith|Indica si la cadena comienza con una subcadena pasada por parámetro|
|endswith<br>i|Indica si la cadena termina en una subcadena pasada por parámetro|
|find|Busca una subcadena e informa la posición en que se encuentra|
|join|Concatena todos los elementos de una secuencia con un delimitador|
|replace|Reemplaza todas las apariciones de una subcadena por otra<br>i|
|strip|Elimina todos los espacios que se encuentren al inicio y al final|
|split|Divide la cadena con un delimitador y devuelve una lista con los valores extraidos|



###### **2.2.2 Cadenas con formato** 

Cuando se requiere concatenar valores constantes con valores de variables, la operación de concatenación es impráctica porque no permite especificar fácilmente el formato de cada variable. Frecuentemente se requiere incluir dentro de una cadena larga el valor de una o más variables pero indicando características para la presentación de tales variables como ancho o alineación. 

Para ello se dispone de las cadenas formateadas o _f-strings_ , las cuales permiten agregar dentro de la cadena de _placeholders_ o zonas de reemplazo, indicadas con un par de llaves {}, dentro de cada uno de los cuales se ubica el valor de una variable u operación. Para indicar que una cadena incluye placeholders debe indicarse con una letra f antes de la comilla de apertura. 

Por ejemplo, para incorporar el valor de las variables nombre y apellido dentro de una cadena que contenga un saludo, en lugar de realizar una concatenación se las puede ubicar dentro de la cadena en un placeholder para cada una: 

saludo = "Hola " + apellido + ", " + nombre + "! ¿cómo estás?" saludo = f"Hola **{** apellido **}** , **{** nombre **}** ! ¿cómo estás?" 

A cada valor incrustado se le puede indicar un tamaño mínimo, de forma tal que si el valor no lo cumple se complete con espacios hasta alcanzar el tamaño indicado. Asimismo, se puede especificar una dirección de alineación para que los espacios sean agregados en uno o ambos extremos del valor y que el mismo quede alineado a la izquierda, a la derecha o centrado. 

De esta manera, en cada placeholder se puede especificar: 

**2.3. Tuplas** 

**27** 

f" **{** expresion **:** direccion ancho **}** " 

La dirección se especifica con los siguientes símbolos 

Símbolo Dirección 

> Alineado a la derecha, agrega espacios antes del valor < Alineado a la izquierda, agrega espacios después del valor ^ Centrado, agrega espacios antes y después del valor 

En el caso de las expresiones de tipo cadena de caracteres, la alineación por defecto es a la izquierda, mientras que para los valores numéricos la alineación por defecto es a la derecha. 

Por ejemplo: 

print(f"Hola **{** apellido **:** >20 **}** , **{** nombre **}** , como estás?") 'Hola Perez, Juan, como estás?' print(f"Hola **{** apellido **:** <20 **}** , **{** nombre **}** , como estás?") 'Hola Perez , Juan, como estás?' print(f"Hola **{** apellido **:** ^20 **}** , **{** nombre **}** , como estás?") 'Hola Perez , Juan, como estás?' 

La especificación del ancho requiere un número entero, excepto en el caso de la presentación de valores de tipo float. Para esta situación el ancho se indica con un número entero indicando el ancho total, incluyendo la parte entera, el punto de decimal y la parte decimal, seguidos por un punto y la cantidad de dígitos que deben presentarse a la derecha del punto decimal y una letra f. De esta manera, para mostrar una variable con dos decimales se debe especificar {variable:8.2f}, y la misma se presenta con 8 caracteres en total, los cuales se reparten con cinco para la parte entera, el punto decimal y dos para los decimales. 

##### **2.3 Tuplas** 

La tupla es un tipo de dato que se utiliza para almacenar una secuencia ordenada e inmutable de elementos. A diferencia de las listas, que se definen utilizando corchetes ([]), las tuplas se definen utilizando paréntesis (()) o simplemente separando los elementos por comas. Por ejemplo: 

**2. Secuencias** 

**28** 

tupla1 = (1, 2, 3) tupla2 = "a", "b", "c" 

En estos ejemplos, tanto tupla1 como tupla2 son variables que contienen tuplas. 

Las tuplas son similares a las listas en el sentido de que pueden contener múltiples elementos, pero tienen la particularidad de ser inmutables, lo que significa que no se pueden modificar una vez creadas. Esto implica que no se pueden agregar, eliminar o cambiar elementos individualmente en una tupla. Se pueden acceder a los elementos individuales de una tupla utilizando el operador de acceso indexado. Por ejemplo: 

tupla3 = (10, 20, 30) primer_elemento = tupla3[0] _# Acceso al primer elemento de la tupla_ print(primer_elemento) _# Resultado: 10_ 

En este ejemplo, se utiliza el operador de acceso indexado para acceder al primer elemento de la tupla “tupla3” y se almacena en la variable “primer_elemento”. 

Las tuplas son útiles cuando se requiere almacenar una colección de elementos que no deben cambiar, como coordenadas de un punto, información fija o estructuras de datos que no deben modificarse accidentalmente. 

Cuando una función retorna una serie de valores separados por comas, en realidad está devolviendo una tupla. Desde la llamada a la misma se puede asignar dicho retorno en una variable que tomará el tipo de datos tupla, o en una serie de variables separadas por comas, de forma tal que cada una de ellas será asignada con cada uno de los valores integrantes de la tupla. Esto se logra mediante una característica del lenguaje denominada desestructuración. 

###### **2.3.1 Desestructuración** 

La desestructuración es una herramienta que ofrece el lenguaje para poder asignar más de una variable a la izquierda del operador de asignación, de forma tal que cada una de tales variables sea asignada con cada uno de los valores de una secuencia que se presente a la derecha del operador. 

De esta manera, son válidas las siguientes asignaciones: 

**2.4. Listas** 

**29** 

x, y = 23, 44 _# x = 23 # y = 44_ precios = [58,22,99] pre1, pre2, pre3 = precios _# pre1 = 58 # pre2 = 22 # pre3 = 99_ letra1, letra2, letra3 = "DAO" _# letra1 = D # letra2 = A # letra3 = O_ 

Este mecanismo permite que si una función retorna más de un valor los mismos puedan ser asignados en variables individuales al retornar la misma. También permite realizar operaciones que de otra forma requeririan varias operaciones de asignación o incluso variables auxiliares. Es notable el caso del intercambio de dos variables, que puede resolverse de una manera muy simple mediante a, b = b, a. 

La cantidad de variables asignadas mediante desestructuración debe coincidir con el tamaño de la secuencia. En el caso de que la secuencia asignada tenga una cantidad grande o variable de elementos la desestructuración puede realizarse dejando que alguna de las variables sea indicada con un *. De esta manera, en las otras variables se asignan valores individualmente mientras que en la indicada con el asterisco se guarda una nueva secuencia con los valores restantes: 

persona = "Juan", "Perez", 34, "San Martin 2423", "5000" nombre, apellido, *otros_datos = persona _# nombre = "Juan" # apellido = "Perez" # otros\_datos = 34, "San Martin 2423", "5000"_ 

##### **2.4 Listas** 

Una lista es un tipo de dato que se utiliza para almacenar una colección ordenada y mutable de elementos. Se definen utilizando corchetes ([]), y los elementos de la lista se separan por comas. Por ejemplo: 

lista1 = [1, 2, 3] lista2 = ['a', 'b', 'c'] lista3 = [0] * 20 

**2. Secuencias** 

**30** 

En estos ejemplos, tanto lista1 como lista2 son variables que contienen listas. Se deben utilizar corchetes y separar los elementos por comas para definir una lista. Incluso se puede declarar una lista vacía con los corchetes y sin indicar ningún valor entre ellos. La listad denominada lista3 esta generada con el operador de producto, el mismo genera una lista de 20 elementos, todos con valor 0. 

Las listas son similares a las tuplas, pero tienen la ventaja de ser mutables, lo que significa que se pueden modificar una vez creadas. Esto implica que se puede agregar, eliminar o cambiar elementos individualmente en una lista. Asimismo se puedes acceder a los elementos individuales de una lista utilizando el operador de acceso indexado. 

Además de acceder a elementos individuales, las listas en Python admiten una variedad de operaciones y métodos que te permiten modificar, agregar, eliminar y manipular los elementos de la lista. Algunas operaciones comunes incluyen: 

lista = [1, 2, 3] _#Agregar elementos a una lista con el método append():_ lista.append(4) print(lista) _# Resultado: [1, 2, 3, 4] #Eliminar elementos de una lista con el método remove():_ lista.remove(2) print(lista) _# Resultado: [1, 2, 4] # Obtener la longitud de una lista con la función len():_ longitud = len(lista) print(longitud) _# Resultado: 3 # Revertir una lista con el método reverse():_ lista.reverse() print(lista) _# Resultado: [4, 2, 1] # Ordenar una lista con el método sort():_ lista.sort() print(lista) _# Resultado: [1, 2, 4]_ 

##### **2.5 Generación de listas por comprensión** 

La generación por comprensión, también conocida como comprensión de listas (list comprehension en inglés), es una construcción sintáctica que permite crear listas de manera concisa y eficiente basándose en una expresión y un conjunto de iteraciones o condiciones. 

La sintaxis básica de una comprensión de lista es la siguiente: 

**2.5. Generación de listas por comprensión** 

**31** 

nueva_lista = [expresión **for** elemento **in** secuencia] 

Donde expresión representa la expresión o cálculo que se realizará en cada elemento de la secuencia, elemento es la variable de iteración que toma el valor de cada elemento en la secuencia, y secuencia es la fuente de valores sobre la cual se iterará. 

Por ejemplo, dada una lista de números la necesidad de crear una nueva lista que contenga el cuadrado de cada número. Se puede usar una comprensión de lista de la siguiente manera: 

numeros = [1, 2, 3, 4, 5] cuadrados = [numero **) 2 **for** numero **in** numeros] print(cuadrados) _# [1, 4, 9, 16, 25]_ 

En este ejemplo, la comprensión de lista [numero **) 2 **for** numero **in** numeros] itera sobre cada elemento numero en la lista numeros y calcula el cuadrado de cada número utilizando la expresión numero **) 2. Los resultados se agregan automáticamente a una nueva lista llamada cuadrados. 

Además de las iteraciones simples, también es posible incluir condiciones en una comprensión de lista. Por ejemplo, si se desea obtener solo los números pares de una lista, se puede agregar una condición utilizando la cláusula if: 

numeros = [1, 2, 3, 4, 5] pares = [numero **for** numero **in** numeros **if** numero % 2 ==) 0] print(pares) _# [2, 4]_ 

En este caso, la comprensión de lista filtra los números de la lista pero solo incluye aquellos que cumplen la condición, es decir, los números pares. 

**2. Secuencias** 

**32** 

##### **2.6 Ejercicios** 

###### **2.6.1 Simulador de ruleta** 

Se necesita desarrollar un programa que simule el juego de la ruleta. Para ello se deben generar al azar 1000 tiradas y luego informar: 

- Cantidad de pares e impares 

- Cantidad de tiradas por cada docena 

- Porcentaje de ceros sobre el total de jugadas. 

- Cantidad de rojos y de negros 

**Solución** La simulación está programada en la función simulacion. Dado que los resultados son numerosos, la función no los retorna sino que los imprime directamente al terminar los cálculos. 

Para el conteo de tiradas clasificado por color, el problema principal es el de conocer el color de cada número en una ruleta real. El algoritmo de determinación del color es el siguiente: 

- Los números 10 y 28 son negros. 

- Los otros números son negros si la suma de sus dígitos es par. 

- La suma de los digitos no es la suma simple, si al sumar los dígitos del número el resultado es mayor a 9, deben volver a sumarse los digitos de dicho resultado hasta reducir a un único dígito. 

Para ello el programa inicia generando una lista con los colores de los números, almacenando en la misma una tupla en la que el primer elemento es un número y el segundo el color asociado al mismo. En dicha lista las tuplas se almacenan de forma que cada número está almacenado en la lista en su mismo índice, por ejemplo, el número 10 esta almacenado como (10,“N”) en la posición 10. La lista es creada en la función generar_ruleta. 

Para el cálculo del color la función get_color recibe un número y devuelve el color correspondiente al parámetro. 

Finalmente la función reducir_numero recibe un número entero y calcula la suma de sus dígitos. La función se llama recursivamente cuando la suma obtenida es mayor a 9 y por lo tanto es un número de más de un dígito. 

**2.6. Ejercicios** 

**33** 

###### **ruleta.py** 

_""" Simulador de Ruleta Desarrollar un programa que simule el juego de la ruleta. Para ello generar al azar 1000 tiradas y luego informar:_ 

- _Cantidad de pares e impares_ 

- _* Cantidad de tiradas por cada docena * Porcentaje de ceros sobre el total de jugadas. * Cantidad de rojos y de negros """_ 

**import random from rich import** print **from rich.console import** Console **from rich.panel import** Panel **from rich.table import** Table _""" Reglas: Comienza en 1,R (1-ROJO) Los números negros N son aquellos cuya reducción es PAR, o sea, la suma de sus dígitos_ �→ _es divisible por 2 """_ console = Console() **def** reducir_numero(numero: int) -> int: _"""La función toma un número entero y devuelve un entero que es igual a la suma de_ �→ _todos sus dígitos. Si la suma tiene dos dígitos repite el proceso hasta que tenga un solo dígito. :param numero: Número que se desea reducir :type numero: int :return: Valor de UN dígito, obtenido a partir de la suma de los dígitos del número_ �→ _original. :rtype: int """ # Caso base: Si el número tiene un solo dígito, devolverlo tal cual_ **if** numero < 10: **return** numero _# Convertir el número en una lista de dígitos_ digitos = [int(digito) **for** digito **in** str(numero)] _# Calcular la suma de los dígitos_ suma_digitos = sum(digitos) _# Llamar recursivamente a la función con la suma de los dígitos_ **return** reducir_numero(suma_digitos) **def** get_color (nro: int) -> str: _"""Dado un número de la ruleta, determinar el color de dicho número en el paño :param nro: Número del cual se desea averiguar el color :type nro: int :return: Color del número indicado. Valores válidos: V (verde), R (rojo), N (negro) :rtype: str """_ **if** nro ==) 0: 

**2. Secuencias** 

**34** 

**return** 'V' **elif** nro ==) 10 **or** nro ==) 28: **return** 'N' **else** : _# Los numeros negros son los pares # Aquellos cuya reducción es par # El 10 y el 28_ **if** reducir_numero(nro)%2 ==) 0: **return** 'N' **else** : **return** 'R' **def** generar_ruleta(): _"""Genera un tablero de ruleta, como una lista de tuplas conteniendo (numero,color) """_ ruleta = [] **for** nro **in** range (0,37): ruleta.append((nro,get_color(nro))) **return** ruleta **def** imprimir_ruleta(rul: list[(int,str)]): _"""Imprime por consola un paño de ruleta, obtenido por medio de una lista de tuplas :param rul: lista que representa el paño de la ruleta :type rul: lista de tuplas (numero, color) """_ col = 1 **for** nro,color **in** rul: **if** color ==) 'V': console.print (f"[bold white on green] **{** nro **:** ^12 **}** [/]", end="") print() **elif** color ==) 'R': console.print (f"[bold white on red] **{** nro **:** ^4 **}** [/]", end="") col += 1 **else** : console.print (f"[bold white on black] **{** nro **:** ^4 **}** [/]", end="") col += 1 **if** col ==) 4: print() col = 1 **def** imprimir_tirada (nro : int, color : str): **if** color ==) 'V': console.print (f"Obtuvimos [bold white on green] **{** nro **}{** color **}** [/]") **elif** color ==) 'R': console.print (f"Obtuvimos [bold white on red] **{** nro **}{** color **}** [/]") **else** : console.print (f"Obtuvimos [bold white on black] **{** nro **}{** color **}** [/]") **def** simulacion(ruleta: list[(int,str)]): _"""Realiza una simulación y obtiene indicadores sobre la misma :param ruleta: Ruleta generada, para determinar los colores de los numeros :type ruleta: lista de tuplas (numero,color) """_ cantidad_pares = cantidad_impares = 0 cantidad_rojos = cantidad_negros = 0 tiradas_primera_docena = tiradas_segunda_docena = tiradas_tercera_docena = 0 cantidad_ceros = 0 jugadas = 1000 

**2.6. Ejercicios** 

**35** 

_# Generar 1000 numeros enteros aleatorios en el rango de la ruleta (0-36)_ **for** i **in** range(jugadas): tirada_nro = random.randint(0,36) tirada_color = ruleta[tirada_nro][1] _#imprimir_tirada(tirada_nro,tirada_color)_ **if** tirada_nro%2 ==) 0: cantidad_pares += 1 **else** : cantidad_impares += 1 **if** tirada_color ==) 'R': cantidad_rojos += 1 **elif** tirada_color ==) 'N': cantidad_negros += 1 **else** : cantidad_ceros += 1 docena = tirada_nro //) 12 **if** docena ==) 1: tiradas_primera_docena += 1 **elif** docena ==) 2: tiradas_segunda_docena += 1 **else** : tiradas_tercera_docena += 1 porcentaje_ceros = cantidad_ceros*100/jugadas console.print() table = Table(title="Resultados de la simulación") table.add_column("Resultado") table.add_column("Valor",justify="center") table.add_row("Cantidad de pares",str(cantidad_pares)) table.add_row("Cantidad de impares",str(cantidad_impares)) table.add_row("Cantidad de tiradas 1º docena",str(tiradas_primera_docena)) table.add_row("Cantidad de tiradas 2º docena",str(tiradas_segunda_docena)) table.add_row("Cantidad de tiradas 3º docena",str(tiradas_tercera_docena)) table.add_row("Porcentaje de ceros",str(porcentaje_ceros)+"%") table.add_row("Cantidad de rojos","[bold white on red]"+str(cantidad_rojos)) table.add_row("Cantidad de negros","[bold white on black]"+str(cantidad_negros)) console.print(table) **def** principal(): ruleta = generar_ruleta() imprimir_ruleta(ruleta) simulacion(ruleta) **if** __name__ ==) "__main__": principal() 

### **Programación funcional** 

##### **6.1 Introducción** 

Al desarrollar software se identifican paradigmas de programación que gobiernan el enfoque con el que se encara el problema, se diseña una solución y finalmente se redacta el código fuente. Entre los paradigmas más utilizados se destacan el paradigma estructurado y el paradigma orientado a objetos. 

Otro paradigma de uso habitual es el paradigma funcional. El mismo tiene una base matemática bastante compleja y por tal motivo existen pocos lenguajes denominados puros, es decir, que permiten únicamente desarrollar con este paradigma. Sin embargo, actualmente todos los lenguajes de uso cotidiano (tales como Java, C#, Python o Javascript) incluyen ciertos elementos de esta metodología. 

A pesar de que estos lenguajes están mayormente concentrados en los paradigmas estructurado y orientado a objetos, ofrecen algunas características de programación funcional. Esto se logra mediante la posibilidad de trabajar con un nuevo tipo de dato denominado “función”. 

El origen de esta perspectiva puede parecer desconcertante, pero se la puede analizar desde el punto de vista de las variables. Cuando se utiliza la programación estructurada, los programas poseen variables donde se almacenan valores. En esta modalidad, cada variable tiene la capacidad de almacenar un único valor de alguno de los tipos de datos ofrecidos por el lenguaje, tales como números, cadenas, booleanos, etc. En cambio, en la programación orientada a objetos, las variables pueden contener objetos, los cuales pueden 

71 

**6. Programación funcional** 

**72** 

tener múltiples atributos y métodos. Aunque es válido argumentar que las variables solo contienen referencias a objetos, en esencia, sigue siendo cierto que cada variable almacena un objeto. 

En la programación funcional, las variables almacenan código fuente, es decir, conjuntos de instrucciones del lenguaje. Por lo tanto, si una variable se declara como una función, es posible ejecutar el código que esta contiene. Y dado que son variables pueden cambiar su contenido, por lo tanto, si en algún momento se asigna un código diferente a la variable y se ejecuta su contenido nuevamente, se llevará a cabo una ejecución distinta. En conclusión, siempre se ejecutará el conjunto de instrucciones que esté almacenado en la variable en ese momento específico. 

##### **6.2 Funciones de orden superior** 

Los lenguajes que ofrecen programación funcional, incluso en su forma más básica, brindan la posibilidad de tener variables cuyo contenido sea una función. También se pueden tener parámetros de tipo función, lo cual implica que un método puede ejecutar una función sin necesidad de saber con exactitud su comportamiento. 

De la misma manera, una función o un método de una clase puede retornar una función para que sea almacenada desde la llamada al mismo. 

Los métodos que poseen parámetros o retorno de tipo función se denominan métodos o funciones de orden superior. Esta noción tiene una gran relevancia matemática y es muy útil en diversas situaciones de programación. 

##### **6.3 Variables de tipo función** 

Una variable puede almacenar una referencia a una función. En el siguiente ejemplo se declara una variable llamada imprimir y se asigna su valor con el nombre de la función print. Debe notarse que no se utilizan los paréntesis que efectivamente iniciarían una llamada a la función print. Luego de la asignación, la variable puede ser ejecutada y el resultado es que se ejecuta un print. 

imprimir = print imprimir("Hola, mundo!") 

**6.4. Colecciones de funciones** 

**73** 

##### **6.4 Colecciones de funciones** 

De la misma manera que una variable puede almacenar una referencia a una función, se pueden crear colecciones cuyos elementos sean funciones. 

En el siguiente ejemplo se crea una calculadora básica con las cuatro operaciones elementales de la aritmética implementadas con una función por cada una. Para que el usuario pueda seleccionar la operación deseada se ofrece un menú con un número natural por cada opción. Al momento de ejecutar la función correspondiente se accede a una lista que contiene en cada posición una referencia a la función correspondiente en el menú. Esto permite acceder a la lista usando como índice la opción seleccionada, y dado que el valor retornado es efectivamente una función se la puede ejecutar pasándole los parámetros que la misma requiera. Para ello la lista operaciones es inicializada con un valor **None** ya que no hay ningúna operación con número 0 en el menú, y luego cada una de las referencias a las funciones de las operaciones aritméticas. 

**def** suma(a, b): **return** a + b **def** resta(a, b): **return** a - b **def** multiplicacion(a, b): **return** a * b **def** division(a, b): **return** a / b **def** ejecutar_calculadora(): operaciones = [ **None** , suma, resta, multiplicacion, division] print("Calculadora básica") print("Seleccione una operación:") print("1. Suma") print("2. Resta") print("3. Multiplicación") print("4. División") print("0. Salir") opcion = int(input()) **while** opcion !=) 0: **if** opcion >=) 1 **and** opcion <=) 4: a = float(input("Ingrese el primer número: ")) b = float(input("Ingrese el segundo número: ")) resultado = operaciones[opcion](a, b) print("El resultado es:", resultado) **else** : 

**6. Programación funcional** 

**74** 

print("Opción inválida. Intente nuevamente.") print() print("Seleccione una operación:") opcion = int(input()) ejecutar_calculadora() 

##### **6.5 Funciones lambda** 

Las funciones lambda, también conocidas como funciones anónimas, son funciones pequeñas y concisas que se definen sin un nombre y se utilizan en el momento en que se necesitan. A diferencia de las funciones normales, que se definen utilizando la palabra clave **def** , las funciones lambda se crean utilizando la palabra clave **lambda** . 

La sintaxis básica de una función lambda es la siguiente: 

**lambda** argumentos: expresión 

Donde lambda es la palabra clave que indica que se está creando una función lambda, la lista de argumentos son los parámetros de la función, separados por comas pero sin los paréntesis que exige el bloque def y la expresión es la que se evalúa y devuelve como resultado de la función. 

Una función lambda está limitada a una sola expresión y no puede contener múltiples líneas de código. En el caso de necesitar realizar múltiples operaciones, ejecutar varias líneas de código o usar estructuras de control, debe desarrolarse una función regular con def. 

En el ejemplo anterior de la calculadora se pueden evitar todas las definiciones de las funciones suma, resta, multiplicacion y división de la siguiente manera: 

suma = **lambda** a, b: a + b resta = **lambda** a, b: a - b multiplicacion = **lambda** a, b: a * b division = **lambda** a, b: a / b operaciones = [ **None** , suma, resta, multiplicacion, division] 

**6.6. Secuencias y operaciones funcionales** 

**75** 

##### **6.6 Secuencias y operaciones funcionales** 

Existen funciones de orden superior que simplifican la manipulación de los datos de las secuencias. 

###### **6.6.1 Filter** 

La función filter() recorre una secuencia y ejecuta por cada uno de los datos de la misma una función recibida como parámetro y que se espera que devuelva un valor de verdad, tanto valores booleanos como convertibles a boolean (truthy). Esta función retorna una nueva secuencia cuyos valores son los mismos de la secuencia original pero únicamente aquellos para los que la función retorna un valor verdadero. 

La sintaxis de filter es: 

filter(funcion, secuencia) 

Dado que filter retorna una nueva secuencia, la misma debe ser recorrida con una instrucción for o convertida a una colección, con las funciones list() o set(). 

Por ejemplo, la siguiente llamada a filter extrae los números pares de una lista: 

es_par = **lambda** x: x \% 2 ==) 0 numeros = [2,1,35,8,5,21,4,6,9,6,3,2] pares = list(filter(es_par, numeros)) print(pares) _#{)[2, 8, 4, 6, 6, 2]_ 

###### **6.6.2 Map** 

La función map() permite generar una nueva secuencia de forma tal que cada elemento se obtenga con el resultado de ejecutar una función a cada elemento de la secuencia original. La sintaxis es idéntica a la de la función filter, de forma tal que el primer parámetro debe ser la función a repetir y el segundo contiene la secuencia que debe procesarse. 

En el siguiente ejemplo se obtienen una lista con los cuadrados de los numeros de la lista original: 

**6. Programación funcional** 

**76** 

numeros = [2,1,35,8,5,21,4,6,9,6,3,2] cuadrados = list(map( **lambda** x: x **) 2, numeros)) print(cuadrados) _#[)4, 1, 1225, 64, 25, 441, 16, 36, 81, 36, 9, 4]_ 

###### **6.6.3 Reduce** 

La función reduce() recorre una secuencia aplicando una función de pliegue o reducción, obteniendo como resultado un único valor. Para la operacion de reducción requiere una función de dos parámetros que realice alguna operación con los mismos y retorne un valor. Al ejecutarse toma los dos primeros elementos de la secuencia e invoca a la función recibida, la cual debe retornar un resultado. A continuación invoca nuevamente a dicha función enviándole como parámetros el tercer elemento de la secuencia y el resultado de la primera ejecución. Luego continúa invocando la función con cada uno de los restantes elemntos de la secuencia y el retorno de la ejecución anterior. 

Por ejemplo, si se dispone de una función suma, que reciba dos números y retorne la suma aritmética de esos parámetros, puede utilizarse reduce de la siguiente manera: 

numeros = [23,6,9] total = reduce(suma, numeros) print(total) _# 38_ 

Al ejecutarse reduce, inicia invocando a la función suma con los dos primeros valores de la lista (23 y 6), obteniendo como resultado el número 29. A continuación vuelve a llamar a suma pasandole como parámetros 29 (el resultado anterior) y 9 (el tercer elemento de la lista), obteniendo 38. Y dado que la lista no posee más elementos retorna ese valor como resultado final de la reducción. 

La función reduce fue movida al módulo functools por lo tanto para poder utilizarla debe ser importada con **from functools import** reduce. 

### **Archivos** 

En muchos casos, los programas requieren almacenar datos de forma persistente, de manera que estos datos se mantengan entre distintas ejecuciones del programa. 

Los archivos son el mecanismo más básico y ampliamente utilizado en cualquier lenguaje de programación para lograr esta persistencia de datos. 

Los archivos difieren significativamente de las bases de datos en el sentido de que son universales, lo que significa que cualquier programa que comprenda el formato de los datos almacenados en un archivo puede leerlos e incluso escribir sobre ellos, sin importar qué programa los haya generado previamente. 

Existen notables diferencias entre los archivos y las bases de datos. Las bases de datos ofrecen ventajas significativas en términos de velocidad y capacidad de manipulación de grandes cantidades de datos. Además, proporcionan características de seguridad, como mecanismos de autenticación y autorización, para gestionar datos sensibles. Otro aspecto destacado de las bases de datos es su capacidad para mantener la consistencia de los datos, evitando la presencia de información incoherente o inconsistente. 

A pesar de estas ventajas, la manipulación de datos a través de archivos ha sido ampliamente utilizada históricamente para transmitir información entre sistemas heterogéneos. Esta práctica es común cuando se requiere transferir datos de un programa a otro que no puede comunicarse directamente entre sí. Los archivos permiten que un programa almacene datos en un archivo y que otro programa, incluso escrito en un lenguaje o sistema diferente, pueda 

37 

**3. Archivos** 

**38** 

manipular esos datos. Este mecanismo ha sido tradicionalmente utilizado y sigue siendo utilizado en el campo de la ciencia de datos, donde se requiere la transferencia y manipulación conjunta de datos provenientes de diferentes fuentes. 

##### **3.1 Tipos de archivos** 

Cuando se requieren manipular datos almacenados en archivos, es fundamental considerar el formato o tipo de archivo. Existen dos tipos principales de archivos: archivos de texto y archivos binarios. 

Los archivos de texto contienen información representada como una secuencia de caracteres legibles, escritos en una determinada codificación (UTF8, ASCII, etc.). Estos archivos utilizan caracteres especiales, como el retorno de carro o la nueva línea, para delimitar cada línea y permitir la manipulación individual de cada dato. El formato de archivo de texto es adecuado para almacenar datos legibles por humanos, como texto plano, configuraciones o registros de datos en formato tabular. 

Por otro lado, los archivos binarios no dependen de los caracteres de retorno de carro para delimitar los datos. En cambio, requieren de algún mecanismo específico para indicar la forma en que los datos están organizados dentro del archivo.Los archivos binarios son archivos en los que la información se almacena en un formato no legible directamente por los humanos y pueden contener datos de diversos tipos, como números, imágenes, audio, video, entre otros, donde la representación en formato de texto no sería práctica o eficiente. A diferencia de los archivos de texto, los archivos binarios no están codificados como caracteres legibles, sino que utilizan una representación binaria de los datos. 

En resumen, los archivos de texto son adecuados para almacenar datos en formato de texto legible, mientras que los archivos binarios son utilizados para guardar datos más complejos y diversos, sin requerir la conversión a cadenas de texto. 

##### **3.2 Apertura y cierre** 

Para interactuar con un archivo en Python, es necesario informar al sistema operativo qué archivo se pretende utilizar, dónde está ubicado y qué operaciones se van realizar en él. Para lograr esto, se debe realizar la operación 

**3.3. Modos de apertura** 

**39** 

de apertura del archivo, indicando al sistema operativo que el programa está utilizando ese archivo y, potencialmente, evitando que otros programas accedan a él simultáneamente. Al finalizar el uso del archivo, es importante cerrarlo. 

El cierre de un archivo cumple dos propósitos básicos. En primer lugar, notifica al sistema operativo que ya no se está utilizando y, por lo tanto, otros programas pueden acceder a él. En segundo lugar, en el caso de operaciones de escritura de datos en el archivo, el cierre garantiza que las últimas escrituras se almacenen correctamente en el disco o en el medio de almacenamiento utilizado. Al realizar escrituras, es probable que la biblioteca de manipulación de archivos o el propio sistema operativo espere a acumular varias operaciones de escritura antes de almacenarlas en el dispositivo de almacenamiento. Si un archivo no se cierra correctamente, es posible que las últimas escrituras no se envíen al destino, por lo que es importante cerrar siempre los archivos. 

Python nos proporciona dos funciones para estas operaciones, llamadas precisamente open y close. La función open recibe dos parámetros. El primero es el nombre del archivo, una cadena que contiene el nombre y la extensión del archivo, y opcionalmente la ubicación utilizando rutas relativas o absolutas para especificar el directorio donde se encuentra el archivo. El segundo parámetro es el modo de apertura, donde se indica el tipo de archivo (texto o binario) y la operación que deseamos realizar en dicho archivo. 

La función open() devuelve un objeto archivo que nos permite operar con el archivo. Este objeto cuenta con un método llamado close(), que se utiliza para indicar que el archivo ha sido cerrado correctamente. 

En general, es recomendable mantener los archivos abiertos el menor tiempo posible. Por lo tanto, se debe abrir el archivo, realizar las operaciones necesarias y cerrarlo inmediatamente. No debe dejarse un archivo abierto más tiempo del necesario, especialmente durante el ingreso de datos por parte del usuario. 

##### **3.3 Modos de apertura** 

El modo de apertura que se especifica como parámetro en la función open es una cadena de texto que puede contener una o dos letras. Estas letras indican la operación que se desea realizar en el archivo. Para la operación de lectura, se utiliza la letra “R” (read), mientras que para la operación de escritura se utiliza la letra “W” (write). 

**3. Archivos** 

**40** 

El modo de apertura “W” tiene la particularidad de que, si el archivo en el que se desea escribir no existe, se crea automáticamente. Sin embargo, si el archivo ya existe, su contenido se borra por completo y se empieza a escribir desde cero, es decir, como un archivo vacío. 

Existe otro modo de apertura para escritura denominado “X”. Este modo permite escribir datos en un archivo, pero si el archivo ya existe, impide borrar su contenido original y arroja un error. En resumen, el modo “X” es utilizado para escribir en un archivo completamente nuevo sin sobrescribir uno existente. 

Otro modo de escritura es el modo “A” (append), que significa agregar. Cuando se abre un archivo en modo “A”, si el archivo no existe, se crea. Sin embargo, si el archivo ya existe, el contenido previo no se borra, sino que se comienza a escribir a continuación del último dato almacenado en el archivo. 

Por último, existe el modo “R+” que permite tanto la lectura como la escritura en un archivo. Al abrir un archivo en modo “R+”, todas las operaciones de lectura y escritura se realizan desde el principio del archivo, aunque con operaciones de desplazamiento se puede indicar una posición específica para continuar a partir de ella. 

Es importante mencionar que también se debe indicar el tipo de archivo con una letra “T” para archivos de texto y una letra “B” para archivos binarios. Si no se especifican estas letras, el modo de apertura predeterminado es de lectura de archivos de texto (“RT”). 

**3.4. Lectura de archivos de texto** 

**41** 

|**Modo**|**Descripción**|**Acción sobre el archivo**|
|---|---|---|
|r|Lectura|Abre el archivo para lectura<br>(modo texto)|
|w|Escritura|Abre el archivo para escritura<br>(modo texto)|
|x|Escritura exclusiva|Abre el archivo para escritura<br>exclusiva (modo texto)|
|a|Adjuntar|Abre el archivo para agregar<br>contenido al final (modo texto)|
|r+|Lectura y escritura|Abre el archivo para lectura y<br>escritura (modo texto)|
|rb|Lectura binaria|Abre el archivo para lectura<br>(modo binario)|
|wb|Escritura binaria|Abre el archivo para escritura<br>(modo binario)|
|xb|Escritura exclusiva binaria|Abre el archivo para escritura<br>exclusiva (modo binario)|
|ab|Adjuntar binario|Abre el archivo para agregar<br>contenido al final (modo bina-<br>rio)|
|r+b|Lectura y escritura binaria|Abre el archivo para lectura y<br>escritura (modo binario)|



##### **3.4 Lectura de archivos de texto** 

Para leer archivos de texto, hay tres métodos disponibles en la estructura devuelta por la función open. El primer método es read, que lee todo el contenido del archivo y devuelve una variable de tipo string. Este método es adecuado para archivos de texto relativamente pequeños, ya que carga todo el contenido en una sola variable. La principal desventaja es que, al leer todo el contenido, es responsabilidad del programador manipular el formato si el archivo tiene una estructura interna. Por ejemplo, si el archivo está separado por comas, será responsabilidad del programa dividir los datos según los delimitadores. Si el archivo contiene varias líneas de texto, read las lee todas y devuelve una cadena que incluye los caracteres de nueva línea o retorno de carro que indican el final de cada línea. 

El segundo método es readline, que lee una sola línea y deja el archivo en 

**3. Archivos** 

**42** 

un estado en el que la siguiente llamada leerá la línea que se encuentre a continación. De esta manera, readline devuelve una cadena con el contenido de una línea y permite la lectura en un ciclo para procesar líneas sucesivas. Este es el método más adecuado cuando se trata de archivos relativamente grandes, ya que al leer las líneas una a una, no se carga todo el contenido del archivo en la memoria, sino que se mantiene una única línea en memoria a la vez. 

Por último, el método readlines (en plural) recorre todo el archivo y lee cada una de las líneas, devolviendo una lista donde cada posición contiene una línea de texto. Si se lo utiliza en un archivo con, por ejemplo, 20 líneas, el mismo devolverá una lista con 20 elementos, cada uno representando una línea del archivo en el orden en que fueron leídas. Readlines se encarga de dividir el archivo según los caracteres de nueva línea, pero ocupa más memoria, ya que todo el contenido del archivo se almacena en la lista. Por lo tanto, no sería apropiado para leer archivos de texto demasiado grandes, en el orden de varios megabytes, ya que consumiría una cantidad considerable de memoria. 

Por lo tanto, para leer todo el contenido de un archivo de texto en una variable e imprimirla, se puede programar el siguiente bloque: 

archivo = open("datos.txt") contenido = archivo.read() print(contenido) archivo.close() 

Y para leer un archivo más largo linea a linea: 

archivo = open("datos.txt") linea = archivo.readline() **while** linea: print(linea) linea = archivo.readline() archivo.close() 

En este ejemplo, se abre el archivo “datos.txt” en modo lectura. Luego se utiliza un ciclo while para leer cada línea del archivo utilizando el método readline(). Dentro del ciclo, se imprime la línea y se lee la siguiente línea. El ciclo continúa hasta que se alcanza el final del archivo, es decir, cuando el método readline() devuelve una cadena vacía. Por último, se cierra el archivo 

**3.5. Escritura de archivos de texto** 

**43** 

utilizando el método close(). 

##### **3.5 Escritura de archivos de texto** 

Para la escritura de archivos de texto existen dos métodos principales. El primer método es write, que permite escribir una cadena en el archivo. Al utilizar este método, la cadena se escribe en el archivo sin incluir automáticamente caracteres de nueva línea. Si se necesita escribir varias líneas de texto, es responsabilidad del programador agregar los caracteres de nueva línea en los lugares adecuados dentro de la cadena. 

El segundo método es writelines, que recibe una lista de cadenas y escribe cada una de ellas en el archivo de texto en el orden en que aparecen en la lista. Al igual que el método write,writelines no agrega automáticamente caracteres de nueva línea, por lo que es responsabilidad del programador asegurarse de que las cadenas de la lista incluyan los caracteres de nueva línea donde sea necesario. 

Por ejemplo: 

nombres = ['Juan', 'María', 'Carlos', 'Laura'] archivo = open("nombres.txt", "w") **for** nombre **in** nombres: archivo.write(nombre + ' **\n** ') archivo.close() 

En este ejemplo, se crea una lista llamada nombres con algunos nombres. Luego se abre el archivo “nombres.txt” en modo escritura. A continuación, se utiliza un bucle for para recorrer cada elemento de la lista nombres. En cada iteración, se utiliza el método write() para escribir el nombre en el archivo, seguido de un carácter de nueva línea \\)n. Esto garantiza que cada nombre se escriba en una línea nueva del archivo. 

##### **3.6 Ejercicios** 

###### **3.6.1 Lectura de un archivo de números** 

Desarrollar un programa que lea todo el contenido del archivo numeros.txt que contiene múltiples líneas de texto, cada una de ellas con un número 

**3. Archivos** 

**44** 

entero. Al leer el archivo se debe almacenar todos los números en una lista. A continuación el programa debe manipular los números cargados en la lista para: 

- Calcular e imprimir el promedio de todos los números 

- Calcular e imprimir la cantidad de números mayores al promedio 

- Generar y mostrar una nueva lista que contenga todos los números pares 

###### **proceso_listas.py** 

**def** cantidad_menor(lista, techo): _""" Cuenta los elementos de una lista que sean menores a un tope :param lista: lista de valores :type lista: lista de datos que soporte comparación por menor :param techo: valor máximo para filtrar :type techo: el mismo de los elementos de la lista :returns: la cantidad de elementos cuyo valor sea menor al techo :rtype: entero """_ c = 0 **for** x **in** lista: **if** x < techo: c += 1 **return** c **def** cantidad_mayor(lista, piso): _""" Cuenta los elementos de una lista que sean menores a un tope :param lista: lista de valores :type lista: lista de datos que soporte comparación por menor :param techo: valor máximo para filtrar :type techo: el mismo de los elementos de la lista :returns: la cantidad de elementos cuyo valor sea menor al techo :rtype: entero """_ c = 0 **for** x **in** lista: **if** x > piso: c += 1 **return** c **def** promedio(lista): _""" Calcula el promedio simple de todos los elemento de una lista :param lista: lista :type lista: lista de números :returns: el promedio de todos los valores de la lista o 0 si la lista está vacía :rtype: flotante_ 

**3.6. Ejercicios** 

**45** 

_"""_ cantidad = len(lista) **if** cantidad ==) 0: **return** 0 suma = 0 **for** x **in** lista: suma += x **return** suma / cantidad **def** existe(lista, buscado): _""" Busca un valor en una lista e informa si lo pudo encontrar :param lista: una lista de cualquier tipo :param buscado: el valor que se busca :tipo buscado: el mismo tipo que el de los datos de la lista :returns: verdadero si el elemento buscado existe en la lista y falso en caso contrario :rtype: boolean """_ **for** x **in** lista: **if** x ==) buscado: **return True return False** 

**lectura_numeros.py from proceso_listas import** * **def** leer_archivo(nombre_archivo): numeros = [] archivo = open(nombre_archivo) **while True** : linea = archivo.readline() **if not** linea: **break** n = int(linea[:-1]) numeros.append(n) archivo.close() **return** numeros **if** __name__ ==) "__main__": lista = leer_archivo("numeros.txt") promedio_todos = promedio(lista) mayores = cantidad_mayor(lista, promedio_todos) pares = [x **for** x **in** lista **if** x % 2 ==) 0] print("Del archivo se leyeron los números") 

**3. Archivos** 

**46** 

print(f"El promedio de esos números es de **{** promedio_todos **:** 5.2f **}** ") print(f"Y **{** mayores **}** son mayores que el promedio") print("Listado de los pares:") **for** x **in** pares: print(x) 

**47 3.6. Ejercicios** 

**3. Archivos** 

**48** 

###### **3.6.2 Lectura de un csv con códigos postales** 

El archivo cp.csv contiene el listado de los códigos postales de tres provincias argentinas. En cada línea se encuentran, separados por un símbolo de punto y coma (;) los siguientes datos: 

- Provincia: representada por una letra mayúscula según el estándar ISO correspondiente. 

- Código: es un número entero de cuatro dígitos que identifica una localidad o varias localidades vecinas. Puede estar repetido. 

- Nombre: es el nombre de la localidad correspondiente a ese código. 

Se requiere leer todo el contenido del archivo y guardarlo en una lista que contenga un elemento por cada línea. En cada elemento debe almacenarse alguna estructura de datos que permita acceder individualmente a cada dato que conforma un codigo postal. 

Luego de la carga el programa debe permitir el ingreso de uno o más códigos numéricos y listar la provincia y nombre de todas las localidades asignadas a dichos códigos 

###### **cp.csv (primeras líneas)** 

K;4743;ACONQUIJA K;4701;ACOSTILLA K;4234;ACHALCO K;5263;ADOLFO E. CARRANZA K;4139;AGUA AMARILLA (LA HOYADA, DPTO. SANTA MARIA) 

**3.6. Ejercicios** 

**49** 

###### **lectura_cp.py** 

**def** leer_codigos(nombre_archivo): codigos = [] archivo = open(nombre_archivo) **for** linea **in** archivo.readlines(): codigo = tuple(linea[:-1].split(";")) codigos.append(codigo) archivo.close() **return** codigos **def** buscar_codigo(lista, buscado): encontrados = [] **for** c **in** lista: **if** c[1] ==) buscado: encontrados.append(c) **return** encontrados _# Con comprensión de listas # return [c for c in lista if c[1] ==) buscado]_ **if** __name__ ==) "__main__": codigos = leer_codigos("cp.csv") buscado = input("Ingrese un código a buscar (fin con cadena vacía):") **while** buscado: encontrados = buscar_codigo(codigos, buscado) **if** encontrados: **for** c **in** encontrados: print(f" **{** c[0] **}** : **{** c[2] **}** ") **else** : print("No se encontró ninguna localidad") buscado = input("Ingrese un código a buscar (fin con cadena vacía):") 

**3. Archivos** 

**50** 

###### **3.6.3 Análisis del archivo de propinas** 

El archivo tips.csv contiene los datos de las propinas recibidas por los empleados de una pizzería en New York. 

El archivo contiene los siguientes campos separados por comas 

- total_bill: Importe total del servicio 

- tip: Importe de la propina 

- sex: Sexo del cliente 

- smoker: El cliente es fumador (Yes, No) 

- day: Día (Juev, Vie, Sab, Dom) 

- time: Horario (Almuerzo, Cena) 

- size: Tamaño de la mesa (comensales) 

Se requiere desarrollar un programa que desde los datos del archivo informe: 

- ¿Quién paga más propinas?¿Hombres o mujeres? 

- ¿Cuáles son los días más ‘lentos’, con menos propinas? 

- ¿Cuál es el promedio de las propinas? 

- ¿Cuándo se vendió la orden más grande (qué día y en qué turno)? 

###### **tips.csv (primeras líneas)** 

total_bill,tip,sex,smoker,day,time,size 16.99,1.01,Mujer,No,Dom,Cena,2 10.34,1.66,Hombre,No,Dom,Cena,3 21.01,3.5,Hombre,No,Dom,Cena,3 23.68,3.31,Hombre,No,Dom,Cena,2 

**3.6. Ejercicios** 

**51** 

###### **tips.py** 

propinas_hombres = propinas_mujeres = 0 propina_fumador = propina_no_fumador = 0 propinas_acum = [0]*4 promedio = 0 cant_operaciones = 0 dia_orden_mayor = **None** turno_orden_mayor = **None** monto_orden_mayor = **None** _###################################################################### # Para utilizar la librería mejorada de consola (rich) primero hay que # instalarla utilizando el comando pip install rich ######################################################################_ **from rich import** print **from rich.console import** Console **from rich.panel import** Panel c = Console() c.clear() first_row = **True with** open("tips.csv","r") **as** file: **for** fila **in** file: _# Debo saltear el primer registro ya que contiene los titulos_ **if** first_row: _# Indicar que ya no estoy en la primera fila_ first_row = **False else** : cant_operaciones += 1 _# Hacer todo el procesamiento # Ahora debo separar la fila leída en sus componentes_ campos = fila[:-1].split(",") _# print(campos) # Saco los campos que necesito_ total = float(campos[0]) propina = float(campos[1]) sexo = campos[2] dia = campos[4] horario = campos[5] _# Acumular por separado las propinas de hombres y mujeres_ **if** sexo ==) 'Hombre': propinas_hombres += propina **else** : propinas_mujeres += propina _# Obtener los datos de la mayor orden # Cuándo? Cuando sea la primera o sea mayor a la anterior_ **if** monto_orden_mayor ==) **None or** total > monto_orden_mayor: monto_orden_mayor = total dia_orden_mayor = dia turno_orden_mayor = horario _# Solo trabajo 4 días así que puedo acumular las propinas # en un vector de 4 elementos, relacionados # a Jue, Vie, Sab, Dom_ **if** dia ==) 'Juev': propinas_acum[0] += propina **elif** dia ==) 'Vie': propinas_acum[1] += propina 

**3. Archivos** 

**52** 

**elif** dia ==) 'Sab': propinas_acum[2] += propina **else** : propinas_acum[3] += propina 

_# Calcular la propina promedio_ promedio = (propinas_hombres+propinas_mujeres)/cant_operaciones _# Recorrer el vector de propinas y ver cual es el menor_ menor_indice = 0 _# Voy a suponer que es el primero_ menor_propina = propinas_acum[0] menor_dia = "" 

**for** i **in** range(len(propinas_acum)): **if** propinas_acum[i] < menor_propina: menor_propina = propinas_acum[i] menor_indice = i _# Cuando termine tengo que ver a qué dia corresponde ese índice_ **if** menor_indice ==) 0: menor_dia = "Jueves" **elif** menor_indice ==) 1: menor_dia = "Viernes" **elif** menor_indice ==) 2: menor_dia = "Sábado" **else** : menor_dia = "Domingo" 

c.print(Panel("Análisis de propinas en New York")) 

print (f"[white bold on green]Propinas de los hombres:[/] **{** propinas_hombres **:** .2f **}** ") print (f"[white bold on green]Propinas de las mujeres:[/] **{** propinas_mujeres **:** .2f **}** ") print (f"[white bold on green]Propina promedio:[/] **{** promedio **:** .2f **}** ") print (f"La mayor venta fué de [on green] **{** monto_orden_mayor **}** [/] y se realizó un [on �→ green] **{** dia_orden_mayor **}** [/] en el turno [on green] **{** turno_orden_mayor **}** [/]") print (f"Los días más lentos son los [on green] **{** menor_dia **}** [/] con solamente [on �→ green] **{** menor_propina **}** [/] de propina") c.print(Panel("Fin de la ejecución")) 

### **Colecciones avanzadas** 

##### **4.1 Conjuntos** 

###### **4.1.1 Introducción** 

Los conjuntos son una estructura de datos proporcionada por el lenguaje que permite almacenar y manipular colecciones de elementos. A diferencia de las listas o las tuplas, los conjuntos tienen características distintivas que los hacen únicos. 

Una de las principales características de los conjuntos es su capacidad para eliminar automáticamente elementos duplicados. Esto significa que, al insertar un elemento repetido en un conjunto, este será ignorado y no se agregará nuevamente. 

Otra diferencia importante es que los conjuntos no admiten acceso indexado. No es posible acceder a elementos individuales utilizando el operador de corchetes o rebanadas, como se puede hacer en las listas o tuplas. 

Sin embargo, la característica principal de los conjuntos es su eficiencia en las operaciones de búsqueda. Mientras que en las listas o tuplas una búsqueda puede requerir recorrer todos los elementos, en los conjuntos la verificación de pertenencia tiene complejidad O(1) en promedio. Esto permite localizar rápidamente un elemento sin recorrer toda la colección. 

Esta propiedad hace que los conjuntos sean especialmente útiles para realizar búsquedas de elementos sin duplicados. Además, los conjuntos son ideales para realizar operaciones de conjuntos matemáticos, como uniones, intersec- 

53 

**4. Colecciones avanzadas** 

**54** 

ciones y diferencias. Estas operaciones, que requerirían una programación relativamente compleja y lenta con listas o tuplas, pueden ser realizadas de manera eficiente y sencilla con conjuntos. 

En resumen, los conjuntos son una valiosa estructura de datos que permiten almacenar y manipular colecciones de elementos sin duplicados. Su eficiencia en las operaciones de búsqueda y su capacidad para realizar operaciones de conjuntos de manera rápida los convierten en una herramienta poderosa para resolver diversos problemas. 

###### **4.1.2 Operaciones de datos** 

###### **Creación** 

Existen tres formas de crear conjuntos en Python. La primera opción es utilizar la función set(), que crea un conjunto vacío. Este conjunto vacío se puede asignar a una variable para su posterior manipulación. Una vez creado el conjunto vacío, se pueden utilizar métodos para insertar elementos en él. 

La segunda opción es crear un conjunto mediante la enumeración de elementos conocidos. Esto se asemeja a la notación matemática, donde se definen los elementos del conjunto entre llaves y separados por comas. Por ejemplo: {1, 2, 3}. 

La tercera opción es utilizar comprensiones de conjuntos, que son similares a las comprensiones de listas. Se utiliza la misma sintaxis de comprensión, pero se delimita con un par de llaves en lugar de un par de corchetes. En ambos casos, es importante tener en cuenta que los conjuntos no permiten elementos duplicados, por lo que la cantidad de elementos en el conjunto resultante puede ser menor a la cantidad de elementos especificados en la creación. Los elementos duplicados serán ignorados. Por ejemplo: {random.randint(1,10000) **for** x **in** range(100)} crea un conjunto con hasta 100 números al azar sin repeticiones. 

###### **Inserción** 

Una vez que se ha creado un conjunto utilizando una de las tres alternativas mencionadas anteriormente, es posible agregar nuevos valores al conjunto utilizando dos métodos específicos. 

El primer método es add(), que permite agregar un nuevo elemento al conjunto verificando que no exista previamente. En caso de que el elemento ya esté presente en el conjunto, el método add() no generará ninguna acción 

**4.1. Conjuntos** 

**55** 

ni devolverá ningún error. El conjunto permanecerá sin modificaciones. Sin embargo, si el elemento que se intenta agregar no se encuentra en el conjunto, el método add() lo añadirá correctamente, expandiendo el conjunto con un elemento adicional. 

El segundo método es update(), el cual recibe como parámetro una secuencia iterable, como un rango, una cadena, una tupla, una lista o incluso otro conjunto. Este método se encarga de recorrer todos los elementos de la secuencia iterable y los inserta en el conjunto original. Sin embargo, al igual que el método add(), el método update() garantiza que solo se insertarán elementos que no estén duplicados y que no existan previamente en el conjunto. Esto significa que no se agregarán elementos repetidos al conjunto durante el proceso de actualización. 

###### **Eliminación** 

Además de agregar elementos a un conjunto, también es posible eliminar elementos utilizando varios métodos disponibles. 

El primer método es remove(), el cual recibe como parámetro el valor que se desea eliminar del conjunto. Este método elimina el elemento especificado y, en caso de que el elemento no exista en el conjunto, generará un error. Es importante tener cuidado al utilizar remove() para asegurarse de que el elemento a eliminar realmente esté presente en el conjunto. 

El segundo método es discard(), que también recibe como parámetro el valor que se desea eliminar. Si el elemento existe en el conjunto, discard() lo eliminará sin generar errores. Sin embargo, si el elemento no está presente, discard() simplemente ignorará la solicitud y permitirá que el programa continúe sin interrupciones. 

Otra opción para eliminar elementos es el método pop(), el cual selecciona y elimina arbitrariamente un elemento del conjunto. El elemento eliminado se devuelve como resultado de la llamada a pop(), lo que permite al usuario conocer qué elemento fue eliminado en caso de necesitarlo. 

Por último, el método clear() borra todos los elementos del conjunto, dejándolo vacío. Este método es útil cuando se desea reiniciar el conjunto y eliminar todos sus elementos sin eliminar la variable en sí. 

**4. Colecciones avanzadas** 

**56** 

###### **Recorridos** 

Cuando se trabaja con conjuntos y se desea recorrer sus elementos, se puede utilizar la instrucción for de manera similar a como se recorren las listas. Con la sintaxis for variable in conjunto, se realizará una iteración por cada elemento almacenado en el conjunto, asignando cada valor a la variable del ciclo for. 

Es importante tener en cuenta que al recorrer un conjunto, los elementos no se encontrarán en un orden específico. A diferencia de las listas, donde los elementos se mantienen en el orden en que se insertaron, un conjunto no preserva el orden de inserción. 

Si se requiere recorrer un conjunto en un orden específico, como un orden numérico o alfabético, no es posible lograrlo directamente con un conjunto. Sin embargo, la función sorted() devuelve una nueva lista con los mismos elementos del conjunto, pero ordenados según sus valores. Es importante destacar que esto implica la creación de una nueva estructura de datos (la lista ordenada) y no afecta el orden interno del conjunto. 

A veces, al recorrer un conjunto, puede parecer que los elementos están ordenados, especialmente si se insertan solo números enteros. Sin embargo, esto no se puede garantizar para otros tipos de datos o para conjuntos más grandes. Por lo tanto, nunca se debe confiar en que un conjunto tendrá los datos ordenados, a menos que se utilice el método sorted() para obtener una lista ordenada explícitamente. 

###### **4.1.3 Operaciones de conjuntos** 

Los conjuntos son especialmente útiles para eliminar elementos duplicados, ya que garantizan la unicidad de los datos almacenados. Además, permiten realizar operaciones de conjuntos similares a las que se utilizan en matemáticas. 

###### **Pertenencia** 

La operación principal en un conjunto es verificar la pertenencia de un elemento. Para esto, se utiliza el operador **in** , que verifica si un valor dado pertenece al conjunto. El operador in devuelve True si el elemento está presente en el conjunto y False en caso contrario. La diferencia principal con respecto a las listas es que la búsqueda en un conjunto tiene complejidad O(1) en promedio, 

**4.1. Conjuntos** 

**57** 

por lo que no es proporcional a la cantidad de elementos almacenados. 

Cuando se trabaja con más de un conjunto, se pueden realizar operaciones de conjuntos, como la unión, la intersección y la diferencia. Estas operaciones se aplican utilizando diferentes métodos. 

###### **Unión** 

La unión de conjuntos se puede lograr mediante el método union(). Este método recibe como parámetro un segundo conjunto y devuelve un nuevo conjunto que contiene todos los elementos no repetidos de ambos conjuntos. También está disponible el método update(), que realiza la unión modificando el conjunto original. 

###### **Intersección** 

La intersección de conjuntos se puede lograr utilizando el método intersection(). Este método recibe como parámetro un segundo conjunto y devuelve un nuevo conjunto con los valores que existen en ambos conjuntos. Además, el método intersection_update() realiza la intersección modificando el conjunto original. 

###### **Diferencias** 

La diferencia de conjuntos se puede obtener mediante el método difference(). Este método se aplica a un conjunto y recibe como parámetro otro conjunto. Retorna un nuevo conjunto con los elementos presentes en el primer conjunto pero no en el segundo. También está disponible el método difference_update(), que realiza la diferencia modificando el conjunto original. 

La diferencia simétrica, también conocida como diferencia exclusiva, se obtiene utilizando el método symmetric_difference(). Este método recibe como parámetro un segundo conjunto y devuelve un nuevo conjunto que contiene todos los elementos presentes en ambos conjuntos, excepto aquellos que existen en ambos conjuntos al mismo tiempo. El método symmetric_difference_update() realiza la diferencia simétrica modificando el conjunto original. 

###### **4.1.4 Casos de aplicación** 

###### **4.1.5 Eliminación de repetidos de una lista** 

En este ejemplo se dispone de una lista llamada lista que contiene elementos duplicados. Para eliminar los duplicados, se convierte la lista en un conjunto 

**4. Colecciones avanzadas** 

**58** 

utilizando la función set(). Los conjuntos en Python sólo pueden contener elementos únicos, por lo que al convertir la lista en un conjunto, automáticamente se eliminan los elementos duplicados. 

Luego se convierte nuevamente el conjunto a una lista utilizando la función list()y se asigna en una nueva lista llamada lista_sin_duplicados que contiene los elementos de la lista original sin duplicados. 

Finalmente, se imprime la lista sin duplicados para verificar el resultado. 

_# Lista con elementos duplicados_ lista = [1, 2, 3, 4, 2, 3, 5, 6, 1, 7, 8, 5, 9] _# Convertir la lista en un conjunto # para eliminar duplicados_ conjunto = set(lista) 

_# Convertir el conjunto nuevamente a una lista_ lista_sin_duplicados = list(conjunto) _# Imprimir la lista sin duplicados_ print(lista_sin_duplicados) _#[)1, 2, 3, 4, 5, 6, 7, 8, 9]_ 

###### **4.1.6 Operaciones entre múltiples conjuntos** 

En este ejemplo se dispone de dos conjuntos curso_a y curso_b que representan los nombres de personas inscriptas en dos cursos diferentes y sobre ellos se utilizan las siguientes operaciones de conjuntos: 

La operación de unión (union()) combina ambos conjuntos y devuelve un nuevo conjunto con todos los elementos únicos de ambos conjuntos. 

La operación de intersección (intersection()) encuentra los elementos comunes entre ambos conjuntos y devuelve un nuevo conjunto con esos elementos. 

La operación de diferencia (difference()) encuentra los elementos que están en el primer conjunto pero no en el segundo conjunto y devuelve un nuevo conjunto con esos elementos. 

La operación de diferencia simétrica (symmetric_difference()) encuentra los elementos que están en uno de los conjuntos pero no en ambos conjuntos y devuelve un nuevo conjunto con esos elementos. 

Cada operación se aplica a los conjuntos y el resultado se almacena en una variable correspondiente. A continuación se imprimen los conjuntos resultantes para ver los nombres de las personas según cada operación. 

**4.2. Diccionarios** 

**59** 

_# Conjunto de nombres de personas del curso A_ curso_a = {"Juan", "María", "Pedro", "Luisa", "Ana"} _# Conjunto de nombres de personas del curso B_ curso_b = {"Pedro", "Ana", "Sofía", "Carlos"} _# Unión: personas inscriptas en al menos uno de los cursos_ union = curso_a.union(curso_b) print(union) _# {'Juan', 'Carlos', 'María', 'Pedro', 'Luisa', 'Ana', 'Sofía'} # Intersección: personas inscriptas en ambos cursos_ interseccion = curso_a.intersection(curso_b) print(interseccion) _# {'Ana', 'Pedro'} # Diferencia: inscriptos sólo en el curso A_ diferencia = curso_a.difference(curso_b) print(diferencia) _# {'María', 'Luisa', 'Juan'} # Diferencia simétrica: inscriptos en # uno de los cursos, pero no en ambos_ diferencia_simetrica = curso_a.symmetric_difference(curso_b) print(diferencia_simetrica) _# {'Carlos', 'Sofía', 'María', 'Juan', 'Luisa'}_ 

##### **4.2 Diccionarios** 

###### **4.2.1 Introducción** 

Los diccionarios son una estructura de datos altamente versátil y poderosa que permite almacenar información de manera distinta a otras estructuras disponibles en el lenguaje. A diferencia de estas, los diccionarios no almacenan conjuntos o grandes volúmenes de datos, sino que se basan en pares de datos conocidos como “clave” y “valor”. También denominados “arreglos asociativos” en otros lenguajes, los diccionarios establecen una relación entre una clave única en todo el conjunto y un valor asociado a esa clave. 

En esencia, los diccionarios almacenan pares de datos, donde la clave actúa como identificador único para un dato específico, y el valor corresponde al dato asociado a esa clave. Este concepto es similar al de las claves primarias utilizadas en estructuras de bases de datos relacionales. Una característica destacada de los diccionarios es la velocidad de las operaciones de búsqueda: en promedio tienen complejidad O(1), incluso cuando el diccionario contiene una gran cantidad de datos. 

Los diccionarios no tienen un índice numérico para acceder a sus elementos y no permiten claves duplicadas. Desde Python 3.7 preservan el orden 

**4. Colecciones avanzadas** 

**60** 

en que se insertan sus pares clave-valor, aunque su principal ventaja sigue siendo la rapidez para recuperar un valor a partir de su clave. 

Los diccionarios son especialmente útiles en situaciones en las que es necesario asociar un dato con un valor identificador. Por ejemplo, al almacenar datos de nombres de personas, es posible utilizar un diccionario en el que los nombres estén asociados con los números de documento de cada individuo. De esta manera, al proporcionar el número de documento al diccionario, se obtendría el nombre correspondiente asociado a ese documento. 

Si bien es posible lograr una funcionalidad similar utilizando arreglos y utilizando el valor clave como índice del arreglo, en muchos casos el valor clave no puede ser equiparado a un índice de arreglo. Por ejemplo, si se requiere almacenar datos de personas y utilizar el número de documento como índice de un arreglo, se enfrentaría a la impracticabilidad de crear un arreglo con 100 millones de elementos para cubrir todas las posibilidades de números de documento de 8 dígitos. Los diccionarios, en cambio, permiten utilizar cualquier tipo de dato disponible en Python como clave, ya sean valores numéricos, cadenas u otros tipos de datos. 

La flexibilidad de los diccionarios radica en su capacidad para establecer relaciones directas entre datos y valores identificadores, independientemente de su tipo o dominio. Esto los convierte en una herramienta poderosa para abordar una amplia gama de situaciones donde es necesario asociar y recuperar datos de manera eficiente. 

###### **4.2.2 Operaciones** 

###### **Creación** 

La sintaxis utilizada para crear diccionarios es bastante similar a la de los conjuntos. Existen tres mecanismos principales para crear un diccionario. 

El primero de ellos es utilizando la función dict(), la cual inicializa un diccionario vacío al que se le pueden ir agregando pares clave-valor. 

Otra forma de crear un diccionario es mediante la enumeración explícita de sus datos. Se utiliza un par de llaves ({}) y se enumeran los valores separados por comas. Sin embargo, a diferencia de los conjuntos, en los diccionarios se debe establecer un par clave-valor para cada valor enumerado. Esto se realiza utilizando dos puntos (:) para asociar la clave con su respectivo valor. 

Por último, se puede utilizar la comprensión de diccionarios para crear diccionarios de manera concisa. La sintaxis es similar a la comprensión de 

**4.2. Diccionarios** 

**61** 

conjuntos, utilizando un par de llaves que encierra una expresión de comprensión. En este caso, se establece el par clave-valor, donde tanto la clave como los valores pueden depender de los valores iterados en un ciclo for, utilizando dos puntos (:) para asociarla con el valor correspondiente. 

###### **Acceso** 

Una vez que se ha creado un diccionario, es posible acceder a sus valores utilizando el operador de corchetes ([]). En este caso, se indica la clave correspondiente al valor que se desea obtener. A diferencia de las listas, en los diccionarios la clave puede ser de cualquier tipo válido en Python. Por lo tanto, se puede utilizar el nombre del diccionario seguido del operador de acceso y, dentro de este, se especifica la clave que se busca. El acceso devuelve en promedio en tiempo O(1) el valor asociado con la clave. Si la clave no existe en el diccionario, se produce una excepción **KeyError** . 

Otra forma de acceder a los valores almacenados en el diccionario es utilizando el método get(). Este método recibe como parámetro la clave que se busca y, en caso de que la clave no se encuentre en el diccionario, devuelve None por defecto. Sin embargo, get() acepta un segundo parámetro opcional que permite especificar un valor por defecto. De esta manera, se puede acceder al valor asociado a la clave sin necesidad de utilizar una instrucción condicional, y se obtendrá el valor por defecto si la clave no existe en el diccionario. 

Por último, existe un método llamado setdefault(), que recibe una clave y un valor por defecto como parámetros. Si la clave existe en el diccionario, el método devuelve el valor asociado a esa clave. En caso contrario, crea una nueva entrada en el diccionario asociando la clave con el valor por defecto especificado en el segundo parámetro. Este método es útil para evitar la verificación de existencia de la clave y asignar un valor predeterminado si no se encuentra en el diccionario. 

Para poder conocer la longitud de un diccionario se dispone de la instrucción len que funciona de la misma manera que con todas las colecciones e iterables. 

###### **Inserción** 

Para agregar nuevos elementos o modificar elementos existentes en un diccionario, se utiliza el operador de acceso indexado de manera similar a como se haría con un arreglo. Es decir, se utiliza el nombre del diccionario seguido 

**4. Colecciones avanzadas** 

**62** 

del símbolo de corchetes con la clave deseada en su interior, y luego se utiliza el operador de asignación (=) para asignar un nuevo valor a esa clave. 

Si la clave ya existe en el diccionario, el valor asociado a esa clave se actualizará con el nuevo valor asignado. En caso de que la clave no exista previamente en el diccionario, se creará una nueva entrada con la clave y el valor especificados. De esta manera, se puede agregar o modificar elementos en el diccionario de forma dinámica y flexible. 

###### **Borrado** 

Para eliminar elementos de un diccionario, existen dos métodos principales. El primero es utilizar la instrucción ‘del‘, seguida del nombre del diccionario y entre corchetes la clave que se desea borrar. Esta instrucción simplemente elimina la clave y el valor asociado a ella. 

El segundo método es el uso del método ‘pop()‘. Este método recibe como argumento la clave que se desea eliminar y devuelve el valor asociado a esa clave. Además, elimina la clave y su valor del diccionario. Si se proporciona un segundo argumento opcional al método ‘pop()‘, se especifica un valor por defecto que será retornado si la clave no existe en el diccionario. Esto evita que se produzca un error en caso de que la clave no exista. 

Otra opción es utilizar el método ‘clear()‘, el cual borra todos los pares clave-valor del diccionario, dejándolo vacío como si estuviera recién creado. Este método no requiere ningún argumento. 

Finalmente, la instrucción ‘del‘ también puede utilizarse para eliminar todo el diccionario por completo, incluyendo sus valores contenidos, lo cual implica eliminar también la variable del diccionario en sí. 

Estas opciones permiten la manipulación y eliminación de elementos en un diccionario de acuerdo a las necesidades específicas del programa. 

###### **Recorrido** 

Los diccionarios ofrecen tres formas de ser recorridos. El método keys() devuelve una vista con todas las claves: no hay claves repetidas y puede recorrerse o utilizarse en operaciones de conjuntos. Por otro lado, values() devuelve una vista con todos los valores; estos pueden repetirse. Las vistas reflejan los cambios realizados posteriormente en el diccionario. 

También pueden recorrerse los pares ordenados (clave, valor) con un ciclo for. Pero en este caso el ciclo posee dos variables que se asignan en cada vuelta. 

**4.2. Diccionarios** 

**63** 

Para ello se dispone del método items(), que devuelve una vista de pares. En cada vuelta del for puede asignarse el par o directamente desempaquetarlo en dos variables. En el ejemplo siguiente se las desempaqueta en las variables numero y nombre: 

diccionario = {1: "Lunes", 2: "Martes", 3: "Miércoles"} **for** numero, nombre **in** diccionario.items(): print(f"El día **{** numero **}** se llama **{** nombre **}** ") 

### **Excepciones y gestión de errores** 

##### **5.1 ¿Qué son las excepciones?** 

Una excepción es una condición de error no prevista en un programa. Tradicionalmente, en la programación estructurada, el programador debía verificar cada resultado de ejecución y detectar los posibles problemas. 

Con la técnica de excepciones el programador debe establecer un bloque de código a ejecutar cuando una excepción se produzca y es el lenguaje el responsable de detectar una condición de ejecución anómala. 

Esto genera un código más claro y un manejo de errores más compacto y ordenado. 

##### **5.2 Captura y disparo de Excepciones** 

Existen dos conceptos fundamentales en el manejo de excepciones, la captura ( **except** ) y el disparo ( **raise** ) de excepciones. 

Durante la captura, el programador escribe código para que, al producirse una excepción de un cierto tipo, se puedan tomar las medidas necesarias, ya sea para corregir la condición de error, reportarla o proveerle al usuario medios alternativos para realizar la operación solicitada. 

b = 10 c = 0 **try** : 

65 

**5. Excepciones y** **<u>gestión de errores</u>** 

**66** 

_# Dividir dos números_ a = b / c print (a) **except ZeroDivisionError** : _# Se produce una excepción de división por cero_ print ("El divisor de la expresión es 0 (cero)") 

Durante el disparo de excepciones el rol del programador es el contrario. Al detectar una condición errónea el programador notifica, por medio de algún tipo de excepción, a otros procesos, que dicha condición se ha producido y provee los datos necesarios para que dichos procesos puedan tomar conocimiento del error, sus posibles causas y tomar medidas al respecto. 

b = 10 c = 0 _# Validar si el divisor es 0 (cero)_ **if** (c ==) 0): _# En caso afirmativo disparar una excepción acorde_ **raise ZeroDivisionError** 

##### **5.3 Tipos de excepciones** 

Python dispone de diversos tipos de excepciones que indican el tipo de error producido. Estos son los más comunes: 

- **TypeError :** Ocurre cuando se aplica una operación o función a un dato del tipo inapropiado. 

**ZeroDivisionError :** Ocurre cuando se intenta dividir por cero. 

- **OverflowError :** Ocurre cuando un cálculo excede el límite para un tipo de dato numérico. 

- **IndexError :** Ocurre cuando se intenta acceder a una secuencia con un índice que no existe. 

- **KeyError :** Ocurre cuando se intenta acceder a un diccionario con una clave que no existe. 

- **FileNotFoundError :** Ocurre cuando se intenta acceder a un fichero que no existe en la ruta indicada. 

**ImportError :** Ocurre cuando falla la importación de un módulo. 

Los módulos de terceros pueden definir sus propios tipos de excepciones, tal como se explicará en más detalle en una sección posterior. 

**5.4. Estructura de control de excepciones** 

**67** 

##### **5.4 Estructura de control de excepciones** 

Python utiliza un bloque **try** - **except** - **else** 

**try** : _# Bloque de código que puede generar # algún tipo de error_ **except** _tipo1_: _# Bloque que se ejecuta si se produce una excepción # de tipo _tipo1__ **except** _tipo2_: _# Bloque que se ejecuta si se produce una excepción # de tipo _tipo2__ **else** : _# Bloque que se ejecuta si NO SE # PRODUCE NINGUN ERROR # El bloque else es opcional_ 

###### **5.4.1 Ejemplo de gestión de excepciones** 

Este ejemplo intenta realizar una división. En caso de que el denominador sea cero se va a disparar una excepción, la cual en lugar de aparecerle al usuario, es capturada por el programa que tiene así la oportunidad de presentar un mensaje claro con respecto al error. 

**def** division(a, b): **try** : result = a / b **except ZeroDivisionError** : print('¡No se puede dividir por cero!') **else** : print(result) 

En este caso se intenta abrir un archivo. Si el archivo no existe se dispara una excepción que es capturada y se informa el error. Esto permitiría la usuario, eventualmente, seleccionar un archivo diferente. 

**try** : f = open('fichero.txt') _# El fichero no existe_ **except FileNotFoundError** : print('¡El fichero no existe!') **else** : print(f.read()) 

**5. Excepciones y** **<u>gestión de errores</u>** 

**68** 



<!-- Start of picture text -->
En el bloque “try” se encuentran todas,<br>try enlas uninstruccionescontexto de quecontrol se debende errores. ejecutar<br>En cada uno de los bloques “except” se<br>gestiona un tipo de error determinado.<br>El bloque “else” contiene el cédigo que<br>else se debe ejecutar SOLO sino se han<br>producido excepciones,<br>. El bloque “finally” se ejecuta siempre, ya<br>finally sea que se han producido o no<br>excepciones.<br><!-- End of picture text -->

Figura 5.1: Estructura completa de un bloque de excepción 

##### **5.5 La estructura completa del bloque try-except** 

El bloque **try** -catch de Python tiene una estructura simple, conformada solamente por esas dos instrucciones, pero también tiene una estructura completa que nos permite realizar varias acciones más, tanto en caso de que se produzcan errores como en caso de que el programa funcione correctamente. 

Las diferentes secciones del bloque tienen las siguientes funciones: 

**try** Este bloque contiene todo el código a ejecutar en condiciones normales. 

- **except** Este bloque contiene el código que se debe ejecutar en respuesta a una excepción de un cierto tipo. Puede repetirse para manejar distintos tipos de excepciones. 

- **else** Este bloque contiene código que se ejecuta solamente cuando no se ha producido ninguna excepción. 

- **finally** Este bloque contiene código que se ejecuta, incondicionalmente, ya sea que se hayan producido o no excepciones como parte del flujo normal de ejecución. 

**5.6. Excepciones definidas por el programador** 

**69** 

##### **5.6 Excepciones definidas por el programador** 

Es posible, en Python, que un programador defina y utilice sus propios tipos de excepciones, para mejorar la legibilidad del código, para expresar con mayor exactitud las condiciones de error de un programa o para considerar situaciones no cubiertas por los tipos de excepciones existentes en el lenguaje o en módulos de terceros. 

Para ello debe crear una clase que herede de clase base **Exception** , la cual es la base de todas las excepciones gestionadas por Python. 

_# Definir una Excepción personalizada_ **class SalarioInsuficiente** ( **Exception** ): _"""Se dispara cuando el salario del empleado es insuficiente. Atributos: salario -- salario que disparó el error message -- explicación del error """_ **def** __init__(self, salario, message="El salario no está entre (5000, 15000)."): self.salario = salario self.message = message super().__init__(self.message) 

Una vez que esa excepción está definida, la misma se puede disparar como cualquier otra excepción estándar del lenguaje, mediante el comando **raise** SalarioInsuficiente(1200). 

### **Clases** 

##### **7.1 Introducción** 

###### **7.1.1 Programación orientada a objetos** 

La programación orientada a objetos (POO) es un paradigma de programación que organiza el código alrededor de objetos, los cuales son instancias de clases. En lugar de enfocarse en las acciones y funciones que se realizan en el programa, la POO se centra en la interacción entre los objetos, permitiendo modelar y representar de manera más precisa entidades del mundo real en el software. 

En la POO, un objeto combina datos y funciones relacionadas en una sola estructura, lo que facilita su manipulación y comprensión. Los objetos se definen mediante clases, que actúan como plantillas o moldes para crear instancias específicas. Cada objeto tiene atributos (propiedades o características) que describen su estado y métodos (funciones o comportamientos) que definen su capacidad para realizar acciones y responder a eventos. 

El enfoque orientado a objetos fomenta la reutilización de código y el diseño modular, ya que los objetos pueden ser utilizados en diferentes partes de un programa y en otros programas. Además, permite una abstracción más efectiva, ya que los objetos encapsulan tanto los datos como el comportamiento relacionado, lo que facilita el desarrollo y el mantenimiento del software a largo plazo. 

La POO se basa en cuatro principios fundamentales: 

79 

**7. Clases** 

**80** 

**Abstracción** Permite representar características y comportamientos esenciales de un objeto en un modelo simplificado. Se identifican las propiedades (atributos) y acciones (métodos) relevantes de un objeto y se encapsulan en una clase. 

**Encapsulamiento** Consiste en ocultar los detalles internos de un objeto y proporcionar una interfaz para interactuar con él. Los datos (atributos) y las funciones (métodos) de un objeto se encapsulan dentro de la clase, y solo se accede a ellos a través de métodos públicos definidos en la interfaz. 

**Herencia** Permite crear nuevas clases basadas en clases existentes, aprovechando las características y comportamientos heredados. Una clase derivada (subclase) puede extender o especializar la funcionalidad de una clase base (superclase), heredando sus atributos y métodos, y agregando o modificando los necesarios. 

**Polimorfismo** Permite que un objeto pueda presentar diferentes formas o comportamientos según el contexto en el que se utilice. Se puede invocar un método de diferentes objetos de una jerarquía de clases y obtener resultados diferentes, siempre que cumplan con la interfaz común definida en una clase base. 

La programación orientada a objetos (POO) fue inventada con el objetivo de proporcionar una mejor forma de organizar y diseñar software complejo. Antes de la POO, los programas se estructuraban principalmente en torno a funciones y procedimientos, lo que a menudo resultaba en un código difícil de mantener, extender y reutilizar. 

La POO surgió en la década de 1960 como una forma de abordar estos desafíos. Su objetivo principal era permitir una representación más fiel de los objetos del mundo real dentro del software, lo que facilitaría el desarrollo de aplicaciones más escalables y flexibles. 

Al enfocarse en los objetos, la POO permitió una mejor modelización de los sistemas, ya que los objetos podían contener tanto datos (atributos) como comportamientos relacionados (métodos). Esto permitió que el código se estructurara de manera más intuitiva y modular, ya que los objetos podían interactuar entre sí mediante mensajes, encapsulando así su funcionalidad interna. 

**7.1. Introducción** 

**81** 



<!-- Start of picture text -->
Bad<br>Programa ie<br><!-- End of picture text -->

Figura 7.1: Programación estructurada 

La programación orientada a objetos (POO) ofrece varias ventajas en comparación con la programación estructurada, especialmente en relación al concepto de la brecha semántica o semantic gap. La brecha semántica se refiere a la diferencia entre cómo se modela y se representa el mundo real en el software y cómo se percibe y comprende el mundo real por parte de los usuarios y desarrolladores. 

De esta manera, si se requiere desarrollar un software que represente, por ejemplo, un sistema de ventas para un comercio, entre los conceptos principales detectados durante la etapa de análisis se encontrarían los de artículos, clientes y ventas. En la programación estructurada, el software sería redactado como una secuencia bastante larga de líneas de código, agrupadas y organizadas con algún criterio, pero orientado principalmente a la funcionalidad esperada por el software. 

Sin embargo, todo software requiere ser susceptible a cambios luego de ser desarrollado. Tales cambios pueden provenir de diversos orígenes, tales como errores detectados durante el funcionamiento, requerimientos nuevos o incluso cambios externos, por ejemplo en la legislación vigente. 

La programación orientada a objetos busca que el código fuente sea lo más parecido posible a la realidad, para que sea más simple identificar el punto donde debe ser modificado cuando se encuentre una modificación en los requerimientos, y que estos afecten en pocos lugares dentro de todo el código fuente. Así, si en el software del sistema de ventas, si hay un cambio en un 

**7. Clases** 

**82** 



<!-- Start of picture text -->
Cliente<br>Venta<br>Programa |= |<br>Articulo<br><!-- End of picture text -->

Figura 7.2: Programación orientada a objetos 

requirimiento del proceso de ventas, los cambios en el código fuente estarían localizados principalmente en la clase que representa a la transacción de la venta, y no en la o las clases que representan a los artículos o a los clientes. 

###### **7.1.2 Clases y objetos** 

Cuando se busca resolver un problema utilizando la programación orientada a objetos, se aborda la representación del problema mediante la creación de objetos y las relaciones entre ellos. Cada objeto encapsula su propio estado y comportamiento, lo que permite modelar de manera más precisa las entidades y relaciones del dominio del problema. 

Cada objeto tiene atributos que describen sus características y métodos que definen sus comportamientos o acciones asociadas. Muchos objetos comparten características que los definen, pudiendo ser agrupados o clasificados bajo una misma definición. Por ejemplo, dos objetos que realicen compras en un comercio generalmente tienen el mismo conjunto de datos y realizan las mismas acciones. A ambos se los puede clasificar como “Clientes”. 

Una clase es una plantilla que define las características comunes compartidas por un conjunto de objetos para los que se aplica la misma definición. En esencia, una clase actúa como un modelo o plano para la creación de objetos. Contiene la estructura y el comportamiento que se aplicarán a cada instancia de esa clase. 

**7.2. Clases** 

**83** 



<!-- Start of picture text -->
oe Cliente ©<br><!-- End of picture text -->

Figura 7.3: Objetos y sus relaciones 

Cuando se crea un objeto en la programación orientada a objetos, se basa en una clase específica. Cada objeto es una instancia individual y concreta de esa clase. Esto significa que cada objeto posee sus propios valores únicos para los atributos definidos en la clase, así como su propia capacidad para ejecutar los métodos asociados a esa clase. Cada objeto es una entidad única y distinta que comparte las características y el comportamiento definidos en su clase, pero puede tener valores de atributos diferentes de las otras instancias de la misma clase y puede responder de manera independiente a los mensajes que reciba. 

##### **7.2 Clases** 

Para la creación de una clase se utiliza el bloque **class** , cuya sintaxis es: 

**class NombreClase** : definición de métodos 

El nombre de la clase generalmente consiste de un sustantivo en singular, con notación Pascal, es decir que esta commpuesto por letras en minúscula con su inicial en mayúscula. En caso de que el identificador esté formado por más de una palabra, se las diferencia sin un delimitador y con mayúscula en 

**7. Clases** 

**84** 



<!-- Start of picture text -->
oe Cliente 2)<br><!-- End of picture text -->

Figura 7.4: Objetos clasificados según su rol en el dominio 

la primera letra de cada palabra, por ejemplo: CodigoPostal. 

##### **7.3 Atributos** 

Los atributos no son declarados con una construcción gramatical en particular, simplemente se los asigna en el momento en que se los requiere crear dentro de algún método. Para diferenciar los atributos de las variables locales se los diferencia usando siempre la sintaxis objeto.atributo, indicando al objeto con el identificador seleccionado para referenciar al receptor del mensaje. 

##### **7.4 Constructor** 

El método constructor se denomina __init__ y para funcionar require recibir como primer parámetro formal una variable que referencia al objeto que se está construyendo. El identificador de este parámetro puede ser cualquier nombre válido de variable, pero la convención prefiere denominarlo usualmente self. 

El uso más habitual del método constructor es el de asignar valores iniciales para los atributos. Tales valores pueden ser recibidos como parámetros o asignados en forma arbitraria. Si bien las clases sólo pueden poseer un único constructor, se le pueden asignar valores por defecto a los parámetros 

**7.4. Constructor** 

**85** 

para ofrecer que en la construcción se indiquen valores concretos durante la creación o se utilicen los valores por defecto. 

Suponiendo una clase Persona con atributos para almacenar documento, nombre, apellido y edad de una persona, se presentan a continuación el diagrama de clases y el bloque class correspondiente: 



###### **persona.py** 

**class Persona** : **def** __init__(self, documento=0, nombre="No", apellido="No", edad=0): self.documento = documento self.nombre = nombre self.apellido = apellido self.edad = edad 

Para instanciar objetos de esta clase Persona se debe ejecutar el constructor con una sintaxis que puede parecer extraña: en lugar de invocar en forma explícita a la función __init__, se indica el nombre de la clase (en este caso Persona) seguido de un par de paréntesis en el que se pueden enviar parámetros. Y hay más, ya que el primer parámetro formal (self) no debe ser enviado, el mismo va a llegar en forma automática al método constructor, referenciando al objeto que se está creando. 

Los métodos cuyos nombres inician y terminan con dos guiones bajos (__) se denominan **métodos mágicos** ya que no son invocados en forma explícita con su nombres sino que se ejecutan en forma automática a partir de otras operaciones. En otro capítulo se los analiza con mayor detalle. 

Por lo tanto, para obtener instancias de personas se las puede crear de la siguiente manera: requiere el siguiente bloque de código: 

> _# Los atributos se inicializan con # valores por defecto_ a = Persona() 

_# Los atributose se inicializan con_ 

**7. Clases** 

**86** 

_# los valores indicados en los # parámetros actuales_ b = Persona(1234, "Juan", "Perez", 23) 

_# Los atributos documento y apellido # se inicializan con los valores enviados # y los otros con valores por defecto_ c = Persona(documento=1234, apellido="Castro") 

Las clases pueden estar programadas en cualquier archivo de código fuente y en cualquier parte del mismo (afuera de una función), sin embargo es usual ubicar cada clase en un archivo cuyo nombre coincida con el de la clase. De esta manera, la clase Persona podría estar programada en un archivo persona.py. Para utilizar la clase deberá ser importada, usualmente con una instrucción de la forma **from persona import** *. 

##### **7.5 Referencias** 

Las variables a las que se les asigna un objeto se crean con un tipo llamado object. Sin embargo, la idea de que la variable almacena un objeto, a pesar de ser cómoda, es incorrecta. 

A diferencia de las variables de la programación estructurada, que son un almacenamiento que ocupa una porción de memoria con tamaño suficiente para que un dato entre completamente y que poseen un identificador, los objetos funcionan de forma diferente. La construcción de un objeto mediante una llamada a un método constructor efectivamente reserva memoria para almacenarlo, pero los objetos **no tienen nombre** !. Cada objeto posee una identidad provista durante su instanciación y que consiste en concreto en la dirección de memoria donde esta almacenado. Pero sin un nombre no se les puede enviar mensajes y por lo tanto los objetos resultan inservibles. 

Las variables de tipo object se denominan **referencias** y su valor efectivamente no es una instancia concreta de alguna clase. El dato que almacenan es la identidad de un objeto, es decir, la dirección de memoria donde el objeto se encuentra. Es práctico imaginar que una variable de tipo referencia guarda en realidad una flecha hasta el objeto. 

Por ejemplo, luego de ejecutar el siguiente código, los objetos quedan asignados como indica la figura: 

**7.5. Referencias** 

**87** 

p1 = Persona(documento=1255,nombre="Juan",apellido="Perez") p2 = Persona(documento=5293,nombre="Ana",apellido="Ruiz") 



<!-- Start of picture text -->
Juan Ana<br>Perez Ruiz<br>1255 EYES<br>|<br>|<br>i] E<br><!-- End of picture text -->

Cada variable de tipo referencia puede señalar o apuntar a un único objeto, pero de la misma forma que dos variables pueden poseer el mismo valor, dos referencias pueden estar señalando al mismo objeto. En estos casos, el envío de mensajes desde una referencia o desde la otra afectan a la misma instancia concreta. La operación de asignación efectivamente copia los valores de las variables, y eso no es diferente en el caso de las referencias: si se asigna una referencia con el valor de otra, dado que ellas almacenan las “flechas”, ambas quedan referenciando al mismo objeto. 

De esta manera, si a continuación del ejemplo anterior se ejecuta p3 = p2, el estado del programa queda como muestra la figura: 



<!-- Start of picture text -->
Juan Ana<br>Perez Ruiz<br>1255 EYES<br><!-- End of picture text -->

**7. Clases** 

**88** 

Otra consecuencia de esto es que la asignación no duplica objetos, la única forma de crear un objeto nuevo es mediante una llamada al constructor. 

Finalmente, si un objeto creado deja de ser apuntado por alguna referencia, el mismo queda inaccesible y por lo tanto inservible, ya que no se le pueden enviar mensajes ni siquiera para consultar su estado. Eventualmente si hace falta memoria durante la ejecución del programa, el interprete de python podrá decidir eliminarlo de la memoria. 

Si en el ejemplo se asigna p1 = p2, ninguna referencia queda apuntando a la persona Juan Perez: 



<!-- Start of picture text -->
@e<br>a<br>is<br>nm / \<br><!-- End of picture text -->

##### **7.6 Métodos** 

###### **7.6.1 Introducción** 

La programación orientada a objetos propone la construcción de programas mediante la interacción entre objetos, los cuales son entidades que encapsulan tanto datos (atributos) como comportamientos (métodos) relacionados. En este enfoque, un programa se concibe como un conjunto de objetos que interactúan entre sí al intercambiar mensajes. 

Cuando un objeto envía un mensaje a otro, está solicitando al objeto receptor que realice una acción o que proporcione información específica. Este proceso se denomina “paso de mensajes”. El objeto receptor, a su vez, atiende el mensaje y ejecuta el método correspondiente para responder adecuadamente a la solicitud. 

**7.6. Métodos** 

**89** 

La forma de implementar este mecanismo de mensajes en los lenguajes orientados a objetos es a través de lo que se denomina “métodos”. Los métodos son funciones asociadas a un objeto particular que definen su comportamiento y permiten que otros objetos interactúen con él. Los mismos pueden acceder a los atributos del objeto y realizar operaciones según la lógica definida en el código. 

Los métodos que residen dentro de cada objeto y se ejecutan cuando el objeto recibe un mensaje. Los mensajes pueden contener parámetros que el método utilizará para llevar a cabo su operación, además de acceder a los atributos propios del objeto para actuar en consecuencia y enviar una respuesta como resultado del mensaje recibido. 

En Python, los métodos se definen como funciones que reciben parámetros, pero el primer parámetro, por convención, es una referencia al propio objeto, que generalmente se nombra como self. Esta referencia self permite que el método acceda a los atributos y otros métodos del objeto actual, lo que facilita la manipulación de los datos y comportamientos específicos de ese objeto. 

Además un objeto puede colaborar con otros objetos para llevar a cabo una tarea o cumplir con un objetivo específico. Cuando un objeto recibe un mensaje y atiende a dicho mensaje, puede requerir la colaboración de otros objetos para lograr su objetivo. 

Para lograr esta colaboración, un método puede acceder a otros objetos y enviarles mensajes. Estos mensajes pueden incluir parámetros o información necesaria para que los objetos colaboradores realicen sus acciones. Luego, el método puede esperar las respuestas de estos objetos colaboradores y utilizar esa información para alcanzar sus propios objetivos y proporcionar una respuesta o resultado al mensaje original. 

###### **7.6.2 Sintaxis** 

Para agregar un método a una clase debe incluirse dentro del bloque **class** una definición de función con **def** cuyo primer parámetro sea self: 

**class Clase** : 

**def** __init__(self, .\))) _# código del constructor_ 

**def** metodo(self, parámetros): _# código del método_ 

**7. Clases** 

**90** 

**return** resultado 

Así, en el contexto de una clase Persona con atributos nombre y apellido, es posible definir un método llamado nombre_completo que concatene ambos atributos y retorne el nombre completo de la persona. Este método se definiría dentro de la clase Persona y recibiría el parámetro self, que es una referencia al objeto actual que recibe el mensaje de la siguiente manera: 

**class Persona** : **def** nombre_completo(self): **return** f" **{** self.nombre **} {** self.apellido **}** " 

Para enviar un mensaje de un objeto a otro, se utiliza la sintaxis de un punto seguido del nombre del método con paréntesis para enviar los parámetros necesarios. Esta sintaxis es equivalente a la de ejecutar una función, pero en este caso, está asociada a una referencia particular (objeto). En la lista de parámetros no se incluye al self, el mismo es llenado en forma implícita. 

El operador punto es el que permite enviar el mensaje al objeto referenciado desde una variable de tipo referencia. Dado que las referencias pueden considerarse que almacenan una flecha que parte desde la variable y llega al objeto. Cuando se utiliza el operador punto en una referencia, este recorre la flecha hasta llegar al objeto al que está apuntando, y es a ese objeto al que se le envía el mensaje mediante la invocación del método. 

per = Persona(123, "Juan", "Perez", 20) print(per.nombre_completo()) 

Es importante tener en cuenta que si la referencia a la que se le envía el mensaje está vacía o tiene el valor **None** (nulo), se generará un error, ya que no hay un objeto apuntado al que pedirle nada. Por lo tanto, el programador debe garantizar que la referencia no esté vacía antes de enviar el mensaje. 

Para evitar este tipo de errores, es común utilizar condicionales para verificar que la referencia no esté vacía antes de enviar el mensaje. 

### **Encapsulamiento** 

##### **8.1 Introducción** 

El encapsulamiento es un concepto fundamental en la programación orientada a objetos que se basa en la idea de que los objetos se comporten como “cápsulas”, es decir, como unidades cerradas que protegen su implementación interna. Esto significa que los detalles internos de la lógica, la naturaleza y la implementación de los atributos y métodos de un objeto están ocultos y no son accesibles directamente desde otros objetos. En lugar de permitir el acceso directo, los objetos deben comunicarse entre sí únicamente a través del paso de mensajes. 

La finalidad del encapsulamiento es proteger y mantener la integridad y coherencia del objeto, evitando que otros objetos interfieran directamente con sus atributos o métodos internos. Esto promueve una mayor modularidad y flexibilidad en el diseño del software, ya que cada objeto puede cambiar su implementación interna sin afectar el funcionamiento de otros objetos que interactúan con él. 

Al ocultar los detalles internos, el encapsulamiento mejora la abstracción y permite enfocarse en la interfaz pública del objeto, es decir, los métodos que están destinados a ser utilizados por otros objetos para interactuar con él. Esto crea una barrera protectora alrededor del objeto, lo que ayuda a prevenir errores y mantener la coherencia del sistema. 

Para establecer una comunicación entre objetos, se utiliza el paso de mensajes, donde un objeto envía un mensaje a otro objeto solicitando la ejecución 

91 

**8. Encapsulamiento** 

**92** 

de un método específico o solicitando información. El objeto receptor responde a este mensaje atendiendo al método correspondiente y puede devolver el resultado o enviar un nuevo mensaje a otro objeto, lo que permite la colaboración y el trabajo conjunto entre los objetos del sistema. 

##### **8.2 Ventajas** 

###### **8.2.1 Ocultamiento de la implementación** 

El encapsulamiento satisface la necesidad de permitir que un objeto pueda modificar su forma de funcionar sin afectar a los demás objetos con los que se comunica. Esta capacidad de adaptarse a cambios internos sin interrumpir la interacción con otros objetos es esencial para el mantenimiento y evolución del software a lo largo del tiempo. 

Si se analiza por ejemplo un escenario donde un objeto tiene la responsabilidad de almacenar datos de manera persistente, podria hacerlo en un archivo de texto. Otros objetos interactúan con él enviándole mensajes para guardar o recuperar datos. En una primera versión del programa, esta puede ser la implementación utilizada, y los objetos que se comunican con él confían en que sus mensajes serán atendidos adecuadamente y que los datos se guardarán en un archivo. 

Sin embargo, si en una versión futura el objeto decide cambiar su implementación para almacenar los datos en una base de datos o en una nube, en lugar de hacerlo en el archivo de texto, el objetivo es que este cambio no afecte al código existente de los otros objetos que interactúan con él. 

Esto se logra a través del encapsulamiento. Los objetos que utilizan al objeto de almacenamiento no necesitan conocer los detalles internos de su implementación ni dónde se almacenan los datos. En su lugar, confían en la interfaz pública del objeto, es decir, los mensajes que pueden enviarle y las respuestas que pueden esperar. 

De esta manera, los objetos que interactúan con el objeto de almacenamiento simplemente le envían mensajes como “guardá este dato” o “recuperá el dato almacenado”. No necesitan saber si el objeto utiliza un archivo de texto o una base de datos en la nube para almacenar los datos; simplemente confían en que sus mensajes serán procesados correctamente y que el objeto cumplirá con su responsabilidad de almacenamiento. 

**8.2. Ventajas** 

**93** 

###### **8.2.2 Validez del estado interno** 

El encapsulamiento surge también debido a la necesidad de mantener la validez del estado interno de un objeto. Un objeto requiere tener la tranquilidad de que sus atributos siempre poseen valores válidos acorde a su lógica interna. Si los atributos estuvieran expuestos y cualquier otro objeto pudiera modificarlos directamente, podrían asignarse valores que no cumplen con las restricciones lógicas del objeto. Como resultado, el objeto se vería forzado a incluir estructuras condicionales para verificar la validez de sus atributos cada vez que necesita operar con ellos. Esta situación generaría una complejidad innecesaria en el funcionamiento del objeto, requiriendo continuamente validaciones para garantizar la coherencia de los datos. 

Entonces se recomienda ocultar los atributos de otros objetos y establecer que cualquier consulta o modificación de un atributo debe realizarse mediante el envío de mensajes específicos al objeto. De esta manera, el objeto tiene un control total sobre la validez de sus atributos y puede validarlos en el momento en que otro objeto intenta cambiarlos o asignarles un nuevo valor. 

Por ejemplo, si un objeto representa un producto con un atributo de “precio”, que no puede ser negativo según la lógica del negocio, el encapsulamiento permite que cualquier intento de modificar el precio se realice mediante el envío de un mensaje específico al objeto, que incluya la nueva información. En este punto, el objeto puede verificar si el nuevo valor cumple con las reglas de validez o si es incorrecto. En caso de ser válido, el objeto procederá a asignar el nuevo valor y almacenar el dato correctamente. Por otro lado, si el valor no es válido, el objeto puede rechazar la asignación y tomar una decisión adecuada según el mecanismo que haya sido establecido, como lanzar una excepción, enviar un mensaje de error o tomar una acción alternativa. 

Este enfoque permite al objeto garantizar que siempre tiene datos válidos y coherentes, ya que tiene el control total sobre la modificación de sus atributos. Asimismo, facilita el mantenimiento del código, ya que las validaciones y la lógica de negocio se concentran dentro del objeto, manteniendo una separación clara de responsabilidades entre objetos. 

Se puede analizar esta característica a través de otro ejemplo. Cada persona tiene una billetera que contiene todos los billetes que posee en un momento dado. Cuando una persona necesita pedir prestado dinero a otra, debe enviarle un mensaje solicitando el préstamo. La persona receptora del mensaje conoce cuánto dinero tiene en su billetera y tiene el derecho de decidir si 

**8. Encapsulamiento** 

**94** 

presta o no, ya que es su propio dinero. Puede responder afirmativamente, negativamente o incluso puede optar por no decir la verdad sobre la disponibilidad de dinero, aunque realmente lo tenga. Esta capacidad de decidir prestar o no es fundamental porque el dinero realmente le pertenece. 

La importancia del encapsulamiento se hace evidente en este escenario. Si no existiera el encapsulamiento, es decir, si cualquier persona pudiera acceder directamente a la billetera de otra, podría tomar prestado dinero sin permiso y sin que el propietario se entere de la operación. Esto desencadenaría dos problemas. En primer lugar, el propietario de la billetera tendría menos dinero, lo que afectaría sus recursos.Pero el problema más significativo es que si el propietario no se diera cuenta de la reducción del dinero, podría tomar decisiones incorrectas al realizar compras o comprometerse con gastos sin saber que su dinero ha disminuido sin autorización. 

Por lo tanto, para mantener la integridad de los datos y preservar la autonomía del objeto dueño de la billetera, se aplica el encapsulamiento. Los objetos ocultan la información sobre cuánto dinero tienen, de manera que no se pueda acceder directamente a su billetera desde otros objetos. La cantidad de dinero en la billetera solo será accesible si otro objeto envía un mensaje preguntando cuánto dinero tiene el propietario. Del mismo modo, si alguien solicita un préstamo, el objeto dueño del dinero decidirá si lo presta o no y nunca permitirá que su cantidad de dinero quede sin control. 

###### **8.2.3 Atributos calculados** 

Por otra parte, el encapsulamiento también brinda al objeto la capacidad de decidir si mostrar o no los datos almacenados en sus atributos cuando otros objetos los consultan. Esto permite que el objeto tenga el control sobre qué información se expone y cómo se presenta, según lo considere conveniente. Asimismo, el objeto puede optar por responder a las consultas calculando los datos a partir de otros atributos disponibles. 

Cuando un objeto recibe un mensaje que consulta un dato específico, no es necesario que el objeto que envía el mensaje sepa si el dato que recibe es simplemente un atributo almacenado o si es calculado en el momento de la consulta. Este enfoque de abstracción oculta los detalles internos de la implementación y permite que el objeto proporcione la información solicitada de una manera coherente y transparente para el objeto solicitante. 

Si por ejemplo un objeto “Círculo” tiene atributos como “radio” y “centro”, 

**8.3. Propiedades** 

**95** 

el mismo podría exponer métodos que simulen tener otros atributos, como “diámetro”, “superficie” y “circunferencia”. Estos atributos calculados podrían obtenerse en el momento de la consulta, basándose en los datos disponibles del círculo. Así una instancia de Circulo podría tener un método llamado diametro() que, en lugar de retornar el valor de un atributo, lo calcule en función del radio disponible. Cuando otro objeto solicita el diámetro del círculo, simplemente accede a este método sin necesidad de saber si el diámetro es un atributo almacenado o si lo calcula en el momento. 

##### **8.3 Propiedades** 

Para implementar el encapsulamiento, una de las formas preferidas es utilizando el decorador @property. Este decorador permite programar los métodos de consulta y asignación, es decir, un método para obtener el valor de un atributo y otro método asociado para asignar un nuevo valor a ese mismo atributo. Cada uno de estos métodos, conocidos como getters (método de consulta) y setters (método de asignación), puede contener la lógica necesaria, tan sencilla o compleja como sea requerida. 

Estos métodos se los decora especificando que conforman un par llamado **propiedad** . Una vez establecidos como propiedades, los objetos clientes pueden utilizar la misma sintaxis que utilizan para acceder a un atributo simple o para asignar un valor a un atributo. De esta manera, el objeto cliente sigue utilizando la sintaxis de atributos, pero en realidad, de forma implícita, se ejecutan los métodos de consulta y asignación correspondientes. Esto permite que el objeto reciba el mensaje de consultar o modificar un atributo sin necesidad de exponer directamente el acceso a sus atributos internos. 

La sintaxis de estos métodos es bastante particular: el método de consulta se define con el nombre de la propiedad, generalmente un sustantivo, y se lo anota con @property. El método de asignación se anota con un decorador que lleva el nombre de la propiedad seguido de .setter, lo que indica que es el método setter asociado a esa propiedad. En el método setter, se recibe como parámetro self, como es habitual en todos los métodos, y el nuevo valor que se intenta asignar al atributo. 

Por ejemplo, en la clase Persona del capítulo anterior, para que esté encapsulado el atributo documento se debería hacer: 

**8. Encapsulamiento** 

**96** 

**class Persona** : **def** __init__(self, documento, nombre, apellido, edad): self._documento = documento self.nombre = nombre self.apellido = apellido self.edad = edad @property **def** documento(self): **return** self._documento @documento.setter **def** documento(self, nuevo_documento): self._documento = nuevo_documento 

Luego, cuando se intenta acceder al atributo documento en realidad se están ejecutando los métodos getter y setter: 

p = Persona(11, "Juan", "Perez", 23) p.documento = 22 _#Ejecuta el método setter_ print(p.documento) _# Ejecuta el getter_ 

En el diagrama de clases, la propiedad se representa como si fuera un atributo público común (documento); el diagrama no distingue si el acceso ocurre a través de una propiedad o de un atributo simple, ya que esa es justamente la idea del encapsulamiento: el cliente de la clase no necesita saberlo. El atributo real que almacena el dato (_documento) es privado. 



##### **8.4 Métodos mágicos** 

En Python, existen métodos que comúnmente se conocen como “métodos mágicos”. Aunque el término “mágicos” puede sonar confuso, estos métodos son efectivamente especiales y poseen características únicas que no se encuentran en otros lenguajes de programación, o que pueden variar de un 

**8.4. Métodos mágicos** 

**97** 

###### lenguaje a otro. 

Lo que distingue a estos métodos es que se invocan de manera implícita, es decir, no se llaman directamente utilizando la sintaxis tradicional de envío de mensajes o llamada a funciones. En lugar de eso, Python proporciona una forma especial de invocar estos métodos, mediante una convención de nomenclatura que los hace reconocibles. Estos métodos son conocidos como “Dunder methods”, una abreviatura de “double underscore methods”, debido a que sus nombres comienzan y terminan con dos guiones bajos (__). 

Un ejemplo conocido de un método “mágico” es __init__, que se utiliza como el constructor de una clase. Cuando se crea una instancia de una clase en Python, el método __init__ se llama de forma implícita para inicializar los atributos y configurar el objeto. No es necesario invocarlo manualmente con su nombre ya que Python lo hace automáticamente al crear un objeto de la clase. 

Un aspecto interesante de estos métodos mágicos es que permiten que las clases personalicen su comportamiento en ciertos contextos. Por ejemplo, el método __str__ se utiliza para definir cómo se debe representar una instancia de una clase como una cadena de caracteres cuando se utiliza la función str(). Al definir este método en una clase, se puede controlar cómo se verá una instancia de esa clase cuando se imprima o se convierta en una cadena. 

Estos métodos mágicos desempeñan un papel crucial en la programación orientada a objetos al proporcionar la capacidad de personalizar el comportamiento de las clases y los objetos creados a partir de ellas. Estos métodos son necesarios debido a la distinción fundamental entre los objetos creados a partir de una clase y los tipos de datos simples o primitivos que ofrece el lenguaje, como números, booleanos y cadenas. 

En Python, los tipos de datos simples pueden participar en operaciones gracias a los operadores. Por ejemplo, los operadores de comparación permiten comparar dos números o dos cadenas, y las operaciones aritméticas aplicadas a números realizan cálculos aritméticos. Sin embargo, cuando se crean clases y se instancian objetos a partir de ellas, estos objetos no tienen la capacidad inherente de realizar operaciones entre ellos como la suma o la comparación de igualdad de sus valores. 

Cuando se comparan por igualdad dos objetos, se obtiene simplemente un valor de verdad que indica si ambas referencias se refieren al mismo objeto o instancia. Sin embargo, no existe una forma natural de realizar comparaciones como “mayor que” o “menor que” entre objetos de una clase, 

**8. Encapsulamiento** 

**98** 

ya que esta lógica no está definida de manera predeterminada para la mayoría de las clases personalizadas. 

Con estos métodos se permite a los programadores agregar lógica específica a sus clases para habilitar operaciones personalizadas entre objetos de la misma clase. Por ejemplo, al definir los métodos __lt__ (menor que) y __gt__ (mayor que) en una clase, se puede personalizar cómo se deben comparar los objetos de esa clase en función de sus atributos internos. O, por ejemplo, con __add__ para la suma, se consigue que los objetos realicen operaciones aritméticas personalizadas. 

###### **8.4.1 Método __str__** 

El método __str__ es un componente fundamental en la programación orientada a objetos en Python. Este método se utiliza para proporcionar una representación en forma de cadena del estado interno de un objeto. Su lógica radica en mostrar, en formato de cadena, todos o algunos de los valores almacenados en los atributos del objeto. En otros lenguajes de programación, como Java o C#, este concepto se implementa mediante un método llamado toString, o el método asString de SmallTalk. 

La ventaja de definir el método str con este nombre especial, con guiones bajos dobles (__str__), es que permite que Python realice conversiones implícitas del objeto a una cadena en diversas situaciones. Por ejemplo, cuando se utiliza la función print, esta puede recibir como parámetro una instancia de una clase definida por el usuario. En este caso, la función print invocará automáticamente al __str__ del objeto y mostrará por pantalla la representación que el objeto decide proporcionar de sí mismo en formato de cadena. 

###### **8.4.2 Métodos de comparación** 

La capacidad de comparar objetos de manera personalizada es esencial para la aplicación de lógicas específicas relacionadas con la igualdad, desigualdad y otros criterios de comparación. 

Un ejemplo de estos métodos especiales es __eq__, que se utiliza para la comparación por igualdad. La lógica subyacente en este método es la de determinar si un objeto es igual a otro en función de los criterios definidos por el programador. Por ejemplo, en el contexto de una clase Persona, se lo podría programar para que devuelva True si todos los atributos de dos objetos Persona tienen el mismo valor. Esta lógica personalizada reflejaría la 

**8.4. Métodos mágicos** 

**99** 

definición específica de igualdad para objetos de esta clase en el contexto de la aplicación. 

Es importante enfatizar que Python no puede adivinar automáticamente cómo se deben comparar objetos personalizados. La razón detrás de esto es que la comparación entre objetos puede depender de lógicas de negocio específicas y variar ampliamente de una aplicación a otra. Por lo tanto los programadores deben proporcionar esta lógica de comparación personalizada en los métodos especiales correspondientes. 

Además existen otros métodos especiales, como __ne__ para la desigualdad, __lt__ para “menor que”, __gt__ para “mayor que”, __le__ para “menor o igual que” y __ge__ para “mayor o igual que”. Cada uno de estos métodos permite a los objetos de una clase personalizada participar en comparaciones utilizando los operadores correspondientes. 

###### **8.4.3 Métodos aritméticos** 

Considerando una clase que represente un concepto matemático, por ejemplo una Fracción, tiene sentido aplicar operaciones aritméticas sobre fracciones, tales como sumarlas o multiplicarlas. Un método especial que podría ser relevante en este contexto es __add__, que se utiliza para sobrecargar el operador de suma (+). Al programar este método dentro de la clase Fraccion, se le proporciona la capacidad de sumar dos instancias de fracciones. La lógica subyacente en el método determina cómo se realiza esta suma y qué significa en el contexto del dominio en el que se va a usar la clase. 

A continuación se presenta una posible implementación de la clase Fraccion y de la sobrecarga de los operadores de adición y multiplicación: 

**from math import** gcd **class Fraccion** : **def** __init__(self, numerador, denominador): _# Simplificamos la fracción al máximo común divisor_ divisor_comun = gcd(numerador, denominador) self.numerador = numerador //) divisor_comun self.denominador = denominador //) divisor_comun 

**def** __str__(self): **return** f' **{** self.numerador **}** / **{** self.denominador **}** ' **def** __add__(self, otra_fraccion): _# Suma de fracciones: (a/b) + (c/d) = (ad + bc) / bd_ nuevo_numerador = (self.numerador * otra_fraccion.denominador) + \ (otra_fraccion.numerador * self.denominador) 

**8. Encapsulamiento** 

**100** 

nuevo_denominador = self.denominador * otra_fraccion.denominador **return** Fraccion(nuevo_numerador, nuevo_denominador) **def** __mul__(self, otra_fraccion): _# Multiplicación de fracciones: (a/b) * (c/d) = (ac) / (bd)_ nuevo_numerador = self.numerador * otra_fraccion.numerador nuevo_denominador = self.denominador * otra_fraccion.denominador **return** Fraccion(nuevo_numerador, nuevo_denominador) _# Crear dos objetos Fraccion_ frac1 = Fraccion(1, 2) frac2 = Fraccion(3, 4) _# Sumar dos fracciones usando el operador +_ suma = frac1 + frac2 print(f'Suma: **{** frac1 **}** + **{** frac2 **}** = **{** suma **}** ') _# Multiplicar dos fracciones usando el operador *_ producto = frac1 * frac2 print(f'Multiplicación: **{** frac1 **}** * **{** frac2 **}** = **{** producto **}** ') 

En este ejemplo, se definió la clase Fraccion para representar números fraccionarios y se sobrecargaron los operadores + y * para que realicen la suma y multiplicación de fracciones según las reglas matemáticas correspondientes. La simplificación de fracciones se realiza en el constructor utilizando el máximo común divisor. 



Con estos métodos, al crear dos objetos Fraccion (frac1 y frac2) se pueden usar los operadores + y * para realizar operaciones aritméticas con fracciones de manera más clara e intuitiva que invocando métodos con nombre. 

### **Composición** 

##### **9.1 Introducción** 

La composición es un principio fundamental que se utiliza para crear objetos complejos al combinar o componer a partir de objetos más simples. La composición es un tipo de relación entre clases en la que un objeto se compone de otros objetos como sus partes constituyentes. 

La composición se basa en la idea de que un objeto puede tener referencias a otros objetos como sus atributos, y puede utilizar sus métodos para realizar acciones específicas. 

##### **9.2 Cardinalidad** 

Dependiendo de la cantidad de objetos involucrados en una relación de composición, la implementación puede variar sensiblemente. Si la cardinalidad es 0, 1 o alguna cantidad constante, puede implementarse mediante el uso de referencias simples, de forma tal que en la clase compuesta existan atributos cuyo tipo sea el de la clase contenida. Por ejemplo, en una clase que represente un partido de algún deporte de equipos, puede plantearse que un objeto de la clase Partido, estará compuesto de dos (y únicamente dos) instancias de la clase Equipo. 

Cuando la cardinalidad indica que el objeto compuesto se relaciona con una cantidad grande, variable o desconocida de objetos de la clase relacionada, la implementación se orienta a disponer de una colección de objetos. 

101 

**9. Composición** 

**102** 

Siguiendo con el ejemplo anterior, un equipo estará compuesto de muchos jugadores, por lo tanto la clase Equipo puede tener un atributo de tipo lista o diccionario que almacene instancias de la clase Jugador. 

##### **9.3 Implementación** 

Para implementar composición en Python se puede plantear un esquema similar al siguiente: 

- En la clase Contenedora agregar un atributo de alguno de los tipos de colección. 

- En el constructor de la clase contenedora no recibir un parámetro para asignar la colección, únicamente debe ser instanciada vacía. 

- No agregar métodos de asignación y consulta para la colección. 

- Agregar un método de agregado a la colección, que reciba como parámetro una instancia de la clase Contenida. 

- Todas las responsabilidades que involucren a la colección, deben ser programadas como métodos en la clase Contenedora. 

##### **9.4 Composición vs. Agregación** 

Dentro de las relaciones “todo/parte” (donde un objeto se compone de otros), UML distingue dos variantes según la fuerza del vínculo entre el objeto contenedor y los objetos contenidos: **composición** y **agregación** . Ambas se representan en el diagrama de clases con una línea terminada en un rombo del lado de la clase contenedora, pero el rombo se dibuja **relleno** en la composición y **vacío** (blanco) en la agregación. 

###### **9.4.1 Ciclo de vida** 

La diferencia semántica fundamental entre ambas relaciones está en el ciclo de vida de los objetos contenidos: 

- **Composición (rombo relleno):** el objeto contenido pertenece exclusivamente a un único contenedor y su ciclo de vida está atado al de este. El contenedor es responsable de crear (y, conceptualmente, destruir) a sus partes. Si el objeto contenedor deja de existir, sus partes dejan de tener sentido y no pueden ser reutilizadas por otro contenedor. Por 

**9.4. Composición vs. Agregación** 

**103** 

ejemplo, los ítems de una factura existen únicamente en el contexto de esa factura: no tiene sentido que un ItemFactura sea compartido entre dos facturas distintas, ni que sobreviva a la eliminación de la factura que lo contiene. 

- **Agregación (rombo vacío):** el objeto contenido tiene existencia propia, independiente del contenedor, y puede ser compartido simultáneamente por varios contenedores. El contenedor simplemente mantiene una referencia a objetos que existen (y pueden seguir existiendo) por fuera de él. Por ejemplo, un Profesor puede pertenecer a la colección de docentes de una Universidad, pero el profesor existe independientemente de esa universidad: podría dictar clases en otra institución, o la universidad podría cerrar sin que eso implique la desaparición del profesor. 

###### **9.4.2 Pertenencia y movilidad** 

El criterio del ciclo de vida (¿sobrevive la parte a la destrucción del todo?) es la consecuencia más visible de la distinción entre composición y agregación, pero no es la pregunta más profunda que hay que hacerse al modelar. La pregunta de fondo es otra: **¿tiene sentido que este objeto exista fuera de esta relación particular, y pueda eventualmente pasar a formar parte de otro contenedor?** 

En una **agregación** , la respuesta es sí: el objeto contenido tiene una identidad y un rol que trascienden a cualquier contenedor específico, y por lo tanto puede _migrar_ de un contenedor a otro a lo largo de su vida –e incluso puede atravesar períodos en los que no pertenece a ninguno–. El caso de un Jugador y un Equipo es paradigmático: un jugador puede ser transferido de un equipo a otro, y en el ínterin puede quedar como agente libre, sin equipo, sin que eso sea contradictorio ni deje al jugador “sin sentido”. El jugador es jugador independientemente de para quién juegue en un momento dado. En una **composición** , en cambio, la respuesta es no: el objeto contenido no tiene un rol propio por fuera del contenedor que lo define, y por lo tanto no tiene sentido que “migre” a otro. No es solamente que no _convenga_ moverlo: es que la pregunta “¿a qué otro contenedor podría pasar este objeto?” ni siquiera está bien planteada, porque la identidad del objeto está constituida por su pertenencia a ese contenedor específico. Un ejemplo que lleva esta idea al extremo es el de un campeonato deportivo, compuesto de fechas, las cuales a su vez están compuestas de partidos: 

**9. Composición** 

**104** 



<!-- Start of picture text -->
© twin<br>ee S<br>© fichar(jugador) es<br>© Liberar(jugador)<br>Un Jugador puede ser transferido de N<br>un Equipo a otro, o quedar libre<br>temporalmente sin ninguno.<br>© caveat rc) °<br>| oy cms] TSlocalatte»: Equi Eu<br>ee |<br>los contiene ni pueden pasar a<br><!-- End of picture text -->

Un Partido no puede “despegarse” de la Fecha en la que fue programado y pasar a integrar otra fecha, ni siquiera de otro campeonato: su identidad –qué partido es– está definida en términos de esa fecha y ese campeonato particulares (“el partido entre tal fecha del torneo tal”). Lo mismo ocurre con la Fecha respecto del Campeonato. Nótese que esto es compatible con que Partido tenga, a su vez, una relación de _agregación_ hacia Equipo (sección anterior): los equipos que juegan un partido sí tienen existencia propia y pueden participar en otros partidos, campeonatos, etc. Una misma clase puede entonces participar simultáneamente como “parte agregada” de una relación y como “contenedor compuesto” de otra, y es perfectamente normal que dentro de un mismo modelo convivan ambos tipos de vínculo en cadenas distintas. 

Con este criterio en mente, el ciclo de vida deja de ser un dato arbitrario y se explica por sí solo: si un objeto no tiene identidad ni sentido fuera de un contenedor específico (composición), es razonable que su existencia termine cuando termina la de su contenedor. Si, en cambio, un objeto tiene identidad propia y puede pertenecer a distintos contenedores a lo largo del 

**9.4. Composición vs. Agregación** 

**105** 

tiempo (agregación), es igual de razonable que sobreviva a la destrucción de cualquiera de ellos en particular. 

Como regla práctica para clasificar una relación “todo/parte” al modelar, conviene hacerse dos preguntas: 

1. **¿Podría el objeto contenido pasar, en algún momento de su vida, a formar parte de** **_otro_ contenedor del mismo tipo?** Si la respuesta es sí (aunque sea una posibilidad poco frecuente), se trata de una agregación. 

2. **¿Tiene sentido preguntarse por la existencia del objeto contenido** **_sin_ hacer referencia a ningún contenedor?** Si la respuesta es sí –el objeto se puede describir y tiene identidad por sí mismo–, también apunta a una agregación. 

Si ambas respuestas son negativas, la relación es una composición: el objeto contenido está definido _en función de_ su contenedor, no simplemente _alojado dentro de_ él. 

###### **9.4.3 Diagrama de clases** 

El siguiente diagrama contrasta ambas notaciones sobre los mismos conceptos genéricos de “contenedor” y “contenida”: 



<!-- Start of picture text -->
| a0) |<br>1,,+ | composicién agregaciin<br>OF<br>© producto : str<br>© cantidador: int<br>|<br>|<br>Rombo relleno: si se elimina la AS Rombo vacio: un Profesor existe K<br><!-- End of picture text -->

**9. Composición** 

**106** 

###### **9.4.4 Implementación** 

Esta distinción conceptual de UML no tiene, en Python, una traducción sintáctica diferenciada: en ambos casos la clase contenedora simplemente guarda una referencia (o una colección de referencias) a instancias de la clase contenida, tal como se describió en la sección anterior. Python tampoco ofrece una forma directa de expresar “este objeto es responsable de destruir a sus partes”, ya que la memoria se gestiona mediante recolección de basura por conteo de referencias: un objeto permanece vivo mientras exista al menos una referencia hacia él, sin importar si esa referencia proviene de una relación de composición o de agregación. 

Por lo tanto, la diferencia entre composición y agregación en Python es principalmente una decisión de **diseño y de documentación del modelo** , más que una restricción que el lenguaje imponga en tiempo de ejecución: 

- En una composición, la convención (ya presentada en la sección 9.3) es que la clase contenedora sea la única responsable de instanciar los objetos contenidos –generalmente dentro de un método de agregado como agregar_libro– y de no exponer métodos que permitan que otro objeto externo inserte referencias arbitrarias o “robe” una parte de otro contenedor. 

- En una agregación, en cambio, es habitual que el método de agregado reciba una instancia ya creada por fuera (por ejemplo, universidad. agregar_profesor(profesor), donde profesor fue instanciado independientemente y podría agregarse también a otra_universidad). 

La misma lógica de diseño se aplica, en espejo, a los métodos que **remueven** un objeto de la colección. La pregunta relevante es qué le entrega el método a quien lo invoca: 

- En una **agregación** , el método de borrado puede devolver el objeto removido sin ningún problema. Como ese objeto tiene existencia propia, entregar una referencia a él es precisamente lo que permite que se lo reasigne a otro contenedor –por ejemplo, jugador = equipo_origen.liberar(nombre) seguido de equipo_destino.fichar(jugador)–. Devolver el objeto es lo que hace posible, en código, la migración a otro contenedor. 

- En una **composición** , el método de borrado _no debería_ devolver el objeto removido. Hacerlo equivaldría a entregarle a quien llama al método 

**9.4. Composición vs. Agregación** 

**107** 

una referencia utilizable a una parte que, por definición, no tiene sentido fuera de ese contenedor –y que podría terminar insertada en otro contenedor del mismo tipo, violando la exclusividad que define a la composición–. Como mucho, el método puede devolver un valor booleano que confirme si el borrado se realizó, o no devolver nada. 

Esta asimetría en la firma de los métodos de borrado es, en Python, la contraparte exacta de la asimetría semántica: no es una regla que el lenguaje imponga, sino una convención de diseño que el programador debe respetar para que el código sea consistente con el modelo que representa. 

Los siguientes fragmentos contrastan ambos casos. Primero, una agregación entre Equipo y Jugador, donde liberar devuelve el jugador removido, habilitando su transferencia a otro equipo: 

**class Jugador** : **def** __init__(self, nombre): self.nombre = nombre **class Equipo** : **def** __init__(self, nombre): self.nombre = nombre self.jugadores = [] **def** fichar(self, jugador): self.jugadores.append(jugador) **def** liberar(self, nombre): coincidencias = list(j **for** j **in** self.jugadores **if** j.nombre ==) nombre) **if** coincidencias: jugador = coincidencias[0] self.jugadores.remove(jugador) **return** jugador _# El jugador migra de un equipo a otro_ equipo1 = Equipo("Deportivo Buenaventura") equipo2 = Equipo("Heladeros Fútbol Club") goleador = Jugador("Perez") equipo1.fichar(goleador) _# Más adelante_ goleador = equipo1.liberar("Perez") **if** goleador: equipo2.fichar(goleador) 

En contraste, en la composición entre Biblioteca y Libro, un eventual método quitar_libro no devuelve el libro removido, ya que no existe ningún contenedor legítimo al que ese libro debiera poder pasar a continuación: 

**9. Composición** 

**108** 

**class Biblioteca** : **def** __init__(self): self.libros = [] **def** agregar_libro(self, libro): self.libros.append(libro) **def** quitar_libro(self, libro): self.libros.remove(libro) _# No se retorna el libro: su ciclo de vida termina aquí, # no tiene sentido que pase a integrar otra Biblioteca._ 

##### **9.5 Cardinalidad** 

###### **9.5.1 Cardinalidad constante** 

Cuando la cardinalidad de la relación es 0, 1 o una cantidad fija, la composición se implementa con referencias simples: un atributo de la clase compuesta almacena directamente la instancia (o instancias) de la clase contenida, sin necesidad de una colección. 

Retomando el ejemplo de un partido de un deporte de equipos, un objeto Partido está compuesto exactamente por dos instancias de la clase Equipo. Esto puede implementarse de la siguiente manera: 



**class Equipo** : **def** __init__(self, nombre): self.nombre = nombre **class Partido** : **def** __init__(self, local, visitante): self.local = local self.visitante = visitante **def** describir(self): print(f" **{** self.local.nombre **}** vs **{** self.visitante.nombre **}** ") 

_# Crear equipos_ equipo1 = Equipo("Boca Juniors") equipo2 = Equipo("River Plate") 

**9.5. Cardinalidad** 

**109** 

_# Crear un partido entre ambos equipos_ partido = Partido(equipo1, equipo2) partido.describir() 

A diferencia del esquema de composición con colecciones, en este caso los atributos local y visitante son recibidos y asignados directamente en el constructor, ya que la cardinalidad de la relación es fija y conocida de antemano (siempre son exactamente dos equipos). 

###### **9.5.2 Cardinalidad variable** 

Suponiendo una relación de composición entre las clases Biblioteca y Libro, estableciendo que una biblioteca está compuesta de 0 o más libros, se puede plantear la siguiente implementación: 



**class Libro** : **def** __init__(self, titulo, autor): self.titulo = titulo self.autor = autor **class Biblioteca** : **def** __init__(self): self.libros = [] **def** agregar_libro(self, libro): self.libros.append(libro) **def** mostrar_libros(self): **for** libro **in** self.libros: print(f"Título: **{** libro.titulo **}** , Autor: **{** libro.autor **}** ") _# Crear libros_ libro1 = Libro("El Gran Gatsby", "F. Scott Fitzgerald") libro2 = Libro("Cien Años de Soledad", "Gabriel García Márquez") _# Crear una biblioteca y agregar libros_ biblioteca = Biblioteca() biblioteca.agregar_libro(libro1) biblioteca.agregar_libro(libro2) _# Mostrar los libros en la biblioteca_ biblioteca.mostrar_libros() 

### **Herencia** 

##### **10.1 Introducción** 

La herencia es un concepto fundamental en la programación orientada a objetos que establece una relación esencial entre clases. Este mecanismo se aplica cuando existen clases que, aunque comparten similitudes notables, no son lo suficientemente idénticas como para ser consideradas como una única clase. En esta situación, la herencia entra en juego para vincular estas clases de manera que los objetos pertenecientes a ambas puedan ser utilizados de manera equivalente, como si efectivamente fueran instancias de la misma clase. 

El proceso de herencia posibilita la creación de una nueva clase basada en una clase preexistente, sin la necesidad de duplicar y repetir el código de la clase original. De esta manera, se evita la tarea de copiar y pegar la implementación de una clase para crear una nueva, lo que redundaría en un mantenimiento engorroso y potencialmente propenso a errores. 

La herencia implica que una clase derivada (o subclase) hereda propiedades y métodos de una clase base (o superclase). La subclase puede agregar nuevas funcionalidades o modificar las existentes, pero también hereda la estructura y el comportamiento de la superclase. 

Esto es útil porque permite organizar y abstraer el código de manera eficiente. Por ejemplo, si se está desarrollando un programa para modelar vehículos, se podría tener una clase base llamada “Vehículo” con propiedades y métodos genéricos como “acelerar” y “frenar”. Luego, se pueden crear 

111 

**10. Herencia** 

**112** 

subclases tales como “Automóvil” y “Motocicleta” que heredan estas características básicas y agregan sus propias particularidades, ya sea agregando nuevos atributos y métodos o modificando métodos heredados brindando una implementación específica para sus responsabilidades y necesidades. 

En síntesis, la herencia permite tratar uniformemente a objetos de distintas clases relacionadas, evitando la duplicación de código y favoreciendo la reutilización de estructura y comportamiento común. 

##### **10.2 “Es un”** 

El concepto de la herencia en la programación orientada a objetos se manifiesta mediante la capacidad de definir una clase a partir de otra, estableciendo una relación específica entre ellas. En este contexto, una de las clases involucradas se denomina **clase base** , mientras que la otra se conoce como **clase derivada** . 

La clase derivada puede conceptualizarse como un caso especial o una variante de la clase base, lo que implica que todos los objetos pertenecientes a la clase derivada pueden ser considerados como objetos de la clase base. Esta relación se expresa de manera precisa con la afirmación: “un objeto de la clase derivada ES UN objeto de la clase base”. En general, es una práctica útil verificar las relaciones de herencia con esa frase: si la frase no tiene sentido, generalmente es síntoma de que las clases no deben estar relacionadas o lo hacen pero por otro tipo de relación. 

Por ejemplo: 

**Clase base Cliente y Clase derivada ClienteOnline** En este contexto, afirmar que “un cliente online ES UN cliente” es totalmente válido. La clase derivada ClienteOnline representa una variante específica de la clase base Cliente, pero todos los clientes en línea son, en última instancia, clientes en sí mismos. 

**Clase base Auto y Clase derivada Rueda** La afirmación “una rueda ES UN auto” es inevitablemente incorrecta, como también lo es “un auto ES UNA rueda”. Esta situación pone en evidencia que tales clases no pueden estar relacionadas mediante herencia. Sin embargo, pueden estar relacionadas mediante algún otro tipo de relación, por caso, composición. 

**10.3. Implementación** 

**113** 

El siguiente diagrama contrasta ambos casos: a la izquierda, una relación de herencia válida (Cliente / ClienteOnline); a la derecha, una relación que no debe modelarse con herencia (Auto / Rueda no superan la prueba “ES UN”), sino con composición. 



##### **10.3 Implementación** 

###### **10.3.1 Bloque class** 

Para implementar herencia en Python no se agregan muchos elementos sintácticos, en general las clases se redactan de una forma bastante similar a aquellas no involucradas en este tipo de relación. 

En la clase base no se debe realizar ninguna modificación si se identifica la necesidad de una clase derivada. En la clase derivada se indica en la cabecera del bloque class, a continuación del nombre de la misma, el nombre de la clase base encerrado entre paréntesis. Retomando el ejemplo de Cliente y ClienteOnline de la sección anterior: 

**class ClienteOnline** (Cliente): 

**10. Herencia** 

**114** 

###### **10.3.2 Función super** 

A diferencia de self, que es un parámetro que cada método recibe automáticamente al ser invocado sobre una instancia, super **no es una referencia** disponible de antemano en el entorno del método, sino una función incorporada del lenguaje. Esto no tiene nada que ver con una herencia implícita desde alguna clase raíz, Python no expone super como un miembro que las instancias reciban por el solo hecho de pertenecer a una jerarquía de herencia, sino como una función del lenguaje que hay que llamar explícitamente, con paréntesis, cada vez que se la necesita. 

Al invocarla sin argumentos dentro de un método de una clase derivada , super() construye y devuelve un objeto **proxy** : un objeto que no almacena datos propios, sino que delega la búsqueda de los miembros solicitados hacia la clase base, permitiendo acceder a los miembros heredados sin necesidad de nombrar explícitamente a dicha clase base. 

Esta diferencia con self también explica una asimetría sintáctica que suele generar dudas: self nunca se “llama” –ya está ahí, recibido como parámetro–, mientras que super() sí se llama, precisamente porque es una función y no una referencia. 

La función super() es ocasionalmente utilizada de forma errónea para acceder a cualquier miembro declarado en la clase base. Esto evidencia una notoria ignorancia del concepto de la herencia: todo miembro de la clase base es heredado y por lo tanto accesible mediante la referencia self. 

El uso de super() debe focalizarse en un único escenario: cuando se sobreescribió un método en la clase derivada y se necesita invocar la versión del mismo método definida en la clase base. Este es el caso del método __init__, que al ser redefinido en la derivada no se ejecuta automáticamente, por lo que es necesario invocarlo explícitamente con super() para completar la inicialización. Pero también aplica a cualquier otro método que haya sido redefinido, como __str__, donde super().__str__() permite reutilizar la representación textual de la clase base y extenderla con nuevos atributos. Si en cualquiera de estos casos se intentara invocar el método con self desde dentro de la propia redefinición, se iniciaría una llamada recursiva; super() permite, en cambio, acceder a la versión original sin recursión. 

La **redefinición** de un método (también llamada _override_ ) consiste en que una clase derivada reimplemente un método ya definido en su clase base para darle un comportamiento propio o especializado. Es, junto con el constructor, 

**10.3. Implementación** 

**115** 

el otro escenario habitual en el que super resulta indispensable: permite que la redefinición, además de su propio agregado, siga apoyándose en la implementación original de la base sin caer en una llamada recursiva sobre sí misma. La redefinición es una técnica central en el trabajo conjunto entre herencia y polimorfismo, y es en el capítulo de Polimorfismo donde se la trata y aplica en detalle. 

###### **10.3.3 Constructor** 

El método constructor de cada clase generalmente recibe parámetros para asignar valores iniciales a los atributos. Cuando se programa un constructor en una clase derivada, el caso más usual es el de recibir parámetros para inicializar los atributos de la propia clase y también los heredados. 

A continuación el constructor de la derivada puede realizar una invocación explícita al constructor de la clase base a través de super. Es importante notar que los parámetros que recibe el constructor de la derivada normalmente **no** coinciden exactamente con los que se le reenvían a la base: la derivada suele recibir, además de los parámetros que la base necesita, otros propios para inicializar sus atributos adicionales, y es responsabilidad de la derivada seleccionar cuáles de ellos le corresponden a super().__init__(). 

Retomando y completando el ejemplo de Cliente y ClienteOnline, y agregando además una segunda clase derivada, ClientePresencial: 

**class Cliente** : **def** __init__(self, nombre): self.nombre = nombre **class ClienteOnline** (Cliente): **def** __init__(self, nombre, email): _# nombre se reenvía tal cual a la base; email es un # parámetro propio de ClienteOnline, que Cliente desconoce._ super().__init__(nombre) self.email = email **class ClientePresencial** (Cliente): **def** __init__(self, nombre, domicilio, sucursal_preferida): _# domicilio y sucursal_preferida tampoco existen en Cliente: # son propios de un cliente que opera en una sucursal física, # probablemente la más cercana a su domicilio._ super().__init__(nombre) self.domicilio = domicilio self.sucursal_preferida = sucursal_preferida _# Crear un cliente online_ cliente1 = ClienteOnline("Ana Gómez", "ana.gomez@correo.com") 

**10. Herencia** 

**116** 

_# Crear un cliente presencial_ cliente2 = ClientePresencial("Beto Ruiz", "Av. Gutierrez 742", "Sucursal Centro") 



<!-- Start of picture text -->
—<br>© cites —i n _d e lenteOniine invocaa e<br>eal)email: str SePeinicializar tD _ t_ tnombre)para © donicitio : str<br>el aributo heredado nombre.<br>a — |<br><!-- End of picture text -->

### **Polimorfismo** 

##### **11.1 Introducción** 

###### **11.1.1 Concepto** 

El polimorfismo es un principio fundamental de la programación orientada a objetos que permite que objetos de diferentes clases sean tratados como objetos de una clase común. Esta característica facilita que un mismo método pueda comportarse de manera diferente según el tipo específico del objeto que lo recibe, proporcionando flexibilidad y extensibilidad al código. 

El término “polimorfismo” deriva del griego y significa “muchas formas”, lo cual describe precisamente su naturaleza: un mismo nombre de método puede tener múltiples implementaciones según la clase que lo contenga. En el contexto de la herencia, el polimorfismo se manifiesta cuando las clases derivadas redefinen métodos heredados de la clase base, proporcionando implementaciones específicas que se ajusten a sus particulares necesidades y características. 

###### **11.1.2 Sobreescritura de métodos** 

La sobreescritura de métodos es el mecanismo mediante el cual una clase derivada proporciona una implementación específica de un método que ya existe en su clase base. En Python, la sintaxis para sobreescribir un método es extremadamente sencilla: simplemente se define un método en la clase derivada con el mismo nombre que el método de la clase base que se desea redefinir. 

117 

**11. Polimorfismo** 

**118** 

No se requieren palabras clave especiales ni anotaciones adicionales. 



**class Vehiculo** : **def** acelerar(self): print("El vehículo está acelerando") **def** describir(self): print("Este es un vehículo genérico") **class Automovil** (Vehiculo): **def** acelerar(self): print("El automóvil acelera suavemente") **def** describir(self): print("Este es un automóvil con cuatro ruedas") **class Motocicleta** (Vehiculo): **def** acelerar(self): print("La motocicleta acelera rápidamente") 

El verdadero efecto del polimorfismo se aprecia cuando un mismo fragmento de código trata a objetos de distintas clases derivadas de manera uniforme, sin necesidad de saber con cuál de ellas está tratando en cada caso. Alcanza con saber que todos son Vehiculo para poder invocar acelerar() sobre cualquiera; la implementación que efectivamente se ejecuta depende del tipo concreto de cada objeto: 

vehiculos = [Automovil(), Motocicleta()] **for** vehiculo **in** vehiculos: vehiculo.acelerar() 

**11.1. Introducción** 

**119** 

Aunque el código del **for** es exactamente el mismo para los dos elementos de la lista –vehiculo.acelerar()–, el mensaje se envía en cada vuelta del ciclo hacia la implementación correspondiente a la clase real del objeto: la de Automovil en la primera iteración, la de Motocicleta en la segunda. Esto es lo que distingue al polimorfismo de simplemente “tener cada clase su propio método”: lo relevante no es que existan varias implementaciones, sino que el código que las invoca puede ser único e ignorar por completo cuál de ellas se va a ejecutar. 

###### **11.1.3 Uso de super** 

El método especial __str__ es particularmente útil para demostrar el uso de super() en el contexto del polimorfismo, ya que frecuentemente es necesario extender la representación de cadena de la clase base en lugar de reemplazarla completamente. 

Cuando se sobreescribe el método __str__ en una clase derivada, es común utilizar super() para invocar la implementación de la clase base y luego agregar información específica de la clase derivada. Esto permite construir representaciones de cadena más completas y jerárquicas. 



<!-- Start of picture text -->
J S<br>~)_ Yagrega su propia informacién.<br><!-- End of picture text -->

**class Persona** : **def** __init__(self, nombre, edad): self.nombre = nombre self.edad = edad **def** __str__(self): **return** f"Persona: **{** self.nombre **}** , **{** self.edad **}** años" **class Estudiante** (Persona): **def** __init__(self, nombre, edad, carrera): 

**11. Polimorfismo** 

**120** 

super().__init__(nombre, edad) self.carrera = carrera **def** __str__(self): **return** f" **{** super().__str__() **}** , Carrera: **{** self.carrera **}** " **class Profesor** (Persona): **def** __init__(self, nombre, edad, materia): super().__init__(nombre, edad) self.materia = materia **def** __str__(self): **return** f" **{** super().__str__() **}** , Materia: **{** self.materia **}** " 

En este ejemplo, las clases Estudiante y Profesor extienden la representación de cadena de la clase Persona agregando información específica. El uso de super().__str__() permite reutilizar la lógica de la clase base y evitar la duplicación de código. 

##### **11.2 Clases y métodos abstractos** 

###### **11.2.1 Concepto** 

Una clase abstracta es aquella que no puede ser instanciada directamente y que generalmente contiene uno o más métodos abstractos. Los métodos abstractos son declaraciones de métodos que deben ser implementados obligatoriamente por las clases derivadas, pero que no poseen implementación en la clase base. 

Las clases abstractas sirven como plantillas o contratos que definen qué métodos deben implementar las clases derivadas, garantizando así una interfaz común entre diferentes implementaciones. Esto es especialmente útil cuando se desea definir un comportamiento común pero la implementación específica varía según cada subclase. 

###### **11.2.2 Uso del Decorador @abstractmethod** 

Python proporciona el módulo abc (Abstract Base Classes) para implementar clases y métodos abstractos. Para crear un método abstracto, se utiliza el decorador @abstractmethod y la clase debe heredar de ABC. 

**11.2. Clases y métodos abstractos** 

**121** 



**from abc import** ABC, abstractmethod **class Figura** (ABC): **def** __init__(self, nombre): self.nombre = nombre @abstractmethod **def** calcular_area(self): **pass** @abstractmethod **def** calcular_perimetro(self): **pass def** describir(self): **return** f"Figura: **{** self.nombre **}** " **class Rectangulo** (Figura): **def** __init__(self, ancho, alto): super().__init__("Rectángulo") self.ancho = ancho self.alto = alto **def** calcular_area(self): **return** self.ancho * self.alto **def** calcular_perimetro(self): **return** 2 * (self.ancho + self.alto) **class Circulo** (Figura): **def** __init__(self, radio): super().__init__("Círculo") self.radio = radio 

**11. Polimorfismo** 

**122** 

**def** calcular_area(self): **return** 3.14159 * self.radio **) 2 **def** calcular_perimetro(self): **return** 2 * 3.14159 * self.radio 

Si se intenta instanciar la clase Figura directamente o crear una subclase que no implemente todos los métodos abstractos, Python generará un error **TypeError** . Esto garantiza que todas las clases derivadas cumplan con el contrato establecido por la clase abstracta. 

##### **11.3 Interfaces** 

###### **11.3.1 Implementación** 

Las interfaces definen un conjunto de métodos que una clase debe implementar, sin proporcionar la implementación de dichos métodos. En UML, las interfaces se representan como contratos que especifican qué servicios debe proporcionar una clase, pero no cómo debe proporcionarlos. 

Aunque Python no tiene una palabra clave específica para interfaces como otros lenguajes, se pueden implementar utilizando clases abstractas que contengan únicamente métodos abstractos. Esta aproximación permite replicar el concepto de interfaces de UML en Python. 

El verdadero valor de una interfaz no aparece cuando la implementa una sola clase, sino cuando la implementan varias clases que **no tienen ninguna otra relación entre sí** –no comparten una clase base común más allá de la interfaz, ni pertenecen al mismo dominio conceptual–. Lo único que las vincula es haberse comprometido con el mismo contrato, y eso alcanza para que un tercero pueda tratarlas de manera uniforme sin conocer su tipo concreto. 

**11.3. Interfaces** 

**123** 



**from abc import** ABC, abstractmethod **class INotificable** (ABC): @abstractmethod **def** notificar(self, mensaje): **pass class ServicioEmail** (INotificable): **def** __init__(self, direccion): self.direccion = direccion **def** notificar(self, mensaje): print(f"Enviando email a **{** self.direccion **}** : **{** mensaje **}** ") **class ServicioSMS** (INotificable): **def** __init__(self, numero): self.numero = numero **def** notificar(self, mensaje): print(f"Enviando SMS al **{** self.numero **}** : **{** mensaje **}** ") **class Impresora** (INotificable): **def** __init__(self, nombre): self.nombre = nombre **def** notificar(self, mensaje): print(f"Imprimiendo aviso en **{** self.nombre **}** : **{** mensaje **}** ") 

ServicioEmail, ServicioSMS e Impresora modelan tres cosas completamente distintas –un servicio de correo, una pasarela de SMS, un dispositivo de impresión– y no derivan unas de otras ni comparten ninguna clase base propia. Lo único que tienen en común es implementar INotificable. Gracias a eso, una función cliente puede recibir una colección heterogénea de objetos y notificarlos a todos por igual, sin necesidad de conocer de qué clase concreta es cada uno: 

**def** notificar_a_todos(destinatarios, mensaje): **for** destinatario **in** destinatarios: destinatario.notificar(mensaje) 

**11. Polimorfismo** 

**124** 

destinatarios = [ ServicioEmail("ana@empresa.com"), ServicioSMS("+54 9 351 555-0123"), Impresora("Impresora de Recepción"), ] 

notificar_a_todos(destinatarios, "Reunión de personal a las 15hs") 

La función notificar_a_todos no necesita ningún **if** ni isinstance para distinguir entre los tres tipos de destinatario: le alcanza con saber que todos implementan INotificable, y por lo tanto todos responden al mensaje notificar. Esta es la idea central de las interfaces: permiten construir código que opera sobre el contrato, completamente desacoplado de las clases concretas que lo cumplen. 

###### **11.3.2 Implementación de múltiples interfaces** 

Python permite que una clase implemente más de una interfaz al mismo tiempo, indicando varias clases base entre paréntesis, tal como se hace en herencia. Esto podría parecer, a primera vista, un caso de herencia múltiple, pero conceptualmente es un mecanismo distinto y considerablemente más seguro. 

La herencia múltiple propiamente dicha ocurre cuando dos o más clases base aportan **implementación** (atributos, cuerpos de métodos concretos) a una misma clase derivada. En ese escenario surge el llamado **problema del diamante** : si dos clases base definen un método con el mismo nombre pero distinta implementación, no existe una forma no ambigua de decidir cuál de las dos se hereda. Este es, precisamente, el motivo por el cual otros lenguajes no permiten que una clase extienda más de una clase concreta. 

Sin embargo, cuando lo que se declara entre paréntesis no son clases con implementación sino **interfaces** –ABCs compuestas únicamente por métodos abstractos, como IVehiculoTerrestre e IVehiculoAcuatico en el ejemplo siguiente–, no hay ninguna implementación en conflicto que heredar: cada interfaz aporta solamente un contrato (qué métodos deben existir), nunca un cuerpo concreto que pueda entrar en colisión con el de otra. 

**11.3. Interfaces** 

**125** 



**class IVehiculoTerrestre** (ABC): @abstractmethod **def** conducir(self): **pass class IVehiculoAcuatico** (ABC): @abstractmethod **def** navegar(self): **pass class VehiculoAnfibio** (IVehiculoTerrestre, IVehiculoAcuatico): **def** __init__(self, modelo): self.modelo = modelo **def** conducir(self): print(f" **{** self.modelo **}** está conduciendo en tierra") **def** navegar(self): print(f" **{** self.modelo **}** está navegando en agua") 

Esta implementación permite que un objeto VehiculoAnfibio sea tratado polimórficamente como un IVehiculoTerrestre o como un IVehiculoAcuatico, dependiendo del contexto en el que se utilice, replicando así el comportamiento de las interfaces múltiples de UML en Python. 

### **Testing unitario** 

##### **12.1 Introducción** 

El testing unitario es una práctica fundamental en el desarrollo de software que consiste en escribir y ejecutar pruebas automatizadas para verificar que las unidades individuales de código funcionen correctamente de manera aislada. Una unidad de código típicamente corresponde a un método, función o clase, y representa la porción más pequeña de código que puede ser probada de forma independiente. 

El propósito principal del testing unitario es detectar errores en las primeras etapas del desarrollo, cuando son más fáciles y económicos de corregir. Al verificar que cada componente individual funciona según lo esperado, se puede tener mayor confianza en que el sistema completo funcionará correctamente cuando todas las partes se integren. 

En la programación orientada a objetos, el testing unitario cobra especial relevancia debido a la naturaleza modular y encapsulada de las clases. Cada clase debe cumplir con un conjunto específico de responsabilidades y mantener su estado interno de manera coherente. Las pruebas unitarias permiten verificar que los métodos de una clase produzcan los resultados esperados, que las validaciones internas funcionen correctamente, y que el encapsulamiento se mantenga adecuadamente. 

Los beneficios del testing unitario incluyen la detección temprana de errores, la facilitación del refactoring seguro del código, la documentación implícita del comportamiento esperado de cada componente, y la reducción 

127 

**12. Testing unitario** 

**128** 

del tiempo necesario para localizar y corregir defectos. Además, las pruebas unitarias actúan como una red de seguridad que permite a los desarrolladores modificar el código con confianza, sabiendo que cualquier regresión será detectada inmediatamente. 

Para que el testing unitario sea efectivo, las pruebas deben ser rápidas de ejecutar, independientes entre sí, repetibles y fáciles de mantener. Cada prueba debe verificar un comportamiento específico y proporcionar información clara sobre qué aspecto del código falló cuando ocurre un error. 

##### **12.2 Pytest** 

Pytest es un framework de testing para Python que se ha convertido en el estándar de facto para escribir y ejecutar pruebas unitarias en este lenguaje. A diferencia de otros frameworks de testing, pytest se destaca por su sintaxis simple y natural, su capacidad de autodescubrimiento de pruebas, y sus potentes características avanzadas que facilitan la escritura de pruebas comprehensivas. 

Una de las principales ventajas de pytest es que permite escribir pruebas utilizando la sintaxis estándar de Python con la instrucción **assert** , eliminando la necesidad de aprender métodos específicos del framework como ocurre con otros sistemas de testing. Esto hace que las pruebas sean más legibles y fáciles de escribir para desarrolladores que ya conocen Python. 

Para instalar pytest, se utiliza el gestor de paquetes pip mediante el siguiente comando: 

pip install pytest 

Una vez instalado, pytest puede ejecutarse desde la línea de comandos. El framework automáticamente descubre y ejecuta todas las pruebas en el directorio actual y sus subdirectorios. Para ejecutar las pruebas, simplemente se utiliza: 

###### pytest 

Pytest busca automáticamente archivos que comiencen con test_ o terminen con _test.py, y dentro de estos archivos ejecuta todas las funciones que comiencen con test_. Esta convención de nomenclatura facilita la organización 

**12.3. Pruebas** 

**129** 

y el descubrimiento automático de las pruebas. 

Además del comando básico, pytest ofrece múltiples opciones de ejecución. Por ejemplo, se puede ejecutar un archivo específico de pruebas, mostrar información más detallada sobre la ejecución, o ejecutar solo las pruebas que contienen una palabra clave específica: 

_# Ejecutar un archivo específico_ pytest test_ejemplo.py _# Mostrar información detallada_ pytest -v _# Ejecutar pruebas que contengan una palabra clave_ pytest -k "suma" 

Pytest también genera reportes claros y detallados cuando las pruebas fallan, mostrando exactamente qué assertion falló, los valores esperados versus los obtenidos, y el contexto completo del error. 

##### **12.3 Pruebas** 

La estructura fundamental de las pruebas en pytest se basa en funciones que contienen assertions para verificar el comportamiento esperado del código. Una suite de pruebas es simplemente un conjunto de funciones de prueba organizadas en uno o más archivos, mientras que cada caso de prueba individual corresponde a una función específica que verifica un aspecto particular del código bajo prueba. 

La sintaxis básica para escribir una prueba en pytest es crear una función cuyo nombre comience con test_ y utilizar la instrucción **assert** para verificar condiciones: 

**def** test_ejemplo_basico(): resultado = 2 + 2 **assert** resultado ==) 4 

Para organizar las pruebas relacionadas con una clase específica, se recomienda crear un archivo de pruebas separado, típicamente con el nombre test_nombre_clase.py. Dentro de este archivo, se pueden agrupar las pruebas utilizando clases de prueba, aunque esto no es obligatorio: 

**12. Testing unitario** 

**130** 

**class TestCalculadora** : **def** test_suma(self): calc = Calculadora() resultado = calc.sumar(2, 3) **assert** resultado ==) 5 **def** test_division_por_cero(self): calc = Calculadora() **with** pytest.raises( **ZeroDivisionError** ): calc.dividir(10, 0) 

###### **12.3.1 Aserciones de igualdad** 

Las aserciones de igualdad son las más comunes en las pruebas unitarias y verifican que un valor obtenido sea exactamente igual al valor esperado. Pytest utiliza la instrucción **assert** estándar de Python junto con el operador de igualdad: 

**def** test_igualdad_numerica(): **assert** 5 ==) 5 **assert** 2.5 ==) 2.5 **def** test_igualdad_cadenas(): **assert** "hola" ==) "hola" **assert** "Python".lower() ==) "python" **def** test_igualdad_listas(): **assert** [1, 2, 3] ==) [1, 2, 3] **assert** sorted([3, 1, 2]) ==) [1, 2, 3] 

Para la desigualdad, se utiliza el operador !=): 

**def** test_desigualdad(): **assert** 5 !=) 3 **assert** "hola" !=) "adiós" 

###### **12.3.2 Aserciones de comparación** 

Las aserciones de comparación permiten verificar relaciones de orden entre valores utilizando los operadores de comparación estándar de Python: 

**def** test_comparaciones_numericas(): **assert** 5 > 3 **assert** 2 < 10 **assert** 5 >=) 5 **assert** 3 <=) 7 

**def** test_comparaciones_cadenas(): 

**12.3. Pruebas** 

**131** 

**assert** "abc" < "def" _# Orden alfabético_ **assert** "z" > "a" 

###### **12.3.3 Aserciones de pertenencia** 

Las aserciones de pertenencia verifican si un elemento está contenido en una colección utilizando el operador **in** : 

**def** test_pertenencia_listas(): numeros = [1, 2, 3, 4, 5] **assert** 3 **in** numeros **assert** 6 **not in** numeros **def** test_pertenencia_cadenas(): texto = "Hola mundo" **assert** "mundo" **in** texto **assert** "Python" **not in** texto **def** test_pertenencia_diccionarios(): datos = {"nombre": "Juan", "edad": 25} **assert** "nombre" **in** datos **assert** "apellido" **not in** datos 

###### **12.3.4 Aserciones de tipo** 

Las aserciones de tipo verifican que un objeto sea de un tipo específico utilizando la función isinstance(): 

**def** test_tipos(): **assert** isinstance(5, int) **assert** isinstance(3.14, float) **assert** isinstance("texto", str) **assert** isinstance([1, 2, 3], list) **assert** isinstance({"a": 1}, dict) 

###### **12.3.5 Aserciones de excepciones** 

Para verificar que el código lance excepciones bajo ciertas condiciones, pytest proporciona el context manager pytest.raises(): 

**import pytest def** test_excepcion_division_cero(): **with** pytest.raises( **ZeroDivisionError** ): resultado = 10 / 0 **def** test_excepcion_valor_incorrecto(): **with** pytest.raises( **ValueError** ): 

**12. Testing unitario** 

**132** 

int("texto_invalido") **def** test_excepcion_con_mensaje(): **with** pytest.raises( **ValueError** , match="invalid literal"): int("abc") 

###### **12.3.6 Aserciones de aproximación** 

Para valores de punto flotante, donde la comparación exacta puede fallar debido a imprecisiones de representación, pytest ofrece pytest.approx(): 

**import pytest def** test_aproximacion(): **assert** 0.1 + 0.2 ==) pytest.approx(0.3) **assert** 3.14159 ==) pytest.approx(3.14, rel=1e-2) 

##### **12.4 Ejemplo** 

Para ilustrar la aplicación práctica del testing unitario con pytest, se presenta una clase Numeros que encapsula una colección de números y proporciona métodos para realizar operaciones estadísticas básicas. Esta clase implementa el principio de composición al contener una lista de números como atributo interno. 

**class Numeros** : **def** __init__(self): self._numeros = [] **def** agregar(self, numero): **if not** isinstance(numero, (int, float)): **raise TypeError** ("Solo se pueden agregar números") self._numeros.append(numero) **def** cantidad(self): **return** len(self._numeros) **def** suma(self): **return** sum(self._numeros) **def** promedio(self): **if** self.cantidad() ==) 0: **raise ValueError** ("No se puede calcular el promedio de una colección vacía") **return** self.suma() / self.cantidad() **def** maximo(self): **if** self.cantidad() ==) 0: **raise ValueError** ("No se puede obtener el máximo de una colección vacía") **return** max(self._numeros) 

**12.4. Ejemplo** 

**133** 

**def** minimo(self): **if** self.cantidad() ==) 0: **raise ValueError** ("No se puede obtener el mínimo de una colección vacía") **return** min(self._numeros) **def** contiene(self, numero): **return** numero **in** self._numeros **def** limpiar(self): self._numeros.clear() 



A continuación se presenta una suite completa de pruebas para esta clase, organizada de manera sistemática para cubrir todos los casos de uso posibles, incluyendo casos límite y situaciones de error: 

**import pytest from numeros import** Numeros **class TestNumeros** : **def** test_coleccion_vacia_inicial(self): _"""Verifica que una nueva instancia esté vacía"""_ coleccion = Numeros() **assert** coleccion.cantidad() ==) 0 **def** test_agregar_numero_entero(self): _"""Verifica que se puedan agregar números enteros"""_ coleccion = Numeros() coleccion.agregar(5) **assert** coleccion.cantidad() ==) 1 **assert** coleccion.contiene(5) **def** test_agregar_numero_flotante(self): _"""Verifica que se puedan agregar números flotantes"""_ coleccion = Numeros() coleccion.agregar(3.14) **assert** coleccion.cantidad() ==) 1 **assert** coleccion.contiene(3.14) 

**12. Testing unitario** 

**134** 

**def** test_agregar_numero_negativo(self): _"""Verifica que se puedan agregar números negativos"""_ coleccion = Numeros() coleccion.agregar(-10) **assert** coleccion.cantidad() ==) 1 **assert** coleccion.contiene(-10) **def** test_agregar_cero(self): _"""Verifica que se pueda agregar el número cero"""_ coleccion = Numeros() coleccion.agregar(0) **assert** coleccion.cantidad() ==) 1 **assert** coleccion.contiene(0) **def** test_agregar_tipo_invalido_cadena(self): _"""Verifica que se lance excepción al agregar una cadena"""_ coleccion = Numeros() **with** pytest.raises( **TypeError** , match="Solo se pueden agregar números"): coleccion.agregar("cinco") **def** test_agregar_tipo_invalido_lista(self): _"""Verifica que se lance excepción al agregar una lista"""_ coleccion = Numeros() **with** pytest.raises( **TypeError** ): coleccion.agregar([1, 2, 3]) **def** test_agregar_multiple_numeros(self): _"""Verifica que se puedan agregar múltiples números"""_ coleccion = Numeros() numeros = [1, 2, 3, 4, 5] **for** numero **in** numeros: coleccion.agregar(numero) **assert** coleccion.cantidad() ==) 5 **for** numero **in** numeros: **assert** coleccion.contiene(numero) **def** test_suma_un_numero(self): _"""Verifica la suma con un solo número"""_ coleccion = Numeros() coleccion.agregar(7) **assert** coleccion.suma() ==) 7 **def** test_suma_multiples_numeros(self): _"""Verifica la suma con múltiples números"""_ coleccion = Numeros() coleccion.agregar(2) coleccion.agregar(3) coleccion.agregar(5) **assert** coleccion.suma() ==) 10 **def** test_suma_numeros_negativos(self): _"""Verifica la suma con números negativos"""_ coleccion = Numeros() coleccion.agregar(-2) coleccion.agregar(5) coleccion.agregar(-1) **assert** coleccion.suma() ==) 2 

**def** test_suma_coleccion_vacia(self): 

**12.4. Ejemplo** 

**135** 

_"""Verifica que la suma de una colección vacía sea cero"""_ coleccion = Numeros() **assert** coleccion.suma() ==) 0 **def** test_promedio_un_numero(self): _"""Verifica el promedio con un solo número"""_ coleccion = Numeros() coleccion.agregar(8) **assert** coleccion.promedio() ==) 8 **def** test_promedio_multiples_numeros(self): _"""Verifica el promedio con múltiples números"""_ coleccion = Numeros() coleccion.agregar(2) coleccion.agregar(4) coleccion.agregar(6) **assert** coleccion.promedio() ==) 4 **def** test_promedio_con_flotantes(self): _"""Verifica el promedio con números flotantes"""_ coleccion = Numeros() coleccion.agregar(1.5) coleccion.agregar(2.5) **assert** coleccion.promedio() ==) pytest.approx(2.0) **def** test_promedio_coleccion_vacia(self): _"""Verifica que se lance excepción al calcular promedio de colección vacía"""_ coleccion = Numeros() **with** pytest.raises( **ValueError** , match="No se puede calcular el promedio de una �→ colección vacía"): coleccion.promedio() **def** test_maximo_un_numero(self): _"""Verifica el máximo con un solo número"""_ coleccion = Numeros() coleccion.agregar(42) **assert** coleccion.maximo() ==) 42 **def** test_maximo_multiples_numeros(self): _"""Verifica el máximo con múltiples números"""_ coleccion = Numeros() numeros = [3, 1, 4, 1, 5, 9, 2, 6] **for** numero **in** numeros: coleccion.agregar(numero) **assert** coleccion.maximo() ==) 9 **def** test_maximo_numeros_negativos(self): _"""Verifica el máximo con solo números negativos"""_ coleccion = Numeros() coleccion.agregar(-5) coleccion.agregar(-2) coleccion.agregar(-8) **assert** coleccion.maximo() ==) -2 **def** test_maximo_coleccion_vacia(self): _"""Verifica que se lance excepción al buscar máximo de colección vacía"""_ coleccion = Numeros() **with** pytest.raises( **ValueError** , match="No se puede obtener el máximo de una �→ colección vacía"): coleccion.maximo() 

**12. Testing unitario** 

**136** 

**def** test_minimo_un_numero(self): _"""Verifica el mínimo con un solo número"""_ coleccion = Numeros() coleccion.agregar(17) **assert** coleccion.minimo() ==) 17 **def** test_minimo_multiples_numeros(self): _"""Verifica el mínimo con múltiples números"""_ coleccion = Numeros() numeros = [3, 1, 4, 1, 5, 9, 2, 6] **for** numero **in** numeros: coleccion.agregar(numero) **assert** coleccion.minimo() ==) 1 **def** test_minimo_numeros_positivos(self): _"""Verifica el mínimo con solo números positivos"""_ coleccion = Numeros() coleccion.agregar(5) coleccion.agregar(2) coleccion.agregar(8) **assert** coleccion.minimo() ==) 2 **def** test_minimo_coleccion_vacia(self): _"""Verifica que se lance excepción al buscar mínimo de colección vacía"""_ coleccion = Numeros() **with** pytest.raises( **ValueError** , match="No se puede obtener el mínimo de una �→ colección vacía"): coleccion.minimo() **def** test_contiene_numero_presente(self): _"""Verifica que contiene devuelva True para números presentes"""_ coleccion = Numeros() coleccion.agregar(10) coleccion.agregar(20) coleccion.agregar(30) **assert** coleccion.contiene(20) **def** test_contiene_numero_ausente(self): _"""Verifica que contiene devuelva False para números ausentes"""_ coleccion = Numeros() coleccion.agregar(10) coleccion.agregar(20) **assert not** coleccion.contiene(15) **def** test_contiene_coleccion_vacia(self): _"""Verifica que contiene devuelva False en colección vacía"""_ coleccion = Numeros() **assert not** coleccion.contiene(5) **def** test_limpiar_coleccion(self): _"""Verifica que limpiar vacíe completamente la colección"""_ coleccion = Numeros() coleccion.agregar(1) coleccion.agregar(2) coleccion.agregar(3) **assert** coleccion.cantidad() ==) 3 coleccion.limpiar() **assert** coleccion.cantidad() ==) 0 

**12.4. Ejemplo** 

**137** 

**assert not** coleccion.contiene(1) **assert not** coleccion.contiene(2) **assert not** coleccion.contiene(3) **def** test_operaciones_despues_limpiar(self): _"""Verifica que las operaciones fallen después de limpiar"""_ coleccion = Numeros() coleccion.agregar(5) coleccion.limpiar() **with** pytest.raises( **ValueError** ): coleccion.promedio() **with** pytest.raises( **ValueError** ): coleccion.maximo() **with** pytest.raises( **ValueError** ): coleccion.minimo() **def** test_flujo_completo(self): _"""Prueba de integración que verifica un flujo completo de operaciones"""_ coleccion = Numeros() _# Agregar números_ numeros = [2, 4, 6, 8, 10] **for** numero **in** numeros: coleccion.agregar(numero) _# Verificar todas las operaciones_ **assert** coleccion.cantidad() ==) 5 **assert** coleccion.suma() ==) 30 **assert** coleccion.promedio() ==) 6 **assert** coleccion.maximo() ==) 10 **assert** coleccion.minimo() ==) 2 _# Verificar pertenencia_ **for** numero **in** numeros: **assert** coleccion.contiene(numero) **assert not** coleccion.contiene(7) 

Esta suite de pruebas cubre exhaustivamente todos los métodos de la clase Numeros, incluyendo casos normales, casos límite y situaciones de error. Las pruebas están organizadas de manera lógica, cada una verifica un comportamiento específico, y utilizan nombres descriptivos que facilitan la comprensión de qué está siendo probado. 

El conjunto de pruebas incluye verificaciones para el manejo correcto de excepciones, validaciones de tipos, operaciones con colecciones vacías, y un caso de prueba de integración que verifica el flujo completo de operaciones. Esta aproximación sistemática al testing garantiza que la clase Numeros funcione correctamente en todas las situaciones previstas. 

23 de octubre de 2023 

# Desarrollo orientado a objetos 

### **Material conceptual:** 

### Acceso a Base de datos 

##### **Conocimiento previo requerido** 

Conceptos de Base de datos 

Lenguaje de Manipulación de Datos (DML) 

Lenguaje de Definición de Datos (DDL) 

##### **Temas incluidos** 

Base de datos SQLite 

Conexión a base de datos 

Cursores 

Ejecutar operaciones con la base de datos 

Uso de librería SQLite3 

##### **Motor de base de datos SQLite** 

No es necesario instalar SQLite por separado en tu PC cuando trabajas con Python, ya que SQLite es una parte integral de la biblioteca estándar de Python. En otras palabras, Python incluye el módulo sqlite3 para interactuar con bases de datos SQLite. Por lo tanto, no necesitas realizar una instalación adicional de SQLite en tu sistema. 

Solo necesitas asegurarte de que Python esté correctamente instalado y que puedas importar el módulo sqlite3. Si puedes importarlo sin errores, entonces estás listo para empezar a trabajar con bases de datos SQLite desde Python. El ejemplo que te proporcioné en la respuesta anterior utiliza este módulo para interactuar con SQLite. 

##### **Librería para trabajar con base de datos SQLite** 

Para acceder a una base de datos SQLite desde Python, necesitas usar el módulo sqlite3, que es parte de la biblioteca estándar de Python. Aquí hay un ejemplo básico de cómo puedes crear una base de datos SQLite y realizar operaciones de lectura y escritura: 



<!-- Start of picture text -->
import sqlite3<br>conn = sqlite3.connect( )<br>cursor = conn.cursor()<br>nombre =<br>apellido =<br>edad =<br>cursor.execute(<br>conn.commit()<br>cursor.close()<br>conn.close()<br><!-- End of picture text -->

**Lectura y escritura** 



<!-- Start of picture text -->
import sqlite3<br>conn = sqlite3.connect( )<br>cursor = conn.cursor()<br>cursor. execute(<br><!-- End of picture text -->



**En este ejemplo:** 

Importamos el módulo sqlite3. 

Conectamos o creamos una base de datos llamada "mi_base_de_datos.db". 

Creamos un cursor que nos permite ejecutar comandos SQL en la base de datos. 

Creamos una tabla llamada "empleados". 

Insertamos datos en la tabla. 

Consultamos datos de la tabla y los imprimimos. 

Finalmente, cerramos la conexión a la base de datos. 

Este es un ejemplo simple para empezar. Puedes adaptar y expandir el código según tus necesidades para trabajar con bases de datos SQLite desde Python. Asegúrate de gestionar las excepciones adecuadamente y seguir las mejores prácticas de seguridad, especialmente si estás trabajando con datos sensibles. 

##### **Cursores en Python** 

En Python, un cursor se refiere a un objeto proporcionado por módulos de bases de datos, como sqlite3 (para SQLite) o psycopg2 (para PostgreSQL), que permite ejecutar consultas SQL y recuperar datos de la base de datos. Un cursor actúa como una interfaz entre tu programa y la base de datos. Aquí hay una breve descripción de su uso: 

Conexión a la Base de Datos: En primer lugar, debes establecer una conexión a la base de datos. Utilizas un objeto de conexión para conectarte a la base de datos utilizando información como el nombre del archivo de la base de datos, el nombre de usuario, la contraseña, etc. 

Crear un Cursor: Una vez que tengas una conexión activa a la base de datos, creas un objeto cursor utilizando el método cursor() de la conexión. Por ejemplo: 



<!-- Start of picture text -->
import sqlite3<br>conn = sqlite3.connect( )<br>cursor = conn.cursor()<br><!-- End of picture text -->

**<mark>Ejecutar Consultas SQL:</mark>** <mark>Utilizas el cursor para ejecutar consultas SQL, como SELECT, INSERT, UPDATE o DELETE, utilizando métodos como</mark> **<u><mark>`execute()`</mark></u>** <mark>. Por ejemplo:</mark> 



Recuperar Datos: Utilizas el cursor para recuperar datos resultantes de la consulta, como filas de una tabla. Puedes iterar sobre las filas o utilizar métodos como fetchall(), fetchone(), etc., para recuperar datos. 

Cerrar el Cursor y la Conexión: Cuando hayas terminado de usar el cursor, es una buena práctica cerrarlo y también cerrar la conexión a la base de datos para liberar recursos. Puedes hacerlo con los métodos close(): 



<!-- Start of picture text -->
cursor.close()<br>conn.close()<br><!-- End of picture text -->

Los cursores son una parte esencial cuando trabajas con bases de datos en Python, ya que te permiten interactuar con la base de datos de una manera segura y eficiente. 

Métodos más usados en Cursores: 

Con un cursor en SQLite, puedes ejecutar varios métodos para interactuar con la base de datos. Algunos de los métodos más comunes son: 

1. **execute(query, parameters)** : Ejecuta una consulta SQL en la base de datos. Puedes pasar una cadena SQL como el parámetro **query** . Si la consulta SQL tiene parámetros, puedes proporcionarlos como una tupla o lista en el parámetro **parameters** . 

2. **executemany(query, seq_of_parameters)** : Ejecuta una consulta SQL múltiples veces con diferentes conjuntos de parámetros. **query** es la consulta SQL, y **seq_of_parameters** es una secuencia que contiene varias tuplas (o listas) de parámetros. 

3. **fetchone()** : Recupera la siguiente fila del resultado de una consulta como una tupla, o **None** si no hay más filas. 

4. **fetchall()** : Recupera todas las filas restantes del resultado de una consulta como una lista de tuplas. 

5. **fetchmany(size)** : Recupera varias filas (especificadas por **size** ) del resultado de una consulta como una lista de tuplas. 

6. **fetchall()** : Recupera todas las filas restantes del resultado de una consulta como una lista de tuplas. 

7. **executeScript(script)** : Ejecuta múltiples sentencias SQL contenidas en una cadena. Esta función se utiliza comúnmente para ejecutar secuencias de instrucciones separadas por punto y coma. 

8. **close()** : Cierra el cursor, liberando recursos. Después de cerrar un cursor, no se pueden ejecutar más consultas. 

Estos son algunos de los métodos más utilizados. El uso de estos métodos depende de tus necesidades específicas al interactuar con la base de datos SQLite. 

Ejemplo de recorrido de una tabla 



<!-- Start of picture text -->
import sqlite3<br>conn = sqlite3.connect( )<br>cursor = conn.cursor()<br>cursor.execute( )<br>row = cursor.fetchone()<br>while row is not None:<br>print( » row[0])<br>print( » row[i])<br>print( » row[2])<br>row = cursor.fetchone()<br>cursor.close()<br>conn.close()<br><!-- End of picture text -->

Este código: 

1. Abre una conexión con una base de datos SQLite llamada "mi_base_de_datos.db" (o la crea si no existe). 

2. Crea un cursor para ejecutar consultas en la base de datos. 

3. Ejecuta una consulta SQL para seleccionar todos los registros de una tabla llamada "mi_tabla". 

4. Utiliza un bucle **while** para recorrer las filas del resultado. Con **fetchone()** , obtiene una fila a la vez y la almacena en la variable **row** . 

5. Dentro del bucle, procesa y muestra los datos de cada fila (en este caso, el nombre, edad y dirección). 

6. Luego, obtiene la siguiente fila con **fetchone()** y continúa el bucle hasta que no haya más filas. 

7. Finalmente, cierra el cursor y la conexión a la base de datos. 

##### **Recorrer N registros en una tabla** 

En este ejemplo, supongamos que tienes una tabla llamada "mi_tabla" en una base de datos SQLite y deseas recuperar los primeros N registros de esa tabla: 



<!-- Start of picture text -->
import sqlite3<br>conn = sqlite3.connect( )<br>cursor = conn.cursor()<br>N=<br>cursor.execute( » (N,))<br>for row in cursor.fetchall():<br>print(row)<br>cursor.close()<br>conn.close()<br><!-- End of picture text -->

##### **Para mostrar una sola columna** 



<!-- Start of picture text -->
import sqlite3<br>conn = sqlite3.connect( )<br>cursor = conn.cursor()<br>N=<br>cursor.execute( » (N,))<br>for row in cursor.fetchall():<br>print(row[0])<br>cursor.close()<br>conn.close()<br><!-- End of picture text -->

**Para agregar registros en una base de datos.** 



<!-- Start of picture text -->
import sqlite3<br>conn = sqlite3.connect( )<br>cursor = conn.cursor()<br>nombre =<br>apellido =<br>edad =<br>cursor. execute(<br>conn.commit()<br>cursor.close()<br>conn.close()<br><!-- End of picture text -->

En este ejemplo, hemos creado una conexión a la base de datos, un cursor y luego hemos ejecutado una consulta SQL de inserción con la declaración INSERT INTO. Los valores se pasan como parámetros en una tupla (nombre, apellido, edad) que coincide con los valores correspondientes en la consulta. 

Luego, para confirmar la inserción, se llama a commit() en la conexión, lo que guarda los cambios en la base de datos. 

##### **Manejo de errores** 

Es muy importante considerar que cuando realizamos operaciones en base datos pueden ocurrir errores y debemos manejarlos para evitar efectos no esperados e inconsistencias. 



<!-- Start of picture text -->
import sqlite3<br>connection = sqlite3.connect( )<br>cursor = connection.cursor()<br>cursor. execute(<br>connection. commit()<br>except sqlite3.Error as error:<br>print( » error)<br>finally:<br>connection.close()<br><!-- End of picture text -->

**En este ejemplo:** 

Importamos el módulo sqlite3 para trabajar con bases de datos SQLite. 

Usamos un bloque try para intentar insertar datos en la base de datos. 

Si ocurre algún error durante la inserción (por ejemplo, un problema de integridad o un campo duplicado), se captura la excepción sqlite3.Error y se imprime un mensaje de error. 

Finalmente, cerramos la conexión a la base de datos en el bloque finally para asegurarnos de que los recursos se liberen adecuadamente. 

Recuerda que debes reemplazar "mi_base_de_datos.db" por el nombre de tu propia base de datos y "tabla_ejemplo" por el nombre de tu propia tabla, además de ajustar los nombres de campo y valores según tus necesidades. También puedes personalizar el manejo de errores según tus requerimientos. 

Uso de Rollback 



<!-- Start of picture text -->
conn = sqlite3.connect( )<br>cursor = conn.cursor()<br>conn.execute( )<br>cursor .execute( )<br>cursor.execute( )<br>conn. commit()<br>( )<br>Exception e:<br>conn.rollback()<br>( )<br>conn.close() v<br><!-- End of picture text -->

##### **Ejercicios de practica** 

1. **Lectura de Datos** : 

   - Escribe un programa que se conecte a una base de datos SQLite y recupere todos los registros de una tabla específica. Luego, muestra los registros en la consola. 

- Crea una tabla que almacene información sobre libros (título, autor, año de publicación). Escribe un programa que lea y muestre todos los libros almacenados en la base de datos. 

##### 2. **Inserción de Datos** : 

   - Crea una base de datos SQLite y una tabla que almacene información de estudiantes (nombre, edad, calificaciones). Escribe un programa que permita al usuario ingresar datos de nuevos estudiantes y los inserte en la base de datos. 

   - Crea una base de datos que almacene información de productos (nombre, precio, cantidad en stock). Escribe un programa que permita al usuario ingresar nuevos productos y sus detalles en la base de datos. 

3. **Actualización de Datos** : 

   - Crea una base de datos que almacene información sobre empleados (nombre, salario, departamento). Escribe un programa que permita actualizar el salario de un empleado específico. 

   - Crea una tabla que almacene información de contactos (nombre, correo electrónico, número de teléfono). Escribe un programa que permita al usuario actualizar el correo electrónico de un contacto. 

##### 4. **Eliminación de Datos** : 

- Crea una base de datos que almacene información de tareas pendientes (nombre de la tarea, fecha de vencimiento). Escribe un programa que permita al usuario eliminar una tarea específica de la base de datos. 

- Crea una tabla que almacene información de productos (nombre, precio, cantidad en stock). Escribe un programa que permita al usuario eliminar un producto de la base de datos. 

##### 5. **Consulta Avanzada** : 

- Escribe un programa que conecte a una base de datos de películas y muestre todas las películas de un género específico. 

- Crea una tabla que almacene información de clientes (nombre, dirección, fecha de registro). Escribe un programa que muestre todos los clientes que se registraron en un mes y año específicos. 

##### 6. **Exportación e Importación** : 

- Crea una base de datos que almacene información de contactos (nombre, correo electrónico, número de teléfono). Escribe un programa que exporte los datos de la base de datos a un archivo CSV. 

- Escribe un programa que importe datos de un archivo CSV a una tabla de la base de datos SQLite. 

**Material adicional:** 

##### **Tutorial** 

<u>htps://likegeeks.com/pythont</u> -sqlite3-tutorial/ 

**Material de BD:** 

EjerciciosSQL.Pdf ManualPracticoSQL.Pdf AprendiendoSQL.Docx 

### **Bases de datos con sqlite3** 

##### **13.1 Introducción** 

La persistencia de datos constituye un aspecto fundamental en el desarrollo de aplicaciones. A lo largo de los capítulos precedentes se ha trabajado con archivos como mecanismo para conservar información; sin embargo, cuando se necesita almacenar grandes volúmenes de datos estructurados, efectuar consultas complejas o preservar la integridad de la información, el empleo de una base de datos relacional se presenta como la alternativa más adecuada. 

Python ofrece interfaces para conectarse con la mayoría de los sistemas de gestión de bases de datos relacionales. Algunas de estas interfaces forman parte de la biblioteca estándar, mientras que para los motores restantes existen bibliotecas que pueden instalarse mediante gestores de paquetes como pip. Python incorpora en su biblioteca estándar el módulo sqlite3, que ofrece una interfaz para trabajar con bases de datos SQLite. 

##### **13.2 SQLite** 

SQLite es un sistema de gestión de bases de datos relacional que no requiere de un servidor independiente, ya que la base de datos completa se almacena en un único archivo. Esta característica la convierte en una alternativa especialmente conveniente para aplicaciones de escritorio, prototipos, aplicaciones móviles y, en general, para todo escenario en el que no se requiera concurrencia masiva. 

141 

**13. Bases de datos con sqlite3** 

**142** 

Se trata de un sistema autocontenido, que no requiere instalación ni con�guración de servidor y funciona directamente, sin archivos de con�guración. Es transaccional, dado que cumple las propiedades ACID (Atomicidad, Consistencia, Aislamiento y Durabilidad), y resulta portable, puesto que la base de datos es un archivo único que puede copiarse entre sistemas. Por último, implementa la mayor parte del estándar SQL, lo que la convierte en una opción completa para la mayoría de las aplicaciones. 

##### **13.3 Conexión a una base de datos** 

Para trabajar con una base de datos SQLite en Python, es necesario primero importar el módulo y establecer una conexión: 

###### **import sqlite3** 

_# Conectar a una base de datos (se crea si no existe)_ conexion = sqlite3.connect('mi_base_datos.db') 

_# Crear un cursor para ejecutar comandos SQL_ cursor = conexion.cursor() 

_# Realizar operaciones�)) # Cerrar la conexión_ conexion.close() 

El método connect() recibe como parámetro el nombre del archivo de base de datos. Si el archivo no existe, SQLite lo crea automáticamente. Para crear una base de datos en memoria (temporal), se utiliza el nombre especial ':memory:'. 

**Buena práctica: uso de context managers** Es recomendable utilizar la sentencia **with** , ya que garantiza que la conexión se cierre correctamente aun cuando ocurra un error durante la ejecución de las operaciones: 

**import sqlite3** 

> **with** sqlite3.connect('mi_base_datos.db') **as** conexion: cursor = conexion.cursor() 

> _# Realizar operaciones�))_ 

> _# La conexión se cierra automáticamente_ 

**13.4. Objeto cursor** 

**143** 

##### **13.4 Objeto cursor** 

El cursor es el objeto a través del cual se ejecutan las sentencias SQL sobre la base de datos y se recuperan los resultados obtenidos. Se obtiene a partir de la conexión mediante el método cursor(). Sus principales métodos son: 

- execute(sql, parametros= **None** ): Ejecuta una sentencia SQL; el segundo argumento, opcional, permite incorporar valores a la consulta por medio de parámetros 

- executemany(sql, secuencia): Ejecuta la misma sentencia una vez por cada conjunto de valores contenido en la secuencia 

- fetchone(): Devuelve la siguiente �la del resultado como una tupla, o **None** si no hay más �las 

- fetchall(): Devuelve todas las �las restantes como una lista de tuplas 

- fetchmany(tam): Devuelve hasta tam �las como una lista de tuplas 

Además de estos métodos, el cursor posee dos atributos de particular utilidad. lastrowid almacena el identi�cador asignado al último registro insertado mediante ese cursor, en tanto que rowcount informa la cantidad de �las afectadas por la última operación ejecutada. 

El siguiente ejemplo ilustra el empleo de los métodos de recuperación de �las: 

**import sqlite3 with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute('SELECT * FROM personas') _# Obtener fila por fila_ print("Primera persona:") fila = cursor.fetchone() print(fila) print(" **\n** Siguientes 2 personas:") filas = cursor.fetchmany(2) **for** fila **in** filas: print(fila) print(" **\n** Restantes:") filas = cursor.fetchall() **for** fila **in** filas: print(fila) 

**13. Bases de datos con sqlite3** 

**144** 

##### **13.5 Consultas** 

Las consultas son las sentencias SQL orientadas a la recuperación de datos. Se estructuran a partir de SELECT y devuelven las �las que satisfacen los criterios indicados. Para recuperar todos los registros de una tabla: 

**import sqlite3 with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() _# Consultar todos los registros_ cursor.execute('SELECT * FROM personas') _# Obtener todos los resultados_ resultados = cursor.fetchall() **for** fila **in** resultados: print(fila) 

###### **13.5.1 Consultas con �ltros** 

La cláusula WHERE permite limitar los resultados de una consulta a las �las que cumplen una condición determinada, mientras que la cláusula ORDER BY ordena los resultados según una columna: 

**import sqlite3 def** buscar_por_documento(documento): **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' SELECT * FROM personas WHERE documento = ? ''', (documento,)) **return** cursor.fetchone() **def** buscar_mayores_de(edad_minima): **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' SELECT * FROM personas WHERE edad �) ? ORDER BY edad DESC ''', (edad_minima,)) **return** cursor.fetchall() 

_# Uso_ persona = buscar_por_documento('12345678') print(f"Persona encontrada: **{** persona **}** ") 

**13.6. Sentencias de modi�cación de datos** 

**145** 

mayores = buscar_mayores_de(30) print(f" **\n** Personas mayores de 30 años:") **for** p **in** mayores: print(p) 

###### **13.5.2 Trabajar con diccionarios en lugar de tuplas** 

Por defecto, el módulo sqlite3 devuelve las �las como tuplas. Para acceder a los datos por el nombre de la columna, es posible con�gurar la propiedad row_factory de la conexión asignándole la clase sqlite3.Row: de este modo, cada �la se comporta como una estructura similar a un diccionario, y los valores pueden consultarse mediante el nombre de la columna: 

**import sqlite3 with** sqlite3.connect('personas.db') **as** conexion: _# Configurar para devolver diccionarios_ conexion.row_factory = sqlite3.Row cursor = conexion.cursor() cursor.execute('SELECT * FROM personas') **for** fila **in** cursor.fetchall(): _# Acceder por nombre de columna_ print(f" **{** fila['nombre'] **} {** fila['apellido'] **}** , " f" **{** fila['edad'] **}** años, DNI: **{** fila['documento'] **}** ") 

##### **13.6 Sentencias de modi�cación de datos** 

Las sentencias INSERT, UPDATE y DELETE permiten crear, modi�car y eliminar los datos almacenados en las tablas. A diferencia de las consultas, estas sentencias no devuelven �las como resultado. Asimismo los cambios que producen deben con�rmarse con commit() para volverse permanentes. 

###### **13.6.1 Inserción de datos** 

Para insertar registros se utiliza la sentencia INSERT INTO: 

**import sqlite3 with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() _# Insertar un registro_ cursor.execute(''' INSERT INTO personas (documento, nombre, apellido, edad) 

**13. Bases de datos con sqlite3** 

**146** 

VALUES ('12345678', 'Juan', 'Pérez', 30) ''') conexion.commit() print(f"Registro insertado con ID: **{** cursor.lastrowid **}** ") 

El atributo lastrowid del cursor almacena el identi�cador correspondiente al último registro insertado. 

###### **13.6.2 Inserción con parámetros** 

Nunca deben construirse consultas SQL concatenando cadenas con valores proporcionados por el usuario, ya que esta práctica expone a la aplicación a ataques de _inyección SQL_ . En lugar de ello, los valores deben incorporarse a la consulta mediante parámetros: 

**import sqlite3 def** insertar_persona(documento, nombre, apellido, edad): **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() _# Uso de parámetros (placeholders con ?)_ cursor.execute(''' INSERT INTO personas (documento, nombre, apellido, edad) VALUES (?, ?, ?, ?) ''', (documento, nombre, apellido, edad)) conexion.commit() **return** cursor.lastrowid _# Uso de la función_ id_persona = insertar_persona('87654321', 'María', 'González', 25) print(f"Persona insertada con ID: **{** id_persona **}** ") 

Los signos de interrogación ? funcionan como marcadores de posición ( _placeholders_ ) que son reemplazados por los valores de la tupla enviada como segundo argumento. 

###### **13.6.3 Inserción múltiple** 

Para insertar varios registros en una misma operación, se utiliza el método executemany(), que recibe la consulta y una secuencia de tuplas con los valores a insertar: 

**13.6. Sentencias de modi�cación de datos** 

**147** 

**import sqlite3** personas = [ ('11111111', 'Pedro', 'Martínez', 35), ('22222222', 'Ana', 'López', 28), ('33333333', 'Luis', 'Rodríguez', 42) ] **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.executemany(''' INSERT INTO personas (documento, nombre, apellido, edad) VALUES (?, ?, ?, ?) ''', personas) conexion.commit() print(f" **{** cursor.rowcount **}** registros insertados") 

###### **13.6.4 Actualización de datos** 

Para modi�car registros existentes se utiliza la sentencia UPDATE: 

**import sqlite3 def** actualizar_edad(documento, nueva_edad): **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' UPDATE personas SET edad = ? WHERE documento = ? ''', (nueva_edad, documento)) conexion.commit() **if** cursor.rowcount > 0: print(f"Edad actualizada para documento **{** documento **}** ") **else** : print(f"No se encontró persona con documento **{** documento **}** ") _# Uso_ actualizar_edad('12345678', 31) 

El atributo rowcount del cursor indica la cantidad de �las afectadas por la última operación ejecutada. Su consulta resulta útil para determinar, por ejemplo, si una actualización alcanzó efectivamente algún registro. 

###### **13.6.5 Eliminación de datos** 

Para eliminar registros se utiliza la sentencia DELETE: 

**13. Bases de datos con sqlite3** 

**148** 

**import sqlite3 def** eliminar_persona(documento): **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' DELETE FROM personas WHERE documento = ? ''', (documento,)) conexion.commit() **if** cursor.rowcount > 0: print(f"Persona con documento **{** documento **}** eliminada") **else** : print(f"No se encontró persona con documento **{** documento **}** ") _# Uso_ eliminar_persona('12345678') 

##### **13.7 Transacciones** 

Una transacción es un conjunto de operaciones que se ejecutan como una única unidad de trabajo. Si alguna de ellas falla, todas las operaciones de la transacción se deben deshacer en conjunto mediante una operación denominada _rollback_ . Este comportamiento garantiza que la base de datos nunca quede en un estado intermedio e inconsistente. 

Por defecto, el módulo sqlite3 agrupa dentro de una misma transacción las sentencias de modi�cación ejecutadas sobre una conexión. Los cambios que estas producen no se vuelven permanentes hasta que la transacción se con�rma con el método commit(); si en su lugar se invoca rollback(), o si la conexión se cierra sin con�rmar, el conjunto completo de cambios se descarta. 

El siguiente ejemplo implementa una transferencia de saldo entre dos cuentas. Solo si las dos operaciones, restar el monto en el origen y sumarlo en el destino, se completan correctamente, se con�rma la transacción; ante cualquier error, el conjunto se deshace: 

**import sqlite3 def** transferir_saldo(cuenta_origen, cuenta_destino, monto): **with** sqlite3.connect('banco.db') **as** conexion: cursor = conexion.cursor() **try** : _# Restar saldo de cuenta origen_ cursor.execute(''' UPDATE cuentas 

**13.8. Manejo de errores** 

**149** 

SET saldo = saldo - ? WHERE numero = ? ''', (monto, cuenta_origen)) _# Sumar saldo a cuenta destino_ cursor.execute(''' UPDATE cuentas SET saldo = saldo + ? WHERE numero = ? ''', (monto, cuenta_destino)) _# Confirmar transacción_ conexion.commit() print("Transferencia exitosa") **except Exception as** e: _# Deshacer cambios en caso de error_ conexion.rollback() print(f"Error en la transferencia: **{** e **}** ") 

##### **13.8 Manejo de errores** 

El manejo adecuado de los errores constituye una parte esencial del trabajo con bases de datos. El módulo sqlite3 de�ne una jerarquía de excepciones que permite distinguir con precisión el tipo de falla ocurrida; todas ellas derivan de sqlite3.Error. Al implementar el manejo de errores se recomienda capturar primero las subclases más especí�cas y, al �nal, sqlite3.Error como caso genérico: 

**import sqlite3 def** insertar_persona_segura(documento, nombre, apellido, edad): **try** : **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' INSERT INTO personas (documento, nombre, apellido, edad) VALUES (?, ?, ?, ?) ''', (documento, nombre, apellido, edad)) conexion.commit() **return True** , "Persona insertada exitosamente" **except** sqlite3.IntegrityError **as** e: _# Violación de restricción (ej: documento duplicado)_ **return False** , f"Error de integridad: **{** e **}** " **except** sqlite3.OperationalError **as** e: _# Error operacional (ej: tabla no existe)_ **return False** , f"Error operacional: **{** e **}** " **except** sqlite3.Error **as** e: _# Otros errores de SQLite_ 

**13. Bases de datos con sqlite3** 

**150** 

**return False** , f"Error de base de datos: **{** e **}** " _# Uso_ exito, mensaje = insertar_persona_segura('12345678', 'Juan', 'Pérez', 30) print(mensaje) _# Intentar insertar el mismo documento nuevamente_ exito, mensaje = insertar_persona_segura('12345678', 'Pedro', 'García', 25) print(mensaje) _# Error: documento ya existe_ 

##### **13.9 Ejemplo completo: Sistema de gestión de personas** 

El siguiente ejemplo completo integra las operaciones CRUD (Create, Read, Update, Delete): 

**Sistema de gestión de personas con SQLite** 

_""" Sistema de gestión de personas con SQLite Ejemplo completo de operaciones CRUD (Create, Read, Update, Delete) """_ **import sqlite3 def** crear_tabla(): _"""Crea la tabla personas si no existe"""_ **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' CREATE TABLE IF NOT EXISTS personas ( id INTEGER PRIMARY KEY AUTOINCREMENT, documento TEXT NOT NULL UNIQUE, nombre TEXT NOT NULL, apellido TEXT NOT NULL, edad INTEGER CHECK(edad �) 0) ) ''') conexion.commit() print("Tabla creada o verificada exitosamente") **def** insertar_persona(documento, nombre, apellido, edad): _"""Inserta una nueva persona en la base de datos"""_ **try** : **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' INSERT INTO personas (documento, nombre, apellido, edad) VALUES (?, ?, ?, ?) ''', (documento, nombre, apellido, edad)) conexion.commit() **return True** , cursor.lastrowid **except** sqlite3.IntegrityError: **return False** , "El documento ya existe en la base de datos" **except** sqlite3.Error **as** e: **return False** , f"Error de base de datos: **{** e **}** " 

**13.9. Ejemplo completo: Sistema de gestión de personas** 

**151** 

**def** listar_todas(): _"""Lista todas las personas de la base de datos"""_ **with** sqlite3.connect('personas.db') **as** conexion: conexion.row_factory = sqlite3.Row cursor = conexion.cursor() cursor.execute('SELECT * FROM personas ORDER BY apellido, nombre') **return** cursor.fetchall() **def** buscar_por_documento(documento): _"""Busca una persona por su documento"""_ **with** sqlite3.connect('personas.db') **as** conexion: conexion.row_factory = sqlite3.Row cursor = conexion.cursor() cursor.execute(''' SELECT * FROM personas WHERE documento = ? ''', (documento,)) **return** cursor.fetchone() **def** buscar_por_apellido(apellido): _"""Busca personas por apellido (búsqueda parcial)"""_ **with** sqlite3.connect('personas.db') **as** conexion: conexion.row_factory = sqlite3.Row cursor = conexion.cursor() cursor.execute(''' SELECT * FROM personas WHERE apellido LIKE ? ORDER BY apellido, nombre ''', (f'% **{** apellido **}** %',)) **return** cursor.fetchall() **def** actualizar_edad(documento, nueva_edad): _"""Actualiza la edad de una persona"""_ **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' UPDATE personas SET edad = ? WHERE documento = ? ''', (nueva_edad, documento)) conexion.commit() **return** cursor.rowcount > 0 **def** eliminar_persona(documento): _"""Elimina una persona de la base de datos"""_ **with** sqlite3.connect('personas.db') **as** conexion: cursor = conexion.cursor() cursor.execute(''' DELETE FROM personas WHERE documento = ? ''', (documento,)) conexion.commit() **return** cursor.rowcount > 0 

**def** mostrar_menu(): 

**13. Bases de datos con sqlite3** 

**152** 

_"""Muestra el menú de opciones"""_ print(" **\n** " + "="*50) print("SISTEMA DE GESTIÓN DE PERSONAS") print("="*50) print("1. Insertar nueva persona") print("2. Listar todas las personas") print("3. Buscar por documento") print("4. Buscar por apellido") print("5. Actualizar edad") print("6. Eliminar persona") print("0. Salir") print("="*50) 

**def** main(): _"""Función principal del programa""" # Crear la tabla al iniciar_ crear_tabla() **while True** : mostrar_menu() opcion = input(" **\n** Seleccione una opción: ") **if** opcion �) "1": print(" **\n** --- INSERTAR NUEVA PERSONA ---") documento = input("Documento: ") nombre = input("Nombre: ") apellido = input("Apellido: ") **try** : edad = int(input("Edad: ")) exito, resultado = insertar_persona(documento, nombre, apellido, edad) **if** exito: print(f"✓Persona insertada con ID: **{** resultado **}** ") **else** : print(f"�Error: **{** resultado **}** ") **except ValueError** : print("�Error: La edad debe ser un número entero") **elif** opcion �) "2": print(" **\n** --- LISTADO DE PERSONAS ---") personas = listar_todas() **if** personas: print(f" **\n** Total: **{** len(personas) **}** persona(s) **\n** ") **for** persona **in** personas: print(f"ID: **{** persona['id'] **}** ") print(f" Documento: **{** persona['documento'] **}** ") print(f" Nombre: **{** persona['nombre'] **} {** persona['apellido'] **}** ") print(f" Edad: **{** persona['edad'] **}** años") print() **else** : print("No hay personas registradas") **elif** opcion �) "3": print(" **\n** --- BUSCAR POR DOCUMENTO ---") documento = input("Ingrese el documento: ") persona = buscar_por_documento(documento) **if** persona: print(f" **\n** Persona encontrada:") print(f" ID: **{** persona['id'] **}** ") print(f" Nombre: **{** persona['nombre'] **} {** persona['apellido'] **}** ") print(f" Documento: **{** persona['documento'] **}** ") 

**13.10. Patrón DAO (Data Access Object)** 

**153** 

print(f" Edad: **{** persona['edad'] **}** años") **else** : print("No se encontró ninguna persona con ese documento") **elif** opcion �) "4": print(" **\n** --- BUSCAR POR APELLIDO ---") apellido = input("Ingrese el apellido (o parte): ") personas = buscar_por_apellido(apellido) **if** personas: print(f" **\n** Se encontraron **{** len(personas) **}** persona(s): **\n** ") **for** persona **in** personas: print(f" **{** persona['nombre'] **} {** persona['apellido'] **}** " f"(DNI: **{** persona['documento'] **}** , **{** persona['edad'] **}** años)") **else** : print("No se encontraron personas con ese apellido") **elif** opcion �) "5": print(" **\n** --- ACTUALIZAR EDAD ---") documento = input("Documento de la persona: ") **try** : nueva_edad = int(input("Nueva edad: ")) **if** actualizar_edad(documento, nueva_edad): print("✓Edad actualizada correctamente") **else** : print("�No se encontró ninguna persona con ese documento") **except ValueError** : print("�Error: La edad debe ser un número entero") **elif** opcion �) "6": print(" **\n** --- ELIMINAR PERSONA ---") documento = input("Documento de la persona a eliminar: ") confirmacion = input("¿Está seguro? (s/n): ") **if** confirmacion.lower() �) 's': **if** eliminar_persona(documento): print("✓Persona eliminada correctamente") **else** : print("�No se encontró ninguna persona con ese documento") **else** : print("Operación cancelada") **elif** opcion �) "0": print(" **\n** ¡Hasta luego!") **break else** : print(" **\n** �Opción inválida. Intente nuevamente.") **if** __name__ �) "__main__": main() 

##### **13.10 Patrón DAO (Data Access Object)** 

Una práctica habitual para organizar el acceso a la base de datos consiste en encapsular las operaciones CRUD en clases especializadas, denominadas _DAO_ ( _Data Access Object_ ). Este esquema reduce la duplicación de código, centraliza los detalles de conexión y facilita la realización de pruebas. 

**13. Bases de datos con sqlite3** 

**154** 

Una clase DAO concentra las operaciones de creación, consulta, actualización y eliminación sobre una tabla. Es habitual de�nir métodos como crear() para insertar registros, obtener_por_id() —o obtener_por_documento(), según el criterio de búsqueda— para recuperar una �la, listar() para obtener la totalidad de los registros, y actualizar() y eliminar() para modi�car y suprimir �las respectivamente. Cada método encapsula la sentencia SQL correspondiente y expone una interfaz simple, de modo que el resto de la aplicación queda desacoplada de los detalles de acceso a los datos. 

El siguiente ejemplo presenta una clase PersonaDAO que concentra las operaciones de creación, consulta, actualización y eliminación sobre la tabla personas: 

**import sqlite3 class PersonaDAO** : **def** __init__(self, db_path='personas.db'): self.db_path = db_path **def** _conn(self): **return** sqlite3.connect(self.db_path) **def** crear(self, documento, nombre, apellido, edad= **None** ): **with** self._conn() **as** cx: cx.execute(''' INSERT INTO personas (documento, nombre, apellido, edad) VALUES (?, ?, ?, ?) ''', (documento, nombre, apellido, edad)) **def** obtener_por_documento(self, documento): **with** self._conn() **as** cx: cx.row_factory = sqlite3.Row cur = cx.execute('SELECT * FROM personas WHERE documento = ?', �→ (documento,)) **return** cur.fetchone() **def** actualizar_edad(self, documento, edad): **with** self._conn() **as** cx: cur = cx.execute('UPDATE personas SET edad=? WHERE documento=?', (edad, �→ documento)) **return** cur.rowcount **def** eliminar(self, documento): **with** self._conn() **as** cx: cur = cx.execute('DELETE FROM personas WHERE documento=?', (documento,)) **return** cur.rowcount 

Cuando la base de datos posee más de una tabla, la práctica habitual consiste en de�nir un DAO por cada tabla principal, es decir, por cada entidad representada en el esquema. Así, en una base ventas.db que contiene las tablas clientes y pedidos, se de�nen las clases ClienteDAO y PedidoDAO; las consultas de cada 

**13.10. Patrón DAO (Data Access Object)** 

**155** 

tabla quedan así aisladas en la clase a la que corresponden. 

Las relaciones de uno a muchos se resuelven por medio de las claves foráneas. En la relación que vincula a los clientes con sus pedidos, un cliente posee muchos pedidos; la tabla pedidos contiene la columna cliente_id que referencia a un registro de clientes. El DAO de la tabla que contiene la clave foránea recibe el identi�cador de la �la relacionada en sus operaciones de creación y ofrece métodos de consulta que toman ese identi�cador como criterio, como obtener_por_cliente(): 

**import sqlite3 class PedidoDAO** : **def** __init__(self, db_path='ventas.db'): self.db_path = db_path **def** _conn(self): **return** sqlite3.connect(self.db_path) **def** crear(self, cliente_id, fecha, total): **with** self._conn() **as** cx: cur = cx.execute(''' INSERT INTO pedidos (cliente_id, fecha, total) VALUES (?, ?, ?) ''', (cliente_id, fecha, total)) **return** cur.lastrowid **def** obtener_por_cliente(self, cliente_id): **with** self._conn() **as** cx: cx.row_factory = sqlite3.Row cur = cx.execute(''' SELECT * FROM pedidos WHERE cliente_id = ? ''', (cliente_id,)) **return** cur.fetchall() 

Para las consultas que combinan información de ambas tablas, como obtener el nombre del cliente junto con cada uno de sus pedidos, se emplean sentencias JOIN que integran los datos de las tablas relacionadas; estas consultas pueden incorporarse como métodos del DAO de la misma manera que las anteriores. 

Las relaciones de muchos a muchos no pueden representarse con una sola clave foránea: se resuelven introduciendo una tabla intermedia que vincula las dos tablas principales. Cuando esa tabla contiene únicamente las claves foráneas a ambas tablas, que en conjunto forman su clave primaria, su único propósito es registrar las asociaciones entre los registros. Por ejemplo, si un pedido puede incluir varios artículos y un artículo puede pertenecer a varios pedidos, se de�ne una tabla pedido_articulo con las columnas 

**13. Bases de datos con sqlite3** 

**156** 

pedido_id y articulo_id. Las operaciones de esta tabla, como agregar_articulo(pedido_id, articulo_id), quitar_articulo(pedido_id, articulo_id) u obtener_articulos_del_pedido(pedido_id), pueden ubicarse en el DAO de una de las tablas principales o en un DAO dedicado a la tabla de unión. 

El segundo caso se presenta cuando la tabla intermedia, además de las claves foráneas, almacena datos propios; en esa situación deja de ser una simple tabla de unión y pasa a constituir una entidad del dominio. Es lo que ocurre con detalle_pedido, tabla intermedia entre pedidos y articulos: cada una de sus �las corresponde a un artículo incluido en un pedido y, junto a las claves pedido_id y articulo_id, conserva información propia como la cantidad comprada o el precio unitario aplicado. Por tratarse de una entidad, la tabla recibe su propio DAO, DetallePedidoDAO, con las operaciones completas de creación, consulta, actualización y eliminación: su método crear() recibe los identi�cadores de ambos extremos junto con los datos propios del detalle, y un método como obtener_por_pedido(pedido_id) recupera todos los detalles que componen un pedido. Tanto en uno como en otro caso, las consultas que integran información de las tablas relacionadas se componen mediante JOIN y pueden incorporarse como métodos de los DAO involucrados. 

### **ORM con SQLAlchemy** 

##### **14.1 Introducción a los ORM** 

Los _ORM_ por ( _Object-Relational Mapping_ ), constituyen una herramienta ampliamente utilizada en la programación, todos los lenguajes incluyen al menos una librería con esta funcionalidad, tales como _JPA_ en Java y con _Sequelize_ en JavaScript. 

La existencia de los ORM se explica por el **desajuste** ( _impedance mismatch_ ) que se produce entre dos modelos de representación de la información: el modelo relacional, organizado en tablas, �las y claves, y el modelo orientado a objetos, organizado en clases, objetos y relaciones. La brecha entre ambos es doble. Por un lado, existe una **brecha sintáctica** : el modelo relacional se manipula mediante SQL, un lenguaje declarativo cuyas sentencias deben escribirse y gestionarse en forma de cadenas de texto, mientras que el modelo orientado a objetos se manipula mediante llamadas a métodos sobre objetos. Por el otro, subsiste una **brecha semántica** : una �la no es equivalente a un objeto, ya que la �la no posee identidad más allá de sus datos, en tanto que el objeto combina identidad, estado y comportamiento; del mismo modo, una tabla no es una clase. 

Un ORM automatiza la traducción entre ambos mundos: empareja tablas en clases, �las en objetos, columnas en atributos y transacciones en sesiones de trabajo. Al hacerlo, reduce de manera signi�cativa la brecha sintáctica y semántica, y permite que el código de persistencia se exprese en los términos del modelo orientado a objetos. 

157 

**14. ORM con SQLAlchemy** 

**158** 

##### **14.2 SQLAlchemy** 

SQLAlchemy es el ORM más completo y utilizado del ecosistema de Python. Proporciona dos enfoques complementarios para trabajar con bases de datos: 

- **SQLAlchemy Core** : Una capa de abstracción SQL que permite construir consultas de forma programática 

- **SQLAlchemy ORM** : El ORM propiamente dicho, que permite trabajar con objetos Python 

En este capítulo se trabajará exclusivamente con SQLAlchemy ORM, que es el enfoque más utilizado para aplicaciones orientadas a objetos. 

###### **14.2.1 Instalación** 

SQLAlchemy no forma parte de la biblioteca estándar de Python, por lo que debe instalarse previamente mediante el administrador de paquetes pip: 

pip install sqlalchemy 

##### **14.3 Con�guración básica** 

Para comenzar a trabajar con SQLAlchemy es necesario realizar tres pasos fundamentales: 

1. Crear un motor de base de datos ( _Engine_ ) 

2. Declarar una clase base para los modelos 

3. Crear una sesión para interactuar con la base de datos 

**from sqlalchemy import** create_engine **from sqlalchemy.orm import** declarative_base, sessionmaker _# 1. Crear el motor de base de datos_ engine = create_engine('sqlite:�))personas.db', echo= **True** ) 

_# 2. Crear la clase base para los modelos_ Base = declarative_base() 

_# 3. Crear una fábrica de sesiones_ Session = sessionmaker(bind=engine) 

**14.3. Con�guración básica** 

**159** 

El parámetro echo= **True** hace que SQLAlchemy imprima en consola todas las consultas SQL que ejecuta, lo cual resulta de gran utilidad durante la depuración. 

###### **14.3.1 Arquitectura y componentes principales** 

La capa ORM de SQLAlchemy se apoya en una serie de componentes bien diferenciados. Comprender el rol de cada uno de ellos facilita el diseño y la depuración de las aplicaciones de persistencia: 

- **Engine** Representa la _puerta de entrada_ a la base de datos. Gestiona el _pool_ de conexiones y sabe cómo emitir instrucciones SQL a un _DBAPI driver_ . No mantiene estado de objetos de negocio. 

- **Dialect** Capa que traduce construcciones genéricas de SQLAlchemy a la sintaxis especí�ca del motor (SQLite, PostgreSQL, etc.). Se selecciona implícitamente según la URL (por ejemplo, sqlite:�))�))). 

- **MetaData** Colección de objetos que describen esquemas de tablas (nombres, columnas, claves, índices). Se accede vía Base.metadata cuando se usa el estilo declarativo. 

- **Declarative Base** Clase base desde la que heredan los modelos. Conecta la de�nición de atributos de clase con las columnas de la tabla y registra la tabla dentro de los metadatos. 

- **Session** Unidad de trabajo ( _Unit of Work_ ). Acumula cambios sobre objetos (nuevos, modi�cados, eliminados) y coordina el envío de dichas mutaciones a la base de datos dentro de una transacción. 

- **Mapper** Objeto interno que enlaza una clase Python con su tabla y reglas de persistencia. Se crea automáticamente al declarar la clase. 

###### **14.3.2 Ciclo de vida y estados de los objetos** 

Las instancias gestionadas por la sesión atraviesan distintos **estados** a lo largo de su ciclo de vida: 

- **Transient** (transitorio): Objeto recién creado en Python, aún no asociado a una sesión ni a ninguna identidad en la base de datos. 

**14. ORM con SQLAlchemy** 

**160** 

- **Pending** : Tras ejecutar session.add(obj) el objeto queda en cola para inserción; todavía no se emitió SQL de INSERT (salvo que ocurra un flush anticipado). 

- **Persistent** : Luego de un flush (implícito o explícito) el objeto obtiene identidad (clave primaria) y está sincronizado con la �la en la base de datos. 

- **Dirty** : Subestado de _Persistent_ ; la sesión detectó cambios en atributos y los enviará al próximo flush. 

- **Detached** : El objeto ya no está asociado a ninguna sesión (por cierre de sesión o expulsión explícita con session.expunge(obj)). Puede leerse pero los cambios no se rastrean hasta volver a asociarlo con session.merge(obj). 

- **Deleted** : Marcado para eliminación (session.delete(obj)). La eliminación física se concreta al flush / commit. 

###### **Flush vs Commit** 

- **Flush** : Sincroniza el estado pendiente de la sesión con la base de datos emitiendo INSERT/UPDATE/DELETE dentro de la transacción abierta. No con�rma la transacción. 

- **Commit** : Finaliza (con�rma) la transacción. Antes ejecuta un �ush implícito si hay cambios pendientes. 

Un rollback() revierte la transacción en curso: los objetos _pending_ vuelven al estado _transient_ y las modi�caciones _dirty_ se descartan. 

###### **14.3.3 Patrón Unidad de Trabajo (Unit of Work)** 

La sesión mantiene, además, un registro interno de identidades ( _identity map_ ) que garantiza que, para una misma clave primaria, exista una única instancia viva durante el ciclo de trabajo. Esto evita inconsistencias y facilita el rastreo de los cambios diferenciales al momento de emitir SQL. 

###### **14.3.4 Sintaxis habitual de creación del Engine** 

A continuación se presentan los formatos de URL más habituales junto con algunos de los parámetros más frecuentes de create_engine(): 

**14.3. Con�guración básica** 

**161** 

**from sqlalchemy import** create_engine _# Formatos de URL comunes # SQLite (archivo local)_ create_engine('sqlite:�))app.db') _# Memoria (solo duración del proceso)_ create_engine('sqlite:�)):memory:') _# PostgreSQL (requiere driver psycopg2 instalado)_ create_engine('postgresql+psycopg2�))usuario:clave@localhost:5432/base') _# MySQL (driver mysqlclient o pymysql)_ create_engine('mysql+pymysql�))usuario:clave@localhost:3306/base?charset=utf8mb4') _# Parámetros frecuentes_ create_engine( 'sqlite:�))app.db', echo= **False** , _# Mostrar o no SQL_ future= **True** , _# Estilo 2.x (select() explícito)_ pool_pre_ping= **True** _# Verificar conexiones antes de usar_ ) 

###### **14.3.5 Creación de sesiones: patrones de uso** 

Se recomienda crear una _fábrica_ de sesiones con sessionmaker y obtener, a partir de ella, instancias de sesión de corta duración (una por transacción, petición web o caso de uso): 

**from sqlalchemy.orm import** sessionmaker SessionLocal = sessionmaker(bind=engine, autoflush= **True** , expire_on_commit= **True** ) _# Obtención y uso mínimo_ session = SessionLocal() **try** : _# Operaciones_ �)) session.commit() **except Exception** : session.rollback() **raise finally** : session.close() 

###### **Parámetros relevantes de sessionmaker** 

- autoflush (True por defecto): Si está activo, se ejecuta un �ush automático antes de ciertas consultas para garantizar coherencia. 

- expire_on_commit (True por defecto): Al con�rmar la transacción, los atributos cargados se marcan como expirados; un nuevo acceso re-consulta datos para asegurar frescura. 

**14. ORM con SQLAlchemy** 

**162** 

###### **14.3.6 Resumen de métodos clave de Session** 

**add(obj)** Coloca un objeto en estado pending. 

**add_all(lista)** Coloca una colección de objetos en estado pending. 

**commit()** Con�rma la transacción (incluye �ush implícito). 

**rollback()** Revierte cambios desde el último commit. 

**�ush()** Fuerza sincronización sin cerrar la transacción. 

**delete(obj)** Marca para eliminación. 

**merge(obj)** Reconcilia un objeto detached con la sesión, devolviendo la instancia gestionada. 

**refresh(obj)** Vuelve a consultar la �la y actualiza atributos. 

**expunge(obj)** Saca un objeto de la sesión (pasa a detached). 

**close()** Cierra la sesión y su transacción implícita si está activa. 

##### **14.4 De�nición de modelos** 

En SQLAlchemy, cada tabla de la base de datos se representa mediante una clase Python que hereda de la clase Base de�nida en la sección anterior. Los atributos de la clase representan las columnas de la tabla, y en ella también pueden incorporarse los métodos que implementan la lógica de negocio de la entidad: 

**from sqlalchemy import** Column, Integer, String 

**class Persona** (Base): __tablename__ = 'personas' id = Column(Integer, primary_key= **True** , autoincrement= **True** ) documento = Column(String(20), nullable= **False** , unique= **True** ) nombre = Column(String(100), nullable= **False** ) apellido = Column(String(100), nullable= **False** ) edad = Column(Integer) **def** __repr__(self): **return** f"<Persona(nombre=' **{** self.nombre **}** ', apellido=' **{** self.apellido **}** ')>" **def** __str__(self): **return** f" **{** self.nombre **} {** self.apellido **}** (DNI: **{** self.documento **}** )" 

**14.5. Creación de tablas** 

**163** 

###### **14.4.1 Tipos de datos en SQLAlchemy** 

SQLAlchemy proporciona un conjunto de tipos de datos que se mapean automáticamente a los tipos nativos de cada motor de base de datos: 

|**Tipo SQLAlchemy**|**Descripción**|
|---|---|
|Integer|Números enteros|
|String(length)|Cadenas de longitud �ja o variable|
|Text|Cadenas de texto largo sin límite de longitud|
|Float|Números de punto �otante|
|Boolean|Valores booleanos|
|Date|Fechas (año, mes, día)|
|DateTime|Fechas con hora|
|Time|Hora del día|
|LargeBinary|Datos binarios (BLOB)|



###### **14.4.2 Restricciones de columna** 

Las restricciones se especi�can como parámetros al momento de declarar cada columna: 

- primary_key= **True** : De�ne la columna como clave primaria 

- nullable= **False** : La columna no puede contener valores NULL 

- unique= **True** : Todos los valores deben ser únicos 

- default=valor: Valor por defecto 

- autoincrement= **True** : Genera valores automáticamente 

##### **14.5 Creación de tablas** 

Una vez de�nidos los modelos, es necesario crear las tablas correspondientes en la base de datos. En SQLAlchemy esta tarea se resuelve con una única instrucción: 

_# Crear todas las tablas definidas_ Base.metadata.create_all(engine) 

Este comando examina todos los modelos que heredan de Base y crea las tablas correspondientes en el caso de que aún no existan. 

**14. ORM con SQLAlchemy** 

**164** 

##### **14.6 Operaciones CRUD con SQLAlchemy** 

Esta sección describe la sintaxis fundamental de las operaciones de persistencia siguiendo el patrón de Unidad de Trabajo presentado anteriormente. Cada operación modi�ca el estado de los objetos en memoria y di�ere su sincronización física con la base de datos hasta que se produce un �ush o un commit. 

###### **14.6.1 Resumen rápido de sintaxis de consulta** 

SQLAlchemy ofrece dos estilos de construcción de consultas, que coexisten en la versión actual de la librería. El estilo clásico, ofrecido des de la primera versión de la librería, se basa en session.query(); el estilo moderno, formalizado en versiones posteriores, se basa en el objeto select(). En este capítulo se utiliza el estilo clásico pero conviene conocer ambos: el primero sigue presente en gran parte del código existente, mientras que el segundo constituye el camino recomendado para los desarrollos nuevos. 

El estilo clásico modela la consulta como una cadena de llamadas a métodos. La expresión session.query(Persona) indica la entidad cuyas �las se desean consultar; a partir de ella, cada método agrega una cláusula y devuelve un nuevo objeto sobre el cual se encadenan las llamadas siguientes: filter() establece las condiciones, order_by() el ordenamiento y limit() la cantidad de �las. La traducción a SQL ocurre recién cuando se invoca un método terminal, como all(), first() o count(); antes de ese momento la consulta es un valor en construcción, no una ejecución. Los criterios se expresan mediante operadores de comparación aplicados sobre los atributos de la clase, como Persona.apellido �) 'Pérez', que el ORM sobrecarga para representar condiciones SQL: 

session.query(Persona).filter(Persona.apellido �) �→ 'Pérez').order_by(Persona.nombre).limit(10) 

El estilo 2.x modi�ca ese esquema al separar la construcción de la consulta de su ejecución. La consulta se representa como un objeto select() independiente, que se asigna a una variable y sobre el cual se agregan las cláusulas con los métodos where(), order_by() y limit(). La ejecución se delega a la sesión mediante session.execute(), que devuelve un objeto Result del cual se extraen las entidades resultantes con result.scalars().all(). La ventaja de este esquema es que la consulta constituye un valor reutilizable y componible: puede asignar- 

**14.6. Operaciones CRUD con SQLAlchemy** 

**165** 

se, pasarse como argumento a una función o combinarse con otras antes de decidir cómo se ejecuta, en lugar de quedar atada a una cadena de llamadas: 

**from sqlalchemy import** select stmt = select(Persona).where(Persona.apellido �) �→ 'Pérez').order_by(Persona.nombre).limit(10) result = session.execute(stmt) personas = result.scalars().all() 

Cuando una condición combina varias cláusulas, estas se componen mediante los operadores booleanos and_(), or_() y not_(), que reciben las condiciones como argumentos y pueden anidarse para expresar �ltros complejos dentro de filter(): 

**from sqlalchemy import** and_, or_, not_ session.query(Persona).filter( and_( Persona.edad �) 18, or_(Persona.apellido.like('P%'), Persona.apellido.like('G%')), not_(Persona.nombre �) 'Test') ) ).all() 

Las cláusulas de comparación pueden utilizar los operadores �), �), >, �), <, �), like(), in_([�))]), between(a,b), is_( **None** ) y isnot( **None** ). 

###### **14.6.2 Inserción de �las** 

Para insertar una nueva �la se crea una instancia del modelo y se la agrega a la sesión mediante session.add(): 

_# Crear una sesión_ session = Session() _# Crear una nueva persona_ persona = Persona( documento='12345678', nombre='Juan', apellido='Pérez', edad=30 ) _# Agregar a la sesión_ session.add(persona) _# Confirmar los cambios_ 

**14. ORM con SQLAlchemy** 

**166** 

session.commit() print(f"Persona insertada con ID: **{** persona.id **}** ") _# Cerrar la sesión_ session.close() 

Para insertar varias �las en una misma operación se utiliza session.add_all(): 

session = Session() personas = [ Persona(documento='11111111', nombre='María', apellido='González', edad=25), Persona(documento='22222222', nombre='Pedro', apellido='Martínez', edad=35), Persona(documento='33333333', nombre='Ana', apellido='López', edad=28) ] session.add_all(personas) session.commit() session.close() 

###### **14.6.3 Consultas** 

Para obtener todas las �las de una tabla se ejecuta la consulta con session.query(Persona).all(); el método all() materializa el resultado y devuelve una lista de instancias del modelo, que se recorren como cualquier colección de objetos: 

session = Session() _# Obtener todas las personas_ personas = session.query(Persona).all() **for** persona **in** personas: print(persona) session.close() 

Las condiciones de �ltrado se incorporan con filter_by(), que recibe los valores buscados por nombre de columna, o con filter(), que admite condiciones más generales construidas con los atributos de la clase y los operadores de comparación mencionados en la sección anterior. El método first() ejecuta la consulta y devuelve la primera �la, o **None** si ninguna la satisface: 

session = Session() _# Buscar por documento_ persona = session.query(Persona).filter_by(documento='12345678').first() 

**14.6. Operaciones CRUD con SQLAlchemy** 

**167** 

print(persona) _# Buscar personas mayores de 25 años_ mayores = session.query(Persona).filter(Persona.edad > 25).all() **for** persona **in** mayores: print(persona) _# Buscar con LIKE_ apellido_buscar = 'Pér%' personas = session.query(Persona).filter( Persona.apellido.like(apellido_buscar) ).all() session.close() 

El ordenamiento se agrega con order_by(), que recibe una o más columnas en el orden de prioridad deseado; aplicar desc() sobre una columna indica que el orden es descendente: 

session = Session() _# Ordenar por apellido y luego por nombre_ personas = session.query(Persona).order_by( Persona.apellido, Persona.nombre ).all() _# Ordenar de forma descendente_ personas_desc = session.query(Persona).order_by( Persona.edad.desc() ).all() session.close() 

La cantidad de �las devueltas se restringe con limit(), mientras que get() recupera directamente una �la a partir de su clave primaria: 

session = Session() _# Obtener las primeras 5 filas_ primeros_cinco = session.query(Persona).limit(5).all() _# Obtener una fila específica por ID_ persona = session.query(Persona).get(1) _# ID = 1_ session.close() 

###### **14.6.4 Actualización de �las** 

Para actualizar una �la, primero se la busca mediante una consulta, luego se modi�can sus atributos y �nalmente se con�rman los cambios: 

**14. ORM con SQLAlchemy** 

**168** 

session = Session() _# Buscar la persona_ persona = session.query(Persona).filter_by(documento='12345678').first() **if** persona: _# Modificar atributos_ persona.edad = 31 _# Confirmar cambios_ session.commit() print("Persona actualizada") **else** : print("Persona no encontrada") session.close() 

Además de la actualización objeto por objeto, es posible efectuar actualizaciones masivas que modi�can varias �las a la vez: 

session = Session() _# Incrementar la edad de todas las personas_ session.query(Persona).update({Persona.edad: Persona.edad + 1}) session.commit() session.close() 

###### **14.6.5 Eliminación de �las** 

Para eliminar una �la, se la busca y se la marca para eliminación con session.delete(): 

session = Session() _# Buscar la persona_ persona = session.query(Persona).filter_by(documento='12345678').first() **if** persona: _# Eliminar_ session.delete(persona) session.commit() print("Persona eliminada") **else** : print("Persona no encontrada") session.close() 

La eliminación masiva se efectúa a partir de una consulta: 

**14.7. Context managers y** **<u>gestión de sesiones</u>** 

**169** 

session = Session() _# Eliminar todas las personas menores de 18 años_ session.query(Persona).filter(Persona.edad < 18).delete() session.commit() session.close() 

##### **14.7 Context managers y gestión de sesiones** 

Para garantizar que las sesiones se cierren correctamente, es recomendable encapsular su ciclo de vida en un context manager que con�rme los cambios cuando la operación se completa, los revierta ante un error y cierre la sesión en todos los casos: 

**from contextlib import** contextmanager @contextmanager **def** obtener_session(): session = Session() **try** : **yield** session session.commit() **except Exception** : session.rollback() **raise finally** : session.close() _# Uso_ **with** obtener_session() **as** session: persona = Persona( documento='44444444', nombre='Luis', apellido='Rodríguez', edad=42 ) session.add(persona) 

##### **14.8 Relaciones entre tablas** 

Una de las características más potentes de SQLAlchemy es el manejo de relaciones entre tablas, que permite recorrer los vínculos del modelo en ambos sentidos sin escribir consultas SQL. 

###### **14.8.1 Relación uno a muchos (One-to-Many)** 

El caso más habitual es la relación uno a muchos. Por ejemplo, un cliente puede tener múltiples órdenes de compra: 

**14. ORM con SQLAlchemy** 

**170** 

**from sqlalchemy import** ForeignKey **from sqlalchemy.orm import** relationship **class Cliente** (Base): __tablename__ = 'clientes' id = Column(Integer, primary_key= **True** ) nombre = Column(String(100), nullable= **False** ) email = Column(String(100), unique= **True** ) _# Relación uno a muchos_ ordenes = relationship('Orden', back_populates='cliente') **def** __repr__(self): **return** f"<Cliente(nombre=' **{** self.nombre **}** ')>" **class Orden** (Base): __tablename__ = 'ordenes' id = Column(Integer, primary_key= **True** ) numero = Column(String(50), unique= **True** ) total = Column(Float) cliente_id = Column(Integer, ForeignKey('clientes.id')) _# Relación muchos a uno_ cliente = relationship('Cliente', back_populates='ordenes') **def** __repr__(self): **return** f"<Orden(numero=' **{** self.numero **}** ', total= **{** self.total **}** )>" 

Uso de la relación: 

_# Crear tablas_ Base.metadata.create_all(engine) **with** obtener_session() **as** session: _# Crear un cliente_ cliente = Cliente(nombre='Juan Pérez', email='juan@example.com') _# Crear órdenes para el cliente_ orden1 = Orden(numero='ORD-001', total=150.50) orden2 = Orden(numero='ORD-002', total=200.00) _# Asociar órdenes al cliente_ cliente.ordenes.append(orden1) cliente.ordenes.append(orden2) session.add(cliente) _# Consultar_ **with** obtener_session() **as** session: cliente = session.query(Cliente).filter_by(nombre='Juan Pérez').first() print(f"Cliente: **{** cliente.nombre **}** ") print(f"Órdenes:") **for** orden **in** cliente.ordenes: print(f" - **{** orden.numero **}** : $ **{** orden.total **}** ") 

**14.8. Relaciones entre tablas** 

**171** 

###### **14.8.2 Relación muchos a uno (Many-to-One)** 

La relación muchos a uno constituye, simplemente, el lado inverso de la relación uno a muchos. En el ejemplo precedente, varias órdenes pertenecen a un único cliente; acceder a la relación desde el lado de la orden permite obtener el cliente asociado: 

**with** obtener_session() **as** session: orden = session.query(Orden).filter_by(numero='ORD-001').first() print(f"Orden: **{** orden.numero **}** ") print(f"Cliente: **{** orden.cliente.nombre **}** ") print(f"Email: **{** orden.cliente.email **}** ") 

###### **14.8.3 Relación muchos a muchos (Many-to-Many)** 

###### **Sin atributos adicionales en la tabla intermedia** 

Cuando un objeto puede vincularse con varios objetos del otro lado y viceversa, se recurre a una relación muchos a muchos mediada por una tabla de asociación. Por ejemplo, un estudiante puede inscribirse en múltiples cursos, y un curso puede contar con múltiples estudiantes: 

**from sqlalchemy import** Table _# Tabla de asociación (intermedia)_ estudiante_curso = Table( 'estudiante_curso', Base.metadata, Column('estudiante_id', Integer, ForeignKey('estudiantes.id')), Column('curso_id', Integer, ForeignKey('cursos.id')) ) **class Estudiante** (Base): __tablename__ = 'estudiantes' id = Column(Integer, primary_key= **True** ) nombre = Column(String(100), nullable= **False** ) matricula = Column(String(20), unique= **True** ) _# Relación muchos a muchos_ cursos = relationship( 'Curso', secondary=estudiante_curso, back_populates='estudiantes' ) **def** __repr__(self): **return** f"<Estudiante(nombre=' **{** self.nombre **}** ')>" **class Curso** (Base): 

**14. ORM con SQLAlchemy** 

**172** 

__tablename__ = 'cursos' id = Column(Integer, primary_key= **True** ) codigo = Column(String(20), unique= **True** ) nombre = Column(String(100), nullable= **False** ) creditos = Column(Integer) _# Relación muchos a muchos_ estudiantes = relationship( 'Estudiante', secondary=estudiante_curso, back_populates='cursos' ) **def** __repr__(self): **return** f"<Curso(codigo=' **{** self.codigo **}** ', nombre=' **{** self.nombre **}** ')>" 

###### Uso: 

_# Crear tablas_ Base.metadata.create_all(engine) **with** obtener_session() **as** session: _# Crear estudiantes_ est1 = Estudiante(nombre='Ana García', matricula='EST-001') est2 = Estudiante(nombre='Carlos López', matricula='EST-002') _# Crear cursos_ curso1 = Curso(codigo='POO-101', nombre='Programación Orientada a Objetos', �→ creditos=6) curso2 = Curso(codigo='BD-201', nombre='Bases de Datos', creditos=4) curso3 = Curso(codigo='WEB-301', nombre='Desarrollo Web', creditos=5) _# Inscribir estudiantes en cursos_ est1.cursos.extend([curso1, curso2]) est2.cursos.extend([curso1, curso3]) session.add_all([est1, est2, curso1, curso2, curso3]) _# Consultar inscripciones_ **with** obtener_session() **as** session: estudiante = session.query(Estudiante).filter_by(matricula='EST-001').first() print(f"Estudiante: **{** estudiante.nombre **}** ") print(f"Cursos inscritos:") **for** curso **in** estudiante.cursos: print(f" - **{** curso.codigo **}** : **{** curso.nombre **}** ( **{** curso.creditos **}** créditos)") _# Desde el lado del curso_ curso = session.query(Curso).filter_by(codigo='POO-101').first() print(f" **\n** Curso: **{** curso.nombre **}** ") print(f"Estudiantes inscritos:") **for** est **in** curso.estudiantes: print(f" - **{** est.nombre **}** ( **{** est.matricula **}** )") 

**14.8. Relaciones entre tablas** 

**173** 

###### **Con atributos adicionales en la tabla intermedia** 

Cuando la tabla intermedia necesita almacenar información adicional (por ejemplo, la nota obtenida por el estudiante en el curso o la fecha de inscripción), una tabla de asociación simple ya no resulta su�ciente. En ese caso debe modelarse una **clase de asociación** ( _Association Object_ ) explícita, con una clave primaria compuesta y relaciones muchos a uno hacia las entidades que vincula: 

**from sqlalchemy import** Date **from datetime import** date **class Inscripcion** (Base): __tablename__ = 'inscripciones' estudiante_id = Column(Integer, ForeignKey('estudiantes.id'), primary_key= **True** ) curso_id = Column(Integer, ForeignKey('cursos.id'), primary_key= **True** ) fecha_inscripcion = Column(Date, default=date.today) nota_final = Column(Float) estado = Column(String(20)) _# 'cursando', 'aprobado', 'desaprobado' # Relaciones_ estudiante = relationship('Estudiante', back_populates='inscripciones') curso = relationship('Curso', back_populates='inscripciones') **def** __repr__(self): **return** f"<Inscripcion(estudiante_id= **{** self.estudiante_id **}** , �→ curso_id= **{** self.curso_id **}** )>" **class Estudiante** (Base): __tablename__ = 'estudiantes' id = Column(Integer, primary_key= **True** ) nombre = Column(String(100), nullable= **False** ) matricula = Column(String(20), unique= **True** ) _# Relación con la tabla de asociación_ inscripciones = relationship('Inscripcion', back_populates='estudiante') **def** __repr__(self): **return** f"<Estudiante(nombre=' **{** self.nombre **}** ')>" **class Curso** (Base): __tablename__ = 'cursos' id = Column(Integer, primary_key= **True** ) codigo = Column(String(20), unique= **True** ) nombre = Column(String(100), nullable= **False** ) creditos = Column(Integer) _# Relación con la tabla de asociación_ inscripciones = relationship('Inscripcion', back_populates='curso') **def** __repr__(self): **return** f"<Curso(codigo=' **{** self.codigo **}** ', nombre=' **{** self.nombre **}** ')>" 

**14. ORM con SQLAlchemy** 

**174** 

El siguiente fragmento crea inscripciones junto con sus datos adicionales y muestra cómo consultar la información asociada: 

_# Crear tablas_ Base.metadata.create_all(engine) **with** obtener_session() **as** session: _# Crear estudiante y curso_ estudiante = Estudiante(nombre='María Rodríguez', matricula='EST-003') curso = Curso(codigo='ALG-101', nombre='Algoritmos', creditos=6) _# Crear inscripción con datos adicionales_ inscripcion = Inscripcion( estudiante=estudiante, curso=curso, fecha_inscripcion=date(2025, 3, 1), estado='cursando' ) session.add_all([estudiante, curso, inscripcion]) _# Consultar con datos de inscripción_ **with** obtener_session() **as** session: estudiante = session.query(Estudiante).filter_by(matricula='EST-003').first() print(f"Estudiante: **{** estudiante.nombre **}** ") print(f"Inscripciones:") **for** insc **in** estudiante.inscripciones: print(f" - **{** insc.curso.nombre **}** ") print(f" Fecha: **{** insc.fecha_inscripcion **}** ") print(f" Estado: **{** insc.estado **}** ") **if** insc.nota_final: print(f" Nota: **{** insc.nota_final **}** ") _# Actualizar nota_ **with** obtener_session() **as** session: inscripcion = session.query(Inscripcion).filter_by( estudiante_id=1, curso_id=1 ).first() inscripcion.nota_final = 8.5 inscripcion.estado = 'aprobado' 

###### **14.8.4 Parámetros importantes de relationship** 

**back_populates** De�ne el atributo complementario en la otra clase para mantener sincronía bidireccional explícita. 

- **backref** Crea automáticamente el atributo inverso (atajo sintáctico). Útil para reducir código cuando no se requieren con�guraciones diferenciadas en cada lado. 

- **cascade** Controla cómo se propagan operaciones (save-update, delete, delete-orphan, etc.). Ejemplo: cascade="all, delete-orphan" en una relación uno-a-muchos que 

**14.9. Ejemplo completo: Sistema de biblioteca** 

**175** 

posee semántica de composición fuerte. 

- **lazy** Estrategia de carga: 'select' (por defecto), 'joined' (JOIN inmediato), 'subquery', 'selectin' (carga por lote e�ciente), 'raise' (lanza error si se accede sin haberla cargado), 'noload'. 

- **uselist** Booleano que indica si el atributo representa una colección (True) o una única entidad (False). Útil para relaciones uno-a-uno. 

- **secondary** Tabla de asociación utilizada para relaciones muchos-a-muchos sin entidad intermedia explícita. 

- **secondaryjoin** Condición adicional para unir la tabla secundaria en relaciones más complejas (por ejemplo, claves compuestas o auto-relaciones). 

**order_by** Orden por defecto de la colección (ej.: order_by="Orden.fecha.desc()"). 

**passive_deletes** Optimiza eliminaciones delegándolas a la base (requiere ON DELETE CASCADE en la clave foránea). 

###### **14.8.5 Elección del patrón de muchos-a-muchos** 

- **Tabla de asociación simple** : Cuando solo se necesitan claves foráneas sin atributos adicionales. 

- **Objeto de asociación (Association Object)** : Cuando se requieren campos extra (fecha, estado, métricas); se modela como clase y se de�ne dos relaciones muchos-a-uno. 

##### **14.9 Ejemplo completo: Sistema de biblioteca** 

El siguiente ejemplo integra todos los conceptos vistos en el capítulo: 

###### **Sistema de biblioteca con SQLAlchemy** 

_""" Sistema de gestión de biblioteca usando SQLAlchemy ORM. Demuestra relaciones uno a muchos y muchos a muchos con datos adicionales. """_ 

**from sqlalchemy import** create_engine, Column, Integer, String, Date, ForeignKey, Table **from sqlalchemy.orm import** declarative_base, relationship, sessionmaker **from contextlib import** contextmanager **from datetime import** date, timedelta 

_# Configuración de la base de datos_ engine = create_engine('sqlite:�))biblioteca.db', echo= **False** ) Base = declarative_base() 

**14. ORM con SQLAlchemy** 

**176** 

_# expire_on_commit=False: los objetos devueltos por los DAO mantienen sus # atributos cargados legibles al cerrarse la sesión. Las relaciones lazy, # en cambio, solo pueden consultarse con la sesión abierta._ Session = sessionmaker(bind=engine, expire_on_commit= **False** ) @contextmanager **def** obtener_session(): _"""Context manager para gestionar sesiones de SQLAlchemy."""_ session = Session() **try** : **yield** session session.commit() **except Exception** : session.rollback() **raise finally** : session.close() _# Tabla de asociación muchos a muchos: libros y autores_ libro_autor = Table( 'libro_autor', Base.metadata, Column('libro_id', Integer, ForeignKey('libros.id')), Column('autor_id', Integer, ForeignKey('autores.id')) ) **class Autor** (Base): _"""Representa un autor de libros."""_ __tablename__ = 'autores' id = Column(Integer, primary_key= **True** ) nombre = Column(String(100), nullable= **False** ) apellido = Column(String(100), nullable= **False** ) nacionalidad = Column(String(50)) _# Relación muchos a muchos con libros_ libros = relationship('Libro', secondary=libro_autor, back_populates='autores') **def** __repr__(self): **return** f"<Autor(nombre=' **{** self.nombre **} {** self.apellido **}** ')>" **def** __str__(self): **return** f" **{** self.nombre **} {** self.apellido **}** " **class Libro** (Base): _"""Representa un libro en la biblioteca."""_ __tablename__ = 'libros' id = Column(Integer, primary_key= **True** ) isbn = Column(String(20), unique= **True** , nullable= **False** ) titulo = Column(String(200), nullable= **False** ) editorial = Column(String(100)) anio = Column(Integer) ejemplares_totales = Column(Integer, default=1) ejemplares_disponibles = Column(Integer, default=1) _# Relaciones_ 

**14.9. Ejemplo completo: Sistema de biblioteca** 

**177** 

autores = relationship('Autor', secondary=libro_autor, back_populates='libros') prestamos = relationship('Prestamo', back_populates='libro') **def** __repr__(self): **return** f"<Libro(titulo=' **{** self.titulo **}** ')>" **def** __str__(self): autores_str = ', '.join([str(autor) **for** autor **in** self.autores]) **return** f" **{** self.titulo **}** - **{** autores_str **}** ( **{** self.anio **}** )" @property **def** disponible(self): _"""Verifica si hay ejemplares disponibles."""_ **return** self.ejemplares_disponibles > 0 **class Socio** (Base): _"""Representa un socio de la biblioteca."""_ __tablename__ = 'socios' id = Column(Integer, primary_key= **True** ) numero_socio = Column(String(20), unique= **True** , nullable= **False** ) documento = Column(String(20), unique= **True** , nullable= **False** ) nombre = Column(String(100), nullable= **False** ) apellido = Column(String(100), nullable= **False** ) email = Column(String(100)) telefono = Column(String(20)) fecha_alta = Column(Date, default=date.today) activo = Column(Integer, default=1) _# 1=activo, 0=inactivo # Relación uno a muchos con préstamos_ prestamos = relationship('Prestamo', back_populates='socio') **def** __repr__(self): **return** f"<Socio(numero_socio=' **{** self.numero_socio **}** ')>" **def** __str__(self): **return** f" **{** self.nombre **} {** self.apellido **}** (N° **{** self.numero_socio **}** )" @property **def** tiene_prestamos_vencidos(self): _"""Verifica si el socio tiene préstamos vencidos."""_ hoy = date.today() **return** any(p.fecha_devolucion_estimada < hoy **and not** p.fecha_devolucion_real **for** p **in** self.prestamos) @property **def** prestamos_activos(self): _"""Retorna la lista de préstamos activos (no devueltos)."""_ **return** [p **for** p **in** self.prestamos **if not** p.fecha_devolucion_real] **class Prestamo** (Base): _"""Representa un préstamo de un libro a un socio."""_ __tablename__ = 'prestamos' id = Column(Integer, primary_key= **True** ) libro_id = Column(Integer, ForeignKey('libros.id'), nullable= **False** ) socio_id = Column(Integer, ForeignKey('socios.id'), nullable= **False** ) fecha_prestamo = Column(Date, default=date.today, nullable= **False** ) fecha_devolucion_estimada = Column(Date, nullable= **False** ) 

**14. ORM con SQLAlchemy** 

**178** 

fecha_devolucion_real = Column(Date) observaciones = Column(String(500)) _# Relaciones_ libro = relationship('Libro', back_populates='prestamos') socio = relationship('Socio', back_populates='prestamos') **def** __repr__(self): **return** f"<Prestamo(libro_id= **{** self.libro_id **}** , socio_id= **{** self.socio_id **}** )>" **def** __str__(self): estado = "Devuelto" **if** self.fecha_devolucion_real **else** "Activo" **return** f"Préstamo # **{** self.id **}** - **{** self.libro.titulo **}** - **{** estado **}** " @property **def** esta_vencido(self): _"""Verifica si el préstamo está vencido."""_ **if** self.fecha_devolucion_real: **return False return** date.today() > self.fecha_devolucion_estimada @property **def** dias_restantes(self): _"""Calcula los días restantes para la devolución."""_ **if** self.fecha_devolucion_real: **return** 0 delta = self.fecha_devolucion_estimada - date.today() **return** delta.days _# Funciones de inicialización_ **def** crear_tablas(): _"""Crea todas las tablas en la base de datos."""_ Base.metadata.create_all(engine) **def** cargar_datos_ejemplo(): _"""Carga datos de ejemplo en la base de datos. Devuelve True si cargó los datos o False si la base ya tenía datos."""_ **with** obtener_session() **as** session: _# Verificar si ya hay datos_ **if** session.query(Autor).count() > 0: **return False** _# Crear autores_ autor1 = Autor(nombre='Gabriel', apellido='García Márquez', �→ nacionalidad='Colombiano') autor2 = Autor(nombre='Jorge', apellido='Luis Borges', �→ nacionalidad='Argentino') autor3 = Autor(nombre='Isabel', apellido='Allende', nacionalidad='Chilena') autor4 = Autor(nombre='Julio', apellido='Cortázar', nacionalidad='Argentino') _# Crear libros_ libro1 = Libro( isbn='978-950-07-0001-1', titulo='Cien años de soledad', editorial='Sudamericana', anio=1967, ejemplares_totales=3, ejemplares_disponibles=3 

**14.9. Ejemplo completo: Sistema de biblioteca** 

**179** 

) libro1.autores.append(autor1) libro2 = Libro( isbn='978-950-07-0002-8', titulo='Ficciones', editorial='Emecé', anio=1944, ejemplares_totales=2, ejemplares_disponibles=2 ) libro2.autores.append(autor2) libro3 = Libro( isbn='978-950-07-0003-5', titulo='La casa de los espíritus', editorial='Plaza & Janés', anio=1982, ejemplares_totales=2, ejemplares_disponibles=2 ) libro3.autores.append(autor3) libro4 = Libro( isbn='978-950-07-0004-2', titulo='Rayuela', editorial='Sudamericana', anio=1963, ejemplares_totales=2, ejemplares_disponibles=2 ) libro4.autores.append(autor4) _# Crear socios_ socio1 = Socio( numero_socio='S001', documento='12345678', nombre='Ana', apellido='Martínez', email='ana@example.com', telefono='1234-5678' ) socio2 = Socio( numero_socio='S002', documento='87654321', nombre='Carlos', apellido='López', email='carlos@example.com', telefono='8765-4321' ) session.add_all([autor1, autor2, autor3, autor4, libro1, libro2, libro3, libro4, socio1, socio2]) **return True** _# DAOs: una clase repositorio por entidad principal. # No interactúan con el usuario: solo acceden a los datos y devuelven_ 

**14. ORM con SQLAlchemy** 

**180** 

_# valores (objetos, diccionarios o None). La interacción (input/print) # queda a cargo del main. # # Los métodos que devuelven datos para mostrar los materializan dentro de # la sesión (como diccionarios), porque las relaciones lazy no pueden # consultarse una vez cerrada la sesión (DetachedInstanceError)._ 

**class LibroDAO** : _"""Operaciones de acceso a datos sobre la tabla de libros."""_ 

**def** obtener_por_isbn(self, isbn): _"""Devuelve el libro con el ISBN indicado, o None si no existe."""_ **with** obtener_session() **as** session: **return** session.query(Libro).filter_by(isbn=isbn).first() 

**def** listar(self): _"""Devuelve todos los libros con los datos listos para mostrar."""_ **with** obtener_session() **as** session: libros = session.query(Libro).all() 

**return** [ { 'isbn': libro.isbn, 'titulo': libro.titulo, 'autores': ', '.join([str(autor) **for** autor **in** libro.autores]), 'editorial': libro.editorial, 'anio': libro.anio, 'disponibles': libro.ejemplares_disponibles, 'totales': libro.ejemplares_totales, } **for** libro **in** libros ] 

**class SocioDAO** : 

_"""Operaciones de acceso a datos sobre la tabla de socios."""_ 

**def** obtener_por_numero(self, numero_socio): _"""Devuelve el socio con el número indicado, o None si no existe."""_ **with** obtener_session() **as** session: **return** session.query(Socio).filter_by(numero_socio=numero_socio).first() **def** listar_activos(self): _"""Devuelve los socios activos con los datos listos para mostrar."""_ **with** obtener_session() **as** session: socios = session.query(Socio).filter_by(activo=1).all() 

**return** [ { 'numero_socio': socio.numero_socio, 'nombre': socio.nombre, 'apellido': socio.apellido, 'documento': socio.documento, 'email': socio.email, 'prestamos_activos': len(socio.prestamos_activos), } **for** socio **in** socios ] 

**14.9. Ejemplo completo: Sistema de biblioteca** 

**181** 

**class PrestamoDAO** : _"""Operaciones de acceso a datos sobre la tabla de préstamos."""_ **def** registrar(self, numero_socio, isbn, dias_prestamo=14): _"""Registra un nuevo préstamo. Lanza ValueError si no se cumplen las reglas de negocio."""_ **with** obtener_session() **as** session: _# Buscar socio_ socio = session.query(Socio).filter_by(numero_socio=numero_socio).first() **if not** socio: **raise ValueError** (f"Socio **{** numero_socio **}** no encontrado") **if not** socio.activo: **raise ValueError** (f"Socio **{** numero_socio **}** no está activo") **if** socio.tiene_prestamos_vencidos: **raise ValueError** (f"Socio **{** numero_socio **}** tiene préstamos vencidos") _# Buscar libro_ libro = session.query(Libro).filter_by(isbn=isbn).first() **if not** libro: **raise ValueError** (f"Libro con ISBN **{** isbn **}** no encontrado") **if not** libro.disponible: **raise ValueError** (f"No hay ejemplares disponibles de ' **{** libro.titulo **}** '") _# Crear préstamo_ fecha_devolucion = date.today() + timedelta(days=dias_prestamo) prestamo = Prestamo( libro=libro, socio=socio, fecha_devolucion_estimada=fecha_devolucion ) _# Actualizar disponibilidad_ libro.ejemplares_disponibles -= 1 session.add(prestamo) **return** { 'titulo': libro.titulo, 'socio': f" **{** socio.nombre **} {** socio.apellido **}** ", 'fecha_devolucion': fecha_devolucion, } **def** devolver(self, prestamo_id, observaciones= **None** ): _"""Registra la devolución de un préstamo. Lanza ValueError si el préstamo no existe o ya fue devuelto."""_ **with** obtener_session() **as** session: prestamo = session.query(Prestamo).get(prestamo_id) **if not** prestamo: **raise ValueError** (f"Préstamo # **{** prestamo_id **}** no encontrado") **if** prestamo.fecha_devolucion_real: **raise ValueError** (f"El préstamo # **{** prestamo_id **}** ya fue devuelto") _# Registrar devolución_ prestamo.fecha_devolucion_real = date.today() **if** observaciones: prestamo.observaciones = observaciones 

**14. ORM con SQLAlchemy** 

**182** 

_# Actualizar disponibilidad_ prestamo.libro.ejemplares_disponibles += 1 **return** { 'titulo': prestamo.libro.titulo, 'vencido': prestamo.esta_vencido, } **def** consultar_por_socio(self, numero_socio): _"""Devuelve el socio y sus préstamos listos para mostrar. Lanza ValueError si el socio no existe."""_ **with** obtener_session() **as** session: socio = session.query(Socio).filter_by(numero_socio=numero_socio).first() **if not** socio: **raise ValueError** (f"Socio **{** numero_socio **}** no encontrado") prestamos = [] **for** prestamo **in** socio.prestamos: estado = "DEVUELTO" **if** prestamo.fecha_devolucion_real **else** "ACTIVO" **if** prestamo.esta_vencido: estado = "VENCIDO" prestamos.append({ 'id': prestamo.id, 'titulo': prestamo.libro.titulo, 'fecha_prestamo': prestamo.fecha_prestamo, 'fecha_devolucion_estimada': prestamo.fecha_devolucion_estimada, 'fecha_devolucion_real': prestamo.fecha_devolucion_real, 'estado': estado, 'dias_restantes': prestamo.dias_restantes, 'observaciones': prestamo.observaciones, }) **return** { 'nombre': socio.nombre, 'apellido': socio.apellido, 'prestamos': prestamos, } **def** listar_activos(self): _"""Devuelve los préstamos activos listos para mostrar."""_ **with** obtener_session() **as** session: prestamos = session.query(Prestamo).filter( Prestamo.fecha_devolucion_real.is_( **None** ) ).all() **return** [ { 'id': prestamo.id, 'titulo': prestamo.libro.titulo, 'socio': f" **{** prestamo.socio.nombre **} {** prestamo.socio.apellido **}** ", 'fecha_devolucion_estimada': prestamo.fecha_devolucion_estimada, 'estado': "VENCIDO" **if** prestamo.esta_vencido **else** "VIGENTE", 'dias_restantes': prestamo.dias_restantes, } **for** prestamo **in** prestamos ] 

_# Menú principal: aquí vive toda la interacción con el usuario_ 

**14.9. Ejemplo completo: Sistema de biblioteca** 

**183** 

**def** mostrar_menu(): _"""Muestra el menú principal."""_ print(" **\n** " + "="*50) print("SISTEMA DE GESTIÓN DE BIBLIOTECA") print("="*50) print("1. Listar libros") print("2. Listar socios") print("3. Registrar préstamo") print("4. Registrar devolución") print("5. Consultar préstamos de un socio") print("6. Listar préstamos activos") print("7. Cargar datos de ejemplo") print("0. Salir") print("="*50) **def** mostrar_catalogo(libros): _"""Muestra el catálogo de libros."""_ print(" **\n** �)) CATÁLOGO DE LIBROS �))") **for** libro **in** libros: print(f" **\n** ISBN: **{** libro['isbn'] **}** ") print(f"Título: **{** libro['titulo'] **}** ") print(f"Autor(es): **{** libro['autores'] **}** ") print(f"Editorial: **{** libro['editorial'] **}** ( **{** libro['anio'] **}** )") print(f"Disponibles: **{** libro['disponibles'] **}** / **{** libro['totales'] **}** ") **def** mostrar_socios(socios): _"""Muestra los socios activos."""_ print(" **\n** �)) SOCIOS ACTIVOS �))") **for** socio **in** socios: print(f" **\n** N° Socio: **{** socio['numero_socio'] **}** ") print(f"Nombre: **{** socio['nombre'] **} {** socio['apellido'] **}** ") print(f"Documento: **{** socio['documento'] **}** ") print(f"Email: **{** socio['email'] **}** ") print(f"Préstamos activos: **{** socio['prestamos_activos'] **}** ") **def** mostrar_prestamos_socio(datos): _"""Muestra los préstamos de un socio."""_ print(f" **\n** �)) PRÉSTAMOS DE **{** datos['nombre'] **} {** datos['apellido'] **}** �))") **if not** datos['prestamos']: print("No tiene préstamos registrados") **return for** prestamo **in** datos['prestamos']: print(f" **\n** Préstamo # **{** prestamo['id'] **}** - **{** prestamo['estado'] **}** ") print(f"Libro: **{** prestamo['titulo'] **}** ") print(f"Fecha préstamo: **{** prestamo['fecha_prestamo'] **}** ") print(f"Fecha devolución estimada: **{** prestamo['fecha_devolucion_estimada'] **}** ") **if** prestamo['fecha_devolucion_real']: print(f"Fecha devolución real: **{** prestamo['fecha_devolucion_real'] **}** ") **else** : print(f"Días restantes: **{** prestamo['dias_restantes'] **}** ") **if** prestamo['observaciones']: print(f"Observaciones: **{** prestamo['observaciones'] **}** ") 

**14. ORM con SQLAlchemy** 

**184** 

**def** mostrar_prestamos_activos(prestamos): _"""Muestra los préstamos activos."""_ print(" **\n** �)) PRÉSTAMOS ACTIVOS �))") **if not** prestamos: print("No hay préstamos activos") **return for** prestamo **in** prestamos: print(f" **\n** Préstamo # **{** prestamo['id'] **}** - **{** prestamo['estado'] **}** ") print(f"Libro: **{** prestamo['titulo'] **}** ") print(f"Socio: **{** prestamo['socio'] **}** ") print(f"Fecha devolución: **{** prestamo['fecha_devolucion_estimada'] **}** ") print(f"Días restantes: **{** prestamo['dias_restantes'] **}** ") 

**def** main(): _"""Función principal."""_ crear_tablas() print("Tablas creadas exitosamente") libro_dao = LibroDAO() socio_dao = SocioDAO() prestamo_dao = PrestamoDAO() **while True** : mostrar_menu() opcion = input(" **\n** Seleccione una opción: ").strip() **try** : **if** opcion �) '1': mostrar_catalogo(libro_dao.listar()) **elif** opcion �) '2': mostrar_socios(socio_dao.listar_activos()) **elif** opcion �) '3': numero_socio = input("Número de socio: ").strip() isbn = input("ISBN del libro: ").strip() datos = prestamo_dao.registrar(numero_socio, isbn) print(f"Préstamo registrado: **{** datos['titulo'] **}** para **{** datos['socio'] **}** ") print(f"Fecha de devolución: **{** datos['fecha_devolucion'] **}** ") **elif** opcion �) '4': prestamo_id = input("ID del préstamo: ").strip() observaciones = input("Observaciones (opcional): ").strip() **try** : prestamo_id = int(prestamo_id) **except ValueError** : print("Error: ID inválido") **else** : datos = prestamo_dao.devolver(prestamo_id, observaciones **or None** ) **if** datos['vencido']: print("Advertencia: Devolución con retraso") print(f"Devolución registrada: **{** datos['titulo'] **}** ") **elif** opcion �) '5': numero_socio = input("Número de socio: ").strip() mostrar_prestamos_socio( prestamo_dao.consultar_por_socio(numero_socio) 

**14.9. Ejemplo completo: Sistema de biblioteca** 

**185** 

) **elif** opcion �) '6': mostrar_prestamos_activos(prestamo_dao.listar_activos()) **elif** opcion �) '7': **if** cargar_datos_ejemplo(): print("Datos de ejemplo cargados exitosamente") **else** : print("La base de datos ya contiene datos") **elif** opcion �) '0': print("¡Hasta luego!") **break else** : print("Opción inválida") **except ValueError as** e: print(f"Error: **{** e **}** ") input(" **\n** Presione Enter para continuar�))") **if** __name__ �) '__main__': main() 

### **Singleton** 

##### **15.1 Introducción** 

El patrón Singleton es un patrón de diseño creacional que garantiza que una clase tenga una única instancia y proporciona un punto de acceso global a esa instancia. Este patrón restringe la instanciación de una clase a un solo objeto, lo cual es útil cuando se necesita exactamente un objeto para coordinar acciones en todo el sistema. 

El concepto central del Singleton es que la clase misma es responsable de mantener su única instancia. La clase debe asegurarse de que no se puedan crear instancias adicionales y debe proporcionar una forma de acceder a la instancia única. Este control se logra haciendo privado el constructor y proporcionando un método estático que retorna la instancia única. 

El patrón Singleton fue documentado por el Gang of Four en su libro “Design Patterns: Elements of Reusable Object-Oriented Software” (1994) como uno de los patrones creacionales fundamentales. Aunque es uno de los patrones más conocidos, también es considerado controvertido por algunos desarrolladores debido a que puede introducir acoplamiento global si se abusa de su uso. 

##### **15.2 Necesidad y casos de uso** 

El patrón Singleton surge de la necesidad de controlar el acceso a recursos compartidos o de garantizar que ciertas operaciones se realicen sobre un 

189 

**15. Singleton** 

**190** 

único objeto en todo el sistema. Sin este patrón, múltiples instancias podrían causar inconsistencias, desperdicio de recursos o comportamiento impredecible. 

La necesidad fundamental que resuelve este patrón es la de coordinar acciones a través de un único objeto. En muchos sistemas, tener múltiples instancias de ciertos objetos no solo es innecesario, sino que puede ser perjudicial. Por ejemplo, tener múltiples gestores de con�guración podría llevar a que diferentes partes del sistema trabajen con con�guraciones inconsistentes. Similarmente, múltiples instancias de un logger podrían resultar en mensajes desordenados o con�ictos al escribir en el mismo archivo. 

###### **15.2.1 Casos de uso típicos** 

**Gestión de conexiones a bases de datos:** Una aplicación necesita una única conexión o pool de conexiones a la base de datos. Crear múltiples instancias del gestor de conexiones podría resultar en un uso ine�ciente de recursos del servidor de base de datos, límites de conexiones excedidos y problemas de sincronización. El Singleton garantiza que todos los componentes de la aplicación utilicen el mismo gestor de conexiones, optimizando el uso de recursos y facilitando el control de transacciones. 

**Gestión de con�guración:** Un objeto que mantiene la con�guración de la aplicación debe ser único para garantizar que todos los componentes del sistema accedan a la misma con�guración y que los cambios se re�ejen en toda la aplicación. Si cada módulo creara su propia instancia de con�guración, podría leer diferentes versiones del archivo de con�guración o mantener valores inconsistentes en memoria, llevando a comportamientos impredecibles. 

**Logger o sistema de registro:** Un sistema de logging debe ser único para garantizar que todos los mensajes se escriban en el mismo archivo o destino, manteniendo el orden cronológico y evitando con�ictos de acceso. Múltiples instancias de logger podrían intentar escribir simultáneamente en el mismo archivo, causando corrupción de datos o pérdida de mensajes. Además, un logger centralizado facilita la con�guración de niveles de log y destinos de salida. 

**Gestión de caché:** Una caché en memoria debe ser única para que todos los componentes del sistema compartan los mismos datos cacheados y se maximi- 

**15.3. Implementación según GoF** 

**191** 

ce el bene�cio del cacheo. Si diferentes partes de la aplicación mantuvieran cachés separadas, se duplicaría el uso de memoria y se perdería la e�ciencia que proporciona compartir datos cacheados. Un Singleton de caché asegura que todos los componentes consulten y actualicen la misma caché. 

**Administrador de recursos:** Gestores de impresoras, spoolers, o administradores de hilos que deben coordinar el acceso a recursos limitados del sistema. Por ejemplo, un administrador de pool de hilos debe ser único para evitar la creación excesiva de hilos y coordinar e�cientemente las tareas concurrentes. Del mismo modo, un gestor de impresión debe serializar los trabajos de impresión de toda la aplicación. 

**Registro de objetos:** Un registro centralizado que mantiene referencias a objetos importantes del sistema, permitiendo el acceso global a estos objetos sin pasar referencias a través de múltiples capas de la aplicación. 

**Contadores globales:** Generadores de identi�cadores únicos o contadores que deben garantizar la unicidad de los valores generados en todo el sistema, como generadores de IDs para objetos o números de factura. 

##### **15.3 Implementación según GoF** 

La implementación clásica del patrón Singleton según GoF utiliza un atributo de clase privado para almacenar la única instancia y controla su creación a través del constructor. En Python, esto se logra sobrescribiendo el método especial __new__, que es el responsable de crear nuevas instancias de una clase. 

El método __new__ se ejecuta antes que __init__ y es el encargado de crear y retornar el objeto. Al sobrescribirlo, podemos controlar la creación de instancias y garantizar que solo se cree una. La estrategia consiste en almacenar la primera instancia creada en un atributo de clase y retornar siempre esa misma instancia en llamadas subsecuentes. 

El siguiente diagrama de clases resume la estructura de esta implementación, tal como la describe GoF: un atributo de clase estático que retiene la única instancia y un método de clase (__new__) que la crea o la retorna: 

**15. Singleton** 

**192** 



###### **15.3.1 Implementación básica** 

**class Singleton** : _# Variable de clase para almacenar la única instancia_ _instance = **None def** __new__(cls): _""" Sobrescribe el método __new__ para controlar la creación de instancias. """_ **if** cls._instance **is None** : _# Crear la instancia usando el __new__ de la clase padre_ cls._instance = super(Singleton, cls).__new__(cls) **return** cls._instance **def** __init__(self): _""" El __init__ se llama cada vez que se intenta crear un objeto, pero __new__ garantiza que siempre sea el mismo. """_ **pass** _# Uso del Singleton_ s1 = Singleton() s2 = Singleton() print(s1 **is** s2) _# True - Ambas variables referencian el mismo objeto_ print(id(s1), id(s2)) _# Muestran el mismo identificador_ 

Es importante notar que aunque __new__ garantiza que solo exista una instancia, el método __init__ se ejecuta cada vez que se intenta crear un objeto. Esto puede ser problemático si __init__ realiza inicializaciones costosas o modi�ca el estado del objeto. Para evitar este problema, se puede agregar una bandera que indique si el objeto ya fue inicializado: 

**class Singleton** : _instance = **None** _initialized = **False def** __new__(cls): **if** cls._instance **is None** : cls._instance = super(Singleton, cls).__new__(cls) 

**15.3. Implementación según GoF** 

**193** 

**return** cls._instance **def** __init__(self): _# Solo inicializar la primera vez_ **if not** Singleton._initialized: self.data = [] Singleton._initialized = **True** print("Singleton inicializado") s1 = Singleton() _# Imprime: Singleton inicializado_ s2 = Singleton() _# No imprime nada_ s1.data.append(42) print(s2.data) _# [42] - Comparten el mismo estado_ 

###### **15.3.2 Ejemplo con conexión a base de datos** 

Un caso práctico muy común es la gestión de conexiones a bases de datos. En el siguiente ejemplo se muestra un Singleton que mantiene una única conexión: 

**class DatabaseConnection** : _instance = **None** _connection_string = **None** _initialized = **False def** __new__(cls, connection_string= **None** ): **if** cls._instance **is None** : cls._instance = super(DatabaseConnection, cls).__new__(cls) **return** cls._instance **def** __init__(self, connection_string= **None** ): _# Solo inicializar en la primera creación_ **if not** DatabaseConnection._initialized: **if** connection_string **is None** : **raise ValueError** ("Debe proporcionar connection_string") self._connection_string = connection_string DatabaseConnection._initialized = **True** print(f"Conexión establecida a: **{** connection_string **}** ") **def** get_connection_string(self): **return** self._connection_string **def** execute_query(self, query): _"""Simula la ejecución de una query"""_ print(f"Ejecutando en **{** self._connection_string **}** : **{** query **}** ") **return** f"Resultado de: **{** query **}** " **def** close(self): _"""Cierra la conexión"""_ print(f"Cerrando conexión a **{** self._connection_string **}** ") _# Primera creación - establece la conexión_ db1 = DatabaseConnection("postgresql�))localhost:5432/mydb") _# Segunda creación - retorna la misma instancia # El connection_string se ignora_ 

**15. Singleton** 

**194** 

db2 = DatabaseConnection("mysql�))localhost:3306/otherdb") print(db1 **is** db2) _# True_ print(db1.get_connection_string()) _# postgresql�))localhost:5432/mydb_ db1.execute_query("SELECT * FROM users") db2.execute_query("INSERT INTO logs VALUES ('test')") _# Ambas queries se ejecutan en la misma conexión_ 

###### **15.3.3 Ejemplo con sistema de con�guración** 

Otro caso común es un sistema de con�guración centralizado: 

**import json from pathlib import** Path **class Configuration** : _instance = **None** _initialized = **False def** __new__(cls): **if** cls._instance **is None** : cls._instance = super(Configuration, cls).__new__(cls) **return** cls._instance **def** __init__(self): **if not** Configuration._initialized: self.settings = {} Configuration._initialized = **True def** load_from_file(self, filepath): _"""Carga la configuración desde un archivo JSON"""_ **try** : **with** open(filepath, 'r') **as** f: self.settings = json.load(f) print(f"Configuración cargada desde **{** filepath **}** ") **except FileNotFoundError** : print(f"Archivo **{** filepath **}** no encontrado") **def** get(self, key, default= **None** ): _"""Obtiene un valor de configuración"""_ **return** self.settings.get(key, default) **def** set(self, key, value): _"""Establece un valor de configuración"""_ self.settings[key] = value **def** save_to_file(self, filepath): _"""Guarda la configuración en un archivo JSON"""_ **with** open(filepath, 'w') **as** f: json.dump(self.settings, f, indent=4) print(f"Configuración guardada en **{** filepath **}** ") _# Uso en diferentes módulos de la aplicación # Módulo A_ config_a = Configuration() 

**15.3. Implementación según GoF** 

**195** 

config_a.set('database_host', 'localhost') config_a.set('database_port', 5432) config_a.set('debug', **True** ) _# Módulo B - obtiene la misma instancia_ config_b = Configuration() print(config_b.get('database_host')) _# localhost_ print(config_b.get('debug')) _# True # Ambas referencias apuntan al mismo objeto_ print(config_a **is** config_b) _# True_ 

###### **15.3.4 Ejemplo con logger** 

Un sistema de logging es otro candidato ideal para Singleton: 

**from datetime import** datetime **from pathlib import** Path **class Logger** : _instance = **None** _initialized = **False** _# Niveles de log_ DEBUG = 0 INFO = 1 WARNING = 2 ERROR = 3 CRITICAL = 4 **def** __new__(cls): **if** cls._instance **is None** : cls._instance = super(Logger, cls).__new__(cls) **return** cls._instance **def** __init__(self): **if not** Logger._initialized: self.log_file = **None** self.log_level = Logger.INFO self.logs = [] Logger._initialized = **True def** configure(self, log_file= **None** , log_level=INFO): _"""Configura el logger"""_ self.log_file = log_file self.log_level = log_level **def** _write_log(self, level, message): _"""Escribe un mensaje de log"""_ timestamp = datetime.now().strftime("%Y-%m- **%d** %H:%M:%S") level_names = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL'] log_entry = f"[ **{** timestamp **}** ] **{** level_names[level] **}** : **{** message **}** " self.logs.append(log_entry) **if** self.log_file: **with** open(self.log_file, 'a') **as** f: f.write(log_entry + ' **\n** ') 

**15. Singleton** 

**196** 

**else** : print(log_entry) **def** debug(self, message): **if** self.log_level �) Logger.DEBUG: self._write_log(Logger.DEBUG, message) **def** info(self, message): **if** self.log_level �) Logger.INFO: self._write_log(Logger.INFO, message) **def** warning(self, message): **if** self.log_level �) Logger.WARNING: self._write_log(Logger.WARNING, message) **def** error(self, message): **if** self.log_level �) Logger.ERROR: self._write_log(Logger.ERROR, message) **def** critical(self, message): **if** self.log_level �) Logger.CRITICAL: self._write_log(Logger.CRITICAL, message) _# Uso desde diferentes partes de la aplicación # Módulo de autenticación_ logger1 = Logger() logger1.configure(log_level=Logger.DEBUG) logger1.info("Usuario intentando iniciar sesión") logger1.debug("Validando credenciales") _# Módulo de base de datos_ logger2 = Logger() logger2.warning("Conexión lenta a la base de datos") logger2.error("Fallo en la query") _# Mismo logger en ambos casos_ print(logger1 **is** logger2) _# True_ print(len(logger1.logs)) _# Muestra todos los logs acumulados_ 

##### **15.4 Implementación simpli�cada en Python** 

Python ofrece varias alternativas para implementar el patrón Singleton de manera más simple y pythónica, aprovechando características particulares del lenguaje. 

###### **15.4.1 Usando un decorador** 

Una forma elegante y reutilizable de implementar Singleton es mediante un decorador que puede aplicarse a cualquier clase: 

**15.4. Implementación simpli�cada en Python** 

**197** 

**def** singleton _"""_ (cls): _Decorador que convierte una clase en Singleton """_ instances = {} **def** get_instance(*args, �)kwargs): **if** cls **not in** instances: instances[cls] = cls(*args, �)kwargs) **return** instances[cls] **return** get_instance @singleton **class Logger** : **def** __init__(self): self.logs = [] **def** log(self, message): self.logs.append(message) print(f"LOG: **{** message **}** ") **def** show_logs(self): **return** self.logs _# Uso_ logger1 = Logger() logger1.log("Primer mensaje") logger2 = Logger() logger2.log("Segundo mensaje") print(logger1 **is** logger2) _# True_ print(logger1.show_logs()) _# ['Primer mensaje', 'Segundo mensaje']_ 

La ventaja de este enfoque es que el decorador es reutilizable y no requiere modi�car la estructura interna de la clase. Cualquier clase puede convertirse en Singleton simplemente aplicando el decorador. Además, el decorador mantiene un diccionario de instancias, lo que permite tener múltiples Singletons diferentes si se aplica a varias clases. 

A diferencia de la implementación GoF, aquí no existe una relación de herencia ni un atributo de clase dentro de Logger: el control de la instancia única queda completamente fuera de la clase, encapsulado en la función get_instance generada por el decorador (un _closure_ que retiene el diccionario instances). El siguiente diagrama complementario ilustra esta diferencia estructural: 

**15. Singleton** 

**198** 



Una versión mejorada del decorador que preserva metadatos de la clase original: 

**from functools import** wraps **def** singleton(cls): _""" Decorador Singleton que preserva metadatos de la clase """_ instances = {} @wraps(cls) **def** get_instance(*args, �)kwargs): **if** cls **not in** instances: instances[cls] = cls(*args, �)kwargs) **return** instances[cls] _# Preservar atributos de clase_ get_instance.__name__ = cls.__name__ get_instance.__doc__ = cls.__doc__ **return** get_instance @singleton **class Cache** : _"""Sistema de caché en memoria"""_ **def** __init__(self): self.data = {} **def** set(self, key, value): self.data[key] = value **def** get(self, key, default= **None** ): **return** self.data.get(key, default) **def** clear(self): 

**15.4. Implementación simpli�cada en Python** 

**199** 

self.data.clear() _# Uso_ cache1 = Cache() cache1.set("usuario", "Juan") cache2 = Cache() print(cache2.get("usuario")) _# Juan_ print(Cache.__doc__) _# Sistema de caché en memoria_ 

###### **15.4.2 Usando clases abstractas (ABC)** 

Otra alternativa es emplear una clase base abstracta para estandarizar la forma en que las clases hijas implementan el comportamiento Singleton. La clase abstracta centraliza la lógica de creación única y expone un punto de inicialización para que cada subclase de�na su con�guración especí�ca. 

La idea es: 

- Interceptar la creación en __new__ para garantizar una única instancia por subclase. 

- Ofrecer un método abstracto initialize(�))) que se ejecute solo una vez (la primera vez). 

- Permitir que __init__ sea idempotente delegando en un helper que asegura la inicialización única. 

**from abc import** ABC, abstractmethod **class SingletonABC** (ABC): _"""Clase base abstracta que implementa Singleton por subclase."""_ _instances = {} _initialized = {} **def** __new__(cls, *args, �)kwargs): **if** cls **is** SingletonABC: **raise TypeError** ("SingletonABC es abstracta y no debe instanciarse") **if** cls **not in** cls._instances: instance = super().__new__(cls) cls._instances[cls] = instance cls._initialized[cls] = **False return** cls._instances[cls] **def** _ensure_initialized(self, *args, �)kwargs): _"""Ejecuta initialize(�))) solo una vez por subclase."""_ c = self.__class__ **if not** c._initialized.get(c, **False** ): self.initialize(*args, �)kwargs) c._initialized[c] = **True** @abstractmethod **def** initialize(self, *args, �)kwargs): _"""Punto de inicialización definido por cada subclase."""_ 

**15. Singleton** 

**200** 

**pass class ServicioConfiguracion** (SingletonABC): _"""Ejemplo: servicio de configuración como Singleton."""_ **def** __init__(self, archivo= **None** ): _# Idempotente: solo inicializa una vez_ self._ensure_initialized(archivo=archivo) **def** initialize(self, archivo= **None** ): **import json** self._settings = {} **if** archivo: **try** : **with** open(archivo, 'r') **as** f: self._settings = json.load(f) **except FileNotFoundError** : print(f"Archivo **{** archivo **}** no encontrado; usando valores por defecto") **def** get(self, clave, por_defecto= **None** ): **return** self._settings.get(clave, por_defecto) **def** set(self, clave, valor): self._settings[clave] = valor _# Uso_ cfg1 = ServicioConfiguracion(archivo="config.json") cfg2 = ServicioConfiguracion() print(cfg1 **is** cfg2) _# True_ cfg1.set('debug', **True** ) print(cfg2.get('debug')) _# True_ 

Esta variante combina herencia (todas las subclases de SingletonABC obtienen el comportamiento Singleton en forma automática) con un contrato explícito (initialize) que cada subclase debe implementar. A diferencia del decorador, aquí sí hay una jerarquía de clases; a diferencia de la implementación GoF básica, el estado (_instances, _initialized) se indexa por subclase, permitiendo que cada clase derivada tenga su propia instancia única: 

**15.5. Consideraciones y críticas** 

**201** 



###### **15.4.3 Comparación de enfoques** 

Cada enfoque tiene sus ventajas y casos de uso apropiados: 

- **Decorador** : Reutilizable y no invasivo. Bueno cuando se necesita aplicar Singleton a múltiples clases sin modi�car su estructura. 

- **__new__ (GoF)** : Implementación tradicional. Clara y explícita, pero conviene controlar la inicialización para evitar costos repetidos en __init__. 

- **Clase abstracta (ABC)** : Estandariza el contrato e integra _una sola instancia por subclase_ con un hook de inicialización único. Útil cuando se desea guiar a equipos/estudiantes a seguir una interfaz común. 

##### **15.5 Consideraciones y críticas** 

Aunque el patrón Singleton es ampliamente utilizado, también es objeto de críticas y debe usarse con precaución. 

**15. Singleton** 

**202** 

###### **15.5.1 Problemas potenciales** 

**Acoplamiento global:** El Singleton introduce un punto de acoplamiento global en la aplicación. Cualquier módulo que lo use depende de esa instancia global, lo que puede di�cultar el testing y la refactorización. 

**Di�cultad para testing:** Los Singletons pueden complicar las pruebas unitarias porque mantienen estado entre tests. Esto puede causar que los tests se afecten mutuamente si no se limpia el estado correctamente. **Violación del principio de responsabilidad única:** Un Singleton tiene dos responsabilidades: su funcionalidad principal y controlar su propia instanciación. 

**Problemas de concurrencia:** En aplicaciones multithreading, se debe garantizar que la creación del Singleton sea thread-safe. 

###### **15.5.2 Alternativas y mejores prácticas** 

- Considerar inyección de dependencias en lugar de acceso global 

- Usar Singleton solo cuando realmente se necesite una única instancia 

- Preferir el enfoque de módulo en Python cuando sea posible 

- Documentar claramente por qué se usa Singleton en cada caso 

- Implementar métodos para resetear el estado en ambientes de testing 

_# Ejemplo de Singleton con método de reset para testing_ **class TestableLogger** : _instance = **None** _initialized = **False def** __new__(cls): **if** cls._instance **is None** : cls._instance = super(TestableLogger, cls).__new__(cls) **return** cls._instance **def** __init__(self): **if not** TestableLogger._initialized: self.logs = [] TestableLogger._initialized = **True def** log(self, message): self.logs.append(message) @classmethod **def** reset_for_testing(cls): _"""Resetea el Singleton para testing"""_ 

**15.6. Conclusión** 

**203** 

**if** cls._instance **is not None** : cls._instance.logs = [] cls._initialized = **False** cls._instance = **None** _# En los tests_ logger = TestableLogger() logger.log("Test message") TestableLogger.reset_for_testing() _# Ahora el Singleton está limpio para el siguiente test_ 

##### **15.6 Conclusión** 

El patrón Singleton es una herramienta poderosa cuando se necesita garantizar una única instancia de una clase en todo el sistema. Python ofrece múltiples formas de implementarlo, desde la aproximación clásica con __new__ hasta enfoques más pythónicos usando módulos o decoradores. 

La elección del enfoque depende del contexto: para con�guraciones simples, un módulo es su�ciente; para casos más complejos con herencia o requisitos de thread-safety, las metaclases pueden ser más apropiadas. Lo importante es entender las implicaciones del patrón y usarlo juiciosamente, considerando alternativas como inyección de dependencias cuando el acoplamiento global pueda ser problemático. 

### **Patrones State y Strategy** 

##### **16.1 Introducción** 

En este capítulo vamos a estudiar dos patrones de diseño del grupo de patrones comportamentales: _State_ y _Strategy_ . Ambos permiten cambiar el comportamiento de un objeto en tiempo de ejecución pero resuelven problemas distintos y con matices propios. 

Primero motivaremos cada patrón, luego veremos su implementación en Python con ejemplos completos y, �nalmente, propondremos ejercicios para consolidar los conceptos. 

##### **16.2 Patrón State** 

###### **16.2.1 Motivación** 

El patrón State sirve cuando un objeto debe cambiar su comportamiento según su estado interno, y cuando ese cambio se puede modelar como la transición entre varias representaciones de estado. En lugar de escribir largas cadenas de condicionales (if/elif/else) que dependen de la variable de estado, el patrón State propone encapsular cada estado en una clase separada que implemente la interfaz común. 

Ventajas: 

- Reduce la complejidad ciclomática: evita condicionales anidados. 

- Facilita añadir nuevos estados sin modi�car la clase contexto. 

205 

**206** 

**16. Patrones State y Strategy** 

- Hace explícitas las transiciones de estado. 

###### **16.2.2 Contrato (interfaz)** 

El patrón de�ne: 

- Una clase _Context_ que mantiene una referencia al estado actual y delega en él las operaciones. 

- Una interfaz común para los _State_ concretos que implementan el comportamiento correspondiente. 

El siguiente diagrama de clases resume la estructura estándar de GoF aplicada al ejemplo del semáforo: el contexto (Semaforo) mantiene una referencia a un estado abstracto y delega en él; cada estado concreto conoce su transición al siguiente estado. 

**16.2. Patrón State** 

**207** 



<!-- Start of picture text -->
1 -e stado : EstadoSenaforo<br>© canbiar _ estado(estado)<br>© siguiente()<br>© actual) : str<br>estado actual<br>|<br>©entrar(contexto)<br>© satir(contexto)<br>© siguiente(contexto)<br>_———<br>o fo<br>—| —) — — |<br><!-- End of picture text -->

###### **16.2.3 Ejemplo: semáforo** 

Motivación del ejemplo: un semáforo cambia entre estados (Rojo, Verde, Amarillo) y cada estado de�ne la acción a realizar (por ejemplo, permitir o detener rillo) y cada estado define la acciona realizar (por ejemplo, permitir o detener el paso). El ejemplo mostrará cómo encapsular los estados y las transiciones. 

**208** 

**16. Patrones State y Strategy** 

###### **16.2.4 Código de ejemplo** 

###### **Ejemplo: State (Semáforo)** 

_"""_ 

_Ejemplo del patrón State: semáforo._ 

_Contiene la implementación del contexto (Semaforo) y los estados (Rojo, Verde,_ 

�→ _Amarillo) Incluye una función de simulación que espera con time.sleep al entrar en cada estado y realiza la transición automáticamente para imitar un semáforo real. """_ **from abc import** ABC, abstractmethod **import time import sys import select import tty import termios try** : **import msvcrt except Exception** : msvcrt = **None class Estado** (ABC): @abstractmethod **def** entrar(self, contexto): **pass** @abstractmethod **def** salir(self, contexto): **pass** @abstractmethod **def** siguiente(self, contexto): **pass class EstadoSemaforo** (Estado): _"""Clase base para estados de semáforo que expone un atributo público `duracion`. Las subclases (Rojo, Verde, Amarillo) deberán sobrescribir `duracion` si necesitan un valor distinto. """ # Duración por defecto en segundos para estados de semáforo_ duracion: int = 2 **class Semaforo** : **def** __init__(self, estado_inicial: EstadoSemaforo): _# Atributo público interno que contiene el estado actual. # Tipado como EstadoSemaforo para que la simulación acceda a `duracion`._ self._estado: EstadoSemaforo | **None** = **None** self.cambiar_estado(estado_inicial) **def** simular(self): _"""Ejecuta una simulación automática del semáforo hasta que el usuario pulse_ �→ _una tecla._ 

_La duración de cada estado se obtiene directamente desde el atributo público `duracion` del estado (clase derivada de `EstadoSemaforo`)._ 

**16.2. Patrón State** 

**209** 

_"""_ print("�)) Simulación: semáforo automático (pulse cualquier tecla para detener) �→ �))") **while True** : nombre = self.actual() estado_actual = self._estado dur = estado_actual.duracion print(f"Estado actual: **{** nombre **}** (esperando **{** dur **}** s)") **try** : time.sleep(dur) **except KeyboardInterrupt** : print(' **\n** Simulación interrumpida por el usuario (Ctrl-C)') **break** _# avanzar al siguiente estado_ self.siguiente() print("Simulación finalizada **\n** ") **def** cambiar_estado(self, estado: EstadoSemaforo): **if** self._estado **is not None** : self._estado.salir(self) self._estado = estado self._estado.entrar(self) **def** siguiente(self): self._estado.siguiente(self) **def** actual(self): **return** type(self._estado).__name__ **class Rojo** (EstadoSemaforo): **def** entrar(self, contexto): print("Semáforo: ROJO - Detener vehículos") _# Duración por defecto en segundos cuando el semáforo está en ROJO_ duracion = 3 **def** salir(self, contexto): print("Saliendo de ROJO") **def** siguiente(self, contexto): contexto.cambiar_estado(Verde()) **class Verde** (EstadoSemaforo): **def** entrar(self, contexto): print("Semáforo: VERDE - Permitir paso") _# Duración por defecto en segundos cuando el semáforo está en VERDE_ duracion = 4 **def** salir(self, contexto): print("Saliendo de VERDE") **def** siguiente(self, contexto): contexto.cambiar_estado(Amarillo()) **class Amarillo** (EstadoSemaforo): **def** entrar(self, contexto): 

**210** 

**16. Patrones State y Strategy** 

print("Semáforo: AMARILLO - Precaución") _# Duración por defecto en segundos cuando el semáforo está en AMARILLO_ duracion = 2 **def** salir(self, contexto): print("Saliendo de AMARILLO") **def** siguiente(self, contexto): contexto.cambiar_estado(Rojo()) **def** demo_semaforo(): print("�)) Demo: Semáforo (State) �))") sem = Semaforo(Rojo()) **for** _ **in** range(6): print(f"Estado actual: **{** sem.actual() **}** ") sem.siguiente() print() **def** demo_simulacion(): _"""Demo que ejecuta la simulación con duraciones razonables por estado."""_ sem = Semaforo(Rojo()) _# Usamos las duraciones definidas en cada estado._ sem.simular() **if** __name__ �) '__main__': demo_simulacion() 

**Ejemplo: Strategy (Envíos)** 

_""" Ejemplo del patrón Strategy: cálculo de coste de envío. Contiene implementaciones por clases y una versión sin herencia (diccionario de_ �→ _funciones). """_ **from abc import** ABC, abstractmethod **class EstrategiaEnvio** (ABC): @abstractmethod **def** calcular(self, paquete): **pass class Paquete** : **def** __init__(self, peso_kg: float, distancia_km: float, dimensiones_cm=(0, 0, 0)): self.peso = peso_kg self.distancia = distancia_km self.dimensiones = dimensiones_cm **class EnvioEstandar** (EstrategiaEnvio): **def** calcular(self, paquete: Paquete): base = 5.0 por_kg = 1.0 * paquete.peso 

**16.2. Patrón State** 

**211** 

por_km = 0.05 * paquete.distancia total = base + por_kg + por_km **return** round(total, 2) **class EnvioExpreso** (EstrategiaEnvio): **def** calcular(self, paquete: Paquete): base = 10.0 por_kg = 2.0 * paquete.peso por_km = 0.12 * paquete.distancia total = base + por_kg + por_km **return** round(total, 2) **class TarifaPlana** (EstrategiaEnvio): **def** calcular(self, paquete: Paquete): **return** 9.99 **class CalculadorEnvio** : **def** __init__(self, estrategia: EstrategiaEnvio): self._estrategia = estrategia **def** set_estrategia(self, estrategia: EstrategiaEnvio): self._estrategia = estrategia **def** calcular(self, paquete: Paquete): **return** self._estrategia.calcular(paquete) **def** demo_strategy_clases(): print("�)) Demo: Strategy con clases �))") paquete = Paquete(peso_kg=2.5, distancia_km=120) calculador = CalculadorEnvio(EnvioEstandar()) print("Estandar:", calculador.calcular(paquete)) calculador.set_estrategia(EnvioExpreso()) print("Expreso:", calculador.calcular(paquete)) calculador.set_estrategia(TarifaPlana()) print("Tarifa plana:", calculador.calcular(paquete)) print() **def** cliente_selecciona_estrategia_clase(): print("�)) Demo: cliente selecciona estrategia (clases) �))") paquete = Paquete(peso_kg=1.0, distancia_km=30) calculador = CalculadorEnvio(EnvioEstandar()) print("Cliente eligió: estandar ->", calculador.calcular(paquete)) calculador.set_estrategia(EnvioExpreso()) print("Cliente cambió a: expreso ->", calculador.calcular(paquete)) print() _# Implementación sin herencia (diccionario de funciones)_ **def** estandar_fn(paquete): **return** round(5.0 + 1.0 * paquete.peso + 0.05 * paquete.distancia, 2) **def** expreso_fn(paquete): **return** round(10.0 + 2.0 * paquete.peso + 0.12 * paquete.distancia, 2) 

**16. Patrones State y Strategy** 

**212** 

**def** demo_strategy_diccionario(): print("�)) Demo: Strategy sin herencia (diccionario) �))") estrategias = { 'estandar': estandar_fn, 'expreso': expreso_fn, 'plana': **lambda** p: 9.99, } paquete = Paquete(peso_kg=3.0, distancia_km=50) **for** nombre **in** ('estandar', 'expreso', 'plana'): coste = estrategias[nombre](paquete) print(f" **{** nombre **}** :", coste) print() **if** __name__ �) '__main__': demo_strategy_clases() cliente_selecciona_estrategia_clase() demo_strategy_diccionario() 

###### **16.2.5 Comentarios de diseño** 

En el ejemplo del semáforo, la clase Semaforo actúa como _Context_ . Las clases Rojo, Verde y Amarillo son los _State_ concretos. Cada clase implementa los métodos necesarios y conoce la transición al siguiente estado. En el ejemplo de envío, CalculadorEnvio actúa como cliente del patrón Strategy y la estrategia concreta se inyecta desde fuera. 

Más allá del diagrama de clases (que muestra la estructura estática heredada de GoF), conviene complementarlo con dos diagramas que re�ejan aspectos que la estructura de clases no captura: el diagrama de estados, que muestra las transiciones reales entre estados; y el diagrama de secuencia, que muestra quién invoca a quién en tiempo de ejecución. 

**16.2. Patrón State** 

**213** 



El diagrama de secuencia siguiente evidencia el punto clave del patrón State: el cliente le pide al contexto que avance (siguiente()), pero es el propio estado actual quien decide y ejecuta la transición, invocando cambiar_estado(�))) sobre el contexto: 

**16. Patrones State y Strategy** 

**214** 



##### **16.3 Patrón Strategy** 

###### **16.3.1 Motivación** 

El patrón Strategy permite de�nir una familia de algoritmos intercambiables y hacer que el cliente los seleccione en tiempo de ejecución. Es útil cuando se desea variar el algoritmo de un objeto sin modi�carlo, o cuando diferentes estrategias son necesarias según la con�guración o el contexto. 

Ventajas: 

- Separa las políticas (algoritmos) de la lógica que las utiliza. 

- Facilita pruebas unitarias de cada estrategia por separado. 

- Añadir nuevas estrategias no requiere cambios en el cliente. 

###### **16.3.2 Contrato (interfaz)** 

- Una interfaz (por ejemplo, un método execute(�)))) que implementan las estrategias concretas. 

- Un objeto cliente que mantiene una referencia a la estrategia actual y la invoca. 

El diagrama de clases del ejemplo de cálculo de envío es estructuralmente muy similar al de State (ambos usan una interfaz común y un contexto que delega), pero la relación semántica es distinta: aquí el contexto (CalculadorEnvio) 

**16.3. Patrón Strategy** 

**215** 

no conoce las transiciones entre estrategias, simplemente delega el cálculo a la estrategia que tiene asignada en cada momento. 



<!-- Start of picture text -->
1 - estrategia : Estrategiatnvio<br>© set e strategia(estrategia)<br>© calcularCpaquete) : Float<br>a)<br>\<br>\<br>\<br>| (© peso : Float<br>© caleutar(paquete) : float O distancia : float<br>S lL XR ———————<br>——<br>—— —<br><!-- End of picture text -->

###### **16.3.3 Ejemplo: cálculo de coste de envío** 

Motivación del ejemplo: un sistema de ventas puede calcular el coste de envío usando distintas políticas (envío estándar, exprés, gratuito por promoción, tarifa plana). El cliente (por ejemplo, un objeto ShipmentCalculator) delega el cálculo a la estrategia seleccionada. 

###### **16.3.4 Código de ejemplo** 

El mismo archivo de ejemplo contiene implementaciones de Strategy y una demostración de intercambio de estrategias en tiempo de ejecución. 

El siguiente diagrama de secuencia complementa al diagrama de clases mostrando el contraste con State: aquí es el cliente quien decide y asigna la estrategia (set_estrategia(�))) set_estrategia(... ) ) antes de pedir el cálculo; el contexto no decide nada por sí mismo. 

**16. Patrones State y Strategy** 

**216** 



##### **16.4 Ejercicios** 

1. Modi�car el ejemplo del semáforo para que soporte modo peatonal: al activar el modo peatonal, las transiciones deben incorporar un estado adicional que permita el cruce peatonal. 

2. Añadir una nueva estrategia de envío que calcule coste en función del peso y dimensiones y compararla con las estrategias existentes. 

3. Diseñar pruebas unitarias (pytest) para las estrategias de envío: cubrir al menos la estrategia estándar y la exprés. 

4. Re�exión: comparar State y Strategy; ¿en qué casos usarías uno u otro? Dar un ejemplo real donde ambos pueden aplicarse pero uno sea más adecuado. 

##### **16.5 Conclusión** 

State y Strategy son patrones primas hermanas: ambos encapsulan comportamientos intercambiables, pero State encapsula comportamientos que corresponden a estados del objeto y normalmente implican transiciones entre estados, mientras que Strategy encapsula algoritmos intercambiables que el 

**16.5. Conclusión** 

**217** 

cliente selecciona sin cambiar su identidad. 

Estos patrones fomentan la separación de responsabilidades, hacen el código más modular y facilitan la extensión del sistema. 

###### **16.5.1 Quién selecciona los cambios: una diferencia clave** 

Una distinción conceptual muy importante entre _State_ y _Strategy_ es _quién_ decide qué comportamiento se usa en cada momento: 

- **State: selección interna.** En el patrón State los cambios de comportamiento son el resultado de las transiciones internas del propio objeto contexto o de la lógica de los estados concretos. Cada estado conoce las reglas para pasar al siguiente estado o para modi�car el comportamiento del contexto. El cliente que utiliza el contexto no selecciona directamente el estado; envía mensajes al contexto y este delega al estado actual. Es decir, el control del �ujo de estados es responsabilidad del contexto/los estados. 

- **Strategy: selección externa.** En el patrón Strategy la elección de la política (algoritmo) la realiza el cliente que usa el objeto contexto o una parte externa del sistema (por ejemplo, una fábrica, una con�guración). El contexto delega el trabajo a la estrategia que tiene asignada, pero no decide por sí mismo qué estrategia usar; la estrategia se le inyecta desde fuera. Esto hace que Strategy sea ideal cuando la política depende de factores externos (con�guración, preferencia del usuario, pruebas A/B, etc.). 

En resumen: si el comportamiento debe cambiar porque el propio objeto evoluciona (transiciones internas), State es la opción natural; si el comportamiento cambia porque el cliente o la con�guración lo decide, Strategy es la opción correcta. 

###### **16.5.2 Consecuencia en los ejemplos** 

En los ejemplos que acompañan este capítulo mostramos ambas situaciones: 

- En la sección _State_ (semáforo) el propio contexto y sus estados realizan las transiciones: el cliente no selecciona el siguiente estado, simplemente solicita operaciones (por ejemplo, siguiente()) y el contexto decide la transición. 

**16. Patrones State y Strategy** 

**218** 

- En la sección _Strategy_ (envío) el cliente selecciona la estrategia: el ejemplo muestra cómo el cliente construye o cambia la estrategia del CalculadorEnvio y cómo, en la versión sin herencia, el cliente selecciona una función del diccionario de estrategias. 

Esto tiene implicaciones de diseño: si quieres que la política pueda ser cambiada por el usuario o por la con�guración, coloca la selección fuera del contexto (Strategy). Si en cambio la política depende del ciclo de vida o del estado interno del objeto, usa State. 

##### **16.6 Implementaciones sin herencia: cuándo usar un diccionario de funciones** 

En casos sencillos donde cada _State_ o _Strategy_ reduce su interfaz a un único método (por ejemplo handle() o calculate(�)))), y donde las implementaciones no requieren mantener un estado interno complejo, es frecuente en Python usar alternativas más ligeras que las jerarquías de clases. Una opción idiomática y pragmática es emplear funciones o _callables_ y almacenarlas en un diccionario que actúe como mapa de comportamiento. 

Ventajas de esta aproximación: 

- Menos código ceremonioso: no hay necesidad de de�nir muchas clases pequeñas. 

- Más simple de leer cuando las funciones son pequeñas y puras. 

- Fácil de serializar/con�gurar (por ejemplo, cargar el nombre de la estrategia desde con�guración y buscarla en el diccionario). 

Limitaciones: 

- Menos �exible si las implementaciones necesitan conservar estado entre llamadas. 

- Pierde la semántica explícita de una jerarquía de tipos (puede ser menos claro para ciertos diseños). 

Ejemplo breve: 

**Ejemplo: Strategy con un diccionario de funciones** 

**class Paquete** : **def** __init__(self, peso, distancia): self.peso = peso 

**21916.6. Implementaciones sin herencia: cuándo usar un diccionario de funciones** 

self.distancia = distancia **def** estandar(paquete): **return** 5.0 + 1.0 * paquete.peso + 0.05 * paquete.distancia **def** expreso(paquete): **return** 10.0 + 2.0 * paquete.peso + 0.12 * paquete.distancia estrategias = { "estandar": estandar, "expreso": expreso, } paquete = Paquete(1.0, 100) costo = estrategias["estandar"](paquete) print(costo) 

El siguiente diagrama complementario ilustra esta variante: no hay jerarquía de clases ni interfaz común, sino un objeto dict que asocia directamente un nombre de estrategia con la función ( _callable_ ) que la implementa. 



Esta técnica es perfectamente válida cuando el conjunto de operaciones es reducido y las alternativas son esencialmente funciones puras. 

Córdoba, 2026. 

## **Desarrollo de Aplicaciones con Objetos** 

#### **Material conceptual** 

**Interfaces graficas en python.** 

##### **Introducción** 

Para crear formularios en pantalla en Python, puedes utilizar bibliotecas gráficas como Tkinter, PyQt, wxPython y Kivy. Cada una de estas bibliotecas tiene sus propias ventajas y desventajas, por lo que puedes elegir la que mejor se adapte a tus necesidades y preferencias. 

A continuación, una breve introducción a cómo utilizar la biblioteca Tkinter para crear formularios simples en pantalla: 

##### **Tkinter** : 

Tkinter es una biblioteca gráfica incorporada en Python que te permite crear interfaces de usuario de manera sencilla. Aquí hay un ejemplo básico de cómo crear un formulario de entrada de datos con Tkinter: 



<!-- Start of picture text -->
import tkinter as tk<br>def Q:<br>nombre = entry_nombre.get()<br>edad = entry_edad.get()<br>print( )<br>ventana = tk.Tk()<br>ventana.title( )<br>label_nombre = tk.Label(ventana, text= )<br>label_nombre.pack()<br>entry_nombre = tk.Entry(ventana)<br>entry_nombre.pack()<br><!-- End of picture text -->



<!-- Start of picture text -->
label_nombre = tk.Label(ventana, text= )<br>label_nombre.pack()<br>entry_nombre = tk.Entry(ventana)<br>entry_nombre.pack()<br>label_edad = tk.Label(ventana, text= )<br>label_edad.pack()<br>entry_edad = tk.Entry(ventana)<br>entry_edad.pack()<br>boton_enviar = tk.Button(ventana, text= , command=enviar_datos)<br>boton_enviar.pack()<br>ventana.mainloop()<br><!-- End of picture text -->

Este es un formulario muy simple que recopila el nombre y la edad de una persona y los muestra en la consola cuando se hace clic en el botón "Enviar". Tkinter ofrece muchas más capacidades para crear interfaces de usuario más complejas con botones, cuadros de lista, casillas de verificación, etc. Puedes personalizar y diseñar tu formulario según tus necesidades. 

Ten en cuenta que Tkinter está disponible por defecto en la mayoría de las instalaciones de Python, por lo que es una excelente opción para comenzar a crear interfaces de usuario simples. Si necesitas funcionalidades más avanzadas o un diseño más atractivo, podrías explorar otras bibliotecas como PyQt o wxPython. 

##### **Controles mas utilizados.** 

Tkinter ofrece una variedad de componentes para crear interfaces gráficas de usuario en Python. Algunos de los componentes más utilizados son: 

1. **Ventana (Window)** : La ventana principal de la aplicación donde se colocan todos los demás componentes. 

2. **Etiqueta (Label)** : Se utiliza para mostrar texto o una etiqueta en la ventana. 

3. **Cuadro de Texto (Entry)** : Permite al usuario ingresar texto, como nombres o contraseñas. 

4. **Botón (Button)** : Se utiliza para activar una acción cuando se hace clic en él, como enviar un formulario. 

5. **Cuadro de Lista (Listbox)** : Proporciona una lista de elementos donde el usuario puede seleccionar uno o más. 

6. **Cuadro de Texto Multilínea (Text)** : Permite la entrada y visualización de texto en varias líneas. 

7. **Casilla de Verificación (Checkbutton)** : Permite al usuario seleccionar o deseleccionar una opción. 

8. **Botón de Radio (Radiobutton)** : Permite al usuario seleccionar una opción entre varias opciones mutuamente excluyentes. 

9. **Barra de Desplazamiento (Scrollbar)** : Se utiliza junto con otros widgets, como cuadros de lista y cuadros de texto, para desplazarse por contenido más largo. 

**10. Cuadro de Diálogo (Dialog):** Ventanas emergentes que permiten al usuario tomar decisiones o proporcionar información adicional. 

11. **Cuadro de Mensaje (Message):** Muestra un mensaje de texto en una ventana emergente. 

**12. Menú (Menu):** Permite crear barras de menú en la parte superior de la ventana. 

**13. Canvas:** Un área rectangular donde se pueden dibujar formas gráficas y gráficos. 

**14. Frames (Marcos):** Se utilizan para organizar y agrupar otros widgets. 

**15. Imagen (PhotoImage):** Permite mostrar imágenes en la ventana. 

**16. Reloj (Clock):** Muestra la hora y fecha actual. 

Estos son solo algunos de los componentes más comunes en Tkinter. Puedes combinarlos y personalizarlos para crear interfaces de usuario completas y funcionales. La elección de los componentes depende de los requisitos específicos de tu aplicación. 

##### **Ventana:** 

En la biblioteca Tkinter, la ventana principal se crea utilizando la clase **Tk()** , y puedes configurar varias propiedades de esta ventana. Algunas de las propiedades más comunes que puedes establecer en una ventana Tkinter incluyen: 

1. **Título de la Ventana (title)** : El título que aparece en la barra de título de la ventana. 

```
ventana.title("Mi Ventana")
```

2. **Dimensiones de la Ventana (geometry)** : El tamaño y la posición inicial de la ventana en píxeles. Por ejemplo, "400x300" crea una ventana de 400 píxeles de ancho por 300 píxeles de alto. 

```
ventana.geometry("400x300")
```

3. **Ícono de la Ventana (iconbitmap)** : Establece un icono personalizado para la ventana. Debe ser un archivo .ico. 

```
ventana.iconbitmap("icono.ico")
```

4. **Color de Fondo (configure)** : Cambia el color de fondo de la ventana. 

```
ventana.configure(bg="lightblue")
```

5. **Modo Redimensionable (resizable)** : Permite o impide que el usuario redimensione la ventana en anchura y altura. Los valores posibles son **"1"** (redimensionable) o **"0"** (no redimensionable). 

```
ventana.resizable(1, 1) # La ventana es redimensionable en ambas
direcciones
```

6. **Posición Inicial (geometry)** : Establece la posición inicial de la ventana en la pantalla. Puedes usar **"+x+y"** para establecer la posición en las coordenadas (x, y). 

```
ventana.geometry("+100+50") # Abre la ventana en la posición (100, 50)
```

7. **Eliminar Ventana (destroy)** : Cierra la ventana cuando se presiona la "X" en la esquina superior derecha. 

```
ventana.destroy()
```

8. **Función al Cerrar (protocol)** : Permite especificar una función que se ejecutará cuando se cierre la ventana. 

```
ventana.protocol("WM_DELETE_WINDOW", funcion_cerrar)
```

9. **Cambiar Cursor (cursor)** : Cambia la apariencia del cursor cuando pasa sobre la ventana. 

```
ventana.config(cursor="arrow")
```

Estas son algunas de las propiedades comunes que puedes configurar en una ventana Tkinter. Puedes ajustar estas propiedades según tus necesidades específicas para personalizar la apariencia y el comportamiento de tu ventana. 

##### **Cuadro de texto:** 

Para un cuadro de texto en Tkinter, generalmente se utiliza el widget **Entry** . Aquí están algunas de las propiedades y configuraciones más comunes que puedes aplicar a un cuadro de texto ( **Entry** ): 

1. **Texto Inicial (insert) y Posición del Cursor (insert)** : Puedes establecer un texto inicial dentro del cuadro de texto y controlar la posición inicial del cursor. 

```
entry = Entry(ventana)
```

```
entry.insert(0, "Texto Inicial")
```

```
entry.icursor(0) # Coloca el cursor al principio
```

2. **Ancho (width) y Altura (height)** : Configura el ancho y la altura del cuadro de texto en caracteres y líneas, respectivamente. 

```
entry = Entry(ventana, width=30, height=5)
```

3. **Estado (state)** : Puede establecer el estado del cuadro de texto como "normal" o "disabled". Cuando está deshabilitado, el usuario no puede editar el contenido. 

```
entry = Entry(ventana, state="normal") # También puedes usar
"disabled"
```

4. **Fondo (bg) y Color del Texto (fg)** : Puedes cambiar el color de fondo y el color del texto del cuadro de texto. 

```
entry = Entry(ventana, bg="lightgray", fg="black")
```

5. **Borde (borderwidth) y Relieve (relief)** : Controla el ancho del borde y el estilo del relieve alrededor del cuadro de texto. 

```
entry = Entry(ventana, borderwidth=2, relief="groove")
```

6. **Ocultar el Texto (show)** : Si deseas que el texto ingresado en el cuadro de texto se muestre como un carácter diferente (por ejemplo, contraseñas), puedes usar la opción **show** . 

```
entry = Entry(ventana, show="*") # Muestra asteriscos en lugar de
texto
```

7. **Evento de Tecla (bind)** : Puedes asignar una función para que se ejecute cuando se presione una tecla en el cuadro de texto. 

`def tecla_presionada(event): print("Tecla presionada:", event.keysym) entry.bind("<Key>", tecla` _presionada) 

8. **Obtener Valor (get) y Establecer Valor (insert)** : Para obtener el valor actual en el cuadro de texto y para establecer un nuevo valor, puedes usar los métodos **get()** e **insert()** . 

`valor = entry.get() # Obtiene el valor actual del cuadro de texto entry.insert(0, "Nuevo Texto") # Establece` un nuevo valor 

Estas son algunas de las configuraciones más comunes que puedes aplicar a un cuadro de texto en Tkinter. Puedes personalizar aún más según tus necesidades específicas. 

##### **Para editar el contenido.** 

El método **insert** del widget **Entry** en Tkinter se utiliza para insertar texto en el cuadro de texto. Tiene dos parámetros: 

1. **Posición de Inserción (index)** : Este es el primer parámetro y especifica dónde se insertará el nuevo texto en el cuadro de texto. Puedes especificar la posición de inserción como un número entero o como una cadena de la forma **"line.column"** , donde **line** es el número de línea y **column** es el número de columna. El primer carácter tiene la posición **1.0** en Tkinter. 

   - Para insertar texto al principio del cuadro de texto: **entry.insert(1.0, "Texto a Insertar")** 

   - Para insertar texto en la posición actual del cursor: **entry.insert(INSERT, "Texto a Insertar")** 

   - Para insertar texto al final del cuadro de texto: **entry.insert(END, "Texto a Insertar")** 

2. **Texto a Insertar (string)** : Este es el segundo parámetro y representa el texto que deseas insertar en el cuadro de texto. 

##### **Borrar el contenido.** 

Puedes borrar el contenido de un widget **Entry** en Tkinter utilizando el método **delete** para eliminar el texto que está actualmente en el cuadro de entrada. El método **delete** toma dos argumentos: 

1. **Índice de Inicio** : Este es el índice del primer carácter que deseas borrar. Puedes especificarlo como una cadena en el formato **"line.column"** o como dos números enteros que representan la línea y la columna. 

2. **Índice de Fin** : Este es el índice del carácter después del último que deseas borrar. De nuevo, puede especificarse como una cadena en el formato **"line.column"** o como dos números enteros. 

Para borrar todo el contenido del cuadro de entrada, puedes usar **"1.0"** como el índice de inicio (que representa el primer carácter) y **END** como el índice de fin (que representa el final del cuadro de entrada). 

##### **Validar texto** 

Para realizar validaciones de datos en una ventana de texto (Entry) en una aplicación de tkinter, puedes usar el método **validate** junto con la opción **validatecommand** . Aquí hay una breve descripción de cómo puedes hacerlo: 

1. **Define una función de validación:** Antes de crear el campo de entrada (Entry), define una función que realizará la validación. Esta función debe tener la firma **(new_value, user_input)** , donde **new_value** es el nuevo valor que se va a establecer en el Entry después de la edición y **user_input** es la entrada actual en el campo. 



<!-- Start of picture text -->
def (new_value, user_input):<br>if new_value.isnumeric() and int(new_value) >= 0:<br>return True<br><!-- End of picture text -->

```
def validate_input(new_value, user_input):
```

```
# Realiza tus validaciones aquí
if new_value.isnumeric() and int(new_value) >= 0:
return True
else:
return False
```

2. **Crea el campo de entrada:** Crea el campo de entrada (Entry) y establece las opciones **validate** y **validatecommand** para que tkinter realice la validación automáticamente: 



<!-- Start of picture text -->
from tkinter import *<br>root = Tk()<br>vemd = root.register(validate_input)<br>entry = Entry(root, validate= » validatecommand=(vemd, : ))<br>entry.pack()<br>root.mainloop()<br><!-- End of picture text -->

```
from tkinter import *
```

```
root = Tk() vcmd = root.register(validate_input) # Registra la función
de validación
entry = Entry(root, validate="key", validatecommand=(vcmd, "%P",
"%S")) entry.pack()
root.mainloop()
```

En el ejemplo anterior: 

- **validate="key"** le indica a tkinter que debe realizar la validación en cada evento de teclado. 

- **validatecommand=(vcmd, "%P", "%S")** especifica la función de validación ( **vcmd** ) y los parámetros **%P** y **%S** . **%P** representa el valor después de la edición, y **%S** representa el carácter que se va a insertar. 

Dentro de la función **validate_input** , puedes realizar tus propias validaciones personalizadas. Si la validación falla, devuelve **False** , lo que evitará que se realice la edición en el Entry. 

Puedes adaptar esta lógica de validación según tus necesidades específicas, como validar números, texto, fechas, etc. 

##### **Método Mainloop()** 

En el contexto de aplicaciones gráficas desarrolladas con bibliotecas como Tkinter (una biblioteca de GUI para Python), **mainloop()** es un método importante que inicia el bucle principal del programa. Este bucle principal se encarga de escuchar y responder a eventos, como clics de ratón, pulsaciones de teclas y otras interacciones del usuario, así como de actualizar la interfaz gráfica según sea necesario. 

Cuando se llama a **mainloop()** , la aplicación entra en un estado en el que está constantemente esperando eventos y respondiendo a ellos. Esto permite que la interfaz gráfica permanezca interactiva y receptiva para el usuario. Si no se llama a **mainloop()** , la ventana de la interfaz gráfica se abrirá, pero la aplicación no responderá a las interacciones del usuario ni se actualizará. 

En resumen, **mainloop()** es esencial para que una aplicación gráfica en Python, creada con bibliotecas como Tkinter, funcione de manera adecuada, ya que inicia el ciclo de eventos que maneja todas las interacciones del usuario. 

##### **Método Pack.** 

En la biblioteca Tkinter de Python, el método **pack()** se utiliza para organizar y colocar widgets (como botones, etiquetas, cuadros de texto, etc.) dentro de un contenedor, generalmente un widget contenedor, como un Frame o una ventana principal. El método **pack()** es una forma de administrar la disposición de los widgets dentro de un contenedor de manera simple y eficiente. 

Aquí hay algunos puntos clave sobre cómo funciona el método **pack()** : 

1. **Empaquetamiento vertical u horizontal:** El método **pack()** organiza los widgets en un contenedor en una sola dirección: vertical (de arriba a abajo) o horizontal (de izquierda a derecha). Esto se controla mediante el argumento **side** , que puede ser **"top"** , **"bottom"** , **"left"** o **"right"** . 

2. **Alineación:** Puedes controlar la alineación de los widgets dentro del contenedor utilizando el argumento **anchor** . Por ejemplo, **"w"** alinea los widgets a la izquierda (oeste), mientras que **"e"** los alinea a la derecha (este). 

3. **Relleno:** Puedes especificar cuánto espacio adicional debe agregarse alrededor de un widget utilizando los argumentos **padx** (para el relleno horizontal) y **pady** (para el relleno vertical). 

4. **Expansión:** Puedes permitir que un widget se expanda para llenar cualquier espacio adicional disponible en su dirección de empaquetamiento utilizando el argumento **fill** . 

5. **Orden de empaquetamiento:** Los widgets se empaquetan en el orden en que se agregan al contenedor. Puedes cambiar este orden utilizando el método **pack()** nuevamente en un widget para moverlo hacia la parte superior o la parte inferior del contenedor. 

6. **Widget maestro:** El método **pack()** generalmente se llama en un widget contenedor (por ejemplo, un Frame) para organizar sus widgets secundarios. Los widgets secundarios se agregan al contenedor utilizando otros métodos, como **Label** , **Button** , etc. 

Aquí hay un ejemplo simple de cómo se usa **pack()** : 



<!-- Start of picture text -->
import tkinter as tk<br>root = tk.Tk()<br>frame = tk.Frame(root)<br>frame .pack(side= » padx=i0, pady=10, fill= » expand=True)<br>labeli1 = tk.Label(frame, text= )<br>label2 = tk.Label(frame, text= )<br>button = tk.Button(frame, text= )<br>label1.pack(side= )<br>label2.pack(side= )<br>button.pack(side= )<br>root.mainloop()<br><!-- End of picture text -->

En este ejemplo, hemos creado un Frame ( **frame** ) y hemos empaquetado tres widgets ( **label1** , **label2** , **button** ) dentro de él usando **pack()** . Los argumentos **side** , **padx** , **pady** , **fill** y **expand** se utilizan para controlar la disposición y el espacio en el contenedor. 

**Eventos en Tkinter** 

El manejo de eventos en Tkinter, una biblioteca de interfaz gráfica de usuario (GUI) para Python, es fundamental para interactuar con los elementos de la interfaz gráfica y responder a las acciones del usuario, como hacer clic en un botón o ingresar texto en un cuadro de texto. Para manejar eventos en Tkinter, sigue estos pasos generales: 

1. **Crear la ventana principal:** Primero, crea la ventana principal de la aplicación utilizando Tk(). 

2. **Definir funciones de controladores de eventos:** Crea funciones que se ejecutarán cuando ocurra un evento específico. Por ejemplo, si deseas que algo suceda cuando un botón se presione, define una función que contenga ese comportamiento. 

3. **Crear widgets:** Crea los widgets (botones, etiquetas, cuadros de texto, etc.) en la ventana principal. 

En este ejemplo, el argumento **command** se utiliza para especificar la función que se llamará cuando se haga clic en el botón. 

4. **Empaquetar widgets:** Utiliza el método **pack()** o **grid()** para colocar los widgets en la ventana principal. 

5. **Iniciar el bucle principal:** Finalmente, inicia el bucle principal de la aplicación para que la ventana se muestre y los eventos sean manejados. 

A continuación, se presentan ejemplos de manejo de eventos para diferentes tipos de widgets en Tkinter: 

**Manejo de eventos de botón:** 



<!-- Start of picture text -->
def QO:<br>label. config(text= )<br>root = tk.Tk()<br>label = tk.Label(root, text="")<br>label. pack()<br>button = tk.Button(root, text= , command=boton_clicado)<br>button. pack()<br>root.mainloop()<br><!-- End of picture text -->

**Manejo de eventos de entrada de texto (Entry):** 



<!-- Start of picture text -->
ef QO:<br>contenido = entry.get()<br>label. config(text= )<br>root = tk.Tk()<br>label = tk.Label(root, text="")<br>label. pack()<br>entry = tk.Entry(root)<br>entry.pack()<br>button = tk.Button(root, text= , command=mostrar_texto)<br>button. pack()<br>root.mainloop()<br><!-- End of picture text -->

Con el uso de bind() y trace(), puedes capturar y manejar eventos en un campo de texto Entry de Tkinter. Estos son algunos de los eventos más comunes: 

- <Return>: Captura cuando se presiona "Enter". 

- <Key>: Captura cualquier pulsación de tecla. 

- trace('write'): Detecta cambios en el texto del Entry. 

- <FocusIn> y <FocusOut>: Capturan cuando el campo de texto gana o pierde el foco. 

- "break": Se usa para evitar que un evento continúe, útil para limitar caracteres. 

Ejemplo Return: Evento para controlar cuando se presiona Enter 

```
import tkinter as tk
# Crear la ventana principal
root = tk.Tk()
root.title("Evento Enter en Entry")
# Función que se ejecuta al presionar "Enter"
def al_presionar_enter(event):
    texto = entry.get()
    print(f"Texto ingresado: {texto}")
```

```
# Crear un campo de entrada
entry = tk.Entry(root)
entry.pack(pady=10)
```

`# Vincular el evento de presionar "Enter" con la función entry.bind('<Return>', al_presionar_enter) # Ejecutar la aplicación root.mainloop()` Ejemplo Evento Obtener y perder foco (FocusIn FocusOut) `import tkinter as tk # Crear la ventana principal root = tk.Tk() root.title("Eventos de foco en Entry") # Función que se ejecuta al obtener el foco def al_obtener_foco(event): print("Entry ha ganado el foco") # Función que se ejecuta al perder el foco def al_perder_foco(event): print("Entry ha perdido el foco") # Crear un campo de entrada entry = tk.Entry(root) entry.pack(pady=10) # Vincular los eventos de foco entry.bind('<FocusIn>', al_obtener_foco) entry.bind('<FocusOut>', al_perder_foco)` 

```
# Ejecutar la aplicación
root.mainloop()
```

##### **Manejo de eventos de listbox:** 



<!-- Start of picture text -->
def Q:<br>seleccion = listbox.curselection()<br>if seleccion:<br>indice = seleccion[0]<br>elemento = listbox.get(indice)<br>label. config(text= )<br>label. config(text= )<br>root = tk.Tk()<br>label = tk.Label(root, text="")<br>label. pack()<br>listbox = tk.Listbox(root)<br>listbox. pack()<br>listbox.insert(i, )<br>listbox.insert(2, )<br>listbox.insert(3, )<br>button = tk.Button(root, text= » command=mostrar_elemento_<br>button. pack()<br>root.mainloop()<br><!-- End of picture text -->

##### **Clase TTK** 

La clase **ttk** en Python se refiere a la biblioteca "themed Tkinter" (ttk), que es una extensión de la biblioteca estándar Tkinter utilizada para crear interfaces gráficas de usuario (GUI) en aplicaciones de escritorio. Tkinter es una biblioteca muy comúnmente utilizada para crear GUI en Python, y ttk mejora y moderniza la apariencia de los widgets de Tkinter. 

Las principales ventajas de usar **ttk** son: 

1. **Aspecto nativo** : ttk proporciona una apariencia más moderna y nativa en diferentes sistemas operativos, lo que significa que sus aplicaciones tendrán una apariencia más coherente en diferentes plataformas. 

2. **Widgets adicionales** : ttk agrega algunos widgets adicionales que no están disponibles en el conjunto estándar de Tkinter, como el Combobox y el Notebook, que son útiles para ciertos tipos de aplicaciones. 

3. **Personalización mejorada** : **ttk** ofrece una mayor capacidad de personalización de la apariencia de los widgets, lo que le permite ajustar el aspecto de su GUI de acuerdo con sus necesidades. 

4. **Temas** : Puede seleccionar entre diferentes temas o estilos predefinidos para su GUI, lo que facilita la creación de interfaces atractivas sin tener que personalizar cada detalle de la apariencia. 

5. **Mejor manejo de fuentes y colores** : ttk proporciona una mejor gestión de fuentes y colores, lo que hace que sea más fácil crear interfaces coherentes y atractivas. 

Para utilizar **ttk** , primero debe importarlo en su código, generalmente de la siguiente manera: 



<!-- Start of picture text -->
import tkinter as tk<br>from tkinter import ttk<br><!-- End of picture text -->

##### **Controles principales** 

La biblioteca **ttk** (tema de Tkinter) agrega varios controles y widgets que pueden utilizarse para crear interfaces de usuario modernas y atractivas en aplicaciones de Python. Aquí hay una lista de algunos de los controles más comunes proporcionados por **ttk** : 

1. **Botones (Button)** : 

   - **ttk.Button** : Un botón con una apariencia moderna y mejorada en comparación con el botón estándar de Tkinter. 

2. **Etiquetas (Label)** : 

   - **ttk.Label** : Una etiqueta de texto que se utiliza para mostrar información o etiquetar otros widgets. 

3. **Entradas de texto (Entry)** : 

   - **ttk.Entry** : Un cuadro de entrada de texto que permite al usuario escribir texto o números. 

4. **Cuadros de lista (Listbox)** : 

   - **ttk.Treeview** : Un cuadro de lista que puede mostrar datos en forma de tabla con columnas y filas. Se utiliza comúnmente para mostrar datos tabulares. 

5. **Combobox (Combobox)** : 

   - **ttk.Combobox** : Un cuadro combinado que combina una entrada de texto con una lista desplegable. Útil cuando se espera que el usuario elija una opción de una lista predefinida. 

6. **Cuadernos (Notebook)** : 

   - **ttk.Notebook** : Un control que permite crear pestañas en una interfaz de usuario. Útil para organizar contenido en múltiples pestañas. 

7. **Barra de progreso (Progressbar)** : 

   - **ttk.Progressbar** : Una barra de progreso que muestra el progreso de una tarea en curso. 

8. **Radiobotones (Radiobuttons)** : 

   - **ttk.Radiobutton** : Botones de opción que permiten al usuario seleccionar una sola opción de un conjunto. 

9. **Casillas de verificación (Checkbuttons)** : 

   - **ttk.Checkbutton** : Casillas que permiten al usuario seleccionar una o varias opciones de un conjunto. 

10. **Barra de desplazamiento (Scrollbar)** : 

   - **ttk.Scrollbar** : Una barra de desplazamiento que se utiliza comúnmente junto con otros widgets para permitir la navegación o el desplazamiento de contenido. 

11. **Separadores (Separator)** : 

   - **ttk.Separator** : Una línea divisoria utilizada para separar visualmente diferentes secciones de una interfaz de usuario. 

12. **Árbol (Tree)** : 

   - **ttk.Treeview** : Un control que muestra datos en una estructura jerárquica, similar a una estructura de árbol. 

Estos son algunos de los controles más utilizados proporcionados por **ttk** . Puede personalizar la apariencia de estos controles y utilizarlos para crear interfaces gráficas atractivas y modernas en sus aplicaciones de Python. 

**Themes – Temas de TTK** 

La biblioteca **ttk** de Tkinter proporciona varios temas predefinidos que puedes utilizar para personalizar la apariencia de tus widgets y controles. Estos temas están diseñados para que puedas cambiar rápidamente la apariencia de tu aplicación sin tener que configurar manualmente cada detalle de cada widget. 

A partir de la versión 8.5 de Tkinter, los temas disponibles pueden variar según tu versión de Python y Tkinter. Sin embargo, algunos de los temas más comunes que puedes encontrar en versiones modernas de Python incluyen: 

1. **clam** : Un tema simple y limpio. 

2. **alt** : Un tema alternativo con botones planos y colores suaves. 

3. **aqua** : Un tema que sigue las convenciones de apariencia de Aqua en macOS. 

4. **default** : El tema predeterminado de la plataforma, que depende del sistema operativo en uso. 

5. **classic** : Un tema que imita el aspecto clásico de Tkinter. 

6. **vista** : Un tema que sigue el estilo de Windows Vista. 

7. **xpnative** : Un tema que sigue el estilo de Windows XP. 

8. **winnative** : Un tema que imita la apariencia nativa de Windows. 

Puedes seleccionar un tema específico utilizando el método **ttk.Style().theme_use(nombre_del_tema)** antes de crear tus widgets. Por ejemplo, para usar el tema "clam", puedes hacerlo de la siguiente manera: 



<!-- Start of picture text -->
import tkinter as tk<br>from tkinter import ttk<br>ttk.Style().theme_use( )<br>ventana = tk.Tk()<br>boton = ttk.Button(ventana, text= )<br>boton.pack()<br>ventana.mainloop()<br><!-- End of picture text -->

##### Ejercicios de practica: 

##### **1. Formulario de Registro de Usuario con Validaciones** 

Crea un formulario de registro de usuario que contenga los siguientes campos: 

- Nombre de usuario (Entry) 

- Correo electrónico (Entry) 

- Contraseña (Entry) 

- Confirmar contraseña (Entry) 

- Botón de "Registrar" 

##### **Requisitos:** 

1. El nombre de usuario debe contener solo letras y números (sin espacios). 

2. El correo electrónico debe tener un formato válido (e.g., nombre@dominio.com). 

3. La contraseña debe tener al menos 8 caracteres y contener al menos una letra y un número. 

4. La contraseña y la confirmación deben coincidir. 

5. Cuando se presione el botón "Registrar", debe aparecer un mensaje indicando si la validación fue exitosa o si hubo errores en alguno de los campos. 

##### **2. Formulario de Inicio de Sesión con Eventos de Teclado** 

Crea un formulario de inicio de sesión que tenga los siguientes campos: 

- Nombre de usuario (Entry) 

- Contraseña (Entry) 

- Botón de "Iniciar sesión" 

##### **Requisitos:** 

1. El formulario debe permitir que, al presionar la tecla **"Enter"** , el formulario se envíe automáticamente sin necesidad de presionar el botón. 

2. Implementa un evento que, al perder el foco del campo "Nombre de usuario", verifique si este campo está vacío. Si está vacío, debe aparecer un mensaje de advertencia debajo del campo. 

3. La contraseña debe ocultarse usando el parámetro show="*" en el campo Entry. 

##### **3. Formulario de Datos Personales con Validación de Edad** 

Crea un formulario que recoja los siguientes datos personales: 

- Nombre completo (Entry) 

- Edad (Entry) 

- País (Combobox) 

- Género (RadioButtons) 

- Botón de "Enviar" 

##### **Requisitos:** 

1. Validar que la edad ingresada sea un número mayor de 18. 

2. Implementa un evento que muestre un mensaje de advertencia cuando la edad no sea un número válido. 

3. Al hacer clic en "Enviar", muestra un cuadro de diálogo con todos los datos ingresados y valida que los campos no estén vacíos. 

##### **4. Formulario de Reserva de Hotel con Validación de Fechas** 

Crea un formulario para una reserva de hotel que contenga: 

- Nombre completo (Entry) 

- Fecha de check-in (Entry con formato dd/mm/yyyy) 

- Fecha de check-out (Entry con formato dd/mm/yyyy) 

- Número de personas (Spinbox) 

- Botón de "Reservar" 

##### **Requisitos:** 

1. Validar que las fechas de check-in y check-out tengan el formato correcto y que la fecha de check-out sea posterior a la de check-in. 

2. Validar que el número de personas sea mayor a 0. 

3. Al hacer clic en "Reservar", mostrar una ventana emergente que confirme si los datos son correctos o si hubo algún error en la validación. 

##### **5. Formulario de Contacto con Eventos Dinámicos** 

Crea un formulario de contacto que contenga: 

- Nombre (Entry) 

- Correo electrónico (Entry) 

- Mensaje (Text widget) 

- Botón de "Enviar" 

##### **Requisitos:** 

1. El campo "Correo electrónico" debe validarse en tiempo real: cuando el usuario escriba, si el correo no tiene el formato correcto, debe aparecer una advertencia en color rojo debajo del campo. 

2. El botón "Enviar" solo debe habilitarse si todos los campos han sido llenados correctamente. 

3. Al hacer clic en "Enviar", mostrar un cuadro de diálogo que confirme que el mensaje ha sido enviado. 

##### **6. Formulario de Encuesta con Selección Múltiple y Validación** 

Crea un formulario de encuesta que permita a los usuarios seleccionar varias opciones: 

- Nombre (Entry) 

- Género (RadioButtons) 

- Opciones de preferencia (Checkbuttons) [Ej: Opción 1, Opción 2, Opción 3] 

- Botón de "Enviar" 

##### **Requisitos:** 

1. El campo "Nombre" no debe quedar vacío, y debe validarse que el usuario seleccione al menos una opción en las "Opciones de preferencia". 

2. Cuando el formulario se envíe, mostrar los datos ingresados y las opciones seleccionadas en un cuadro de diálogo. 

3. Si algún campo no es completado, resaltar los campos faltantes con un borde rojo. 

