"""Lógica central de análisis de código: linting y reglas de seguridad."""

from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path

from auditor_agent.rules.security_rules import SECURITY_RULES
from auditor_agent.rules.lint_rules import LINT_RULES


@dataclass
class Finding:
    file: str
    line: int
    severity: str  # "info" | "warning" | "critical"
    rule_id: str
    message: str


@dataclass
class CodeAuditor:
    target: Path
    findings: list[Finding] = field(default_factory=list)

    def _iter_python_files(self):
        if self.target.is_file():
            yield self.target
        else:
            yield from self.target.rglob("*.py")

    def run(self) -> list[Finding]:
        self.findings = []
        for file_path in self._iter_python_files():
            self._audit_file(file_path)
        return self.findings

    def _audit_file(self, file_path: Path) -> None:
        try:
            lines = file_path.read_text(encoding="utf-8", errors="ignore").splitlines()
        except OSError:
            return

        for idx, line in enumerate(lines, start=1):
            for rule in (*SECURITY_RULES, *LINT_RULES):
                if rule.matches(line):
                    self.findings.append(
                        Finding(
                            file=str(file_path),
                            line=idx,
                            severity=rule.severity,
                            rule_id=rule.rule_id,
                            message=rule.message,
                        )
                    )
