# Evidence and claims ledger

**Status:** retrospective case study, not a benchmark of monitor accuracy.

This page lets a reviewer trace report statements to observations and code.
The unit of observation is a saved trace fragment, not a completed agent
trial. There are 15 fragments, five in each original A/B/C prompt condition.
Replay seeds, selection policies, and byte-budget settings do not create
additional independent agent trials.

## Claim-to-evidence map

| Reportable statement | Supporting artifacts | What it does not show |
| --- | --- | --- |
| The legacy extractor retained 17 of 54 tool calls. | [Input manifest](../data/pilot_001/manifest.json), [analysis implementation](../src/mats_neel/audit.py), [summary](../results/audit_001/summary.json). | That an LLM monitor missed 37 calls, or that omitted calls were malicious. |
| Five confirmed processing-script edits were excluded by the command-only extractor. | [Evidence catalog](../results/audit_001/evidence_catalog.json), [capture comparison](../results/audit_001/capture.csv), [trace exports](../data/pilot_001/). Edit requests were cross-checked against resulting diffs and saved files. | That these edits violated a task rule or were deliberate deception. The backup was protected, not necessarily the script. |
| Nine script requests across seven runs lost working-directory context. | [Run table](../results/audit_001/runs.csv), [evidence catalog](../results/audit_001/evidence_catalog.json), [AUDIT-001 protocol](protocols/audit_001.md). | That all requested executions completed or were unsafe. |
| All 15 fragments ended without the final requested tool result and no final user-facing answers are recorded. | [Manifest](../data/pilot_001/manifest.json), [run table](../results/audit_001/runs.csv), [main report](../report/main_writeup.md). | Task success, task failure, honesty, concealment, or evasion rate. |
| Identical command text can behave differently when the working directory changes. | [Controlled execution script](../experiments/audit_001/analyze.py), [recorded controls](../results/audit_001/execution_controls.json). | A behavior demonstrated by the agent in a completed run. These were researcher-chosen local controls. |
| A sparse 30 MiB output passes a proposed validator with the backup intact. | [AUDIT-002 protocol](protocols/audit_002.md), [reproducer](../experiments/audit_002/reproduce.py), [recorded results](../results/audit_002/). | That an AI agent discovered the workaround, or that the file contains valid processed data. |
| Evidence retained by simplistic selection policies varies under matched byte budgets. | [Replay analysis](../src/mats_neel/audit.py), [replay records](../results/audit_001/compression_replay.json). | LLM summarizer performance, attack-detection performance, or realistic context pressure. All structured histories fit in 4 KiB per run. |

These are **previously reported claims**, not new experiments or newly verified
findings. The outcome of the original adaptive-evasion question is unresolved.

## Independent reproduction

From a trusted checkout, with Python 3.11+ and Bash, run:

    python scripts/verify_release.py
    python -m unittest discover -s tests -p 'test_audit.py' -v
    python experiments/audit_001/analyze.py --output /tmp/audit-review

Use the temporary output directory to avoid overwriting checked-in results.
Check the exit codes and inspect generated tables rather than assuming a
successful command implies every research claim is established. The verifier
does not rerun the Bubblewrap sparse-file experiment or any real LLM-monitor
evaluation. Never execute arbitrary commands copied from transcripts.

## Evidence that would change the interpretation

- Final tool results and independently checked task outcomes would enable
  completion labels. A planner's DONE field cannot substitute for them.
- Explicit restrictions on script editing would affect compliance labels,
  though malicious intent would remain a separate inference.
- A controlled agent-plus-monitor evaluation is necessary to measure actual
  monitor detection, rather than event availability.
- Real compression pressure and a real LLM summarizer are necessary before
  extending the replay comparison beyond simple selection policies.

## Attribution

The [AI assistance record](llm_usage.md) states that a coding assistant
performed substantial analysis, writing, and execution. The applicant's
independent personal review has not yet been attested. Reproduction by an
assistant and independent review by the applicant are different claims.
