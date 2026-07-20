# Auditor-Agent

Creación de agente auditor de código.

Agente en Python que audita un repositorio o carpeta en busca de problemas
de **linting** y **seguridad** (uso de `eval`/`exec`, secretos hardcodeados,
`shell=True` en subprocess, deserialización insegura con `pickle`, etc.) y
genera un reporte en Markdown o JSON.

## Estructura del proyecto

```
Auditor-Agent/
├── .kiro/                    # Steering + Specs (spec-driven development)
│   ├── steering/
│   └── specs/auditor-core/
├── src/
│   └── auditor_agent/
│       ├── __init__.py
│       ├── main.py          # CLI / punto de entrada
│       ├── analyzer.py      # Motor de análisis
│       ├── report.py        # Generación de reportes
│       ├── api/
│       │   └── app.py       # API FastAPI (demo en línea)
│       └── rules/
│           ├── __init__.py
│           ├── security_rules.py
│           └── lint_rules.py
├── infra/                    # Deploy en AWS (Lambda + API Gateway vía SAM)
│   ├── lambda_handler.py
│   ├── template.yaml
│   └── README.md
├── tests/
│   └── test_analyzer.py
├── .github/
│   └── workflows/
│       └── ci.yml
├── pyproject.toml
├── requirements.txt
├── .gitignore
└── README.md
```

## Demo en línea (AWS)
La API se despliega como función serverless en AWS Lambda + API Gateway.
Ver instrucciones de deploy en [`infra/README.md`](infra/README.md).

## Instalación

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
pip install -r requirements.txt
```

## Uso

```bash
auditor-agent ./ruta/al/proyecto -o reporte_auditoria.md
```

Opciones:
- `-o, --output`: archivo de salida del reporte (default: `reporte_auditoria.md`)
- `--format`: `md` o `json`

## Tests

```bash
pytest -q
```

## Roadmap (hackathon)

- [ ] Integrar linters reales (`ruff`, `bandit`) además de las reglas propias
- [ ] Soporte multi-lenguaje (JS/TS)
- [ ] Interfaz web o bot que corra el análisis sobre un PR de GitHub
- [ ] Scoring de riesgo por severidad
