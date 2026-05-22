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
↓ verifica
Bootloader (shim/GRUB)
↓ verifica
Kernel Linux
↓ verifica
Módulos del Kernel

Cada componente verifica criptográficamente al siguiente antes de permitir su ejecución. Si una firma es inválida o el certificado no pertenece a una entidad confiable, la ejecución es bloqueada.

De esta manera, Secure Boot protege al sistema frente a modificaciones maliciosas de bajo nivel y evita que software no autorizado se ejecute antes de que el sistema operativo tome control de la computadora.
