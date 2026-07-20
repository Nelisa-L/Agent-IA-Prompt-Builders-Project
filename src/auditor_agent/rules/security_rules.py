"""Reglas simples de detección de patrones inseguros en código Python."""

from __future__ import annotations

import re
from dataclasses import dataclass


@dataclass(frozen=True)
class Rule:
    rule_id: str
    pattern: re.Pattern
    severity: str
    message: str

    def matches(self, line: str) -> bool:
        return bool(self.pattern.search(line))


SECURITY_RULES = [
    Rule(
        rule_id="SEC001",
        pattern=re.compile(r"\beval\("),
        severity="critical",
        message="Uso de eval() detectado: riesgo de ejecución de código arbitrario.",
    ),
    Rule(
        rule_id="SEC002",
        pattern=re.compile(r"\bexec\("),
        severity="critical",
        message="Uso de exec() detectado: riesgo de ejecución de código arbitrario.",
    ),
    Rule(
        rule_id="SEC003",
        pattern=re.compile(r"(?i)(api_key|secret|password)\s*=\s*['\"][^'\"]+['\"]"),
        severity="critical",
        message="Posible credencial o secreto hardcodeado en el código.",
    ),
    Rule(
        rule_id="SEC004",
        pattern=re.compile(r"subprocess\.(call|run|Popen)\(.*shell\s*=\s*True"),
        severity="warning",
        message="Uso de shell=True en subprocess: riesgo de inyección de comandos.",
    ),
    Rule(
        rule_id="SEC005",
        pattern=re.compile(r"\bpickle\.load\("),
        severity="warning",
        message="Deserialización insegura con pickle.load().",
    ),
]
