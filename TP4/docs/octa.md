# Análisis del artículo: Actualización de Microsoft y problemas con GRUB

**Artículo:** https://arstechnica.com/security/2024/08/a-patch-microsoft-spent-2-years-preparing-is-making-a-mess-for-some-linux-users/

## a. ¿Cuál fue la consecuencia principal del parche de Microsoft sobre GRUB en sistemas dual boot?

La principal consecuencia fue que numerosos sistemas configurados con **dual boot (Windows y Linux)** dejaron de poder iniciar Linux cuando **Secure Boot** estaba habilitado. Después de instalar una actualización de seguridad de Microsoft destinada a mitigar una vulnerabilidad en GRUB, muchos usuarios recibieron mensajes de error como:

> "Something has gone seriously wrong"  
> "SBAT self-check failed: Security Policy Violation"

Como resultado, el gestor de arranque GRUB era bloqueado por Secure Boot, impidiendo el inicio de diversas distribuciones Linux.

## b. ¿Qué implicancia tiene desactivar Secure Boot como solución?

Desactivar Secure Boot permite que Linux vuelva a arrancar normalmente, evitando el bloqueo producido por la actualización. Sin embargo, esta solución implica una **reducción del nivel de seguridad** del sistema.

Sin Secure Boot, el firmware deja de verificar la autenticidad y firma digital de los componentes que participan en el proceso de arranque, aumentando el riesgo de que software malicioso se ejecute antes de que el sistema operativo se cargue completamente.

## c. ¿Cuál es el propósito principal de Secure Boot?

El propósito principal de **Secure Boot** es garantizar que únicamente se ejecuten componentes de arranque confiables y firmados digitalmente durante el encendido del equipo.

Esta característica protege la cadena de arranque verificando la integridad y autenticidad del firmware, del gestor de arranque (como GRUB) y de otros componentes críticos. De esta manera, ayuda a prevenir ataques de malware de bajo nivel, como bootkits y rootkits, que intentan tomar control del sistema antes de que el sistema operativo se inicie.

# Investigación adicional: Secure Boot, módulos del kernel y cadena de confianza UEFI

## 1. ¿Qué ocurre cuando un módulo firmado por un integrante es cargado en otra PC?

Un módulo del kernel (`.ko`) puede estar firmado digitalmente mediante una clave privada generada por un desarrollador o integrante del equipo. La firma se adjunta al módulo y permite verificar su autenticidad e integridad.

Cuando dicho módulo es cargado en otra PC, pueden ocurrir dos situaciones:

### Caso 1: La clave pública es confiable para el sistema

Si el certificado correspondiente a la clave utilizada para firmar el módulo se encuentra registrado entre las claves confiables del kernel o de Secure Boot (por ejemplo, mediante MOK – Machine Owner Key), la firma será validada correctamente y el módulo podrá cargarse sin inconvenientes.

### Caso 2: La clave pública no es reconocida

Si la PC no posee registrada la clave pública asociada a la firma del módulo, el kernel no podrá verificar su autenticidad.

En sistemas donde la verificación de firmas es obligatoria (`CONFIG_MODULE_SIG_FORCE=y`) o donde Secure Boot impone restricciones de integridad, el resultado será:

- rechazo de la carga del módulo;
- mensajes de error en `dmesg`;
- imposibilidad de utilizar el driver o funcionalidad implementada por dicho módulo.

Por lo tanto, firmar un módulo no garantiza que pueda ejecutarse en cualquier equipo; además es necesario que la clave utilizada para la firma forme parte de la base de confianza del sistema destino.

---

## 2. Relación entre claves criptográficas, firmas digitales y Secure Boot

Secure Boot utiliza criptografía de clave pública para verificar que los componentes cargados durante el arranque provengan de una fuente confiable y no hayan sido modificados.

El mecanismo funciona de la siguiente manera:

1. El desarrollador genera un par de claves:
   - clave privada;
   - clave pública.

