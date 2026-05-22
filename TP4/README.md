# TP4 — Módulos de Kernel Linux y Seguridad

Trabajo práctico grupal orientado al desarrollo y análisis de módulos de kernel Linux, exploración de drivers, firma de módulos y conceptos asociados a Secure Boot.

# Objetivos del trabajo

El objetivo principal del trabajo práctico es comprender el funcionamiento de los módulos de kernel Linux y su relación con los mecanismos modernos de seguridad del sistema operativo.

Durante el desarrollo del trabajo se realizarán actividades relacionadas con:

- compilación y carga de módulos de kernel,
- análisis de drivers y módulos del sistema,
- exploración de información del kernel y hardware,
- comparación de configuraciones entre distintos equipos,
- investigación sobre firma de módulos,
- análisis de Secure Boot y cadena de confianza,
- documentación técnica de evidencias y resultados.


# Organización del repositorio

El repositorio se encuentra organizado para separar:

- código fuente,
- evidencias,
- salidas generadas por cada integrante,
- documentación individual,
- informe final consolidado.

```text
kernel-modules-tp/
│
├── src/
├── evidencias/
├── outputs/
├── docs/
└── README.md
```

## Directorios principales

### `src/`

Contiene el código fuente relacionado con el módulo de kernel y los archivos utilizados durante el desarrollo del trabajo práctico.

### `evidencias/`

Almacena capturas y registros obtenidos durante las pruebas realizadas por cada integrante.

Incluye, por ejemplo:

* carga y descarga de módulos,
* mensajes del kernel,
* intentos de firma,
* evidencia de ejecución,
* resultados observados durante las pruebas.


### `outputs/`

Contiene las salidas generadas en cada computadora de los integrantes del grupo.

Estas salidas serán utilizadas posteriormente para realizar comparaciones y análisis técnicos entre distintos entornos.

Cada integrante posee su propio subdirectorio.

### `docs/`

Incluye la documentación individual desarrollada por cada integrante y el informe final consolidado del trabajo práctico.

La idea es que cada integrante trabaje inicialmente sobre su propio archivo markdown y posteriormente se integren todos los contenidos en un único informe final.

# Dependencias entre tareas

La organización del trabajo contempla algunas dependencias mínimas entre actividades.

| Actividad                       | Dependencia                |
| ------------------------------- | -------------------------- |
| Desarrollo inicial del módulo   | Ninguna                    |
| Generación de outputs           | Requiere módulo funcional  |
| Análisis comparativo            | Requiere outputs generados |
| Investigación sobre Secure Boot | Independiente              |

Esto permite que parte del trabajo pueda realizarse en paralelo mientras se desarrollan las actividades técnicas principales.

# Uso del repositorio base provisto por la cátedra

La consigna original propone forkear un repositorio alojado en GitLab.

En este trabajo se decidió utilizar un repositorio propio en GitHub para centralizar la organización grupal y simplificar la colaboración entre integrantes.

En lugar de utilizar submódulos de Git, se optó por integrar directamente los archivos necesarios del repositorio original dentro de este repositorio.

Esta decisión permite:

* simplificar el flujo de trabajo,
* evitar problemas de sincronización asociados a submódulos,
* facilitar el clonado y revisión del trabajo,
* mantener toda la documentación y evidencias en un único repositorio.

El repositorio original utilizado como referencia es:

* [https://gitlab.com/sistemas-de-computacion-unc/kenel-modules.git](https://gitlab.com/sistemas-de-computacion-unc/kenel-modules.git)


# Estrategia de documentación

Cada integrante desarrollará inicialmente su documentación de manera individual utilizando archivos markdown separados.

Posteriormente, toda la información será integrada en un informe final consolidado que incluirá:

* introducción,
* desarrollo técnico,
* análisis comparativos,
* investigación teórica,
* evidencias,
* conclusiones.

Esto permite mantener trazabilidad de las contribuciones individuales y reducir conflictos durante el trabajo colaborativo.


# Bibliografía y referencias

* Linux Kernel Module Programming Guide
* Documentación de Red Hat sobre firma de módulos
* Documentación y artículos sobre Secure Boot
* Material provisto por la cátedra
* Artículo técnico sobre GRUB y Secure Boot propuesto en la consigna

