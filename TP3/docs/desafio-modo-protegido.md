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
