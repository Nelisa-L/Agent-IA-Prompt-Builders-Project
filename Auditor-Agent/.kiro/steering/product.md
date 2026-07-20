# Product Context — Auditor-Agent

## ¿Qué es?
Auditor-Agent es un agente que audita código Python en busca de problemas de
**seguridad** (uso de `eval`/`exec`, secretos hardcodeados, `shell=True`,
deserialización insegura con `pickle`, etc.) y **estilo/linting** básico,
generando un reporte claro y accionable.

## Problema que resuelve
En proyectos de hackathon y equipos pequeños no siempre hay tiempo para
revisiones de seguridad manuales. Auditor-Agent automatiza una primera pasada
de auditoría para detectar riesgos comunes antes de un commit, PR o demo.

## Usuarios objetivo
- Desarrolladores en el hackathon que quieren validar su código rápido.
- Equipos que quieren un check de seguridad básico en su pipeline de CI.

## Alcance actual (MVP)
- Analiza archivos `.py` de una carpeta o repositorio.
- Aplica reglas de seguridad y linting basadas en expresiones regulares.
- Genera reporte en Markdown o JSON.
- Corre en CI vía GitHub Actions.

## Fuera de alcance (por ahora)
- Soporte multi-lenguaje (JS/TS, etc.).
- Integración con linters externos (ruff, bandit) — ver roadmap.
- Interfaz web.
