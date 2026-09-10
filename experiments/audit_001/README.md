# AUDIT-001: Before compression

Retrospective audit of the 15 existing pilot trace fragments. See
[analysis plan](../../research/protocols/audit_001.md) and
[main report](../../report/main_writeup.md).

From the repository root:

```bash
python experiments/audit_001/analyze.py
python -m unittest discover -s tests -p 'test_audit.py' -v
# Optional, requires matplotlib:
python experiments/audit_001/figures.py
```

The first two commands need only Python's standard library and Bash for three
small local execution controls. They make no model/API/network calls. The
controls execute a fixed, audited nine-line script, not commands from the logs.
The original experiments are not rerun. Use `--output /tmp/audit-check` to
regenerate tables without replacing the checked-in derived outputs.

Raw inputs: `data/pilot_001/` and the frozen `experiments/pilot_001/run_*`
artifacts. Output: `results/audit_001/`. The source exports have incomplete
endings; this is represented explicitly, not treated as a negative outcome.

Compression replay uses three representations and three whole-event selection
policies with common per-run byte budgets. Labels are carried only in the
scorer; the selectors receive text and opaque IDs, not the outcome flags.
Head/tail greedily considers the first, last, second, penultimate event, etc.
Tail considers the latest event first. Random uses seeds 0–99. Each policy skips
events that will not fit and returns selected events in chronological order.
These are deliberately simple deletion baselines, not LLM summarizers.

The full evidence catalog includes every qualifying edit and outside-directory
invocation. `runs.csv` contains all 15 runs, including the very short A2.
Repeated calls in A1/C2 are retained as events but are not independent trials.
