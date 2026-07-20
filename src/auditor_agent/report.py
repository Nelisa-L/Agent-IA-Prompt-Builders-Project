"""Generación de reportes de auditoría en Markdown o JSON."""

from __future__ import annotations

import json
from dataclasses import asdict
from pathlib import Path


class ReportGenerator:
    def __init__(self, findings):
        self.findings = findings

    def save(self, output_path: str, fmt: str = "md") -> None:
        path = Path(output_path)
        if fmt == "json":
            path.write_text(
                json.dumps([asdict(f) for f in self.findings], indent=2, ensure_ascii=False),
                encoding="utf-8",
            )
        else:
            path.write_text(self._to_markdown(), encoding="utf-8")

    def _to_markdown(self) -> str:
        lines = ["# Reporte de Auditoría de Código", ""]
        if not self.findings:
            lines.append("✅ No se encontraron hallazgos.")
            return "\n".join(lines)

        lines.append(f"Se encontraron **{len(self.findings)}** hallazgos.\n")
        lines.append("| Severidad | Regla | Archivo | Línea | Mensaje |")
        lines.append("|---|---|---|---|---|")
        for f in self.findings:
            lines.append(
                f"| {f.severity} | {f.rule_id} | {f.file} | {f.line} | {f.message} |"
            )
        return "\n".join(lines)
