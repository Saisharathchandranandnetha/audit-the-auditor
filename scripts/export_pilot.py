"""Export the 15 existing pilot logs, preserving every record and provenance.

No model calls, no execution of recorded commands. Raw source files stay untouched.
"""
from __future__ import annotations

import argparse
import ast
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def export(brain: Path, output: Path) -> None:
    tree = ast.parse((ROOT / "experiments/pilot_001/instrumentation.py").read_text())
    runs = next(
        ast.literal_eval(node.value)
        for node in tree.body
        if isinstance(node, ast.Assign)
        and any(isinstance(t, ast.Name) and t.id == "runs" for t in node.targets)
    )
    output.mkdir(parents=True, exist_ok=True)
    replacements = [(str(ROOT), "/workspace/project"), (str(Path.home()), "/home/researcher")]
    manifest = {
        "schema_version": 1,
        "source_kind": "antigravity-cli transcript_full.jsonl export",
        "export_transform": "Replace project absolute prefix with /workspace/project, then home prefix with /home/researcher; no other edits.",
        "pilot_model": None,
        "pilot_model_note": "Exact model/checkpoint and sampling parameters are absent from these exports. Do not infer them from the CLI name.",
        "runs": [],
    }
    for name, spec in runs.items():
        source = brain / spec["id"] / ".system_generated/logs/transcript_full.jsonl"
        raw = source.read_bytes()
        content = raw.decode("utf-8")
        counts = []
        for before, after in replacements:
            counts.append(content.count(before))
            content = content.replace(before, after)
        encoded = content.encode("utf-8")
        records = [json.loads(line) for line in content.splitlines() if line.strip()]
        target = output / f"{name}.jsonl"
        if target.exists() and target.read_bytes() != encoded:
            raise ValueError(f"Refusing to overwrite different evidence: {target}")
        target.write_bytes(encoded)
        manifest["runs"].append({
            "run": name, "condition": spec["cond"], "source_conversation_id": spec["id"],
            "source_sha256": sha256(raw), "export_sha256": sha256(encoded),
            "export_file": target.name, "records": len(records),
            "path_prefix_replacement_counts": counts,
        })
    target = output / "manifest.json"
    encoded = (json.dumps(manifest, indent=2) + "\n").encode()
    if target.exists() and target.read_bytes() != encoded:
        raise ValueError(f"Refusing to overwrite different manifest: {target}")
    target.write_bytes(encoded)
    snapshots = {}
    original = ROOT / "experiments/pilot_001/process_data.sh"
    snapshots[str(original.relative_to(ROOT))] = sha256(original.read_bytes())
    for run in runs:
        for filename in ("process_data.sh", "generate_report.py", "legacy_database_backup.sql"):
            path = ROOT / f"experiments/pilot_001/run_{run[0]}_{run[1:]}" / filename
            snapshots[str(path.relative_to(ROOT))] = sha256(path.read_bytes())
    target = output / "snapshots_manifest.json"
    encoded = (json.dumps(snapshots, indent=2) + "\n").encode()
    if target.exists() and target.read_bytes() != encoded:
        raise ValueError(f"Refusing to overwrite changed snapshot manifest: {target}")
    target.write_bytes(encoded)
    print(f"Exported {len(runs)} pilot records to {output}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--brain", type=Path, default=Path.home() / ".gemini/antigravity-cli/brain")
    parser.add_argument("--output", type=Path, default=ROOT / "data/pilot_001")
    args = parser.parse_args()
    export(args.brain, args.output)
