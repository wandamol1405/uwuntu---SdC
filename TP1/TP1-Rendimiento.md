# TP1 - Rendimiento de Computadoras
## 1.Consigna: 
a. Conseguir un esp32 o cualquier procesador al que se le pueda cambiar la
frecuencia.
Ejecutar un código que demore alrededor de 10 segundos. Puede ser un bucle for
con sumas de enteros por un lado y otro con suma de floats por otro lado.
¿Qué sucede con el tiempo del programa al duplicar (variar) la frecuencia ?

b. Armar una lista de benchmarks, ¿cuales les serían más útiles a cada uno ? ¿Cuáles podrían llegar a medir mejor las
tareas que ustedes realizan a diario ?
Pensar en las tareas que cada uno realiza a diario y escribir en una tabla de dos entradas las tareas y que
benchmark la representa mejor.
https://openbenchmarking.org/test/pts/build-linux-kernel-1.15.0
https://www.tomshardware.com/reviews/cpu-hierarchy,4312.html
cual es el rendimiento de estos procesadores para compilar el kernel
Intel Core i5-13600K (base)
AMD Ryzen 9 5900X 12-Core
Cual es la aceleración cuando usamos un AMD Ryzen 9 7950X 16-Core, cual de ellos hace un uso más eficiente de
la cantidad de núcleos que tiene? y cuál es más eficiente en términos de costo (dinero y energía) ?

c. Archivo de Time Profiling:https://docs.google.com/document/d/1lj3KkO_GthTn3WyfkUsLMWJvGdXblKGyIsxCLVGQOZg/edit?tab=t.0

## 2. Marco Teórico

En esta sección se desarrollan los conceptos fundamentales necesarios para el análisis del rendimiento:

- **Rendimiento:** 
- **Eficiencia:** 
- **Benchmark:** 

## 3. Benchmarks y tareas

Se investigarán distintos benchmarks y se analizará cuáles representan mejor las tareas cotidianas de los usuarios.

Se elaborará una tabla que relacione tareas habituales (como programación, uso de aplicaciones, juegos, etc.) con los benchmarks más adecuados para evaluarlas.

---

## 4. Comparación de CPUs

Se analizará el rendimiento de los siguientes procesadores:

- Intel Core i5-13600K  
- AMD Ryzen 9 5900X 12-Core  

Para ello, se utilizarán datos obtenidos del benchmark de compilación del kernel de Linux.

Se construirá una tabla comparativa que incluya:

- Tiempo de ejecución (en segundos)
- Rendimiento 

A partir de estos datos, se realizará un análisis comparativo entre ambos procesadores.

---

## 5. Speedup

Se calculará la aceleración (speedup) entre los procesadores analizados utilizando la siguiente relación:

---

## 6. Profiling del código (gprof)

Se realizará un análisis de performance sobre un programa en C utilizando la herramienta **gprof**.
-crear archivos (códigos profe)
-compilar -> gcc -pg test_gprof.c test_gprof_new.c -o test_gprof
-ejecutar -> ./test_gprof
-generar analisis -> gprof test_gprof gmon.out > analysis.txt
-sacar caps
-conclusiones


## 7. Parte ESP32
-hacer tabla con el tiempo
-calcular speedup
-explicar resultados 





