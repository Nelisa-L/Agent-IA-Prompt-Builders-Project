"""Punto de entrada del Auditor-Agent.

Ejecuta un análisis de linting y seguridad sobre un repositorio o carpeta
de código y genera un reporte con los hallazgos.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from auditor_agent.analyzer import CodeAuditor
from auditor_agent.report import ReportGenerator


def build_arg_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="auditor-agent",
        description="Agente auditor de código: linting y seguridad.",
    )
    parser.add_argument(
        "path",
        type=str,
        help="Ruta al proyecto o archivo a auditar",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=str,
        default="reporte_auditoria.md",
        help="Archivo de salida del reporte (default: reporte_auditoria.md)",
    )
    parser.add_argument(
        "--format",
        choices=["md", "json"],
        default="md",
        help="Formato del reporte generado",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_arg_parser()
    args = parser.parse_args(argv)

    target = Path(args.path)
    if not target.exists():
        print(f"Error: la ruta '{target}' no existe.", file=sys.stderr)
        return 1

    auditor = CodeAuditor(target)
    findings = auditor.run()

    reporter = ReportGenerator(findings)
    reporter.save(args.output, fmt=args.format)

    print(f"Auditoría completada. Reporte generado en: {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
