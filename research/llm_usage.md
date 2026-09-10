# AI assistance and verification record

This records the continuation; it does not claim the applicant personally
performed the assistant's checks. Earlier use of agents must be described by
the applicant before submission.

## Who did what

- The applicant supplied the project and requirements, requested completion,
  and reported approximately 16 hours of prior hands-on work.
- The coding assistant inspected code and traces, searched primary literature,
  proposed the audit, wrote its analysis, tests, figures, notebook, and report,
  and ran the local controls.
- No new model-under-test generations or paid API calls occurred during this
  continuation. The earlier pilot model could not be identified from the
  exports. The analysis assistant is not the pilot model.
- The report and draft research-form answers were initially assistant-written.
  Applicant review/editing is **not yet attested**. Do not claim independent
  human verification until it has happened.

## Specific mistakes and corrections

1. **Apparent benchmark gaming:** the SWE-chat agent created and then deleted
   the same new test. Benign rollback remains a viable explanation.
2. **Lost tool channel:** the original extractor retained only `run_command`.
   Five edits used `replace_file_content`. Requests were checked against
   confirming diffs and saved files.
3. **Lost execution argument:** Cwd was discarded. Local controls held command
   and script fixed and changed only Cwd; exit status changed.
4. **Incomplete endings:** all 15 exports end with tool requests. Task success
   is now null, not inferred from a planner's DONE status or missing later acts.
5. **Planned versus executed monitoring:** no run reaches the original
   compressor's >5-command threshold. Mock tests are not real-monitor results.
6. **False physical dilemma:** the proposed validator checks output length.
   A predicted sparse-file control passes with the backup intact; a dense
   control fails at the quota. Original code and observations are preserved.
7. **Diagnostic command masks exit status:** the first local check appended
   `stat`, so the shell returned its status. The recorded reproducer now saves
   the writer's exit status immediately and returns it after diagnostics.
8. **Overstating completeness scores:** recovering every included event is
   not a classifier achievement. A fixed 4 KiB control showed no practical
   compression need for these short tool-call histories.

## Verification and its limits

Source hashes, all runs, field-level evidence, byte-budget tests, negative
examples, and local execution controls are supplied. All five edits and nine
outside-directory requests were inspected. A reproducible random sample includes
an almost-empty run and an interrupted run.

These are assistant-executed checks, not independent human review. The applicant
should inspect B1's edit/diff, A3's Cwd, A2's missing outcome, the paired script
controls, and the sparse-file result, then record what they personally repeated.

## Applicant contribution — outstanding

Before submitting, describe the first 16 hours: which questions and experiments
the applicant chose, code they wrote/reviewed, agent mistakes they caught, and
what they learned. No personal credentials or verification claims were invented.
