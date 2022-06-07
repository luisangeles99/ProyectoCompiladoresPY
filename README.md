# Java++
Java++ nace de la idea de construir un compilador en python3, teniendo como objetivo el desarrollo de un lenguaje con el paradigma orientado a objetos. Durante el desarrollo de Java++ hubo muchas ideas diferente que se quisieron incorporar y parte de ellas fue la integracion de una pieza tan importante como PLY.

## Propósito 
Crear un lenguaje de programación orientado a objetos, que sea capaz de crear programas ejecutables capaces de correr operaciones iterativas, recursivas y propias de un lenguaje actual para diseño de programas básicos. 
OOP compiler using python3 . Java++ language name.

## Alcance 
Dirigido a estudiantes de programación o personas con intereses a fin, donde puedan realizar programas básicos que les ayude a tender el funcionamiento básico de un lenguaje de programación. 

# Uso
Java++ viene preparado con una forma muy sencilla de utilizarse, de manera que puedas comenzar a programar lo antes posible. Solamente es necesario utilizar le bash desarrollado de la siguiente manera.

    $bash run.bash fileName

# Versions
## Avance 1
Lexer y Parser

## Avance 2
Tabla de funciones y de variables

## Avance 3
Generación de cod intermedio para expresiones lineales y no lineales

## Avance 4
Generación de cod intermedio para funciones

## Avance 5
Generación de cod intermedio para arreglos

## Avance 6
Definicion de la memoria, limites y estructura
Generacion de cod intermedio usando direcciones

## Avance 7
Documentación versión 1
Definición 

# Errores actuales (Backlog)
  *La declaración de variables globales siempre deberá estar entre la declaración del programa y la primera función, de no ser así habrá un error en compilación debido a que se reiniciará el conteo de variables globales.  

  *Operaciones aritméticas entre funciones marcaran un error, debido a que no cuentan con un suelo falso, primero se intentara hacer la operación, cuando debería ser primero la obtención del resultado de las funciones en cuestión y luego la operación aritmética.  

  *Los arreglos no pueden ser globales, estos tienen no tienen una implementación, por lo cual si son declarados de manera global un error ocurría.  