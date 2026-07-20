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
