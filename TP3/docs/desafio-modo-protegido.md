# Desafío modo protegido

## 1. Introducción

El objetivo de este trabajo es documentar la transición de un procesador x86 desde el Modo Real (estado inicial primitivo de 16 bits) hacia el Modo Protegido de 32 bits. Mientras que el modo real limita el direccionamiento a 1 MB y carece de seguridad, el modo protegido introduce protección de memoria, multitarea estable y soporte para memoria virtual, permitiendo direccionar hasta 4 GB.

## 2. Pasaje a modo protegido

El proceso de transición se realizó siguiendo los pasos críticos definidos por la arquitectura:

- Deshabilitar interrupciones: Para evitar que una interrupción de modo real sea tratada incorrectamente durante la transición.

- `lgdt` **(Load Global Descriptor Table):** Esta instrucción carga la dirección y el límite de la GDT en el registro GDTR, indicando al procesador dónde buscar los descriptores de segmento.

- `CR0` **(Control Register 0):** Se activa el bit de **Protection Enable (PE)**, que es el bit más bajo de este registro. Al ponerlo en 1, el hardware comienza a operar en modo protegido.

- `ljmp` **(Far Jump):** Es obligatorio realizar un salto largo inmediatamente después de activar el bit PE para actualizar el registro de segmento de código (CS) y limpiar el pipeline de instrucciones de 16 bits, comenzando la ejecución en el segmento de 32 bits (`.code32`).

## 3. GDT Implementada

La **Global Descriptor Table (GDT)** es la estructura central que define los segmentos de memoria.

- **Estructura:** Consiste en descriptores de 8 bytes (64 bits) que contienen la base (32 bits), el límite (20 bits) y los atributos de acceso.

- **Descriptores utilizados:** Se definieron al menos tres descriptores: un descriptor nulo (obligatorio), un descriptor para el segmento de código y otro para el segmento de datos.

- **Campos relevantes:** El campo **Type** define si el segmento es de lectura/escritura/ejecución, y el **Privilege Level (DPL)** establece el nivel de seguridad (anillos 0-3).

## 4. Segmentación

En el sistema implementado, se separó la memoria mediante el uso de **selectores**. A diferencia del modo real, donde el registro de segmento se multiplica por 16, en modo protegido el registro de segmento contiene un **índice** que apunta a una entrada en la GDT.

- Los registros de segmento (DS, ES, FS, GS) se cargan con el selector del segmento de datos para actualizar sus registros caché invisibles.

## 5. Protección de memoria

Se realizó un experimento configurando el segmento de datos como **Solo Lectura** (cambiando los bits de acceso en la GDT).

- **Resultado observado:** Al intentar escribir en este segmento, el hardware genera una excepción de protección (General Protection Fault).

- **Comportamiento teórico:** Según el manual de Intel, el procesador verifica los derechos de acceso antes de cada operación; si la operación (escritura) no está permitida por el descriptor, se aborta la ejecución y se invoca un manejador de excepciones.

## 6. Debugging con GDB

La validación se realizó mediante **QEMU** y **GDB**:

- **Metodología:** Se utilizó `qemu-system-i386 -s -S` para pausar la ejecución en el primer ciclo.

- **Breakpoints:** Se colocó un breakpoint en `0x7c00` (arranque) y otro tras el `ljmp` para verificar el cambio de modo.

- **Observación clave:** Se verificó que los registros de segmento cambiaron de valores base a **selectores** y que el procesador pasó a ejecutar instrucciones de 32 bits.

## 7. Respuestas a consignas

#### Segmentación

**¿Cómo sería un programa que tenga dos descriptores de memoria diferentes, uno para cada segmento (código y datos) en espacios de memoria diferenciados?**
Se deben crear dos entradas en la GDT con bases diferentes. Por ejemplo, el descriptor de código podría tener base `0x0` y el de datos base `0x10000`. De esta forma, una dirección lógica 0x0 en datos apuntaría físicamente a `0x10000`, logrando un aislamiento físico entre las instrucciones y las variables.

#### Protección de memoria

**Al cambiar los bits de acceso a solo lectura e intentar escribir:**

- **¿Qué sucede?**
 Se produce un fallo de protección que detiene el flujo normal del programa.

