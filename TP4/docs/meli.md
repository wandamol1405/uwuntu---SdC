# Análisis comparativo de módulos y respuestas técnicas

## 1. Introducción
El presente informe documenta el análisis técnico realizado durante el Trabajo Práctico N° 4, centrado en el estudio de módulos del kernel Linux, drivers y mecanismos básicos de interacción entre el sistema operativo y el hardware. 

A lo largo de la práctica se trabajó con la compilación y carga dinámica de módulos, el análisis de información del kernel mediante herramientas como `modinfo`, `lsmod` y `dmesg`, y la observación de diferencias entre espacio de usuario y espacio kernel. Además, se estudiaron conceptos relacionados con drivers, llamadas al sistema (*syscalls*) y errores de memoria como los *segmentation faults*.

## Metodología y Procedimiento Experimental
Para generar la base de datos técnica utilizada en este análisis, se siguió un procedimiento estandarizado de desarrollo y recolección de evidencias en un entorno de ejecución real.

### 2.1. Preparación del entorno 
Se configuró el sistema instalando las cabeceras del núcleo y herramientas de compilación esenciales para generar objetos de kernel compatibles con la versión residente `(uname -r)`.

`sudo apt-get install build-essential kernel-package linux-source kmod`


Este paso garantizó la presencia de los *headers* del kernel, es decir, los archivos que contienen definiciones, estructuras y funciones internas utilizadas por Linux. Estos headers son necesarios para que el compilador pueda reconocer símbolos del kernel como `printk`, `module_init` o `MODULE_LICENSE` durante la construcción del módulo.

### 2.2. Ciclo de vida y monitoreo con `dmesg`

Se realizaron pruebas de carga y descarga del módulo utilizando comandos del kernel para validar su funcionamiento.

- **Carga (`insmod`):**  
  Se insertó el módulo mediante:

```bash
sudo insmod mimodulo.ko
```
   La ejecución de este comando carga el módulo en memoria y dispara automáticamente la función registrada mediante la macro `module_init()`.

* **Verificación con `dmesg`:**
Debido a que los módulos del kernel no imprimen información directamente en la terminal de usuario, se consultaron los registros del kernel utilizando:

```bash
dmesg | tail
```
Allí se observaron los mensajes generados con `printk()` dentro de `mimodulo.c`, incluyendo la confirmación de carga correcta del módulo.
```bash
=====================================
   TP4 - MODULO CARGADO
=====================================
 u     u  w     w  u     u  n   n  ttttt  u    u 
 u     u  w  w  w  u     u  nn  n    t    u    u 
 u     u  w w w w  u     u  n n n    t    u    u 
 u     u  ww   ww  u     u  n  nn    t    u    u 
  uuuu     w   w    uuuu    n   n    t     uuuu  

[TP4] Modulo cargado correctamente
```
![captura del mensaje generado por el comando `printk()` dentro de `mimodulo.c` ](../evidencias/carga_modulo.png)

Ese texto venía de los printk() definidos en:
```bash
modulo_lin_init(void)
```

- **Descarga (`rmmod`):**  
  Finalmente, el módulo fue removido mediante:

```bash
sudo rmmod mimodulo
```
La descarga ejecuta la función registrada con `module_exit()`, permitiendo finalizar correctamente el ciclo de vida del módulo dentro del kernel.

### 2.3. Desafío #1: Empaquetado y seguridad 


Como parte del desafío inicial, se exploró el uso de `checkinstall`, una herramienta que permite generar paquetes instalables (`.deb` o `.rpm`) a partir de software compilado. Esto facilita la administración del software mediante el gestor de paquetes del sistema, permitiendo instalarlo, registrarlo y desinstalarlo de forma más ordenada, en lugar de copiar archivos manualmente dentro del sistema operativo.
![Captura 1 del comando `checkinstall` ](../evidencias/checkinstall1.png)
![Captura 2 del comando `checkinstall` ](../evidencias/checkinstall2.png)
![Captura 3 del comando `checkinstall` ](../evidencias/checkinstall3.png)
![Captura 4 del comando `checkinstall` ](../evidencias/checkinstall4.png)


