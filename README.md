# Sistemas de Computación
Este repositorio contiene los trabajos prácticos de la materia Sistemas de Computación, realizados como parte de la cursada de la carrera de Ingeniería en Computación e Ingeniería Electrónica.
## Contenido
Cada carpeta corresponde a un trabajo practico (TP) de la materia:

- TP1: Rendimiento
- TP2: Stack frame
- TP3: Modo protegido

## Objetivo
El objetivo de este repositorio es documentar y centralizar los ejercicios prácticos y experimentos realizados durante la cursada, con el fin de:

- Reforzar los conceptos teóricos de la materia.

- Generar una base de ejemplos y soluciones.

- Facilitar el estudio y la preparación para evaluaciones.

## Metodología de trabajo (Git y colaboración)

Para organizar el desarrollo de los trabajos prácticos, se define la siguiente metodología de uso de ramas, commits y pull requests.

---

### Estrategia de ramas

El repositorio contiene múltiples trabajos prácticos (TP). Para cada TP se utilizará la siguiente estructura:

- `main` → versión final entregada de cada TP
- `dev-tpX` → rama de desarrollo del TP correspondiente (ej: `dev-tp1`)
- `feature/...` → ramas individuales por issue

#### Ejemplo:

```
main
└── dev-tp2
    ├── feature/api-consumo
    ├── feature/c-reader
    └── feature/gini-calculo

```

---

### Flujo de trabajo

1. Crear una rama de feature desde la rama de desarrollo del TP:
```

git checkout dev-tp1
git checkout -b feature/nombre-descriptivo

```

2. Trabajar de forma independiente en esa rama.

3. Subir cambios al repositorio:
```

git push origin feature/nombre-descriptivo

```

4. Crear un Pull Request (PR) hacia `dev-tpX`.

5. Una vez revisado, hacer merge a `dev-tpX`.

6. Cuando el TP esté finalizado, se mergea `dev-tpX` → `main`.

---

### Política de Pull Requests

- No se permite hacer push directo a `dev` ni a `main`.
- Todo cambio debe ingresar mediante Pull Request.
- Cada PR debe:
   - Estar asociada a una issue
   - Tener una descripción clara
   - Ser revisada por al menos un integrante

---

### Trabajo por issues

Cada funcionalidad se divide en issues.

Para cada issue:

- Se crea una rama `feature/...`
- Se asigna un responsable (driver)

---

### Convención de commits

Se recomienda usar mensajes claros y descriptivos:

```

feat: agrega consumo de API
fix: corrige lectura de archivo en C
refactor: mejora estructura del cálculo de GINI

```

Tipos sugeridos:
- `feat` → nueva funcionalidad
- `fix` → corrección de errores
- `refactor` → mejoras internas sin cambiar comportamiento
- `docs` → documentación

---

## Autores
- Baccino, Octavio

- Molina, Maria Wanda

- Verdú, Melisa Noel
 
### Año de cursada

2026

### Facultad / Universidad

Facultad de Ciencias Exactas, Físicas y Naturales - Universidad Nacional de Córdoba

