"""Cliente mínimo para leer issues (hallazgos) de un proyecto en SonarCloud.

Usa la API pública de SonarCloud: https://sonarcloud.io/web_api/api/issues
Requiere un token (SONAR_TOKEN) con permisos de lectura sobre el proyecto.
"""

from __future__ import annotations

from dataclasses import dataclass

import requests

SONARCLOUD_API_BASE = "https://sonarcloud.io/api"


@dataclass
class SonarIssue:
    key: str
    rule: str
    severity: str  # INFO | MINOR | MAJOR | CRITICAL | BLOCKER
    component: str
    line: int | None
    message: str
    type: str  # BUG | VULNERABILITY | CODE_SMELL


class SonarCloudClient:
    def __init__(self, token: str, organization: str, project_key: str) -> None:
        self.token = token
        self.organization = organization
        self.project_key = project_key

    def fetch_issues(self, statuses: str = "OPEN,CONFIRMED,REOPENED") -> list[SonarIssue]:
        """Trae los issues abiertos del proyecto configurado."""
        response = requests.get(
            f"{SONARCLOUD_API_BASE}/issues/search",
            params={
                "organization": self.organization,
                "componentKeys": self.project_key,
                "statuses": statuses,
                "ps": 200,  # page size máximo
            },
            auth=(self.token, ""),
            timeout=30,
        )
        response.raise_for_status()
        data = response.json()

        issues: list[SonarIssue] = []
        for item in data.get("issues", []):
            text_range = item.get("textRange") or {}
            issues.append(
                SonarIssue(
                    key=item.get("key", ""),
                    rule=item.get("rule", ""),
                    severity=item.get("severity", "INFO"),
                    component=item.get("component", ""),
                    line=text_range.get("startLine"),
                    message=item.get("message", ""),
                    type=item.get("type", "CODE_SMELL"),
                )
            )
        return issues
