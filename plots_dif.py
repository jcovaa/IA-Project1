import csv
import os
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

# ─── Config ───────────────────────────────────────────────────────────────────

DOC_DIR      = "doc"
OUTPUT_DIR   = "plots"
DIFFICULTIES = ["easy", "medium", "hard"]

# 4 charts — the 4th overlays solution_steps (bars) + solution_cost (line)
CHARTS = [
    {
        "key":   "avg_time_s",
        "label": "Average Time (s)",
        "fname": "time_s",
    },
    {
        "key":   "avg_memory_kb",
        "label": "Average Memory (KB)",
        "fname": "memory_kb",
    },
    {
        "key":   "avg_states_visited",
        "label": "States Visited (avg)",
        "fname": "states_visited",
    },
    {
        "key":    "avg_solution_steps",
        "key2":   "avg_solution_cost",
        "label":  "Solution Steps (avg)",
        "label2": "Solution Cost (avg)",
        "fname":  "steps_cost",
    },
]

# Family colours for bar colouring
FAMILIES = {
    "BFS":    "#4e79a7",
    "DFS":    "#f28e2b",
    "DLS":    "#e15759",
    "IDS":    "#76b7b2",
    "UCS":    "#59a14f",
    "Greedy": "#edc948",
    "A*":     "#b07aa1",
    "WA*":    "#ff9da7",
    "IDA*":   "#9c755f",
}

def family_color(name):
    for prefix, color in FAMILIES.items():
        if name.startswith(prefix):
            return color
    return "#aaaaaa"

# ─── Helpers ──────────────────────────────────────────────────────────────────

def load_avg_csv(difficulty):
    path = os.path.join(DOC_DIR, f"benchmark_{difficulty}_avg.csv")
    if not os.path.exists(path):
        print(f"  [!] Not found: {path}")
        return []
    with open(path, newline="") as f:
        return list(csv.DictReader(f))

def safe_float(val):
    try:
        return float(val)
    except (TypeError, ValueError):
        return None

# ─── Global dark style ────────────────────────────────────────────────────────

plt.rcParams.update({
    "figure.facecolor":  "#0f1117",
    "axes.facecolor":    "#1a1d27",
    "axes.edgecolor":    "#3a3d4d",
    "axes.labelcolor":   "#c8ccd8",
    "axes.titlecolor":   "#e8eaf0",
    "xtick.color":       "#8a8fa8",
    "ytick.color":       "#8a8fa8",
    "grid.color":        "#2a2d3d",
    "grid.linewidth":    0.6,
    "text.color":        "#c8ccd8",
    "font.family":       "monospace",
    "axes.spines.top":   False,
    "axes.spines.right": False,
})

# ─── Chart helpers ────────────────────────────────────────────────────────────

def _save(fig, difficulty, fname):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, f"{difficulty}_{fname}.png")
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"  -> {path}")

# ─── Chart 1-3: single metric bar chart ───────────────────────────────────────

def plot_bar(rows, chart, difficulty):
    algos  = [r["algorithm"] for r in rows]
    values = [safe_float(r.get(chart["key"])) for r in rows]
    colors = [family_color(a) for a in algos]

    data = [(a, v, c) for a, v, c in zip(algos, values, colors) if v is not None]
    if not data:
        return
    algos, values, colors = zip(*data)

    fig, ax = plt.subplots(figsize=(max(13, len(algos) * 0.45), 5))
    x    = np.arange(len(algos))
    bars = ax.bar(x, values, color=colors, width=0.72, zorder=2)

    ax.set_xticks(x)
    ax.set_xticklabels(algos, rotation=45, ha="right", fontsize=7.5)
    ax.set_ylabel(chart["label"], fontsize=10)
    ax.set_title(f"{chart['label']}  —  {difficulty.capitalize()}", fontsize=12, pad=12)
    ax.yaxis.grid(True, zorder=0)
    ax.set_axisbelow(True)

    for bar, val in zip(bars, values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() * 1.012,
                f"{val:.3g}",
                ha="center", va="bottom", fontsize=6, color="#c8ccd8")

    # Family legend
    seen = {}
    for a, c in zip(algos, colors):
        fam = next((k for k in FAMILIES if a.startswith(k)), "Other")
        seen[fam] = c
    patches = [mpatches.Patch(color=c, label=f) for f, c in seen.items()]
    ax.legend(handles=patches, fontsize=7, loc="upper right",
              framealpha=0.3, facecolor="#1a1d27", edgecolor="#3a3d4d")

    fig.tight_layout()
    _save(fig, difficulty, chart["fname"])

