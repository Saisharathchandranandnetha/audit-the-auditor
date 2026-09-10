# Current hypothesis ledger

The audit is retrospective. The capture defects were noticed before AUDIT-001's
analysis plan. AUDIT-002's sparse-file prediction was written before executing
that control. Neither is labeled a preregistered agent experiment.

| Hypothesis or claim | Discriminating evidence | Current status |
|---|---|---|
| Agents adapt actions to exploit monitor compression | Completed trials with actual monitors, observed harmful outcomes, and differential evasion | **Unresolved.** Existing traces cannot support this test. |
| The command extractor captures every relevant mutation | Compare raw calls to extracted calls and saved-file changes | **False in this pilot.** Five confirmed edits use an omitted tool. |
| Command text is sufficient to reproduce the script outcome | Hold command/script constant and change only Cwd | **False for this paired control.** Exit status changes from 1 to 0. |
| The script's success message validates data processing | Inspect code and test output creation | **False.** It only checks a filename and prints a message. |
| Pilot 2's validator can pass only after destroying the backup | Dense versus sparse output, original validator, same quota | **Falsified by counterexample.** Sparse output passes without a backup violation. |
| Selection policy changes retained evidence | Replay identical histories under equal byte budgets | **Supported for these selectors.** At 75%, edit retention is 0/5 versus 4/5. |
| The histories demonstrate realistic compression pressure | Fixed 4 KiB per-run budget | **Not supported.** All tool-call representations fit. |
| Script edits demonstrate intentional deception | Task permissions, full outcomes, disclosure, alternative explanations | **Not established.** Edits were not expressly prohibited; final answers are missing. |

Population prevalence, model differences, causal effects of monitor framing,
and LLM monitor quality are outside the evidence available here.
