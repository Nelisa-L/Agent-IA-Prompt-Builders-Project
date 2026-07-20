"""Reglas simples de estilo/linting."""

from __future__ import annotations

import re
from auditor_agent.rules.security_rules import Rule

LINT_RULES = [
    Rule(
        rule_id="LINT001",
        pattern=re.compile(r"[ \t]+$"),
        severity="info",
        message="Espacios en blanco al final de la línea.",
    ),
    Rule(
        rule_id="LINT002",
        pattern=re.compile(r".{101,}"),
        severity="info",
        message="Línea excede 100 caracteres.",
    ),
    Rule(
        rule_id="LINT003",
        pattern=re.compile(r"\bprint\("),
        severity="info",
        message="Uso de print() detectado; considera usar logging.",
    ),
]
