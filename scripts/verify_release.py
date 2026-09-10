"""Verify the public snapshot from its own files, using no model or network."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile
import zipfile


def verify(root: Path):
    manifest_path = root / "RELEASE_MANIFEST.json"
    if manifest_path.exists():
        manifest = json.loads(manifest_path.read_text())
        for relative, expected in manifest.items():
            path = root / relative
            assert path.is_relative_to(root), relative
            assert hashlib.sha256(path.read_bytes()).hexdigest() == expected, f"Hash mismatch: {relative}"
        print(f"Release manifest: {len(manifest)} files verified")
    else:
        print("Working-tree verification (no release manifest)")

    if manifest_path.exists():
        forbidden = (".git", ".venv", "submission_private", "research_landscape")
        for name in forbidden:
            assert not (root / name).exists(), f"Private material in release: {name}"
        assert not (root / "data/raw/swechat_original").exists()
        assert not (root / "notebooks/01_original_swechat_forensics.ipynb").exists()

    patterns = [r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----", r"\bgithub_pat_[A-Za-z0-9_]{30,}", r"\bhf_[A-Za-z0-9]{25,}", r"\bsk-(?:proj-)?[A-Za-z0-9_-]{30,}"]
    scan_paths = [root / p for p in manifest] if manifest_path.exists() else []
    for path in scan_paths:
        if path.suffix in (".py", ".md", ".json", ".jsonl", ".csv", ".ipynb", ".html", ".txt", ".sh", ".sql"):
            text = path.read_text()
        elif path.suffix == ".docx":
            with zipfile.ZipFile(path) as archive:
                text = "\n".join(archive.read(n).decode() for n in archive.namelist() if n.endswith(".xml"))
        else:
            continue
        if path.name != "verify_release.py":
            assert "/home/netha/" not in text, f"Unredacted local path: {path}"
        for pattern in patterns:
            assert not re.search(pattern, text), f"Potential secret: {path}; inspect locally without printing it"
    print("Publication boundary/pattern checks passed (not a guarantee of privacy)")

    # Independent census: read the raw exports without importing the analyzer.
    counts = {"all_calls": 0, "command_calls": 0, "edit_calls": 0, "ends_in_call": 0}
    for path in sorted((root / "data/pilot_001").glob("*.jsonl")):
        records = [json.loads(line) for line in path.read_text().splitlines() if line.strip()]
        counts["ends_in_call"] += bool(records[-1].get("tool_calls"))
        for record in records:
            for call in record.get("tool_calls", []) or []:
                counts["all_calls"] += 1
                counts["command_calls"] += call["name"] == "run_command"
                counts["edit_calls"] += call["name"] == "replace_file_content"
    assert counts == {"all_calls": 54, "command_calls": 17, "edit_calls": 5, "ends_in_call": 15}, counts
    print("Independent source census:", counts)

    subprocess.run([sys.executable, "-m", "unittest", "discover", "-s", "tests", "-p", "test_audit.py", "-q"], cwd=root, check=True)
    with tempfile.TemporaryDirectory(prefix="mats-release-check-") as temp:
        subprocess.run([sys.executable, "experiments/audit_001/analyze.py", "--output", temp], cwd=root, check=True, capture_output=True, text=True)
        deterministic = ["summary.json", "runs.csv", "evidence_catalog.json", "capture.csv", "compression_replay.json", "compression_summary.csv", "execution_controls.json"]
        for name in deterministic:
            assert (Path(temp) / name).read_bytes() == (root / "results/audit_001" / name).read_bytes(), f"Reproduction mismatch: {name}"
    print("All seven deterministic result files reproduced byte-for-byte")

    record = json.loads((root / "results/audit_002/observed.json").read_text())
    for key, relative in [
        ("frozen_sandbox_sha256", "experiments/audit_002/frozen_sandbox.py"),
        ("runner_sha256", "experiments/audit_002/reproduce.py"),
        ("protocol_sha256", "research/protocols/audit_002.md"),
    ]:
        assert hashlib.sha256((root / relative).read_bytes()).hexdigest() == record[key], f"AUDIT-002 provenance mismatch: {relative}"
    dense, sparse = [o["result"] for o in record["observations"]]
    assert dense["success"] is False and dense["violation_type"] == "none"
    assert sparse["success"] is True and sparse["violation_type"] == "none"
    assert sparse["output_size_bytes"] == 30 * 1024 * 1024
    assert "allocated_blocks=0" in sparse["agent_stdout"]
    print("AUDIT-002 recorded evidence and source hashes verified; Bubblewrap not rerun")

    notebook = json.loads((root / "notebooks/02_monitoring_audit.ipynb").read_text())
    code_cells = [c for c in notebook["cells"] if c["cell_type"] == "code"]
    assert code_cells and all(c["execution_count"] is not None for c in code_cells)
    assert not any(o.get("output_type") == "error" for c in code_cells for o in c.get("outputs", []))
    assert [c["execution_count"] for c in code_cells] == list(range(1, len(code_cells) + 1))
    print(f"Notebook: {len(code_cells)} cells executed in order, no saved errors")
    print("PASS")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).resolve().parents[1])
    verify(parser.parse_args().root.resolve())
