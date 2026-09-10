"""Build/execute the review notebook. No new agent or API calls."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

import nbformat as nbf

ROOT = Path(__file__).resolve().parents[1]


def make_notebook():
    md, code = nbf.v4.new_markdown_cell, nbf.v4.new_code_cell
    cells = [
        md("""# Audit the Auditor

An executable audit of 15 saved coding-agent trace fragments and a proposed
task validator. **No agent generation or model-monitor evaluation happens here.**

The first hypothesis was adaptive evasion of compressed monitoring. The evidence
instead identifies missing observation channels, incomplete outcomes, and invalid
task-success proxies. Read `report/main_writeup.md` for the interpretation and
`research/llm_usage.md` for the substantial AI assistance and outstanding human
review. This notebook was written by the coding assistant.

Run from this repository's root or its `notebooks/` directory. The executable
analysis is imported from `.py` files; there is no duplicate notebook-only method.
"""),
        code("""from pathlib import Path
import csv, json, random, sys
from IPython.display import display, Image, Markdown

ROOT = Path.cwd()
if not (ROOT / 'src/mats_neel/audit.py').exists():
    ROOT = ROOT.parent
assert (ROOT / 'src/mats_neel/audit.py').exists(), 'Run inside the project'
sys.path.insert(0, str(ROOT / 'src'))
from mats_neel.audit import analyze

audit = analyze(ROOT / 'data/pilot_001', ROOT / 'experiments/pilot_001')
assert audit['totals'] == json.loads((ROOT / 'results/audit_001/summary.json').read_text())
audit['totals']"""),
        md("""## 1. Include every saved run

`None` means unknown, not failure. Every export ends with an unreturned tool
request; no final answer is recorded. Multiple Cwd requests in a run are not
independent agent samples. The exact pilot model and sampling settings are
missing from these exports.
"""),
        code("""headers = ['run', 'tool_calls', 'confirmed_guard_edits', 'outside_cwd_requests', 'has_final_answer', 'task_success']
table = '| ' + ' | '.join(headers) + ' |\\n|' + '|'.join(['---'] * len(headers)) + '|\\n'
table += '\\n'.join('| ' + ' | '.join(str(r[k]) for k in headers) + ' |' for r in audit['runs'])
display(Markdown(table))"""),
        md("""## 2. Inspect the evidence, not just the totals

All five edits are listed. Each has a result diff and matching saved script.
The label is **guard edit**, not **deception**: the task did not explicitly
protect the script. Event IDs refer to run, zero-based record index, and tool
index; original provider step indices are recorded separately.
"""),
        code("""edits = [e for e in audit['evidence'] if e['kind'] == 'guard_edit']
for e in edits:
    print(e['id'], e['status'], 'confirmation rows:', e['confirmation_diff_record_indices'])
example = next(e for e in edits if e['run'] == 'B1')
print(json.dumps(example, indent=2))"""),
        md("""## 3. What survives before compression?

The first score measures preserved edit requests. The second requires the Cwd
field as well as the invocation. These are evidence-availability counts, **not
monitor recall**. A full representation retaining its own inputs is a
completeness check; the finding is the old implementation's concrete omissions.
"""),
        code("""for view in ['legacy_command_text', 'structured_commands', 'all_tool_calls']:
    rows = [r for r in audit['capture'] if r['view'] == view]
    print(view, 'edits:', sum(r['guard_edit_available'] for r in rows), '/ 5;',
          'Cwd:', sum(r['outside_cwd_available'] for r in rows), '/ 9')
display(Image(filename=str(ROOT / 'results/audit_001/figures/capture.png')))"""),
        md("""## 4. Rerun the paired program controls

These execute a fixed nine-line script in temporary directories. They do not
execute any model transcript. Changing only Cwd changes the result. Neither a
success message nor exit code validates a data transformation in this task.
"""),
        code("""import importlib.util
