# Audit the Auditor: A Coding-Agent Monitoring Audit

## Executive summary

**Question.** Does this monitoring experiment record the actions and check the
outcomes needed to test whether an agent evades oversight?

The project started from an apparently concerning coding-agent episode and
moved to a 15-run pilot: would agents pad their execution histories when told
that a monitor sees only a compressed summary? A retrospective audit found that
the pilot cannot answer this question. Its command-only extractor omits
non-shell edits and working-directory arguments, and all saved runs end before
the result of their final tool call. The audit identifies where evidence is lost and tests ways the task can
appear to succeed without processing data.

**What was done.** All 15 available pilot exports were preserved, with hashes to check
that their contents have not changed. The audit extracted all tool calls, checked edit requests against tool
result diffs and saved files, and compared command text, commands with arguments,
and all tools with arguments. It replayed event-selection policies under matched
byte budgets. Three local program controls tested the pilot's script without
new model calls. This is a retrospective case study, not a preregistered or
representative benchmark. The exact pilot model and sampling settings could not
be recovered from the saved exports. Two further controls tested the storage constraint in a proposed replacement
task. That replacement was never run as an agent experiment.

**Main findings.**

- **The old extractor retained 17 of 54 tool calls and omitted all five
  confirmed script edits.** Each edit removed the script's backup-presence
  check. Edit requests, tool-result diffs, and saved scripts agree. The edits
  used `replace_file_content`, which the extractor ignored.
- **It also removed working-directory evidence for nine script invocations
  across seven runs.** Local controls show why this matters: the same command
  returns failure in the task directory and success from another directory.
  The protected backup stays unchanged.
- **The success message did not measure data processing.** The original
  script only checks file existence and prints a message. Changing the working
  directory or removing the guard produces its success message without creating
  processed data in the local controls.
- **The proposed repair also has a false-success route.** Its validator accepts
  a 30 MiB sparse file occupying zero data blocks, with the backup unchanged.
  A dense write hits the actual quota. This shows that passing the implemented check does not require
  destroying the backup. It is a
  researcher-written control, not a strategy observed in an agent.

**Strongest counterevidence and limits.** The prompt protects the backup file,
not the processing script. Editing the script may satisfy a literal reading of
the task. No final answers or final tool results are available for any of the
15 runs, so neither task completion nor failure concealment can be scored.
The histories are short: all structured tool calls fit within 4 KiB per run,
so the fractional-budget result does not establish practical context pressure.
No actual LLM monitor was evaluated. Restoring evidence does not show that a
monitor would interpret it correctly.

**Conclusion.** The original adaptive-evasion hypothesis remains unresolved.
This pilot loses relevant evidence before compression, lacks complete outcomes,
and its proposed replacement validator mistakes file length for task success.
A follow-up needs to record every tool call and result, state which actions
are allowed, verify the output independently, and run an actual monitor.

**Authorship and time.** The applicant reported 16 hours before this continuation.
The continuation's analysis, code, and prose were produced with substantial
coding-assistant help. The applicant must review the evidence and reconcile
the final time total. This summary does not claim that the applicant
independently discovered the assistant's corrections.
