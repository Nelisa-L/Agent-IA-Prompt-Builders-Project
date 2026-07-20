# Tech Context — Auditor-Agent

## Lenguaje y versión
- Python >= 3.10

## Empaquetado
- `pyproject.toml` con `setuptools`, layout `src/`.
- Comando CLI instalado como `auditor-agent` (entry point en
  `auditor_agent.main:main`).

## Dependencias
- `pytest` para tests (ver `requirements.txt`).
- Sin dependencias externas para el análisis (solo `re` de stdlib), a
  propósito, para mantener el MVP ligero y fácil de correr en el hackathon.

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
