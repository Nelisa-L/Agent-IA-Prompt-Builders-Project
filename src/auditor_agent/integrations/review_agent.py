"""Agente que combina hallazgos propios + SonarCloud y los prioriza con un LLM.

Este módulo es el corazón "agéntico" de Auditor-Agent: toma dos fuentes de
análisis estático (nuestras reglas rápidas y SonarCloud) y usa la API de
Anthropic (Claude) para generar un resumen priorizado en lenguaje natural,
señalando qué atender primero y por qué.
"""

from __future__ import annotations

import os

import anthropic

from auditor_agent.analyzer import Finding
from auditor_agent.integrations.sonarcloud_client import SonarIssue

SYSTEM_PROMPT = """\
Eres un revisor de código senior especializado en seguridad. Recibirás dos \
listas de hallazgos sobre un mismo repositorio: una de un analizador propio \
(reglas simples) y otra de SonarCloud (análisis estático más profundo).

Tu tarea:
1. Deduplicar hallazgos que apunten al mismo problema real.
2. Priorizar: primero vulnerabilidades de seguridad explotables, luego bugs, \
   luego code smells / estilo.
3. Para cada hallazgo priorizado, explica en 1-2 líneas el riesgo real y una \
   sugerencia concreta de corrección.
4. Sé conciso. No repitas el mensaje crudo de la herramienta, interprétalo.

Devuelve la respuesta en Markdown con esta estructura:
## Crítico
## Importante
## Menor / Estilo
"""


def _format_own_findings(findings: list[Finding]) -> str:
    if not findings:
        return "(sin hallazgos del analizador propio)"
    return "\n".join(
        f"- [{f.severity}] {f.rule_id} en {f.file}:{f.line} — {f.message}"
        for f in findings
    )


def _format_sonar_issues(issues: list[SonarIssue]) -> str:
    if not issues:
        return "(sin hallazgos de SonarCloud)"
    return "\n".join(
        f"- [{i.severity}/{i.type}] {i.rule} en {i.component}:{i.line} — {i.message}"
        for i in issues
    )


class ReviewAgent:
    """Agente que llama a Claude para priorizar y explicar hallazgos."""

    def __init__(self, api_key: str | None = None, model: str = "claude-sonnet-4-6") -> None:
        self.client = anthropic.Anthropic(api_key=api_key or os.environ.get("ANTHROPIC_API_KEY"))
        self.model = model

    def review(self, own_findings: list[Finding], sonar_issues: list[SonarIssue]) -> str:
        user_content = (
            "### Hallazgos del analizador propio\n"
            f"{_format_own_findings(own_findings)}\n\n"
            "### Hallazgos de SonarCloud\n"
            f"{_format_sonar_issues(sonar_issues)}\n"
        )

        message = self.client.messages.create(
            model=self.model,
            max_tokens=1500,
            system=SYSTEM_PROMPT,
            messages=[{"role": "user", "content": user_content}],
        )

        return "".join(
            block.text for block in message.content if getattr(block, "type", "") == "text"
        )
