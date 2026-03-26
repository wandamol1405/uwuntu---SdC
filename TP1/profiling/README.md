## Time Profiling - Instrucciones

### Objetivo

El objetivo de este tutorial es analizar el rendimiento de un programa en C utilizando herramientas de profiling, identificando qué funciones consumen mayor tiempo de ejecución y detectando posibles cuellos de botella.

El profiling permite validar experimentalmente la eficiencia del código, midiendo el tiempo de ejecución de cada función.

#### Requerimientos e instalación

##### 🔹 Herramientas de compilación

```bash
sudo apt update
sudo apt install build-essential 
```

Incluye:

gcc: compilador de C
make: automatización de compilación

##### 🔹 Instalación de perf

```bash
sudo apt install linux-tools-common
sudo apt install linux-tools-$(uname -r)
```

`perf` es una herramienta de profiling basada en muestreo que permite analizar el comportamiento del programa durante su ejecución.

##### 🔹 Herramientas de visualización

```bash
sudo apt install pipx
pipx ensurepath
pipx install gprof2dot
sudo apt install graphviz
```

`python3-pip`: gestor de paquetes de Phyton, necesario para gprof2dot
`gprof2dot`: convierte la salida de gprof en un grafo
`graphviz`: genera imágenes a partir del grafo

##### 📁 Estructura del proyecto

```bash
profiling/
├── src/
├── bin/
├── results/
├── images/
```

##### 🛠️ Compilación con profiling

Ubicarse en la carpeta src:

```bash
cd profiling/src
```

Compilar:

```bash
gcc -Wall -pg test_gprof.c test_gprof_new.c -o ../bin/test_gprof
```

##### ▶️ Ejecución

```bash
cd ../bin
./test_gprof
```

##### 📊 Generación del análisis

```bash
gprof test_gprof gmon.out > ../results/analysisApellido.txt
```

##### 🎨 Generación del gráfico

```bash
cd ../bin
gprof test_gprof gmon.out | gprof2dot -o output.dot
dot -Tpng output.dot -o profile.png
```
