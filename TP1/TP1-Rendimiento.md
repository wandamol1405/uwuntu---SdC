# TP1 - Rendimiento de Computadoras

## 1.Consigna


## 1.Consigna

a. Conseguir un esp32 o cualquier procesador al que se le pueda cambiar la
frecuencia.
Ejecutar un código que demore alrededor de 10 segundos. Puede ser un bucle for
con sumas de enteros por un lado y otro con suma de floats por otro lado.
¿Qué sucede con el tiempo del programa al duplicar (variar) la frecuencia ?

b. Armar una lista de benchmarks, ¿cuales les serían más útiles a cada uno ? ¿Cuáles podrían llegar a medir mejor las
tareas que ustedes realizan a diario ?
Pensar en las tareas que cada uno realiza a diario y escribir en una tabla de dos entradas las tareas y que benchmark la representa mejor.

- <https://openbenchmarking.org/test/pts/build-linux-kernel-1.15.0>
- <https://www.tomshardware.com/reviews/cpu-hierarchy,4312.html>

Cual es el rendimiento de estos procesadores para compilar el kernel
Intel Core i5-13600K (base) AMD Ryzen 9 5900X 12-Core.
Cual es la aceleración cuando usamos un AMD Ryzen 9 7950X 16-Core, cual de ellos hace un uso más eficiente de la cantidad de núcleos que tiene? y cuál es más eficiente en términos de costo (dinero y energía) ?
Pensar en las tareas que cada uno realiza a diario y escribir en una tabla de dos entradas las tareas y que benchmark la representa mejor.

- <https://openbenchmarking.org/test/pts/build-linux-kernel-1.15.0>
- <https://www.tomshardware.com/reviews/cpu-hierarchy,4312.html>

Cual es el rendimiento de estos procesadores para compilar el kernel
Intel Core i5-13600K (base) AMD Ryzen 9 5900X 12-Core.
Cual es la aceleración cuando usamos un AMD Ryzen 9 7950X 16-Core, cual de ellos hace un uso más eficiente de la cantidad de núcleos que tiene? y cuál es más eficiente en términos de costo (dinero y energía) ?

c. Archivo de Time Profiling:

- <https://docs.google.com/document/d/1lj3KkO_GthTn3WyfkUsLMWJvGdXblKGyIsxCLVGQOZg/edit?tab=t.0>
c. Archivo de Time Profiling:

- <https://docs.google.com/document/d/1lj3KkO_GthTn3WyfkUsLMWJvGdXblKGyIsxCLVGQOZg/edit?tab=t.0>

## 2. Marco Teórico

En esta sección se desarrollan los conceptos fundamentales necesarios para el análisis del rendimiento:

- **Rendimiento:**
- **Eficiencia:**
- **Benchmark:**
- **Rendimiento:**
- **Eficiencia:**
- **Benchmark:**

---

## 3. Benchmarks

#### 3.1 Definición de benchmarck

Un benchmarck es un conjunto de programas de prueba o programas reales que sirven para medir el rendimiento de un sistema o componente, bajo condiciones específicas y controladas, permitiendo obtener métricas comparables y reproducibles, útiles para tomar desiciones de diseño o compra.

#### 3.2 Clasificación

Los benchmarks pueden clasificarse según el tipo de carga y el objetivo de medición en:

##### 1. Microbenchmarks o programas de juguete

Consisten en pequeños fragmentos de código (generalmente entre 10 y 100 líneas) utilizados para medir una característica específica del sistema, como el rendimiento de un algoritmo o una operación puntual.
Ejemplos: Java Micro Benchmark, Quicksort, criba de Eratóstenes.

##### 2. Benchmarks sintéticos

Son programas diseñados para simular el comportamiento de aplicaciones reales en términos de carga de trabajo y ejecución de instrucciones. Se utilizan para evaluar el rendimiento de componentes específicos o del sistema en general.
Ejemplos: Whetstone, Dhrystone.

##### 3. Benchmarks de kernel (o de núcleo)

Consisten en fragmentos de código extraídos de programas reales, seleccionando la parte más representativa y crítica para el rendimiento. Permiten analizar el desempeño en situaciones cercanas al uso real.

##### 4. Benchmarks con programas reales

Utilizan aplicaciones reales ejecutadas con conjuntos de datos reducidos para evitar tiempos de ejecución excesivos. Son los más representativos del uso real del sistema.
Ejemplos: benchmarks de la familia SPEC (SPECint y SPECfp).

##### 5. Otros benchmarks específicos

Incluyen pruebas orientadas a evaluar aspectos particulares del sistema, como entrada/salida, bases de datos o procesamiento paralelo.
Ejemplos: Linpack, Livermore, NAS, PARSEC.

#### 3.3 Tabla de tareas

#### Benchmarks según tipo de tarea

| Tarea | Benchmark | Justificación |
|------|----------|---------------|
| Navegación web (Google Chrome, Mozilla Firefox) | Basemark Web 3.0  | Evalúa el rendimiento del navegador en tareas web reales como HTML, CSS y JavaScript, simulando el uso cotidiano de páginas. |
| Reproducir videos en línea | UL Procyon Video Playback | Mide la capacidad del sistema para decodificar y reproducir contenido multimedia de forma fluida, evaluando CPU y GPU. |
| Reproducir música en línea | JetStream 2 | Mide la capacidad del sistema de transmitir audio sin problemas. |
| Jugar videojuegos | 3DMark, GFXBench | Prueban el rendimiento gráfico (GPU) y la capacidad del sistema para manejar gráficos 3D exigentes en tiempo real. |
| Redes sociales | Speedometer 2.0 | Simula aplicaciones web interactivas, evaluando la rapidez en la respuesta del navegador ante acciones del usuario. |
| Utilizar IDEs | Cinebench R23, CrystalDiskMark | Cinebench mide rendimiento de CPU en tareas intensivas (compilación), mientras que CrystalDiskMark evalúa velocidad de disco (lectura/escritura de archivos). |
| Modelar usando programas de simulación (Proteus, MultiSIM) | PassMark (CPU y RAM) | Evalúa el rendimiento general del sistema, especialmente CPU y memoria, fundamentales en simulaciones y cálculos complejos. |
---

