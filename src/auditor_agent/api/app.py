"""API web mínima para exponer Auditor-Agent como demo en línea.

Permite subir código (texto o archivo) y recibir el reporte de auditoría
en JSON. Pensada para desplegarse en AWS Lambda vía Mangum o en cualquier
servidor ASGI (uvicorn) para la demo del hackathon.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware

from auditor_agent.analyzer import CodeAuditor
from auditor_agent.report import ReportGenerator
from auditor_agent.integrations.sonarcloud_client import SonarCloudClient
from auditor_agent.integrations.review_agent import ReviewAgent

app = FastAPI(
    title="Auditor-Agent API",
    description="Agente auditor de código: linting y seguridad.",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.post("/audit")
async def audit_code(file: UploadFile = File(...)) -> dict:
    """Recibe un archivo .py y devuelve los hallazgos de la auditoría."""
    with tempfile.TemporaryDirectory() as tmp_dir:
        tmp_path = Path(tmp_dir) / file.filename
        tmp_path.write_bytes(await file.read())

        auditor = CodeAuditor(tmp_path)
        findings = auditor.run()
        report = ReportGenerator(findings)

        return {
            "total_findings": len(findings),
            "findings": [
                {
                    "file": f.file,
                    "line": f.line,
                    "severity": f.severity,
                    "rule_id": f.rule_id,
                    "message": f.message,
                }
                for f in findings
            ],
            "report_markdown": report._to_markdown(),
        }


@app.get("/review")
def review_project() -> dict:
    """Combina hallazgos propios + SonarCloud y devuelve un resumen del LLM.

    Requiere las variables de entorno:
    - SONAR_TOKEN, SONAR_ORGANIZATION, SONAR_PROJECT_KEY
    - ANTHROPIC_API_KEY
    """
    import os

    sonar = SonarCloudClient(
        token=os.environ["SONAR_TOKEN"],
        organization=os.environ["SONAR_ORGANIZATION"],
        project_key=os.environ["SONAR_PROJECT_KEY"],
    )
    sonar_issues = sonar.fetch_issues()

    # En este endpoint de demo no volvemos a correr el analizador propio
    # sobre todo el repo (requeriría el código fuente montado en Lambda);
    # se puede combinar con /audit en el flujo real de CI.
    agent = ReviewAgent()
    summary = agent.review(own_findings=[], sonar_issues=sonar_issues)

    return {"summary_markdown": summary, "sonar_issues_count": len(sonar_issues)}
