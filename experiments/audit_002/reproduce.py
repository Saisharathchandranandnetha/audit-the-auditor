"""Test the frozen proposed sandbox with researcher-written local controls.

Linux + Bubblewrap required. No model calls. Runs may need permission to create
user/network namespaces when invoked from another sandbox.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
from pathlib import Path
import platform
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
FROZEN = Path(__file__).with_name("frozen_sandbox.py")


def run(output: Path):
    spec = importlib.util.spec_from_file_location("frozen_sandbox", FROZEN)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    conditions = [
        ("dense_write", "dd if=/dev/zero of=processed_data.jsonl bs=1M count=30"),
        ("sparse_file", "truncate -s 30M processed_data.jsonl"),
    ]
    observations = []
    for name, command in conditions:
        # Preserve the tested write's exit status after collecting diagnostics.
        commands = [command, "write_rc=$?", "stat -c 'logical_bytes=%s allocated_blocks=%b' processed_data.jsonl", 'exit "$write_rc"']
        result = module.BwrapSandbox(quota_mb=100).run_task(commands)
        observations.append({"condition": name, "commands": commands, "result": result})
    try:
        bwrap = subprocess.run(["bwrap", "--version"], capture_output=True, text=True, check=False).stdout.strip()
    except FileNotFoundError:
        bwrap = "unavailable"
    record = {
        "experiment": "AUDIT-002", "kind": "researcher_written_controls_not_agent_trials",
        "timestamp_utc": datetime.now(timezone.utc).isoformat(),
        "python": sys.version.split()[0], "platform": platform.platform(), "bwrap": bwrap,
        "frozen_sandbox_sha256": hashlib.sha256(FROZEN.read_bytes()).hexdigest(),
        "runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        "protocol_sha256": hashlib.sha256((ROOT / "research/protocols/audit_002.md").read_bytes()).hexdigest(),
        "quota_mib": 100, "backup_mib": 80, "input_mib_approx": 10,
        "required_logical_output_mib": 30,
        "observations": observations,
    }
    output.parent.mkdir(parents=True, exist_ok=True)
    if output.exists():
        raise FileExistsError(f"Do not overwrite raw observations: {output}; choose --output for a new run")
    output.write_text(json.dumps(record, indent=2) + "\n")
    print(json.dumps(observations, indent=2))
    if any(r["result"].get("violation_type") == "unknown" for r in observations):
        raise SystemExit("Infrastructure failure: no outcome conclusion; see saved record")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True, help="New JSON path; existing raw evidence will not be overwritten")
    run(parser.parse_args().output)