2. La clave privada se utiliza para firmar digitalmente:
   - cargadores de arranque;
   - kernels;
   - módulos del kernel.

3. La clave pública o certificado correspondiente se almacena en la base de claves confiables del sistema.

4. Durante el arranque o carga del módulo, el firmware UEFI o el kernel:
   - calcula el hash del archivo;
   - verifica la firma digital;
   - comprueba que el certificado pertenezca a una entidad autorizada.

Si la verificación es correcta, el componente es ejecutado. En caso contrario, es rechazado.

De esta manera:

- la firma digital garantiza integridad y autenticidad;
- las claves públicas determinan quién es considerado confiable;
- Secure Boot aplica estas verificaciones antes de permitir la ejecución del software.

---

## 3. Cadena de confianza UEFI (Chain of Trust)

La seguridad proporcionada por Secure Boot se basa en una cadena de confianza que comienza en el firmware UEFI y continúa hasta el sistema operativo.

El proceso simplificado es el siguiente:

1. **UEFI Firmware**
   - contiene claves raíz de confianza almacenadas en memoria protegida;
   - verifica la firma del gestor de arranque.

2. **Bootloader (por ejemplo, GRUB o shim)**
   - verifica la firma del kernel Linux;
   - sólo permite continuar si la validación es correcta.

3. **Kernel Linux**
   - verifica módulos del kernel y otros componentes firmados;
   - rechaza elementos no autorizados cuando la política de seguridad lo exige.

4. **Módulos del kernel**
   - deben estar firmados con certificados reconocidos por el kernel o por la infraestructura Secure Boot.

Representación simplificada:

1. **UEFI Firmware** verifica la firma digital del **bootloader** (por ejemplo, shim o GRUB).
2. El **bootloader** verifica la firma digital del **kernel Linux**.
3. El **kernel Linux** verifica la firma digital de los **módulos del kernel** que se cargan dinámicamente.
4. Si alguna verificación falla, el componente correspondiente es rechazado y el proceso de arranque o carga se detiene.

UEFI Firmware → Bootloader (shim/GRUB) → Kernel Linux → Módulos del Kernel

Cada elemento confía en el anterior. Si cualquiera de las verificaciones falla, la cadena se rompe y el componente no es ejecutado.

---

## 4. Relación con el problema del artículo

El artículo analizado describe una actualización distribuida por Microsoft para corregir una vulnerabilidad relacionada con GRUB.

La actualización modificó políticas de validación utilizadas por Secure Boot y por el mecanismo SBAT (Secure Boot Advanced Targeting). Como consecuencia, ciertos cargadores GRUB previamente aceptados dejaron de considerarse válidos.

Desde el punto de vista técnico, la cadena de confianza se interrumpió en la etapa de verificación del bootloader:

UEFI Firmware
✗ rechaza GRUB
→ Linux no puede iniciarse

Aunque el kernel y los módulos permanecían intactos, el proceso de arranque se detenía porque uno de los componentes de la cadena ya no cumplía las condiciones criptográficas requeridas.

Este mismo principio se aplica a los módulos del kernel: si la firma no puede validarse mediante una clave confiable, el kernel rechaza su carga para preservar la integridad del sistema.

---

# Referencias bibliográficas

1. Ars Technica. *A patch Microsoft spent 2 years preparing is making a mess for some Linux users*. 2024. Disponible en:
   https://arstechnica.com/security/2024/08/a-patch-microsoft-spent-2-years-preparing-is-making-a-mess-for-some-linux-users/

2. Linux Kernel Documentation. *Kernel module signing facility*. Disponible en:
   https://docs.kernel.org/admin-guide/module-signing.html

3. UEFI Documentation. *Secure Boot and Driver Signing*. Disponible en:
   https://uefi.org/specs/UEFI/2.10/32_Secure_Boot_and_Driver_Signing.html

4. *UEFI Secure Boot*. Disponible en:
   https://eci.intel.com/docs/3.0.1/development/secure_boot.html


