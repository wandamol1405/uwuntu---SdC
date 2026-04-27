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

**Evidencia Requerida:**
Captura de la terminal de GDB mostrando la dirección 0x0000fff0.

---

### B. Salto a Modo Protegido (CR0)

Mediante el comando `info registers cr0`, se verificó que el bit PE (Protection Enable) cambia de 0 a 1 tras ejecutar la instrucción que activa el modo protegido.

**Evidencia Requerida:**
Captura de GDB mostrando cr0 con el valor 0x11 (o similar, con el bit 0 en 1).

---

### C. Fallo de Protección

Al ejecutar paso a paso (`si`) hasta la instrucción de escritura, el procesador detecta que el segmento de datos no permite escritura.

**Comportamiento observado:**

- El procesador genera una General Protection Fault (#GP).
- Al no existir una IDT configurada, el sistema entra en un Triple Fault y se reinicia automáticamente.

**Evidencia Requerida:**
Captura de GDB indicando el reinicio del sistema o el salto abrupto del registro EIP.

---

## 5. Interpretación Teórica

### ¿Qué sucedió exactamente?

Al intentar realizar la escritura, la Unidad de Gestión de Memoria (MMU) del x86 consulta el descriptor de segmento almacenado en la caché del registro de segmento correspondiente. Al verificar que el bit W (Writable) del Access Byte en la GDT está en 0, el hardware bloquea la ejecución de la instrucción y lanza la excepción #GP (0x0D).

---

### Relación con la Protección de Memoria

Este experimento demuestra que el Modo Protegido utiliza la GDT como un contrato de seguridad. El hardware valida cada acceso a memoria contra los permisos definidos, permitiendo que el sistema operativo proteja regiones críticas de datos frente a escrituras no autorizadas o errores de programación.

---

## 📂 Archivos del Desafío

- Código fuente: src/protected-mode/main.s
- Imagen de disco: src/protected-mode/main.img
- Evidencias: docs/evidencias/modo-protegido/
