# Targeted related-work check

Checked September 9 local time / September 10 UTC, 2026. Primary sources only.
This is not an exhaustive review. Historical discovery claims are not adopted
without verification in the current report.

| Source | What was read | Relevance and boundary |
|---|---|---|
| [Singh et al., Model Forensics](https://arxiv.org/html/2606.26071v2) | Protocol, environment design, limitations | Guides benign alternatives and interventions. The current evidence does not establish motivation. |
| [Najt et al., SLEIGHT-Bench](https://alignment.anthropic.com/2026/sleight-bench/) | Authors' methods/results article | Studies blind spots with paired harmful/benign cases; evidence availability is a prerequisite, not monitor quality. |
| [Rajan et al., Where Facts Go Missing, v3](https://arxiv.org/html/2607.22448v3) | Abstract, taxonomy, deterministic-audit method, limitations | Direct prior work separating software omission from behavioral loss. That general decomposition is not new here. |
| [Kale et al., Reliable Weak-to-Strong Monitoring](https://arxiv.org/abs/2508.19461) | Abstract | Prior work on scaffolding and awareness, not a replication target for this pilot. |
| [Baumann et al., SWE-chat](https://arxiv.org/abs/2604.20779) | Abstract and [dataset card](https://huggingface.co/datasets/SALT-NLP/SWE-chat/blob/main/README.md) | Source of one selected motivating case, not representative evidence. Dataset card lists ODC-BY. |
| [GNU Coreutils: truncate](https://www.gnu.org/s/coreutils/manual/html_node/truncate-invocation.html) | Command semantics | Describes sparse holes; our local validator counterexample was independently executed. |

Searches covered model forensics, monitoring blind spots, omitted tool calls,
working-directory context, and information loss across compression pipelines.
Related work already covers much of the broad idea. No first-of-its-kind or
state-of-the-art claim is made. The retained question is whether the existing
experiment licenses its proposed behavioral conclusions.
