# Análisis del artículo: Actualización de Microsoft y problemas con GRUB

**Artículo:** https://arstechnica.com/security/2024/08/a-patch-microsoft-spent-2-years-preparing-is-making-a-mess-for-some-linux-users/

## a. ¿Cuál fue la consecuencia principal del parche de Microsoft sobre GRUB en sistemas dual boot?

La actualización distribuida por Microsoft tenía como objetivo mitigar vulnerabilidades conocidas en GRUB mediante el mecanismo SBAT (Secure Boot Advanced Targeting). SBAT permite revocar versiones específicas de cargadores de arranque consideradas vulnerables sin invalidar todos los certificados utilizados para firmarlos.

La consecuencia principal fue que numerosos sistemas configurados con dual boot (Windows y Linux) dejaron de poder iniciar Linux cuando Secure Boot estaba habilitado. Durante el arranque, el firmware UEFI verificaba la firma y los metadatos SBAT del cargador GRUB. Debido a los nuevos criterios de validación introducidos por la actualización, algunas versiones de GRUB fueron consideradas no válidas y rechazadas antes de transferir el control al kernel Linux.

Desde el punto de vista técnico, se produjo una ruptura de la cadena de confianza de Secure Boot en la etapa correspondiente al gestor de arranque:

UEFI → GRUB ✗ → Kernel Linux

Al no poder verificarse correctamente GRUB, el proceso de arranque se detenía antes de que el kernel pudiera ejecutarse.

Además, este mismo mecanismo de validación es utilizado posteriormente para verificar componentes firmados del sistema, incluidos los módulos del kernel cuando la política de seguridad así lo requiere.

---

## b. ¿Qué implicancia tiene desactivar Secure Boot como solución?

Desactivar Secure Boot elimina las verificaciones criptográficas realizadas durante el arranque y permite ejecutar componentes independientemente de su firma digital. Como consecuencia, Linux vuelve a iniciar incluso cuando el cargador GRUB es rechazado bajo las políticas de Secure Boot.

Sin embargo, esta solución implica la pérdida de las garantías de integridad y autenticidad proporcionadas por la cadena de confianza UEFI. El firmware deja de comprobar que los componentes cargados hayan sido firmados por entidades autorizadas y que no hayan sido modificados.

En sistemas Linux esto también afecta el control sobre módulos del kernel firmados. Cuando Secure Boot está habilitado, el kernel puede restringir la carga de módulos no firmados o firmados con claves no confiables. Al desactivarlo, dichas restricciones pueden relajarse dependiendo de la configuración del sistema, permitiendo potencialmente la ejecución de código no verificado dentro del espacio privilegiado del kernel.

Por lo tanto, aunque desactivar Secure Boot resuelve el problema de arranque, reduce significativamente las medidas de protección frente a bootkits, rootkits y otros ataques dirigidos a comprometer el sistema antes o durante la carga del kernel.

---

## c. ¿Cuál es el propósito principal de Secure Boot?

Secure Boot es una funcionalidad definida por la especificación UEFI cuyo objetivo principal es garantizar que únicamente se ejecuten componentes autorizados y criptográficamente verificables durante el proceso de arranque.

Para ello utiliza criptografía de clave pública. Los componentes del sistema (bootloaders, kernels y, en ciertos casos, módulos del kernel) son firmados digitalmente mediante una clave privada. Durante la ejecución, el firmware UEFI o el kernel verifican dichas firmas utilizando las claves públicas almacenadas en la base de confianza del sistema.

El mecanismo establece una cadena de confianza:

UEFI Firmware
    │
    ▼ verifica firma
Bootloader (shim/GRUB)
    │
    ▼ verifica firma
Kernel Linux
    │
    ▼ verifica firma
Módulos del Kernel

Cada componente verifica criptográficamente al siguiente antes de permitir su ejecución. Si una firma es inválida o el certificado no pertenece a una entidad confiable, la ejecución es bloqueada.

De esta manera, Secure Boot protege al sistema frente a modificaciones maliciosas de bajo nivel y evita que software no autorizado se ejecute antes de que el sistema operativo tome control de la computadora.

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

UEFI Firmware
↓ verifica
Bootloader (shim/GRUB)
↓ verifica
Kernel Linux
↓ verifica
Módulos del Kernel

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

# Conclusiones

La firma digital de módulos y componentes del sistema constituye un mecanismo fundamental para garantizar integridad y autenticidad. Secure Boot utiliza una infraestructura basada en claves criptográficas y certificados para construir una cadena de confianza desde el firmware UEFI hasta los módulos del kernel.

Un módulo firmado por un desarrollador sólo podrá cargarse en otra computadora si la clave pública correspondiente forma parte de la base de confianza del sistema. De lo contrario, el kernel podrá rechazarlo, especialmente cuando Secure Boot se encuentra habilitado.

El incidente analizado en el artículo demuestra cómo una modificación en las políticas de validación puede romper la cadena de confianza e impedir la ejecución de componentes considerados previamente válidos, afectando directamente el proceso de arranque de Linux.

# Referencias bibliográficas

1. Ars Technica. *A patch Microsoft spent 2 years preparing is making a mess for some Linux users*. 2024. Disponible en:
   https://arstechnica.com/security/2024/08/a-patch-microsoft-spent-2-years-preparing-is-making-a-mess-for-some-linux-users/

2. Linux Kernel Documentation. *Kernel module signing facility*. Disponible en:
   https://docs.kernel.org/admin-guide/module-signing.html

3. Linux Kernel Documentation. *UEFI Secure Boot*. Disponible en:
   https://docs.kernel.org/admin-guide/efi-stub.html

4. UEFI Forum. *UEFI Specification*. Disponible en:
   https://uefi.org/specifications

5. Red Hat Documentation. *Managing Secure Boot*. Disponible en:
   https://access.redhat.com/documentation

6. Canonical Documentation. *Secure Boot and Machine Owner Keys (MOK)*. Disponible en:
   https://ubuntu.com/security/secure-boot

7. Microsoft Documentation. *Secure Boot Overview*. Disponible en:
   https://learn.microsoft.com/windows/security/hardware-security/secure-boot