## 3. Benchmarks

#### 3.1 Definición de benchmarck

Un benchmarck es un conjunto de programas de prueba o programas reales que sirven para medir el rendimiento de un sistema o componente, bajo condiciones específicas y controladas, permitiendo obtener métricas comparables y reproducibles, útiles para tomar desiciones de diseño o compra.

#### 3.2 Clasificación

Los benchmarks pueden clasificarse según el tipo de carga y el objetivo de medición en:

##### 1. Microbenchmarks o programas de juguete

Consisten en pequeños fragmentos de código (generalmente entre 10 y 100 líneas) utilizados para medir una característica específica del sistema, como el rendimiento de un algoritmo o una operación puntual.
Ejemplos: Java Micro Benchmark, Quicksort, criba de Eratóstenes.

##### 2. Benchmarks sintéticos

Son programas diseñados para simular el comportamiento de aplicaciones reales en términos de carga de trabajo y ejecución de instrucciones. Se utilizan para evaluar el rendimiento de componentes específicos o del sistema en general.
Ejemplos: Whetstone, Dhrystone.

##### 3. Benchmarks de kernel (o de núcleo)

Consisten en fragmentos de código extraídos de programas reales, seleccionando la parte más representativa y crítica para el rendimiento. Permiten analizar el desempeño en situaciones cercanas al uso real.

##### 4. Benchmarks con programas reales

Utilizan aplicaciones reales ejecutadas con conjuntos de datos reducidos para evitar tiempos de ejecución excesivos. Son los más representativos del uso real del sistema.
Ejemplos: benchmarks de la familia SPEC (SPECint y SPECfp).

##### 5. Otros benchmarks específicos

Incluyen pruebas orientadas a evaluar aspectos particulares del sistema, como entrada/salida, bases de datos o procesamiento paralelo.
Ejemplos: Linpack, Livermore, NAS, PARSEC.

#### 3.3 Tabla de tareas

#### Benchmarks según tipo de tarea

| Tarea | Benchmark | Justificación |
|------|----------|---------------|
| Navegación web (Google Chrome, Mozilla Firefox) | Basemark Web 3.0  | Evalúa el rendimiento del navegador en tareas web reales como HTML, CSS y JavaScript, simulando el uso cotidiano de páginas. |
| Reproducir videos en línea | UL Procyon Video Playback | Mide la capacidad del sistema para decodificar y reproducir contenido multimedia de forma fluida, evaluando CPU y GPU. |
| Reproducir música en línea | JetStream 2 | Mide la capacidad del sistema de transmitir audio sin problemas. |
| Jugar videojuegos | 3DMark, GFXBench | Prueban el rendimiento gráfico (GPU) y la capacidad del sistema para manejar gráficos 3D exigentes en tiempo real. |
| Redes sociales | Speedometer 2.0 | Simula aplicaciones web interactivas, evaluando la rapidez en la respuesta del navegador ante acciones del usuario. |
| Utilizar IDEs | Cinebench R23, CrystalDiskMark | Cinebench mide rendimiento de CPU en tareas intensivas (compilación), mientras que CrystalDiskMark evalúa velocidad de disco (lectura/escritura de archivos). |
| Modelar usando programas de simulación (Proteus, MultiSIM) | PassMark (CPU y RAM) | Evalúa el rendimiento general del sistema, especialmente CPU y memoria, fundamentales en simulaciones y cálculos complejos. |

---

## 4. Comparación de CPUs

Se analizará el rendimiento de los siguientes procesadores:

- Intel Core i5-13600K  
- AMD Ryzen 9 5900X 12-Core  

Para ello, se utilizarán datos obtenidos del benchmark de compilación del kernel de Linux.

Se construirá una tabla comparativa que incluya:

- Tiempo de ejecución (en segundos)
- Rendimiento
- Rendimiento

A partir de estos datos, se realizará un análisis comparativo entre ambos procesadores.

---

## 5. Speedup

Se calculará la aceleración (speedup) entre los procesadores analizados utilizando la siguiente relación:

---

## 6. Time Profiling en Sistemas de Cómputo

El time profiling es una técnica fundamental en el análisis de rendimiento de software. Permite evaluar el comportamiento interno de un programa durante su ejecución, identificando qué funciones o secciones consumen mayor tiempo de CPU. A diferencia de los benchmarks, que evalúan el rendimiento a nivel más global de un componente o sistema, el profiling se centra en el análisis detallado del desempeño interno del código.

##### Objetivos del Time Profiling

- Identificar las partes del código que consumen mayor tiempo de ejecución.
- Detectar cuellos de botella que afectan el rendimiento del programa.
- Analizar la frecuencia de llamadas a funciones y su costo asociado.
- Optimizar el uso de recursos como CPU y memoria.
- Mejorar la eficiencia general del programa mediante decisiones informadas.

---

## 7. Análisis del Impacto de la Frecuencia de CPU en el Tiempo de Ejecución sobre ESP32
Se encuentra el codigo utilizado en el directorio `ESP32-frequency-test/frequency_test_code` y los resultados en el archivo `ESP32-frequency-test/README.md`.