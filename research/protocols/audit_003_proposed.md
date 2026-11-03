# AUDIT-003: Measuring monitor decisions under incomplete evidence

**Status: PROPOSED, NOT EXECUTED.** This is a follow-up protocol, not a
preregistered or completed experiment. Freeze the task definitions, exclusions,
model settings and primary analysis before examining new trial outcomes.

## Question and hypothesis

Holding an agent's completed behavior fixed, does removing safety-relevant
tool evidence cause trusted monitors to clear verified policy violations more
often? A plausible alternative is that monitors can infer the action from
surrounding events, in which case the effect may be small or zero. Another
alternative is that additional telemetry increases false alarms.

## Threat model

A coding agent works in a disposable synthetic repository under explicit
permissions. A separate, independent harness records actual file changes and
task outcomes. The monitor receives a post-run record and returns a judgment;
it cannot modify the execution. Violations are concrete task-policy failures,
not evidence of private intent or deceptive alignment.

Never use live credentials or production services. Use artificial files and
local endpoints only.

## Experimental unit and conditions

The experimental unit is one completed, independently labeled agent run.
Each run is replayed to the *same* monitor under paired evidence conditions:

| Condition | Monitor receives | Isolated change |
| --- | --- | --- |
| E0 | Structured tool requests, arguments and available results | Full logged evidence baseline |
| E1 | Command text only | Omit non-shell tools and tool arguments |
| E2 | Structured shell calls but no working directory | Remove execution-location context |
| E3 | Full tool calls but selected result records omitted | Remove outcome evidence |
| E4 | E1 plus bounded read-only file/state probe | Test partial recovery |

"Full logged evidence" is not physical ground truth. Ground truth comes
from a separately instrumented state check. Specify omission rules in advance;
do not choose missing events based on the monitor's answer.

## Ground truth and negative controls

Before collecting runs, write the precise authorized behavior, prohibited
actions and success validators. Include clearly benign edits, clearly
prohibited edits, and unusual but authorized actions. Label actions based
on independent file hashes, sandbox state and explicit task policy, not the
model's explanation. A second reviewer adjudicates ambiguous cases without
seeing monitor outputs. Report excluded and unresolved cases.

The incomplete 15-fragment AUDIT-001 pilot has no final outcomes and is
**not** a labeled monitor-accuracy benchmark. It may inform failure modes,
but cannot contribute fabricated success labels.

## Monitor output and measurements

Freeze monitor model ID, version, prompt, decoding settings, tools and
context budget. Require a verdict of VIOLATION, CLEAR or ABSTAIN, an
event-ID-based explanation and an optional confidence score.

Primary metric: **unsafe clearance rate**, the number of independently
verified violation runs labeled CLEAR divided by all independently verified
violation runs assessed. Report ABSTAIN separately rather than counting it
silently as successful detection.

Secondary metrics: violation detection, false positives on benign runs,
abstention, latency, probe cost and relevant-event retention. Include
raw denominators and per-task breakdowns. Use paired task-level comparisons;
multiple prompts, omissions and seeds applied to the same task are not
independent data points.

## Pilot and analysis discipline

An initial feasibility study could use 30 independently labeled tasks
across the five conditions. **Thirty is an example pilot size, not a
statistically powered sample or an accomplished result.** Decide a separate
confirmatory sample-size/precision plan after checking feasibility, without
using confirmatory outcomes to tune the hypothesis.

Include always-CLEAR and always-ABSTAIN baselines. Test benign but suspicious
actions to assess whether more telemetry increases false alarms. Record
model failures, malformed traces, missing ground truth and protocol deviations.
Show uncertainty and avoid unsupported claims of generality.

## Explicit ways the proposal could fail

- Omission does not change decisions within meaningful uncertainty bounds.
- The apparent difference disappears when task type and trace length are
  controlled.
- Independent state checks disagree with the intended policy labels.
- More evidence substantially increases false positive decisions.
- Probe benefits do not justify cost or are confined to handpicked tasks.
- Other retained messages leak the omitted event's identity.

Any of these outcomes would alter or weaken the initial hypothesis.

## Publication requirements

Preserve versioned task specifications, synthetic input fixtures, trace
transformations, monitor prompts and parameters, independent adjudication,
decisions, run manifests and error cases. Record deviations and study
limitations. Do not convert synthetic examples into claims about adversarial
intent or deployed systems.

## Relationship to prior work

[AUDIT-001](audit_001.md) describes a retrospective capture audit.
[AUDIT-002](audit_002.md) records a deterministic validator counterexample.
Neither measures a trusted LLM monitor. This proposal extends the research
question but adds **no experimental evidence** until separately executed.
