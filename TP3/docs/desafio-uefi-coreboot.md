# Desafío: UEFI y coreboot

## UEFI y uso

### ¿Qué es UEFI?

UEFI (Unified Extensible Firmware Interface) es el estándar moderno de firmware para computadoras que reemplaza a la BIOS tradicional. A diferencia de la BIOS, que opera en modo real del procesador con capacidades limitadas, UEFI provee un entorno de ejecución más avanzado, flexible y extensible desde las primeras etapas del arranque.

---

### ¿Cómo puedo usarlo?

Para utilizar UEFI, el programador interactúa con sus servicios mediante estructuras de datos y punteros a funciones, en lugar de interrupciones como en BIOS.

UEFI expone una estructura central llamada **System Table**, que contiene:

- **Boot Services** → servicios disponibles durante el arranque
- **Runtime Services** → servicios disponibles incluso después de cargar el sistema operativo

Esta arquitectura permite desarrollar aplicaciones UEFI (generalmente en C) que se ejecutan directamente sobre el firmware.

---

### Función de ejemplo

Una función típica que puede utilizarse en este entorno es:

- `GetMemoryMap()`

Esta función permite obtener un mapa detallado de la memoria del sistema, indicando qué regiones están disponibles o en uso. Es fundamental para que el cargador del sistema operativo pueda gestionar correctamente la memoria.

También es común el uso de funciones como:

- `Print()`

Ejemplo conceptual:

Esta función permite mostrar texto en pantalla durante etapas tempranas del arranque.

---

## Seguridad

### Casos de bugs de UEFI explotados

Las vulnerabilidades en UEFI son especialmente críticas porque se ejecutan antes del sistema operativo y con máximo nivel de privilegio.

Algunos ejemplos reales son:

- **BlackLotus (2023)**  
  Bootkit que logra evadir Secure Boot incluso en sistemas actualizados, permitiendo la ejecución de código malicioso antes del sistema operativo. Logra evadir la funcionalidad de seguridad de Arranque Seguro (Secure Boot) de Windows.

- **LogoFAIL (2023)**  
  Vulnerabilidad que explota errores en los parsers de imágenes utilizados por UEFI para mostrar logos durante el arranque.  
  Permite ejecutar código malicioso reemplazando imágenes aparentemente inofensivas.

Estas vulnerabilidades demuestran que el firmware es una superficie de ataque crítica, ya que comprometerlo implica control total del sistema.

---

## Componentes de bajo nivel

### Converged Security and Management Engine (CSME)

El CSME es un subsistema integrado en los procesadores Intel que actúa como un microcontrolador independiente dentro del sistema.

Características principales:

- Ejecuta su propio firmware (basado en MINIX)
- Tiene acceso completo a memoria y dispositivos
- Funciona incluso cuando la computadora está apagada (pero con energía)

Se encarga de funciones como:

- Seguridad del sistema
- Criptografía a nivel hardware
- Gestión remota

Debido a su alto nivel de privilegio y naturaleza cerrada, representa un punto crítico desde el punto de vista de seguridad.

---

### Intel Management Engine BIOS Extension (Intel MEBx)

Intel MEBx es una interfaz de configuración que permite administrar el Intel Management Engine (CSME).

Se accede durante el arranque del sistema (por ejemplo, mediante combinaciones de teclas como `Ctrl + P`).

Permite:

- Configurar Intel AMT (Active Management Technology)
- Habilitar administración remota
- Ajustar parámetros de seguridad

En términos simples:

- **CSME** → motor interno
- **MEBx** → interfaz de configuración

---

## Alternativas open-source

### ¿Qué es coreboot?

coreboot es un proyecto de firmware open-source que busca reemplazar la BIOS/UEFI propietaria.

Su objetivo es realizar únicamente la inicialización mínima del hardware y luego transferir el control a un **payload**, como:

- SeaBIOS
- TianoCore
- Un kernel de Linux

---

### ¿Qué productos lo incorporan?

Ejemplos reales de uso de coreboot:

- **Chromebooks** → ampliamente utilizados en dispositivos con ChromeOS
- **System76 y Purism** → laptops orientadas a software libre (ej. Librem)
- **Servidores OCP (Open Compute Project)** → utilizados en centros de datos

---

### Ventajas de su utilización

- **Velocidad**  
  Reduce significativamente el tiempo de arranque al eliminar funcionalidades innecesarias.

- **Seguridad y auditoría**  
  Al ser open-source, permite inspeccionar el código en busca de vulnerabilidades o puertas traseras.

- **Personalización**  
  Permite integrar directamente el kernel o configuraciones específicas en el firmware.

---

## Conclusión

El paso de BIOS a UEFI representa una evolución significativa en el proceso de arranque, incorporando mayor flexibilidad y capacidades avanzadas. Sin embargo, también introduce nuevas superficies de ataque críticas.

Componentes como el CSME amplían las capacidades de gestión y seguridad, pero a costa de complejidad y menor transparencia.

Alternativas como coreboot buscan recuperar el control del firmware mediante un enfoque abierto, aunque con ciertas limitaciones de compatibilidad.

---
