# Informe de Debugging: Análisis de Stack y Registros (C → ASM)

## 1. Introducción
Este informe detalla la sesión de depuración realizada sobre el binario del **TP2 (Issue 8)**. El objetivo es validar el cumplimiento de la convención **System V AMD64** durante la llamada desde el lenguaje C hacia una subrutina en Assembler, analizando específicamente el paso de parámetros, el comportamiento de la pila (*stack*) y el valor de retorno.

---

## 2. Análisis del Flujo de Control en `main`
Al desensamblar la función principal, se identifica el bloque donde se prepara la llamada a la función externa `process_value_asm`.

### Código Ensamblador de `main`
Como se observa en la imagen, el programa realiza las siguientes acciones antes de la llamada:
1. Mueve un valor desde la pila (`-0x18(%rbp)`) al registro `%eax`.
2. Transfiere dicho valor al registro vectorial `%xmm0` mediante la instrucción `movd`.

<img width="1570" height="1605" alt="Captura de pantalla 2026-04-19 202606" src="https://github.com/user-attachments/assets/9d476fb5-fa99-430e-b3d1-f85c705b97cf" />


---

## 3. Estado del Sistema ANTES de la Llamada
Antes de ejecutar la instrucción `call`, se inspeccionó el estado de los registros y el tope de la pila para verificar la integridad de los datos.

### Registros y Stack
* **Registro `%xmm0`**: Contiene el valor `0x422acccd` (representación float de aproximadamente **42.7**).
* **Registro `%rsp`**: Apunta a la dirección `0x7ffffffdde50`.

<img width="2857" height="226" alt="Captura de pantalla 2026-04-19 203057" src="https://github.com/user-attachments/assets/c4a0cb4d-66a5-4fba-8523-4a44685988e8" />

<img width="1126" height="197" alt="Captura de pantalla 2026-04-19 203226" src="https://github.com/user-attachments/assets/602856c2-57a5-4423-b3c9-39f9d61cf2b9" />

---

## 4. Ejecución de `process_value_asm`
Una vez dentro de la función en Assembler, se ejecutan las instrucciones paso a paso con `stepi`. La función realiza una conversión de float a entero y un incremento posterior.

### Conversión y Aritmética
1. **Conversión**: `%rax` toma el valor hexadecimal `0x2a` (**42** decimal).
2. **Incremento**: El registro `%rax` finaliza en `0x2b` (**43** decimal).

<img width="2829" height="233" alt="Captura de pantalla 2026-04-19 203924" src="https://github.com/user-attachments/assets/f9770a79-7bca-4011-a7e3-db5dc24aa305" />

<img width="739" height="122" alt="Captura de pantalla 2026-04-19 204124" src="https://github.com/user-attachments/assets/a7f641c6-9475-48dc-8001-080780324c10" />

---

## 5. Análisis Dinámico del Stack
Durante la ejecución de la instrucción `call`, el procesador apila automáticamente la dirección de retorno, lo que modifica el puntero de pila.

### Inspección del Stack en Llamada
Al inspeccionar el stack con `x/8xg $rsp`, se observa que el puntero ha descendido a `0x7ffffffdde48`. El valor almacenado en ese tope es `0x000055555555526c`.

<img width="1125" height="238" alt="Captura de pantalla 2026-04-19 204039" src="https://github.com/user-attachments/assets/940c3fc2-49c3-4dcd-b845-ff0d6c175e28" />

**Validación**: Al contrastar esta dirección con el desensamblado de `main`, se confirma que apunta a la instrucción inmediatamente posterior al `call` (+147), garantizando que el programa retome su ejecución correctamente tras el `ret`.

---

## 6. Conclusión
La sesión de debugging demuestra exitosamente:
* **Paso de parámetros**: El `float` se transfiere correctamente vía `%xmm0`.
* **Valor de retorno**: El resultado entero se entrega en `%rax`.
* **Integridad del Stack**: Se verificó el almacenamiento de la dirección de retorno y el comportamiento LIFO de la pila.

El código cumple con los requisitos del TP2 y las especificaciones de la convención de llamadas.
