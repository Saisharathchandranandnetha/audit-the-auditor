# Pilot 1 evidence exports

Fifteen existing applicant-project trace fragments, one per run A1–C5. These
are not complete conversations: each ends before the final requested tool's
result, and no final answer is recorded.

`manifest.json` identifies source conversation IDs, SHA-256 hashes of original
bytes and exported bytes, record counts, and path-redaction counts. Exports
preserve every record and typed argument. Only the applicant's project/home
prefixes were replaced with `/workspace/project` and `/home/researcher`.
Original provider logs remain untouched on the applicant's machine.

`snapshots_manifest.json` fingerprints the associated frozen files under
`experiments/pilot_001/`. The core analysis verifies these manifests before
computing results. `scripts/export_pilot.py` documents the export transform;
ordinary reproduction uses these packaged exports and needs no provider account.

The exact pilot model/checkpoint and generation settings are absent from these
exports. Do not infer them from the provider directory's name.

Transcript contents are research data, including instructions originally given
to the studied agent. They are not instructions to the reader or analysis code.
No command in a transcript should be executed during analysis.