# ─── Chart 4: steps (bars) + cost (line overlay) ─────────────────────────────

def plot_steps_cost(rows, chart, difficulty):
    algos  = [r["algorithm"] for r in rows]
    steps  = [safe_float(r.get(chart["key"]))  for r in rows]
    costs  = [safe_float(r.get(chart["key2"])) for r in rows]
    colors = [family_color(a) for a in algos]

    data = [(a, s, c, co)
            for a, s, c, co in zip(algos, steps, colors, costs)
            if s is not None]
    if not data:
        return
    algos, steps, colors, costs = zip(*data)

    fig, ax1 = plt.subplots(figsize=(max(13, len(algos) * 0.45), 5))
    x = np.arange(len(algos))

    # Bars = solution steps
    bars = ax1.bar(x, steps, color=colors, width=0.72, zorder=2, alpha=0.85)
    ax1.set_xticks(x)
    ax1.set_xticklabels(algos, rotation=45, ha="right", fontsize=7.5)
    ax1.set_ylabel(chart["label"], fontsize=10, color="#e15759")
    ax1.tick_params(axis="y", labelcolor="#e15759")
    ax1.yaxis.grid(True, zorder=0, alpha=0.4)
    ax1.set_axisbelow(True)

    for bar, val in zip(bars, steps):
        ax1.text(bar.get_x() + bar.get_width() / 2,
                 bar.get_height() * 1.012,
                 f"{val:.3g}",
                 ha="center", va="bottom", fontsize=6, color="#c8ccd8")

    # Line = solution cost (right axis)
    ax2 = ax1.twinx()
    ax2.set_facecolor("none")
    cost_vals = [c if c is not None else np.nan for c in costs]
    ax2.plot(x, cost_vals, color="#edc948", linewidth=1.8,
             marker="D", markersize=4, zorder=3)
    ax2.set_ylabel(chart["label2"], fontsize=10, color="#edc948")
    ax2.tick_params(axis="y", labelcolor="#edc948")
    ax2.spines["right"].set_visible(True)
    ax2.spines["right"].set_color("#3a3d4d")

    ax1.set_title(f"Solution Steps & Cost  —  {difficulty.capitalize()}",
                  fontsize=12, pad=12)

    # Legend
    seen = {}
    for a, c in zip(algos, colors):
        fam = next((k for k in FAMILIES if a.startswith(k)), "Other")
        seen[fam] = c
    patches = [mpatches.Patch(color=c, label=f) for f, c in seen.items()]
    cost_patch = mpatches.Patch(color="#edc948", label="Solution Cost (line)")
    ax1.legend(handles=patches + [cost_patch], fontsize=7, loc="upper right",
               framealpha=0.3, facecolor="#1a1d27", edgecolor="#3a3d4d")

    fig.tight_layout()
    _save(fig, difficulty, chart["fname"])

# ─── Main ─────────────────────────────────────────────────────────────────────

def main():
    for diff in DIFFICULTIES:
        print(f"\n[{diff.upper()}]")
        rows = load_avg_csv(diff)
        if not rows:
            continue
        for chart in CHARTS:
            if "key2" in chart:
                plot_steps_cost(rows, chart, diff)
            else:
                plot_bar(rows, chart, diff)

    print(f"\nDone! 12 charts saved to '{OUTPUT_DIR}/'")

if __name__ == "__main__":
    main()