Además de la compilación y carga de módulos, esta parte del trabajo permitió analizar cómo Linux organiza y administra el software a nivel del sistema. El uso de paquetes instalables simplifica la distribución del software y mantiene un mejor control sobre versiones, dependencias y archivos instalados.

Por otro lado, también se investigaron mecanismos de seguridad asociados al kernel Linux y a la carga de módulos. Debido a que un módulo del kernel se ejecuta con privilegios elevados dentro del núcleo, permitir la carga de código arbitrario representa un riesgo importante para la integridad del sistema operativo.

En este contexto, se estudiaron conceptos relacionados con módulos firmados, validación de firmas digitales y Secure Boot. Estas medidas buscan restringir la ejecución de código no confiable dentro del kernel, verificando que los módulos cargados provengan de fuentes autorizadas y no hayan sido modificados.

La investigación permitió comprender que un módulo del kernel posee acceso directo a recursos internos del sistema y al hardware, por lo que un módulo malicioso o alterado podría comprometer completamente el funcionamiento del sistema operativo. Por este motivo, Linux incorpora mecanismos de validación y control orientados a preservar la integridad y confiabilidad del kernel.

### 2.4. Organización de outputs y evidencias

Para garantizar la trazabilidad del análisis, los resultados se organizaron en el repositorio bajo las rutas `outputs/integrante/` y `evidencias/integrante/`. Allí se almacenaron tanto las salidas generadas por comandos del sistema como las capturas obtenidas durante las pruebas realizadas sobre el módulo.

Entre los archivos generados se encuentran:

- `lsmod.txt`: listado de módulos cargados en memoria, incluyendo tamaño y dependencias.
- `proc_modules.txt`: contenido de `/proc/modules`, archivo virtual generado por el kernel desde donde herramientas como `lsmod` obtienen la información sobre módulos cargados.
- `modinfo_mimodulo.txt`: información del módulo desarrollado durante el TP, incluyendo licencia, descripción, versión del kernel y metadatos.
- `modinfo_sistema.txt`: información de un módulo oficial del sistema utilizada para realizar comparaciones posteriores.
- `hwinfo.txt`: reporte detallado del hardware detectado y drivers asociados, utilizado para documentar la configuración física del equipo y relacionarla con los módulos cargados.

## 3. Desarrollo Técnico y Análisis

### 3.1. Análisis de metadatos (`modinfo`)

Se comparó la información técnica obtenida en `outputs/meli/modinfo_mimodulo.txt` frente al módulo oficial del sistema `libdes.ko.zst` (`outputs/meli/modinfo_sistema.txt`). El objetivo fue analizar las diferencias entre un módulo desarrollado localmente y uno distribuido junto al kernel Linux.

| Característica    | Módulo Propio (`mimodulo.ko`)                                           | Módulo del Sistema (`libdes.ko.zst`)          |
| ----------------- | ----------------------------------------------------------------------- | --------------------------------------------- |
| Licencia          | GPL.                                                                    | GPL / módulo oficial del kernel.              |
| Firma Digital     | Ausente.                                                                | Firmas criptográficas de la distribución.     |
| Estado del Kernel | Puede marcar el kernel como *tainted* al tratarse de un módulo externo. | Módulo considerado confiable por el sistema.  |
| Version Magic     | Asociado a la compilación local.                                        | Sincronizado con el kernel oficial instalado. |

El análisis permitió observar que los módulos oficiales del sistema poseen mecanismos adicionales de validación y confianza, especialmente relacionados con firmas digitales y compatibilidad con la versión exacta del kernel en ejecución.

En contraste, el módulo desarrollado durante el TP fue compilado localmente y cargado manualmente mediante `insmod`, por lo que Linux lo considera un módulo externo (*out-of-tree module*).

#### Estado “Kernel Tainted”

Linux marca el kernel como *tainted* cuando se carga código que se aparta del entorno considerado completamente estándar o confiable para tareas de depuración. Esto puede ocurrir por distintos motivos, entre ellos:

