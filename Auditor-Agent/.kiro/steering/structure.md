# Structure Context — Auditor-Agent

```
Auditor-Agent/
├── .kiro/
│   ├── steering/            # Contexto persistente (este set de archivos)
│   └── specs/               # Specs por feature (requirements/design/tasks)
├── src/
│   └── auditor_agent/
│       ├── __init__.py
│       ├── main.py          # CLI: parsea args, orquesta análisis + reporte
│       ├── analyzer.py      # CodeAuditor: recorre archivos y aplica reglas
│       ├── report.py        # ReportGenerator: exporta a Markdown/JSON
│       └── rules/
│           ├── security_rules.py  # Reglas de seguridad (Rule + SECURITY_RULES)
│           └── lint_rules.py      # Reglas de estilo (LINT_RULES)
├── tests/
│   └── test_analyzer.py
├── .github/workflows/ci.yml
├── pyproject.toml
├── requirements.txt
└── README.md
```

## Flujo de datos
1. `main.py` recibe la ruta a auditar por CLI.
2. `CodeAuditor.run()` (en `analyzer.py`) recorre archivos `.py` y, línea por
   línea, evalúa las reglas de `rules/security_rules.py` y
   `rules/lint_rules.py`.
3. Cada coincidencia genera un `Finding` (archivo, línea, severidad, regla,
   mensaje).
4. `ReportGenerator` (en `report.py`) transforma la lista de `Finding` en un
   reporte Markdown o JSON y lo guarda en disco.

## Dónde agregar cosas nuevas
- **Nueva regla de seguridad/lint** → agregar una instancia de `Rule` en
  `rules/security_rules.py` o `rules/lint_rules.py`.
- **Nuevo formato de reporte** (ej. HTML) → extender `ReportGenerator.save()`.
- **Nuevo lenguaje** → nuevo módulo `analyzer_<lenguaje>.py` reutilizando el
  patrón de `Finding`/`Rule`.
