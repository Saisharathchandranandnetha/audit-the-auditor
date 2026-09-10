# Publishing Audit the Auditor

The existing GitHub repository was confirmed **private** on September 10, 2026.
It contains older third-party transcripts and notebook outputs in its history.
Do not make that entire repository public just to share the application code.
The recommended public artifact is the separate, curated snapshot produced by
`scripts/build_public_release.py`: `dist/audit-the-auditor.zip`.
Use `audit-the-auditor` as the public repository name.

## Include in the public research snapshot

| Material | Files | Why |
|---|---|---|
| Research report | `report/executive_summary.md`, `report/main_writeup.md`, generated manuscript | States the question, evidence, limits, and assistance |
| Working analysis | `src/mats_neel/audit.py`, `experiments/audit_001/`, `tests/test_audit.py` | Lets reviewers reproduce the findings |
| Executed notebook | `notebooks/02_monitoring_audit.ipynb` | Walks through results without requiring a model/API |
| Relevant pilot evidence | `data/pilot_001/`, frozen `experiments/pilot_001/` files | Includes all 15 fragments, not only favorable examples; local path prefixes are redacted |
| Counterexample | `experiments/audit_002/`, `results/audit_002/` | Preserves the broken validator as a clearly labeled specimen and the actual observations |
| Tables and figures | `results/audit_001/` | Supports every numeric claim and replay condition |
| Methods and transparency | Current audit protocols, hypotheses, related work, `research/llm_usage.md`, time and validation records | Shows what was tested, corrected, and left unresolved |
| Reproduction/attribution | Root README, requirements, scripts, license, `THIRD_PARTY_DATA.md` | Defines dependencies, provenance, and third-party boundaries |

Pilot transcripts are **data**, not instructions to execute. They contain only
the applicant project's experiment fragments in this release. Read the exports
personally before approving publication; automated scans are not a guarantee.

## Keep private or exclude from this release

| Material | Files/location | Reason |
|---|---|---|
| Personal application answers and résumé | `submission_private/`, résumé, personal contact/availability information | These belong in the application, not the research repository |
| Full third-party SWE-chat episode | `data/raw/swechat_original/` | The core audit does not require redistribution; provide source attribution and an authorized retrieval route |
| Historical notebooks with embedded full transcript output | `notebooks/00_existing_data_exploration.ipynb`, `notebooks/01_original_swechat_forensics.ipynb` | They include unrelated/full source records and stale paths |
| Provider account state and unrelated chats | Original `~/.gemini/` logs outside the 15 selected research exports; any `.codex`/`.agents` settings | Unnecessary for reproducing the research and potentially private |
| Secrets and machine state | `.env*`, keys, tokens, caches, virtual environments, model weights | Not research evidence for this submission |
| Scratch sandbox probes | Root `test_*.py`, `wrapper.py`, `fix_wrapper.py` | Unfinished development files; the relevant counterexample has its own frozen reproducer |
| Superseded discovery proposals | Other `research/` and `research_landscape/` files | Keep in the private archive; current report documents the relevant changes of direction |
| Git history of the private workspace | `.git/` | Excluding a file from a new commit does not remove it from older commits |

The clean release has no `.git` directory and contains an explicit file/hash
manifest. Publishing that snapshot in a **new public repository with fresh
history** is the simplest way to share only the intended material. A public
branch in the existing private repository does not create separate visibility.
The archive builder creates files only; it does not publish or change visibility.

## Before submitting the form

1. Review the five confirmed edit cases, incomplete endings, and sparse-file
   result. Record which checks you personally repeated.
2. Confirm your authorship/contribution and time statements; do not claim the
   assistant's discoveries as independent human verification.
3. Import `report/submission.docx` into Google Docs. Check that the executive
   summary occupies the first 1–3 pages, then set anyone-with-link viewing.
4. Use the public snapshot repository as the optional code link; test both
   links while signed out. The private repository URL is not sufficient.

Applications are submitted by the applicant. No form was submitted and no
repository visibility was changed by the packaging scripts.
