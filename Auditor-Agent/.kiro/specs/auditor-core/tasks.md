# Tasks — auditor-core

## Fase 1: Núcleo (ya implementado en este scaffold)
- [x] Definir `Rule` y `Finding` como dataclasses.
- [x] Implementar `SECURITY_RULES` (eval, exec, secretos, shell=True, pickle).
- [x] Implementar `LINT_RULES` (líneas largas, espacios finales, print).
- [x] Implementar `CodeAuditor.run()` con recorrido recursivo de `.py`.
- [x] Implementar `ReportGenerator` (Markdown y JSON).
- [x] CLI (`main.py`) con `argparse`.
- [x] Tests básicos (`tests/test_analyzer.py`).
- [x] Workflow de CI (`.github/workflows/ci.yml`).

## Fase 2: Robustez (siguiente para el hackathon)
- [ ] Agregar más reglas de seguridad (SQL injection por f-strings, `assert`
      en producción, `yaml.load` sin `SafeLoader`).
- [ ] Manejar encoding de archivos de forma más robusta.
- [ ] Agregar `--severity-min` para filtrar hallazgos por severidad mínima.
- [ ] Agregar exit code != 0 si hay hallazgos `critical` (útil para CI/gates).

## Fase 3: Extensión
- [ ] Integrar linters reales opcionales (`ruff`, `bandit`) como capa
      adicional, dejando las reglas propias como fallback sin dependencias.
- [ ] Soporte para `.gitignore`/exclusión de carpetas (`venv/`, `node_modules/`).
- [ ] Reporte HTML simple para mostrar en la demo del hackathon.

## Fase 4: Demo / Presentación
- [ ] Preparar un repo de ejemplo con código "sucio" a propósito para
      mostrar hallazgos en vivo.
- [ ] Grabar reporte generado como parte del pitch.
- [ ] (Opcional) Deploy simple como GitHub Action reutilizable por otros
      repos del equipo.

> Notas: marca cada tarea como completada (`[x]`) a medida que avances;
> Kiro puede ejecutar/asistir cada tarea individualmente desde este archivo.