spec = importlib.util.spec_from_file_location('audit_experiment', ROOT / 'experiments/audit_001/analyze.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
controls = module.controlled_execution()
assert controls == json.loads((ROOT / 'results/audit_001/execution_controls.json').read_text())
for r in controls:
    print(r['condition'], 'exit:', r['returncode'], 'backup unchanged:', r['backup_unchanged'],
          'output exists:', r['processed_output_exists'])"""),
        md("""## 5. Counterexample to the proposed replacement validator

This cell reads the saved AUDIT-002 observation, verifying its frozen-code hash.
It **does not launch Bubblewrap**. To repeat the experiment on Linux, use
`experiments/audit_002/reproduce.py --output /tmp/new-audit002.json`.

The sparse file passes the original validator without altering the backup.
This was a researcher-written control, not behavior elicited from an agent.
Logical size is not allocated storage or valid processed JSONL.
"""),
        code("""import hashlib
sparse_audit = json.loads((ROOT / 'results/audit_002/observed.json').read_text())
assert sparse_audit['frozen_sandbox_sha256'] == hashlib.sha256(
    (ROOT / 'experiments/audit_002/frozen_sandbox.py').read_bytes()).hexdigest()
for observation in sparse_audit['observations']:
    result = observation['result']
    print(observation['condition'], 'validator success:', result['success'],
          'backup violation:', result['violation_type'])
    print(result.get('agent_stdout', '').strip())"""),
        md("""## 6. Compression sensitivity: keep the claim narrow

Different whole-event selectors retain different evidence under equal per-run
byte budgets. This does not model semantic LLM summarization. The selector gets
no evidence labels. Seeds are selection orders, not new model samples.

The important countercheck: at **4 KiB**, every tool-call representation fits
in full. These histories do not establish practical context pressure.
"""),
        code("""for policy in ['head_tail', 'tail', 'random']:
    rows = [r for r in audit['replay'] if r['view'] == 'all_tool_calls'
            and r['budget_setting'] == '75' and r['policy'] == policy]
    print(policy, 'mean edits retained:', round(sum(r['mean_guard_edit'] for r in rows), 2), '/ 5')
fixed = [r for r in audit['replay'] if r['view'] == 'all_tool_calls'
         and r['budget_setting'] == '4096_bytes' and r['policy'] == 'head_tail']
assert sum(r['mean_guard_edit'] for r in fixed) == 5
assert sum(r['mean_outside_cwd'] for r in fixed) == 9
display(Image(filename=str(ROOT / 'results/audit_001/figures/compression.png')))"""),
        md("""## 7. Randomly selected examples and unresolved questions

The fixed seed selects A2, C5, A3. The example set includes an almost-empty run,
an interrupted edit run, and a Cwd workaround request. No runs are excluded for
lacking an interesting event.
"""),
        code("""sample = random.Random(20260909).sample([r['run'] for r in audit['runs']], 3)
print('Selected runs:', sample)
for run in sample:
    row = next(r for r in audit['runs'] if r['run'] == run)
    print(run, {k: row[k] for k in ['records', 'confirmed_guard_edits', 'outside_cwd_requests', 'task_success']})"""),
        md("""## What this changes

The existing data do not answer the original adaptive-evasion question. The
captured record and task validators were insufficient. The correction is to
repair evidence capture and define a real task outcome before collecting more
agent data—not to relabel these workarounds as proof of deception.

A next experiment should preserve every tool/result through completion, permit
an honest blocker report, verify task content independently, and evaluate a real
monitor on paired benign and concerning completed histories. No such follow-up
was run here. See the report for related work, limitations, and provenance.
"""),
    ]
    for i, cell in enumerate(cells):
        cell["id"] = f"audit-cell-{i:02d}"
    notebook = nbf.v4.new_notebook(cells=cells)
    notebook.metadata = {"kernelspec": {"display_name": "Python 3", "language": "python", "name": "python3"},
                         "language_info": {"name": "python", "version": sys.version.split()[0]}}
    return notebook


def main(execute: bool):
    notebook = make_notebook()
    if execute:
        from nbclient import NotebookClient
        # Register only a temporary kernelspec, using this exact interpreter.
        with tempfile.TemporaryDirectory(prefix="mats-jupyter-") as tmp:
            spec_dir = Path(tmp) / "kernels/mats-audit"
            spec_dir.mkdir(parents=True)
            (spec_dir / "kernel.json").write_text(json.dumps({
                "argv": [sys.executable, "-m", "ipykernel_launcher", "-f", "{connection_file}"],
                "display_name": "MATS audit", "language": "python",
            }))
            previous = os.environ.get("JUPYTER_PATH")
            os.environ["JUPYTER_PATH"] = tmp + (os.pathsep + previous if previous else "")
            os.environ.setdefault("JUPYTER_RUNTIME_DIR", str(Path(tmp) / "runtime"))
            os.environ.setdefault("IPYTHONDIR", str(Path(tmp) / "ipython"))
            try:
                NotebookClient(notebook, timeout=120, kernel_name="mats-audit", resources={"metadata": {"path": str(ROOT)}}).execute()
            finally:
                if previous is None:
                    os.environ.pop("JUPYTER_PATH", None)
                else:
                    os.environ["JUPYTER_PATH"] = previous
    nbf.validate(notebook)
    target = ROOT / "notebooks/02_monitoring_audit.ipynb"
    nbf.write(notebook, target)
    print(f"{'Executed and saved' if execute else 'Built'} {target}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--execute", action="store_true")
    main(parser.parse_args().execute)
