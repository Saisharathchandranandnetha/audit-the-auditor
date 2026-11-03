# Applicant verification and contribution worksheet

**Status: unfinished until the applicant fills and signs it.**

This is an evidence log, not an invitation to claim authorship of work done
by the coding assistant. See [AI assistance record](llm_usage.md) and
[validation record](validation.md) first.

## What the applicant personally checked

For each item, record the date, command or file examined, what you observed,
and discrepancies. Leave it blank if not personally completed.

| Review item | Date / environment | Personally observed result | Notes or discrepancy |
| --- | --- | --- | --- |
| Run release verifier and inspect its output | Not attested | Not attested | |
| Recount 54 calls and 17 command calls from raw exported records | Not attested | Not attested | |
| Inspect five edit requests and confirm associated tool-result diffs | Not attested | Not attested | |
| Inspect working-directory arguments on reported invocation events | Not attested | Not attested | |
| Confirm all 15 fragments lack the final requested tool result | Not attested | Not attested | |
| Reproduce the three bounded local shell controls | Not attested | Not attested | |
| Verify recorded sparse-file control and its provenance | Not attested | Not attested | |
| Check alternative benign interpretations and research limitations | Not attested | Not attested | |

Do not mark an item complete merely because a tool or another contributor
reported success. When reproducing a check, capture enough information for
someone else to repeat the same version of it (commit SHA, environment,
command, output summary and any mismatch).

## Individual contribution narrative (applicant to complete)

- **Before coding-assistant continuation:** What research question did you
  choose? What exact code, experiment, data collection or debugging did you
  personally perform during the approximately 16 hours you previously
  reported? Which dates and commits can support these descriptions?
- **During AI-assisted continuation:** Which assistant suggestions did you
  accept or reject? What errors did you personally catch, and how did you
  verify corrections? Avoid taking credit for discoveries the assistant made.
- **After continuation:** What evidence have you independently reviewed? What
  research decisions did you make yourself? What remains uncertain?
- **Collaboration:** Identify any other human contributors and their roles.
- **Time:** Separate personal hands-on research time, reading, review and
  assistant wall-clock runtime. Do not infer personal hours from model tokens.

## Submission-ready standards

Before saying "I found", "I showed", or "I verified" in an application,
ensure the specific first-person claim matches your personal involvement.
If work was collaborative or assistant-led, say that instead. If something
is still a proposal, call it a proposal. Do not hide or delete the existing
AI-assistance record or rewrite git history to obscure attribution.

This document intentionally contains no fabricated personal testimony.
