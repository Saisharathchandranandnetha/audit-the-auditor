# Audit the Auditor

### What can a coding-agent monitor conclude when its evidence is incomplete?

This repository is a **reproducible, retrospective audit** of an early
coding-agent monitoring experiment. It began by asking whether an agent
would change its behavior when told that a monitor would see a compressed
history. After examining the saved records, that original question remained
unanswered: the records omit relevant tool actions, execution context, and
the final results needed to establish task outcomes.

The contribution is a concrete diagnosis of **what reached the observation
pipeline**. This is **not** evidence that agents intentionally evaded a
monitor, nor a measurement of LLM-monitor detection accuracy.

## Findings from the saved pilot

The dataset contains **15 saved trace fragments**, five in each of three
original prompt conditions. These are not 15 verified completed tasks.

| Finding | Observed evidence | Boundary of the claim |
| --- | --- | --- |
| Tool coverage | The original command-only extractor kept **17 of 54** tool calls. It omitted **all five confirmed processing-script edits**, which used a different editing tool. | Measures extraction coverage, not monitor recall or agent intent. |
| Execution context | **Nine script-execution requests across seven runs** lost the working-directory argument. Local controls showed the same command could behave differently from a different directory. | Requests are not proof of completed execution. |
| Incomplete outcomes | **All 15** exported fragments stop before the final requested tool result, with no final user-facing answers preserved. | Cannot label task success, concealment or honest refusal. |
| Validator counterexample | A researcher-run local control produced a **30 MiB sparse file** that passed a proposed replacement validator without modifying the protected backup. | Not an agent-discovered strategy or valid data-processing result. |

The original hypothesis about adaptive monitor evasion is **unresolved**.
The precise pilot model/checkpoint and sampling settings are unavailable.
This study compares a command-only extractor with more complete structured
representations and simple byte-budget selection policies; it does **not**
evaluate a running LLM monitor or realistic semantic compression.

![Evidence lost before compression](results/audit_001/figures/capture.png)

## Why this matters

An oversight system can only judge evidence made available to it. A clean
monitor decision may provide little reassurance if the upstream recorder
missed a relevant tool channel or execution argument. The broader research
question is whether collecting and checking that missing evidence improves
actual safety decisions. **That broader question has not been tested here.**

## Read and inspect the research

- [Executive summary](report/executive_summary.md) — short statement of
  the findings, caveats and authorship.
- [Main report](report/main_writeup.md) — complete case study and alternatives.
- [Evidence-to-claims ledger](research/evidence_and_claims.md) — direct
  links from each claim to its source and limitations.
- [AUDIT-001 protocol](research/protocols/audit_001.md) — retrospective trace
  analysis, evidence retention and fixed shell controls.
- [AUDIT-002 protocol](research/protocols/audit_002.md) — proposed-validator
  counterexample tested using local sandbox controls.
- [Hypotheses and counterevidence](research/audit_hypotheses.md) — what
  the observations support and what remains unresolved.
- [Executed analysis notebook](notebooks/02_monitoring_audit.ipynb) —
  saved analytical outputs; the notebook alone is not a new validation run.

## Reproduction

For a **fresh research snapshot** containing the current README and source
files, start with Python 3.11+ and Bash. The core audit uses only the Python
standard library; no GPU, model key or network request is required.

```bash
python scripts/build_public_release.py --output /tmp/audit-the-auditor-review
python scripts/verify_release.py --root /tmp/audit-the-auditor-review
```

The first command creates a **new allowlisted directory and ZIP** with
source hashes in a newly generated `RELEASE_MANIFEST.json`. Do not reuse
an existing output directory. The second validates that snapshot's hashes,
recounts tool calls, runs the core tests, compares seven deterministic
result files byte-for-byte, and checks recorded notebook and AUDIT-002
evidence. It **does not** rerun Bubblewrap or an LLM monitor.

To run only the core audit and regenerate outputs without replacing
checked-in results:

```bash
python -m unittest discover -s tests -p 'test_audit.py' -v
python experiments/audit_001/analyze.py --output /tmp/audit-review
```

The analysis executes three **fixed, locally defined** shell controls; it
does **not** execute commands from recorded agent transcripts. A separate
Linux/Bubblewrap control is available for environments with namespace
permission:

```bash
python experiments/audit_002/reproduce.py --output /tmp/audit002-new-run.json
```

Optional report/figure generation requires packages listed in
`requirements-report.txt`; see [validation details](research/validation.md).
CI builds and checks a fresh snapshot via
[research-checks.yml](.github/workflows/research-checks.yml). A passing
check supports software reproducibility of the tested artifacts; it is not
independent human verification or a finding about agent deception.

**Historical release note:** the checked-in `RELEASE_MANIFEST.json`
captures the earlier frozen release and is intentionally not rewritten when
the README changes. Passing `python scripts/verify_release.py` against
a later working tree is therefore *not* the expected workflow. Build a new
snapshot as above, which receives its own manifest.

## Follow-up study: proposed, not run

[AUDIT-003](research/protocols/audit_003_proposed.md) proposes a paired
evaluation in disposable coding-agent environments: hold independently
verified agent behavior fixed while varying which tool events, arguments
and results a monitor can see. It defines `CLEAR`, `VIOLATION` and
`ABSTAIN` outcomes; separate false-positive and unsafe-clearance rates;
negative controls; and falsification criteria.

There are **no AUDIT-003 agent trials or monitoring results** in this repo.
Treat the document as a research plan, not a result or benchmark.

## Repository map

| Path | Contents |
| --- | --- |
| `data/pilot_001/` | All 15 path-redacted saved trace fragments |
| `experiments/pilot_001/` | Original task scripts, instrumentation and snapshots |
| `experiments/audit_001/` | Retrospective analysis and controlled execution |
| `experiments/audit_002/` | Frozen validator and separate local counterexample |
| `results/` | Saved figures, evidence tables, replay and control observations |
| `src/mats_neel/audit.py` | Core deterministic audit implementation |
| `tests/` | Core research-code checks |
| `report/` | Executive summary, full manuscript and generated formats |
| `research/` | Protocols, alternative explanations, provenance and contribution records |

## Documentation and data use

For publication boundaries and third-party material, see
[publication guidance](PUBLICATION.md) and
[data attribution](THIRD_PARTY_DATA.md).
Research protocols, verification records, and contribution documentation
are maintained in [`research/`](research/).