- carga de módulos externos desarrollados fuera del árbol oficial del kernel,
- uso de módulos propietarios o con licencias incompatibles con GPL,
- carga forzada de módulos ignorando validaciones de compatibilidad.

Este mecanismo no implica necesariamente un error del sistema, sino que informa que el kernel se encuentra ejecutando componentes externos cuya estabilidad o procedencia no pueden garantizarse completamente.

### 3.2. Drivers y módulos disponibles

El kernel Linux posee una gran cantidad de módulos almacenados físicamente en el sistema bajo la ruta:

```bash
/lib/modules/$(uname -r)/kernel
```
Muchos de estos módulos no se encuentran cargados en memoria de forma permanente. En cambio, Linux los carga dinámicamente únicamente cuando detecta el hardware correspondiente o cuando alguna funcionalidad los requiere.

Este mecanismo permite reducir el consumo de memoria y mantener el sistema más eficiente, cargando únicamente los drivers necesarios para el hardware presente en cada equipo.

**¿Qué sucede cuando un driver no está disponible?**

Si el sistema detecta un dispositivo para el cual no posee un driver compatible, el hardware no podrá funcionar correctamente, ya que el sistema operativo no dispone del controlador necesario para comunicarse con él.

Dependiendo del dispositivo, esto puede provocar:

- ausencia total de funcionamiento
* funcionamiento limitado mediante drivers genéricos o pérdida de funcionalidades específicas del hardware.

### 3.3. Comparativa: módulos de kernel vs. programas de usuario

Aunque tanto los programas tradicionales como los módulos del kernel pueden desarrollarse en lenguaje C, ambos poseen diferencias fundamentales en su forma de ejecución y en el nivel de acceso que tienen dentro del sistema operativo.

- **Punto de inicio:**  
  Un programa convencional comienza su ejecución en la función `main()`, realiza sus tareas y luego finaliza. En cambio, un módulo del kernel no posee un `main()`, sino que registra funciones mediante las macros `module_init()` y `module_exit()`. Cuando el módulo es cargado con `insmod`, el kernel ejecuta automáticamente la función de inicialización y el módulo permanece residente en memoria hasta ser removido.

- **Espacio de ejecución y privilegios:**  
  Los programas normales se ejecutan en *User Space* (modo usuario), donde poseen acceso restringido a memoria y hardware para proteger la estabilidad del sistema. Por el contrario, los módulos operan en *Kernel Space*, es decir, dentro del propio núcleo del sistema operativo y con privilegios elevados sobre memoria, CPU y dispositivos físicos.

  Debido a esto, un error en un programa de usuario normalmente solo provoca la finalización de ese proceso, mientras que un fallo dentro de un módulo puede comprometer completamente la estabilidad del sistema operativo.

- **Funciones y bibliotecas disponibles:**  
  Los programas de usuario utilizan bibliotecas estándar como `libc`, incluyendo funciones como `printf()` o `malloc()`. En cambio, los módulos del kernel no pueden utilizar estas bibliotecas tradicionales, ya que se ejecutan dentro del núcleo. En su lugar, deben utilizar únicamente símbolos y funciones exportadas por el kernel, como `printk()` o `kmalloc()`, visibles en archivos como `/proc/kallsyms`.

### 3.4. Visualización de llamadas al sistema (*syscalls*)

Para observar cómo un programa de usuario interactúa con el kernel Linux, se utilizó la herramienta `strace` sobre un programa simple tipo “Hello World”.

El análisis permitió comprobar que funciones de alto nivel como `printf()` no acceden directamente al hardware o a la terminal, sino que internamente realizan llamadas al sistema (*syscalls*) para solicitar servicios al kernel.

Durante la ejecución se observaron syscalls como:
- `write()`
- `openat()`
- `mmap()`
- `exit_group()`

Por ejemplo, la impresión del mensaje en pantalla termina utilizando la syscall `write()`, demostrando cómo incluso programas simples dependen constantemente de la interacción con el kernel.

### 3.5. El *Segmentation Fault* y el manejo del kernel

Un *segmentation fault* ocurre cuando un proceso intenta acceder a una dirección de memoria inválida o para la cual no posee permisos.

