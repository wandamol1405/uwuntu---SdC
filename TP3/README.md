# TP3 — Modo Protegido (x86)

## Descripción

En este trabajo práctico se implementa, en bajo nivel, el pasaje de un sistema x86 desde **modo real a modo protegido**, configurando manualmente la **Global Descriptor Table (GDT)** y validando el comportamiento del procesador mediante herramientas de debugging.

El objetivo es comprender:

* el proceso de arranque en arquitecturas x86
* las diferencias entre modo real y modo protegido
* el uso de segmentación y protección de memoria
* el comportamiento del CPU ante accesos inválidos

---

## Objetivos del trabajo

* Generar una imagen booteable desde cero
* Comprender el rol del linker en bajo nivel
* Implementar el cambio a modo protegido
* Configurar correctamente la GDT
* Validar el uso de segmentos (código y datos)
* Provocar y analizar una violación de protección
* Utilizar GDB para inspección del sistema

---

## Estructura del proyecto

```bash
tp3-modo-protegido/
│
├── docs/
│   ├── desafio-uefi-coreboot.md
│   ├── desafio-linker.md
│   ├── desafio-modo-protegido.md
│   └── evidencias/
│       ├── linker/
│       ├── modo-protegido/
│       └── uefi/
│
├── src/
│   ├── boot/
│   │   ├── main.S
│   │   ├── linker.ld
│   │   └── Makefile
│   │
│   ├── protected-mode/
│   │   ├── boot.S
│   │   ├── gdt.S
│   │   └── Makefile
│
├── scripts/
│   ├── run-qemu.sh
│   └── debug.sh
│
└── README.md
```

---

## Requisitos

* Linux (recomendado)
* QEMU
* GDB
* Toolchain:

  * `gcc`
  * `ld`
  * `as`

Instalación rápida:

```bash
sudo apt update
sudo apt install build-essential qemu-system-x86 gdb
```

---

## Cómo ejecutar

### 🔹 Ejecución en QEMU

```bash
qemu-system-x86_64 --drive file=main.img,format=raw,index=0,media=disk
```

---

### 🔹 Ejecución en modo debug

```bash
qemu-system-i386 -fda main.img -boot a -s -S -monitor stdio
```

Luego, en otra terminal:

```bash
gdb
target remote localhost:1234
```

---

## Desafíos implementados

### UEFI, CSME y coreboot

Investigación teórica sobre firmware moderno:

* UEFI vs BIOS
* vulnerabilidades
* Intel Management Engine
* coreboot

📄 Ver: `docs/desafio-uefi-coreboot.md`

---

### Linker y generación de imagen

* Creación de imagen booteable
* Uso de linker script
* Análisis de memoria (`objdump` vs `hd`)
* Ejecución en QEMU y hardware real

📄 Ver: `docs/desafio-linker.md`

---

### Modo protegido

* Definición de GDT
* Activación del modo protegido
* Configuración de segmentos
* Protección de memoria
* Debugging con GDB

📄 Ver: `docs/desafio-modo-protegido.md`

---

## Evidencia

Toda la evidencia requerida se encuentra en:

```bash
docs/evidencias/
```

Incluye:

* ejecución en QEMU
* debugging con GDB
* análisis de binarios
* ejecución en hardware real (USB)

---

## Conceptos clave

* Bootloader (MBR — 512 bytes)
* Dirección de carga: `0x7C00`
* Global Descriptor Table (GDT)
* Segmentación en x86
* Registro `CR0` (bit PE)
* Selectores de segmento
* Excepción de protección general (#GP)

---

## Referencias

* OSDev Wiki
* Intel Manual (x86)
* Material de cátedra
* Repositorios de ejemplos bare metal
* Presentacion de Javier Jorge: https://docs.google.com/presentation/d/16mx1jQte3ud1xRnyM0YB-3l9mvVQ1fVskg3Fi7M40Ig/edit?slide=id.g73994de295_0_5#slide=id.g73994de295_0_5 

---

