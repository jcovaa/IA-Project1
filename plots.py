import csv
import os
import matplotlib.pyplot as plt
import numpy as np

# ─── Config ───────────────────────────────────────────────────────────────────

DOC_DIR      = "doc"
OUTPUT_DIR   = "plots"
DIFFICULTIES = ["easy", "medium", "hard"]

DIFF_COLORS = {
    "easy":   "#59a14f",
    "medium": "#edc948",
    "hard":   "#e15759",
}

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_avg_csv(difficulty, doc_dir=DOC_DIR):
    path = os.path.join(doc_dir, f"benchmark_{difficulty}_avg.csv")
    if not os.path.exists(path):
        print(f"  [!] File not found: {path}")
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

def get_algos(all_data):
    seen = {}
    for diff in DIFFICULTIES:
        for row in all_data.get(diff, []):
            seen.setdefault(row["algorithm"], None)
    return list(seen.keys())

# ─── Style ────────────────────────────────────────────────────────────────────

plt.rcParams.update({
    "figure.facecolor": "#0f1117",
    "axes.facecolor":   "#1a1d27",
    "axes.edgecolor":   "#3a3d4d",
    "axes.labelcolor":  "#c8ccd8",
    "axes.titlecolor":  "#e8eaf0",
    "xtick.color":      "#8a8fa8",
    "ytick.color":      "#8a8fa8",
    "grid.color":       "#2a2d3d",
    "grid.linewidth":   0.6,
    "text.color":       "#c8ccd8",
    "font.family":      "monospace",
    "axes.spines.top":  False,
    "axes.spines.right":False,
})

# ─── Grouped bar chart (1 metric, 3 difficulties) ─────────────────────────────

def plot_grouped(all_data, metric, title, ylabel, filename):
    algos   = get_algos(all_data)
    n       = len(algos)
    width   = 0.25
    x       = np.arange(n)

    fig, ax = plt.subplots(figsize=(max(16, n * 0.52), 6))

    for i, diff in enumerate(DIFFICULTIES):
        rows   = all_data.get(diff, [])
        lookup = {r["algorithm"]: safe_float(r.get(metric)) for r in rows}
        vals   = [lookup.get(a) or 0 for a in algos]
        offset = x + (i - 1) * width

        bars = ax.bar(offset, vals, width=width,
                      color=DIFF_COLORS[diff], label=diff.capitalize(),
                      zorder=2, alpha=0.88)

        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() * 1.013,
                        f"{val:.3g}",
                        ha="center", va="bottom",
                        fontsize=5, color="#c8ccd8", rotation=90)

    ax.set_xticks(x)
    ax.set_xticklabels(algos, rotation=45, ha="right", fontsize=7.5)
    ax.set_ylabel(ylabel, fontsize=11)
    ax.set_title(title, fontsize=13, pad=14, fontweight="bold")
    ax.yaxis.grid(True, zorder=0, linestyle="--", alpha=0.45)
    ax.set_axisbelow(True)
    ax.legend(fontsize=9, framealpha=0.25,
              facecolor="#1a1d27", edgecolor="#3a3d4d", loc="upper right")

    fig.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, filename)
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  -> {out}")

# ─── Chart 4: Steps (solid) + Cost (hatched) ──────────────────────────────────

def plot_steps_and_cost(all_data):
    algos  = get_algos(all_data)
    n      = len(algos)
    width  = 0.13
    x      = np.arange(n)

    # 6 bars per group: steps_easy, cost_easy, steps_med, cost_med, steps_hard, cost_hard
    series = [(diff, metric, hatched)
              for diff in DIFFICULTIES
              for metric, hatched in [("avg_solution_steps", False),
                                      ("avg_solution_cost",  True)]]

    fig, ax = plt.subplots(figsize=(max(18, n * 0.65), 6))

    for i, (diff, metric, hatched) in enumerate(series):
        rows   = all_data.get(diff, [])
        lookup = {r["algorithm"]: safe_float(r.get(metric)) for r in rows}
        vals   = [lookup.get(a) or 0 for a in algos]
        offset = x + (i - 2.5) * width

        label = f"{diff.capitalize()} {'Cost' if hatched else 'Steps'}"
        bars  = ax.bar(offset, vals, width=width,
                       color=DIFF_COLORS[diff],
                       hatch="//" if hatched else "",
                       label=label, zorder=2,
                       alpha=0.55 if hatched else 0.88,
                       edgecolor=DIFF_COLORS[diff] if hatched else "#0f1117")

        for bar, val in zip(bars, vals):
            if val > 0:
                ax.text(bar.get_x() + bar.get_width() / 2,
                        bar.get_height() * 1.013,
                        f"{val:.3g}",
                        ha="center", va="bottom",
                        fontsize=4.5, color="#c8ccd8", rotation=90)

    ax.set_xticks(x)
    ax.set_xticklabels(algos, rotation=45, ha="right", fontsize=7.5)
    ax.set_ylabel("Average Steps / Cost", fontsize=11)
    ax.set_title("Solution Steps & Cost by Algorithm",
                 fontsize=13, pad=14, fontweight="bold")
    ax.yaxis.grid(True, zorder=0, linestyle="--", alpha=0.45)
    ax.set_axisbelow(True)
    ax.legend(fontsize=8, framealpha=0.25, facecolor="#1a1d27",
              edgecolor="#3a3d4d", loc="upper right", ncol=2)

    fig.tight_layout()
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    out = os.path.join(OUTPUT_DIR, "chart_steps_cost.png")
    fig.savefig(out, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  -> {out}")

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    all_data = {diff: load_avg_csv(diff) for diff in DIFFICULTIES}

    plot_grouped(all_data,
                 "avg_time_s",
                 "Execution Time by Algorithm",
                 "Average Time (s)",
                 "chart_time.png")

    plot_grouped(all_data,
                 "avg_memory_kb",
                 "Memory Usage by Algorithm",
                 "Average Memory (KB)",
                 "chart_memory.png")

    plot_grouped(all_data,
                 "avg_states_visited",
                 "States Visited by Algorithm",
                 "Average States Visited",
                 "chart_states.png")

    plot_steps_and_cost(all_data)

    print(f"\nDone! 4 charts saved to '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()