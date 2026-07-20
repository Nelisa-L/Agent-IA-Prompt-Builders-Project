# Tech Context — Auditor-Agent

## Lenguaje y versión
- Python >= 3.10

## Empaquetado
- `pyproject.toml` con `setuptools`, layout `src/`.
- Comando CLI instalado como `auditor-agent` (entry point en
  `auditor_agent.main:main`).

## Dependencias
- `pytest` para tests.
- `fastapi`, `uvicorn`, `mangum`, `python-multipart` para la API/demo.
- `requests` para consumir la API de SonarCloud.
- `anthropic` para el agente que prioriza/explica hallazgos con Claude.
- El motor de reglas propio (regex, stdlib) se mantiene sin dependencias
  para poder correr rápido y offline como primera capa de análisis.

## Integraciones externas
- **SonarCloud**: análisis estático profundo (bugs, vulnerabilidades, code
  smells, cobertura). Se dispara vía GitHub Actions
  (`.github/workflows/sonarcloud.yml`) en cada push/PR. Config en
  `sonar-project.properties`.
- **Claude (Anthropic API)**: el `ReviewAgent`
  (`src/auditor_agent/integrations/review_agent.py`) combina los hallazgos
  propios + los de SonarCloud y genera un resumen priorizado en lenguaje
  natural (Crítico / Importante / Menor).

## Variables de entorno necesarias
- `SONAR_TOKEN`, `SONAR_ORGANIZATION`, `SONAR_PROJECT_KEY`
- `ANTHROPIC_API_KEY`

## Testing
- `pytest` sobre la carpeta `tests/`.
- Los tests usan `tmp_path` de pytest para crear archivos temporales y no
  tocar el filesystem real del usuario.

## CI/CD
- GitHub Actions (`.github/workflows/ci.yml`): instala el paquete y corre
  `pytest` en cada push/PR a `main`.

## Convenciones de código
- Usar `from __future__ import annotations` en todos los módulos.
- Tipar funciones públicas.
- Reglas nuevas de auditoría van en `rules/` como instancias de `Rule`
  (`rule_id`, `pattern`, `severity`, `message`).
- Mantener las reglas simples (regex) en el MVP; lógica más compleja
  (AST, análisis de flujo) queda para iteraciones futuras.

## Cómo correr localmente
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
auditor-agent ./mi-proyecto -o reporte.md
pytest -q
```
