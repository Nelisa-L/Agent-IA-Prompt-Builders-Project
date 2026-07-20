from pathlib import Path

from auditor_agent.analyzer import CodeAuditor


def test_detects_eval_usage(tmp_path: Path):
    bad_file = tmp_path / "bad.py"
    bad_file.write_text("result = eval(user_input)\n")

    auditor = CodeAuditor(tmp_path)
    findings = auditor.run()

    rule_ids = {f.rule_id for f in findings}
    assert "SEC001" in rule_ids


def test_no_findings_on_clean_code(tmp_path: Path):
    clean_file = tmp_path / "clean.py"
    clean_file.write_text("def add(a, b):\n    return a + b\n")

    auditor = CodeAuditor(tmp_path)
    findings = auditor.run()

    assert findings == []
