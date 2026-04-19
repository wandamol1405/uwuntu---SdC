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


> **Observación:** El uso de `%xmm0` confirma que el argumento es un valor de punto flotante, cumpliendo con la convención de llamadas para arquitectura x86_64.

---

## 3. Estado del Sistema ANTES de la Llamada
Antes de ejecutar la instrucción `call`, se inspeccionó el estado de los registros y el tope de la pila para verificar la integridad de los datos.

### Registros y Stack
* **Registro `%xmm0`**: Contiene el valor `0x422acccd` (representación float de aproximadamente **42.7**).
* **Registro `%rsp`**: Apunta a la dirección `0x7ffffffdde50`.

![Estado de registros inicial](Captura%20de%20pantalla%202026-04-19%20203057.png)
![Estado inicial del stack](Captura%20de%20pantalla%202026-04-19%20203226.png)

---

## 4. Ejecución de `process_value_asm`
Una vez dentro de la función en Assembler, se ejecutan las instrucciones paso a paso con `stepi`. La función realiza una conversión de float a entero y un incremento posterior.

### Conversión y Aritmética
1. **Conversión**: `%rax` toma el valor hexadecimal `0x2a` (**42** decimal).
2. **Incremento**: El registro `%rax` finaliza en `0x2b` (**43** decimal).

![Resultado intermedio rax](Captura%20de%20pantalla%202026-04-19%20203924.png)
![Resultado final rax](Captura%20de%20pantalla%202026-04-19%20204124.png)

---

## 5. Análisis Dinámico del Stack
Durante la ejecución de la instrucción `call`, el procesador apila automáticamente la dirección de retorno, lo que modifica el puntero de pila.

### Inspección del Stack en Llamada
Al inspeccionar el stack con `x/8xg $rsp`, se observa que el puntero ha descendido a `0x7ffffffdde48`. El valor almacenado en ese tope es `0x000055555555526c`.

![Dirección de retorno en stack](Captura%20de%20pantalla%202026-04-19%20204039.png)

**Validación**: Al contrastar esta dirección con el desensamblado de `main`, se confirma que apunta a la instrucción inmediatamente posterior al `call` (+147), garantizando que el programa retome su ejecución correctamente tras el `ret`.

---

## 6. Conclusión
La sesión de debugging demuestra exitosamente:
* **Paso de parámetros**: El `float` se transfiere correctamente vía `%xmm0`.
* **Valor de retorno**: El resultado entero se entrega en `%rax`.
* **Integridad del Stack**: Se verificó el almacenamiento de la dirección de retorno y el comportamiento LIFO de la pila.

El código cumple con los requisitos del TP2 y las especificaciones de la convención de llamadas.