- **En programas de usuario (*User Space*):**  
  El procesador detecta el acceso inválido y genera una excepción. Luego, el kernel interviene enviando la señal `SIGSEGV`, finalizando únicamente el proceso que produjo el error para proteger la estabilidad del resto del sistema operativo.

- **En módulos del kernel (*Kernel Space*):**  
  La situación es considerablemente más crítica. Debido a que el módulo se ejecuta dentro del propio kernel y comparte su espacio de memoria, un error puede corromper estructuras críticas del sistema. En estos casos, el kernel no puede aislar el fallo de la misma forma que lo hace con procesos de usuario, pudiendo provocar un *Kernel Panic* y la caída completa del sistema.

## Análisis de los archivos obtenidos

### Archivo `lsmod.txt`

El archivo `lsmod.txt` contiene la salida del comando `lsmod`, utilizado para listar los módulos del kernel que se encuentran cargados actualmente en el sistema Linux. Este comando muestra principalmente:
- nombre del módulo,
- tamaño en memoria,
- cantidad de usos o dependencias.

En outputs/meli, dentro del archivo se pueden observar módulos relacionados con:
- gráficos (`amdgpu`),
- audio (`snd_*`),
- red inalámbrica (`rtw89_*`, `cfg80211`, `mac80211`),
- bluetooth (`bluetooth`, `btusb`, `rfcomm`),
- almacenamiento (`nvme`),
- y el módulo personalizado `mimodulo`. :contentReference[oaicite:0]{index=0}

### Comparación con el equipo de mi compañera

Al comparar ambos equipos, se observó que muchos módulos coinciden debido a que ambos utilizan Linux y comparten varios subsistemas comunes del kernel. Sin embargo, también aparecen diferencias importantes relacionadas con el hardware específico de cada computadora.

En el equipo de mi compañera aparecen numerosos módulos asociados a hardware AMD moderno, especialmente:
- `amdgpu` para gráficos,
- `snd_sof_*` para audio,
- `rtw89_*` para Wi-Fi Realtek,
- y módulos de Bluetooth y webcam. :contentReference[oaicite:1]{index=1}

Estas diferencias se producen porque Linux carga dinámicamente únicamente los módulos necesarios según el hardware detectado en cada sistema.

Además, ambos equipos muestran correctamente cargado el módulo desarrollado durante la práctica (`mimodulo`), lo que confirma que la compilación e inserción del módulo funcionó correctamente. 



### Archivo `/proc/modules`

El archivo obtenido desde `/proc/modules` contiene información similar a `lsmod`, ya que ambos reflejan los módulos actualmente cargados en el kernel. Sin embargo, `/proc/modules` brinda información más detallada y de más bajo nivel.

En este archivo se observan:
- nombre del módulo,
- tamaño,
- dependencias,
- estado del módulo (`Live`),
- dirección de memoria,
- y relaciones entre módulos.

Por ejemplo:

```bash
amdgpu 20103168 40 - Live 0x0000000000000000
```

Esto permite visualizar información interna que lsmod simplifica para hacerla más legible.

### Comparación con el equipo de mi compañera

En ambos equipos, `/proc/modules` refleja los módulos activos correspondientes al hardware presente en cada sistema.

En el caso de mi compañera, nuevamente aparecen muchos módulos relacionados con:

- GPU AMD,
- audio avanzado SOF,
- Wi-Fi Realtek,
- Bluetooth,
- dispositivos multimedia.

La principal diferencia respecto a `lsmod` es que aquí pueden observarse claramente: las dependencias exactas entre módulos, el estado activo (Live), y la dirección de memoria asignada a cada módulo. En `/proc/modules` también aparece el estado `Live`, el cual indica que el módulo se encuentra actualmente cargado y activo en memoria dentro del kernel. Esto confirma que el módulo fue insertado correctamente y que el sistema operativo puede utilizarlo mientras el kernel se encuentre en ejecución.

Además, el módulo mimodulo también aparece correctamente cargado en este archivo, confirmando que el kernel lo reconoce como un módulo activo.

