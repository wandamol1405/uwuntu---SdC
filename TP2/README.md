# Calculadora de Indice GINI

## Descripcion

Este trabajo práctico tiene como objetivo implementar una aplicación multicapa para el cálculo del índice de GINI utilizando una arquitectura escalonada:
- Capa superior (Python): consumo de API REST del Banco Mundial
- Capa intermedia (C): procesamiento de datos
- Capa inferior (Assembler): (includa en la Iteracion 2)

En esta Iteración 1, se implementa una versión simplificada donde toda la lógica se resuelve entre Python y C, dejando preparada la arquitectura para incorporar assembler en la siguiente fase.

El sistema deberá:

- Obtener datos desde una API REST
- Procesarlos en C
- Retornar resultados a Python para su visualización

## Estructura del proyecto

```bash
.
├── python/        # capa superior (API REST)
│   └── main.py
├── c/             # capa intermedia
│   └── main.c
├── data/          # datos de prueba
├── docs/          # diagramas / informes
├── tests/         # pruebas
├── scripts/       # scripts auxiliares
├── README.md
└── .gitignore 
```

## Requisitos
- Linux (se recomienda Ubuntu 22.04)
- Python 3.x
- GCC
- NASM, GDB (para la siguiente Iteracion)

Instalacion de dependencias base:

```bash
sudo apt update
sudo apt install build-essential python3 python3-venv
```

## Configuracion del entorno de Python

Crear entorno virtual:

```bash
python3 -m venv venv
source venv/bin/activate
```

Instalar dependencias:

```bash
pip install -r requirements.txt
```

Dentro de `requirements.txt` agregar:

```bash
requests
```

## Ejecucion

### Python

```bash
python3 python/main.py
```

### C
#### Compilar

```bash
gcc c/main.c -o c/main
```

#### Ejecutar

```bash
./c/main
```

## Consideraciones técnicas del TP
- Se utilizará arquitectura x86_64 sobre Linux
- En próximas iteraciones:
    - C invocará funciones en assembler
    - Se utilizará stack para paso de parámetros
    - Se aplicará convención System V AMD64 ABI
- Python consumirá la API del Banco Mundial mediante REST

## Trabajo colaborativo

Las políticas de ramas, commits y pull requests se encuentran definidas en el README principal del repositorio.