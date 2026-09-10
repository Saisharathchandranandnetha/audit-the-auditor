"""Generate standalone figures from AUDIT-001 tables; no model execution."""
from pathlib import Path
import csv
import json
import os

os.environ.setdefault("MPLCONFIGDIR", "/tmp/mats-audit-matplotlib")
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parents[2]
RESULTS = ROOT / "results/audit_001"
FIGURES = RESULTS / "figures"


def main():
    FIGURES.mkdir(parents=True, exist_ok=True)
    plt.rcParams.update({"font.size": 10, "axes.spines.top": False, "axes.spines.right": False, "svg.fonttype": "none"})
    capture = list(csv.DictReader((RESULTS / "capture.csv").open()))
    views = ["legacy_command_text", "structured_commands", "all_tool_calls"]
    labels = ["Command text only\n(original extractor)", "Commands with\narguments", "All tool calls\nwith arguments"]
    fig, axes = plt.subplots(1, 2, figsize=(10, 4), layout="constrained")
    for ax, key, denominator, title in zip(axes,
        ["guard_edit_available", "outside_cwd_available"], [5, 9],
        ["Confirmed guard-edit evidence", "Outside-directory invocation evidence"]):
        values = [sum(int(r[key]) for r in capture if r["view"] == view) for view in views]
        ax.bar(range(3), values, color=["#ba4d40", "#d79435", "#267a70"], width=.6)
        ax.set_xticks(range(3), labels)
        ax.set_ylim(0, denominator * 1.25)
        ax.set_yticks(range(denominator + 1))
        ax.set_ylabel("Evidence-bearing events available")
        ax.set_title(title)
        for i, value in enumerate(values):
            ax.text(i, value + denominator * .035, f"{value}/{denominator}", ha="center")
    fig.suptitle("Evidence disappears before compression", fontsize=15)
    for ext in ("png", "pdf", "svg"):
        fig.savefig(FIGURES / f"capture.{ext}", dpi=180)
    plt.close(fig)

    table = list(csv.DictReader((RESULTS / "compression_summary.csv").open()))
    fig, axes = plt.subplots(1, 2, figsize=(10, 4.2), layout="constrained")
    for ax, key, denominator, title in zip(axes,
        ["guard_edit_retained_mean", "outside_cwd_retained_mean"], [5, 9],
        ["Guard edits (5 events)", "Outside-directory invocations (9 events)"]):
        for policy, label, color in [("head_tail", "Head/tail", "#ba4d40"), ("tail", "Tail", "#267a70"), ("random", "Random order (100 seeds)", "#586f9b")]:
            rows = [r for r in table if r["view"] == "all_tool_calls" and r["policy"] == policy and r["budget_setting"] != "4096_bytes"]
            ax.plot([int(r["budget_setting"]) for r in rows], [100 * float(r[key]) / denominator for r in rows], marker="o", label=label, color=color)
        ax.set(xlabel="Budget (% of full tool-call UTF-8 bytes)", ylabel="Evidence retained (%)", title=title, ylim=(-3, 106))
        ax.set_xticks([10, 25, 50, 75, 100])
        ax.grid(alpha=.2)
    axes[1].legend(loc="upper left", fontsize=8)
    fig.suptitle("Replay sensitivity: selection policy changes what survives", fontsize=14)
    for ext in ("png", "pdf", "svg"):
        fig.savefig(FIGURES / f"compression.{ext}", dpi=180)
    plt.close(fig)
    print(f"Figures written to {FIGURES}")


if __name__ == "__main__":
    main()
