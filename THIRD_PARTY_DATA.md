# Third-party data and attribution

The software license in `LICENSE` applies to project-authored code. It does not
relicense third-party transcripts or source snippets.

The original motivating episode comes from
[SALT-NLP/SWE-chat](https://huggingface.co/datasets/SALT-NLP/SWE-chat), described
by Baumann et al., [SWE-chat: Coding Agent Interactions From Real Users in the
Wild](https://arxiv.org/abs/2604.20779). Its dataset card lists the
[Open Data Commons Attribution License](https://opendatacommons.org/licenses/by/1-0/).
Original repository content retains its applicable underlying license.

The local historical transcript is identified by session
`f1a73ca3-8465-45b0-a8f3-7e924af08f5c`. Provenance is recorded in
`data/raw/swechat_original/*_metadata.json`. It was already tracked in the
repository before this continuation. The prepared public release excludes that
full transcript, its extracted full-text log, and historical notebooks with
embedded transcript contents. Authorized readers can obtain it from SWE-chat.

The core AUDIT-001 results use only the applicant's 15 pilot records, not the
third-party transcript. The public release includes their path-redacted exports
and the associated task scripts. All quoted third-party episode details in the
report are attributed and limited to what is needed to explain the motivating
case. The report does not claim ownership of the underlying developer's work.
