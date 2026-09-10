# Snapshot boundaries

`scripts/build_public_release.py` uses a positive allowlist. The release is a
fresh directory/ZIP, not a git checkout; private history is not copied.
`RELEASE_MANIFEST.json` records SHA-256 hashes for every included file.

All 15 pilot fragments and the frozen artifacts needed by their manifest are
included. No trial is omitted because of its behavior or short length. The full
SWE-chat motivating episode is excluded; it is not used to compute the headline
audit counts. Personal application answers, provider account state, local
scratch code, and superseded proposals are excluded.

`scripts/verify_release.py` runs against the snapshot itself and checks its
manifest, core tests, exact deterministic reproduction, notebook completion,
and forbidden-file boundaries. Pattern scans supplement these checks but do
not establish that every possible private detail has been removed.
