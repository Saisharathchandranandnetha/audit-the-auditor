# Validation record

Checks below were performed by the coding assistant on September 10, 2026.
They establish specific properties of the supplied artifacts, not independent
human review or a positive result about agent deception.

- **Core audit:** 13 standard-library unit tests passed. These cover dropped
  edit channels and Cwd, false-positive controls, evidence confirmation, input
  hash failures, incomplete outcomes, byte limits, and deterministic replay.
- **Working-repository regression subset:** 43 tests passed across the audit,
  channels, compression, instrumentation, and monitor-validation modules.
  Historical mock-monitor tests check plumbing, not real monitor performance.
  The entire legacy repository test suite was not run.
- **Reproduction:** all seven deterministic AUDIT-001 output files were
  regenerated and matched the committed-for-release files byte for byte.
  An independent raw JSON census confirmed 54 calls, 17 command calls, five
  edit calls, and 15 fragments ending in a tool request.
- **Program controls:** the three paired script controls were executed.
  The dense and sparse Bubblewrap controls were separately executed and their
  actual outputs recorded. Release verification checks that recorded evidence
  and the source hashes; it does not rerun Bubblewrap.
- **Notebook:** all eight code cells executed in order without errors. The
  notebook imports the shared analysis and checks its saved results.
- **Manuscript:** DOCX, HTML, and PDF were generated. PDF text extraction showed
  seven pages, with the executive summary on page one and the main report
  starting on page two. The summary page was visually inspected for cropping.
  Google Docs may paginate differently after import.

The public snapshot has its own verification command:

```bash
python scripts/verify_release.py
```

This command passed against a separate 116-file candidate snapshot using the
system Python interpreter, without the working repository's virtual environment.

It checks every manifest hash, publication boundaries and selected secret
patterns, the independent census, the 13 core tests, exact result reproduction,
counterexample provenance, and saved notebook execution. Pattern scanning is
not a comprehensive privacy review. No new agent generations, monitor-model
evaluation, or mechanistic intervention was performed in this continuation.

## Title and release revision

The project was renamed **Audit the Auditor**. The README and summary were
simplified, and the manuscript was regenerated. Notebook changes are limited
to markdown; its executed code and outputs are unchanged. Scientific input
files, analysis code, and recorded result files were not changed for this edit.
The renamed archive is checked again with the same release verifier.
