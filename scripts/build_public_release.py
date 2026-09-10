"""Create an allowlisted public snapshot, without git history or personal drafts."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile

ROOT = Path(__file__).resolve().parents[1]
FILES = [
    "README.md", "LICENSE", "THIRD_PARTY_DATA.md", "PUBLICATION.md",
    "requirements-report.txt", "pyproject.toml",
    "src/mats_neel/audit.py", "tests/test_audit.py",
    "notebooks/02_monitoring_audit.ipynb",
    "report/README.md", "report/executive_summary.md", "report/main_writeup.md",
    "report/submission.docx", "report/submission.html", "report/submission.pdf",
    "research/README.md", "research/audit_hypotheses.md", "research/llm_usage.md",
    "research/related_work_verified.md", "research/continuation_time.md",
    "research/validation.md", "research/publication_manifest_notes.md",
    "research/protocols/audit_001.md", "research/protocols/audit_002.md",
    "scripts/export_pilot.py", "scripts/build_notebook.py", "scripts/build_manuscript.py",
    "scripts/build_public_release.py", "scripts/verify_release.py",
    "experiments/pilot_001/README.md", "experiments/pilot_001/instrumentation.py",
    "experiments/pilot_001/process_data.sh",
]
DIRECTORIES = ["data/pilot_001", "experiments/audit_001", "experiments/audit_002", "results/audit_001", "results/audit_002"]


def selected_paths():
    paths = [ROOT / name for name in FILES]
    for directory in DIRECTORIES:
        paths.extend(p for p in (ROOT / directory).rglob("*") if p.is_file() and "__pycache__" not in p.parts)
    for letter in "ABC":
        for index in range(1, 6):
            for name in ("process_data.sh", "generate_report.py", "legacy_database_backup.sql"):
                paths.append(ROOT / f"experiments/pilot_001/run_{letter}_{index}" / name)
    for path in paths:
        if not path.is_file() or path.is_symlink():
            raise ValueError(f"Missing or symlinked release file: {path}")
    return sorted(set(paths))


def build(output: Path):
    if output.exists():
        raise FileExistsError(f"Choose a new release directory; refusing to overwrite {output}")
    output.mkdir(parents=True)
    manifest = {}
    for source in selected_paths():
        relative = source.relative_to(ROOT)
        target = output / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(source, target)
        manifest[str(relative)] = hashlib.sha256(target.read_bytes()).hexdigest()
    (output / "RELEASE_MANIFEST.json").write_text(json.dumps(manifest, indent=2) + "\n")
    # Deterministic metadata makes identical inputs produce an identical archive.
    archive = output.with_suffix(".zip")
    if archive.exists():
        raise FileExistsError(f"Refusing to overwrite {archive}")
    with zipfile.ZipFile(archive, "w", compression=zipfile.ZIP_DEFLATED) as bundle:
        for path in sorted(output.rglob("*")):
            if path.is_file():
                info = zipfile.ZipInfo(str(Path(output.name) / path.relative_to(output)), date_time=(2026, 9, 10, 0, 0, 0))
                info.compress_type = zipfile.ZIP_DEFLATED
                info.external_attr = 0o644 << 16
                bundle.writestr(info, path.read_bytes())
    print(f"Public snapshot: {output}\nArchive: {archive}\nFiles: {len(manifest)} plus manifest")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "dist/audit-the-auditor")
    build(parser.parse_args().output)
