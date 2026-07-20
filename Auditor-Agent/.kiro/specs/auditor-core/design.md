# Design — auditor-core

## Visión general
Pipeline simple de 3 etapas: **recolectar archivos → aplicar reglas →
generar reporte**. Sin dependencias externas para mantener el MVP portable.

## Componentes

### `Rule` (rules/security_rules.py)
```python
@dataclass(frozen=True)
class Rule:
    rule_id: str
    pattern: re.Pattern
    severity: str  # "info" | "warning" | "critical"
    message: str

    def matches(self, line: str) -> bool: ...
```
Cada regla es independiente y declarativa: agregar una nueva regla no
requiere tocar el motor de análisis.

### `Finding` (analyzer.py)
```python
@dataclass
class Finding:
    file: str
    line: int
    severity: str
    rule_id: str
    message: str
```

### `CodeAuditor` (analyzer.py)
- `run() -> list[Finding]`: recorre archivos `.py` (recursivo si es
  carpeta), lee línea por línea, evalúa `SECURITY_RULES + LINT_RULES`.
- Ignora errores de lectura de archivos individuales (no detiene el run
  completo).

### `ReportGenerator` (report.py)
- `save(output_path, fmt)`: escribe Markdown (tabla) o JSON
  (lista de `Finding` serializados).

### CLI (main.py)
- `argparse` con: `path` (posicional), `-o/--output`, `--format`.
- Valida que `path` exista antes de correr el análisis.

## Diagrama de flujo

```
CLI (main.py)
   │
   ▼
CodeAuditor.run()
   │  itera archivos .py
   ▼
por cada línea → evalúa SECURITY_RULES + LINT_RULES
   │
   ▼
lista[Finding]
   │
   ▼
ReportGenerator.save() → reporte.md / reporte.json
```

## Decisiones de diseño
- **Regex en vez de AST**: más rápido de implementar para el MVP de
  hackathon; documentado como limitación conocida (falsos positivos/negativos
  posibles). Iteración futura: migrar a `ast` para detección más precisa.
- **Sin dependencias externas**: facilita correr el proyecto en cualquier
  máquina durante el hackathon sin instalar linters pesados.
- **Reglas como datos, no código**: permite a cualquier miembro del equipo
  agregar reglas nuevas sin entender el motor completo.

## Testing strategy
- Unit tests con `pytest`, usando `tmp_path` para no tocar archivos reales.
- Casos mínimos: detecta patrón inseguro conocido (`eval`) y no genera falsos
  positivos en código limpio.
