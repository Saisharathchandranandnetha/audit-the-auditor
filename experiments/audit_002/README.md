# AUDIT-002: a sparse-file counterexample to the proposed physical dilemma

This is a red-team check of the **unexecuted Pilot 2's validator**, not a new
agent experiment. `frozen_sandbox.py` preserves the original implementation
without repairs. It is an experimental specimen, not a recommended sandbox.

```bash
python experiments/audit_002/reproduce.py --output /tmp/audit002-new-run.json
```

Requirements: Linux, Bubblewrap, and permission to create namespaces. The
outer sandbox may block this operation even when the host supports it. Such
failures are infrastructure failures, not negative research outcomes.

The script creates fresh temporary workspaces using the existing sandbox.
Only the two specified researcher-written commands execute. Raw recorded
observations are in `results/audit_002/observed.json`; no historical model
transcript is replayed or altered.

The dense control should hit the actual quota. The sparse control asks for
logical length without allocating its data blocks. A validator that checks only
logical length can accept it while the protected backup remains intact. Neither
control produces semantically valid processed JSONL. A real processing task
needs an independent content validator, not a file-length proxy.