- **¿Qué debería suceder a continuación?**
El procesador debería invocar una excepción (como #GP) para que el Sistema Operativo tome el control, usualmente terminando el proceso malformado.

- **Verificación con GDB:**
Al ejecutar paso a paso (`si`), se observa que la instrucción de escritura no modifica la memoria y el flujo salta al vector de interrupción correspondiente.

#### Registros de segmento

**¿Con qué valor se cargan los registros de segmento en modo protegido y por qué?**
Se cargan con un **Selector**. El selector es un valor de 16 bits que contiene un índice (para ubicar el descriptor en la GDT) y el nivel de privilegio solicitado (RPL). Esto es necesario porque en modo protegido la dirección base y los permisos no están implícitos en el número del registro, sino que deben buscarse en la tabla de descriptores.

## 8. Conclusiones

Se logró implementar la base de un sistema operativo de 32 bits mediante la transición exitosa a modo protegido. Se comprendió que la seguridad del hardware (anillos de protección) depende de una correcta configuración de la GDT y que el uso de selectores es fundamental para la gestión moderna de la memoria.

---

## Evidencia Referenciada

#### 1. Fragmentos de Código Relevantes (Implementación Real)

- **Definición de la GDT y configuración de selectores**

 ```bash
# =======================================
# Protected mode entry point
# =======================================
.code32
protected_mode_entry:
  # Set up segment registers
   mov $0x10, %ax # Data segment selector
   mov %ax, %ds
   mov %ax, %ss
   mov %ax, %es
   mov %ax, %fs
   mov %ax, %gs


  # set up the stack
   mov $0x90000, %esp # Set the stack pointer to a safe location


  # =======================================
  # Access memory in protected mode to verify it's working
  # =======================================
   movl $0x12345678, 0x0


hang:
   hlt # Halt the CPU
   jmp hang 


# =======================================
# GDT (Global Descriptor Table) setup
# =======================================
gdt:
  # Null descriptor
   .quad 0x0000000000000000


  # Code segment descriptor (base=0, limit=4GB, executable, readable)
   .quad 0x00CF9A000000FFFF


  # Data segment descriptor (base=0, limit=4GB, writable)
   .quad 0x00CF92000000FFFF


gdt_end:


gdt_descriptor:
   .word gdt_end - gdt - 1 # Limit (size of GDT - 1)
   .long gdt               # Base address of the GDT
```

- **Transición de Modo:**

```bash
.code16
.global _start


_start:
   cli # Disable interrupts


   # Set up the GDT (Global Descriptor Table)
   xor %ax, %ax
   mov %ax, %ds


  # =======================================
  # Load the GDT
  # =======================================
   lgdt gdt_descriptor


  # =======================================
  # Enable protected mode
  # =======================================
   mov %cr0, %eax
   or $0x1, %eax # Set the PE (Protection Enable) bit
   mov %eax, %cr0


  # =======================================
  # Far jump to flush the instruction pipeline and switch to protected mode
   jmp $0x08, $protected_mode_entry
```

- **Experimento de Protección:**

```bash
  # =======================================
  # Access memory in protected mode to verify it's working
  # =======================================
   movl $0x12345678, 0x0
```

#### 2. Capturas de GDB y Validación de Registros

- **Registro CR0 (Bit PE):**
![alt text](image-4.png)

***Registros de Segmento:**
![alt text](image-5.png)
![alt text](image-6.png)

- **Breakpoints:**
![alt text](image-7.png)

#### 3. Evidencia del Fallo de Protección

Tras intentar realizar la escritura inválida mediante la instrucción movl $0x12345678, 0x0 en un segmento configurado como solo lectura, se documentó el siguiente comportamiento técnico:

**Análisis del EIP:** Mediante la inspección con GDB, se verificó que el registro EIP (Instruction Pointer) quedó apuntando a la dirección de memoria exacta de la instrucción movl conflictiva. Esto confirma que el procesador identificó la instrucción de escritura como la causante de la violación de acceso antes de completar su ejecución.

**Comportamiento observable:** El síntoma principal del fallo fue la desconexión inmediata entre QEMU y GDB. Este comportamiento es característico de un error crítico del sistema generado por una excepción de Protección General (#GP), la cual ocurre cuando el hardware detecta que una operación (en este caso, una escritura) viola las reglas de acceso definidas en el descriptor de segmento de la GDT.

#### 4. Capturas de Ejecución (QEMU y Hardware Real)

- **Ejecución en QEMU:**
![alt text](image-8.png)

- **Prueba en Hardware:**
![alt text](image-9.png)

#### 5. Respuestas a Consignas

**Segmentación:** En el sistema implementado, se definieron dos descriptores de memoria con el objetivo de separar las facultades de ejecución y almacenamiento. Ambos descriptores comparten la misma base (0) y el mismo límite (4GB), abarcando la totalidad del espacio direccionable. Sin embargo, se diferencian por sus atributos: el descriptor de código se configuró como ejecutable y leíble (0x00CF9A000000FFFF), mientras que el descriptor de datos se configuró como escribible (0x00CF92000000FFFF), permitiendo así que el procesador distinga entre instrucciones y variables.

**Valores de registros de segmento:** En modo protegido, los registros de segmento (DS, SS, ES, etc.) ya no almacenan direcciones físicas, sino que se cargan con selectores. En nuestra implementación, se utilizaron valores como 0x08 para el segmento de código y 0x10 para el segmento de datos. Estos valores son necesarios porque actúan como índices dentro de la GDT; el procesador utiliza estos índices para buscar el descriptor correspondiente y cargar de forma automática la base, el límite y las reglas de acceso en sus registros caché invisibles.
# 🛡️ Desafío: Protección de Memoria y GDT en Modo Protegido

## 1. Descripción del Experimento

Este desafío consiste en configurar el sistema para que un segmento de datos tenga permisos de **solo lectura** (Read-Only) y validar el mecanismo de protección del procesador intentando realizar una escritura sobre dicho segmento.

El objetivo es observar la generación de una excepción de protección general (**#GP**) ante accesos inválidos, relacionándolo con la configuración de la **GDT (Global Descriptor Table)** en arquitecturas x86.

---

## 2. Objetivos Alcanzados

- [x] Configuración del **Access Byte** de un descriptor de datos.
- [x] Implementación del pasaje a **Modo Protegido**.
- [x] Validación de registros de control (`CR0`).
- [x] Observación del comportamiento del CPU ante una violación de permisos.
- [x] Análisis mediante **GDB** y **QEMU**.

---

## 3. Implementación Técnica

### Modificación de la GDT (`src/protected-mode/main.s`)

Se editó el descriptor de segmento de datos en la tabla GDT. Se cambió el valor del descriptor de **Lectura/Escritura** a **Solo Lectura**.

**Código modificado:**

```asm
# Data segment descriptor (Base=0, Limit=4GB, Read-Only)
.quad 0x00CF90000000FFFF  

# El valor '90' (en lugar de '92') desactiva el bit Writable (W) del Access Byte.

```
## Código de Violación de Segmento

Se agregó una instrucción de escritura hacia una dirección de memoria (0x0) que pertenece al segmento de datos configurado anteriormente.

### Fragmento de código:

```asm
# Una vez cargados los selectores de segmento (DS, ES, SS)
movl $0x12345678, 0x0  ; <--- Intento de escritura prohibida
```

---

## 4. Evidencia de Debugging (GDB)

### A. Conexión y Estado Inicial

Al iniciar QEMU con los parámetros de depuración (-s -S) y conectar GDB, el procesador se encuentra pausado en el Reset Vector.

<img width="1379" height="187" alt="Captura de pantalla 2026-04-27 125500" src="https://github.com/user-attachments/assets/75311e2e-5534-4666-8da9-6a9c833244ee" />

---

### B. Salto a Modo Protegido (CR0)

Mediante el comando `info registers cr0`, se verificó que el bit PE (Protection Enable) cambia de 0 a 1 tras ejecutar la instrucción que activa el modo protegido.

<img width="2771" height="224" alt="Captura de pantalla 2026-04-27 130234" src="https://github.com/user-attachments/assets/3d01a5f8-60c0-4a0d-a935-07c90ea5a35d" />

<img width="1007" height="188" alt="Captura de pantalla 2026-04-27 140202" src="https://github.com/user-attachments/assets/693ab481-6429-4c53-aeae-2d96756fabd1" />

---

### C. Fallo de Protección

Al ejecutar paso a paso (`si`) hasta la instrucción de escritura, el procesador detecta que el segmento de datos no permite escritura.

**Comportamiento observado:**

- El procesador genera una General Protection Fault (#GP).
- Al no existir una IDT configurada, el sistema entra en un Triple Fault y se reinicia automáticamente.

<img width="2803" height="511" alt="Captura de pantalla 2026-04-27 140711" src="https://github.com/user-attachments/assets/859bfdab-03f9-4469-be55-74129e4df03a" />

<img width="2795" height="767" alt="Captura de pantalla 2026-04-27 140955" src="https://github.com/user-attachments/assets/56416294-2977-469c-a410-aa1d4396d989" />

---

## 5. Interpretación Teórica

### ¿Qué sucedió exactamente?

Al intentar realizar la escritura, la Unidad de Gestión de Memoria (MMU) del x86 consulta el descriptor de segmento almacenado en la caché del registro de segmento correspondiente. Al verificar que el bit W (Writable) del Access Byte en la GDT está en 0, el hardware bloquea la ejecución de la instrucción y lanza la excepción #GP (0x0D).

---

### Relación con la Protección de Memoria

Este experimento demuestra que el Modo Protegido utiliza la GDT como un contrato de seguridad. El hardware valida cada acceso a memoria contra los permisos definidos, permitiendo que el sistema operativo proteja regiones críticas de datos frente a escrituras no autorizadas o errores de programación.

