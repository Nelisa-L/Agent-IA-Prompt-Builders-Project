# Requirements — auditor-core

## Introducción
Feature central de Auditor-Agent: analizar código Python y producir un
reporte de hallazgos de seguridad y linting.

## User Stories (formato EARS)

### US-1: Analizar un archivo o carpeta
**Como** desarrollador,
**quiero** ejecutar el auditor sobre un archivo o carpeta,
**para** detectar problemas de seguridad y estilo antes de un commit/PR.

- CUANDO el usuario ejecuta `auditor-agent <ruta>`,
  EL SISTEMA DEBERÁ recorrer todos los archivos `.py` bajo `<ruta>`
  (o el archivo único si `<ruta>` es un archivo).
- SI `<ruta>` no existe,
  ENTONCES EL SISTEMA DEBERÁ mostrar un error claro y salir con código != 0.

### US-2: Detectar patrones inseguros
**Como** desarrollador,
**quiero** que el auditor detecte patrones de código inseguro conocidos,
**para** reducir riesgos antes de llegar a producción.

- CUANDO se encuentre `eval(`, `exec(`, `shell=True` en subprocess,
  `pickle.load(` o un posible secreto hardcodeado (`api_key=`, `password=`,
  `secret=` con valor literal),
  EL SISTEMA DEBERÁ registrar un `Finding` con severidad `critical` o
  `warning` según la regla.

### US-3: Detectar problemas de estilo básicos
**Como** desarrollador,
**quiero** avisos de estilo simples (líneas largas, espacios finales,
`print` en vez de logging),
**para** mantener consistencia de código.

- CUANDO una línea exceda 100 caracteres, tenga espacios al final, o use
  `print(`,
  EL SISTEMA DEBERÁ registrar un `Finding` de severidad `info`.

### US-4: Generar reporte
**Como** desarrollador,
**quiero** un reporte legible de los hallazgos,
**para** compartirlo con mi equipo o revisarlo yo mismo.

- CUANDO termine el análisis,
  EL SISTEMA DEBERÁ generar un archivo de reporte en formato Markdown o JSON
  (según `--format`), en la ruta indicada por `--output`.
- SI no hay hallazgos,
  ENTONCES EL REPORTE DEBERÁ indicar explícitamente que el código está limpio.

### US-5: Integración continua
**Como** mantenedor del repo,
**quiero** que la auditoría corra automáticamente en cada push/PR,
**para** detectar regresiones de seguridad temprano.

- CUANDO se haga push o se abra un PR contra `main`,
  EL SISTEMA (CI) DEBERÁ instalar dependencias y correr la suite de tests
  (`pytest`).

## Criterios de aceptación generales
- Los tests de `tests/test_analyzer.py` deben pasar en CI.
- El CLI debe correr sin dependencias externas más allá de la stdlib.
