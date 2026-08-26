"""Generate all figures for the IEEE paper on AGENTS.md instruction file benchmarking."""

import json
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path

# ── Load data ─────────────────────────────────────────────────────────────────
ROOT = Path(r"C:\Users\arsat\OneDrive\Desktop\agents-md-arena")
R1_DIR = ROOT / "results"
R2_DIR = ROOT / "round2" / "results"
FIG = ROOT / "paper" / "figures"
FIG.mkdir(parents=True, exist_ok=True)

VARIANTS = ["none", "concise", "tdd-rigorous", "orchestrator-heavy", "user-proposed"]
SHORT    = ["None", "Concise", "TDD-Rig.", "Orchestr.", "User-Prop."]
TRACKS   = ["A", "B", "C", "D"]
COLORS   = ["#2ecc71", "#3498db", "#e74c3c", "#f39c12", "#9b59b6"]

def load_r1():
    scores, times = {}, {}
    for v in VARIANTS:
        d = R1_DIR / v
        scores[v] = json.loads((d / "score.json").read_text(encoding="utf-8-sig"))["score_pct"]
        times[v]  = json.loads((d / "meta.json").read_text(encoding="utf-8-sig"))["seconds"]
    return scores, times

def load_r2():
    data = {}  # {track: {variant: {score, time, capped}}}
    for t in TRACKS:
        data[t] = {}
        for v in VARIANTS:
            d = R2_DIR / f"{t}-{v}"
            score = json.loads((d / "score.json").read_text(encoding="utf-8-sig"))["score_pct"]
            meta_p = d / "meta.json"
            if meta_p.exists():
                meta = json.loads(meta_p.read_text(encoding="utf-8-sig"))
                time_s = meta.get("seconds", 0)
                capped = meta.get("timed_out", False)
            else:
                time_s = 0
                capped = True
            data[t][v] = {"score": score, "time": time_s, "capped": capped}
    return data

plt.rcParams.update({
    "font.family": "serif",
    "font.size": 9,
    "axes.titlesize": 10,
    "axes.labelsize": 9,
    "xtick.labelsize": 8,
    "ytick.labelsize": 8,
    "legend.fontsize": 7.5,
    "figure.dpi": 300,
    "savefig.bbox": "tight",
    "savefig.pad_inches": 0.05,
})

# ── Figure 1: Benchmark Architecture ──────────────────────────────────────────
def fig1_architecture():
    fig, ax = plt.subplots(figsize=(7, 3.0))
    ax.set_xlim(0, 10); ax.set_ylim(0, 4.2); ax.axis("off")
    ax.set_title("Fig. 1.  Benchmark pipeline architecture", fontsize=10, pad=10)

    boxes = [
        (0.5,  2.8, 2.2, 1.0, "Task Suite\n20 Python tasks\n174 tests",    "#d5e8d4"),
        (3.5,  2.8, 2.2, 1.0, "AGENTS.md\nVariant\n(5 candidates)",       "#dae8fc"),
        (6.5,  2.8, 2.2, 1.0, "opencode run\n(headless, 25 min)",         "#fff2cc"),
        (3.5,  0.8, 2.2, 1.0, "Score + Time\n(per variant)",               "#f8cecc"),
        (6.5,  0.8, 2.2, 1.0, "Leaderboard\nComparison",                   "#e1d5e7"),
        (0.5,  0.8, 2.2, 1.0, "Round 2\n4 themes\n(20 runs)",             "#d5e8d4"),
    ]
    for x, y, w, h, txt, col in boxes:
        ax.add_patch(mpatches.FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.08",
                      facecolor=col, edgecolor="#333", linewidth=0.8))
        ax.text(x + w/2, y + h/2, txt, ha="center", va="center", fontsize=7.5, linespacing=1.3)

    arrows = [(2.7,3.3,3.5,3.3), (5.7,3.3,6.5,3.3), (7.6,2.8,7.6,1.8),
              (5.7,1.3,3.5,1.3), (1.6,1.8,1.6,2.8), (2.7,1.3,3.5,1.3)]
    for x1,y1,x2,y2 in arrows:
        ax.annotate("", xy=(x2,y2), xytext=(x1,y1),
                     arrowprops=dict(arrowstyle="-|>", color="#555", lw=1.0))
    plt.savefig(FIG / "fig1_architecture.pdf")
    plt.savefig(FIG / "fig1_architecture.png", dpi=300)
    plt.close()
    print("fig1 done")

# ── Figure 2: Round 1 scores (all 100%) ──────────────────────────────────────
def fig2_round1():
    scores, times = load_r1()
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7, 2.8), gridspec_kw={"width_ratios": [1, 1.3]})

    # Left: scores
    vals = [scores[v] for v in VARIANTS]
    bars = ax1.bar(SHORT, vals, color=COLORS, edgecolor="#333", linewidth=0.5)
    ax1.set_ylim(0, 110); ax1.set_ylabel("Score (%)")
    ax1.set_title("(a) Accuracy", fontsize=9)
    ax1.axhline(100, color="#999", ls="--", lw=0.5)
    for b, v in zip(bars, VARIANTS):
        ax1.text(b.get_x() + b.get_width()/2, 103, "100%", ha="center", fontsize=7)

    # Right: times
    tvals = [times[v]/60 for v in VARIANTS]
    bars2 = ax2.bar(SHORT, tvals, color=COLORS, edgecolor="#333", linewidth=0.5)
    ax2.set_ylabel("Time (min)")
    ax2.set_title("(b) Speed", fontsize=9)
    for b, t in zip(bars2, tvals):
        ax2.text(b.get_x() + b.get_width()/2, b.get_height() + 0.15,
                 f"{t:.1f}", ha="center", fontsize=7)

    fig.suptitle("Fig. 2.  Round 1 results — bug-fix suite (all variants scored 100%)", fontsize=10, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG / "fig2_round1.pdf")
    plt.savefig(FIG / "fig2_round1.png", dpi=300)
    plt.close()
    print("fig2 done")

# ── Figure 3: Round 2 Track A scores (the differentiator) ────────────────────
def fig3_trackA():
    r2 = load_r2()
    fig, ax = plt.subplots(figsize=(5.5, 3.0))
    vals = [r2["A"][v]["score"] for v in VARIANTS]
    bars = ax.bar(SHORT, vals, color=COLORS, edgecolor="#333", linewidth=0.5)
    ax.set_ylim(0, 115); ax.set_ylabel("Score (%)")
    ax.set_title("Track A: Spec-to-Code (8 libraries, 177 tests)", fontsize=9)
    ax.axhline(100, color="#999", ls="--", lw=0.5)
    for b, v in zip(bars, VARIANTS):
        sc = r2["A"][v]["score"]
        cap = " (cap)" if r2["A"][v]["capped"] else ""
        dnf = " (DNF)" if sc < 5 else ""
        label = f"{sc:.1f}%{cap}{dnf}"
        ax.text(b.get_x() + b.get_width()/2, b.get_height() + 1.5,
                label, ha="center", fontsize=7, fontweight="bold" if sc == 100 else "normal")
    fig.suptitle("Fig. 3.  Track A accuracy — the only track that broke saturation", fontsize=10, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG / "fig3_trackA.pdf")
    plt.savefig(FIG / "fig3_trackA.png", dpi=300)
    plt.close()
    print("fig3 done")

# ── Figure 4: All tracks grouped bar chart ────────────────────────────────────
def fig4_alltracks():
    r2 = load_r2()
    fig, axes = plt.subplots(1, 4, figsize=(7.5, 2.8), sharey=True)
    track_names = [
        "A: Spec-to-Code",
        "B: Refactor",
        "C: SQL Analytics",
        "D: API Client",
    ]
    for i, (t, ax) in enumerate(zip(TRACKS, axes)):
        vals = [r2[t][v]["score"] for v in VARIANTS]
        ax.bar(SHORT, vals, color=COLORS, edgecolor="#333", linewidth=0.4)
        ax.set_ylim(0, 115)
        ax.set_title(track_names[i], fontsize=8, pad=4)
        ax.tick_params(axis="x", rotation=45)
        if i == 0:
            ax.set_ylabel("Score (%)")
        for j, sc in enumerate(vals):
            ax.text(j, sc + 1.5, f"{sc:.0f}" if sc >= 10 else f"{sc:.1f}",
                    ha="center", fontsize=6)
    fig.suptitle("Fig. 4.  Round 2 accuracy across all four tracks", fontsize=10, y=1.02)
    plt.tight_layout()
    plt.savefig(FIG / "fig4_alltracks.pdf")
    plt.savefig(FIG / "fig4_alltracks.png", dpi=300)
    plt.close()
    print("fig4 done")

# ── Figure 5: Speed comparison (horizontal bar) ──────────────────────────────
def fig5_speed():
    r2 = load_r2()
    fig, ax = plt.subplots(figsize=(7, 3.5))
    y = np.arange(len(VARIANTS))
    height = 0.18
    offsets = [-2, -1, 0, 1, 2]
    for i, (t, off) in enumerate(zip(TRACKS, offsets)):
        times = [r2[t][v]["time"]/60 for v in VARIANTS]
        ax.barh(y + off*height, times, height, label=f"Track {t}",
                color=["#2ecc71","#3498db","#e74c3c","#f39c12"][i],
                edgecolor="#333", linewidth=0.3)
    ax.set_yticks(y); ax.set_yticklabels(SHORT)
    ax.set_xlabel("Time (min)")
    ax.legend(loc="lower right", fontsize=7)
    ax.set_title("Fig. 5.  Wall-clock time by variant and track", fontsize=10)
    plt.tight_layout()
    plt.savefig(FIG / "fig5_speed.pdf")
    plt.savefig(FIG / "fig5_speed.png", dpi=300)
    plt.close()
    print("fig5 done")

# ── Figure 6: Speed vs Accuracy scatter ───────────────────────────────────────
def fig6_scatter():
    r2 = load_r2()
    fig, ax = plt.subplots(figsize=(5.5, 3.5))
    for i, v in enumerate(VARIANTS):
        avg_sc = np.mean([r2[t][v]["score"] for t in TRACKS])
        avg_tm = np.mean([r2[t][v]["time"] for t in TRACKS]) / 60
        ax.scatter(avg_tm, avg_sc, c=COLORS[i], s=120, edgecolor="#333",
                   linewidth=0.6, zorder=5, label=SHORT[i])
        ax.annotate(SHORT[i], (avg_tm, avg_sc), textcoords="offset points",
                    xytext=(8, 4), fontsize=7)
    ax.set_xlabel("Average time (min)")
    ax.set_ylabel("Average score (%)")
    ax.set_ylim(70, 105); ax.set_xlim(4, 18)
    ax.axhline(100, color="#999", ls="--", lw=0.5)
    ax.set_title("Fig. 6.  Speed vs. accuracy trade-off (Round 2)", fontsize=10)
    ax.legend(loc="lower left", fontsize=7)
    plt.tight_layout()
    plt.savefig(FIG / "fig6_scatter.pdf")
    plt.savefig(FIG / "fig6_scatter.png", dpi=300)
    plt.close()
    print("fig6 done")

# ── Figure 7: Heatmap ────────────────────────────────────────────────────────
def fig7_heatmap():
    r2 = load_r2()
    fig, ax = plt.subplots(figsize=(5, 3.0))
    matrix = np.array([[r2[t][v]["score"] for v in VARIANTS] for t in TRACKS])
    im = ax.imshow(matrix, cmap="RdYlGn", vmin=0, vmax=105, aspect="auto")
    ax.set_xticks(range(len(SHORT))); ax.set_xticklabels(SHORT, rotation=30, ha="right")
    ax.set_yticks(range(len(TRACKS))); ax.set_yticklabels([f"Track {t}" for t in TRACKS])
    for i in range(len(TRACKS)):
        for j in range(len(VARIANTS)):
            v = matrix[i, j]
            txt = f"{v:.0f}" if v >= 10 else f"{v:.1f}"
            color = "white" if v < 50 else "black"
            ax.text(j, i, txt, ha="center", va="center", fontsize=8, color=color, fontweight="bold")
    plt.colorbar(im, ax=ax, label="Score (%)", shrink=0.85)
    ax.set_title("Fig. 7.  Variant × Track accuracy heatmap", fontsize=10, pad=8)
    plt.tight_layout()
    plt.savefig(FIG / "fig7_heatmap.pdf")
    plt.savefig(FIG / "fig7_heatmap.png", dpi=300)
    plt.close()
    print("fig7 done")

# ── Figure 8: Provider dropout timeline (Track A user-proposed) ───────────────
def fig8_dropout():
    fig, ax = plt.subplots(figsize=(5.5, 2.8))
    phases = ["Prompt 1\n(read libs)", "Prompt 2\n(read libs)", "Prompt 3\n(read libs)",
              "Prompt 4\n(attempt edit)", "Prompt 5\n(attempt edit)"]
    scores = [0, 0, 0, 0.56, 0.56]
    events = ["stream drop", "stream drop", "stream drop", "1 edit applied", "stream drop"]
    ax.plot(range(5), scores, "o-", color="#e74c3c", linewidth=2, markersize=8, zorder=5)
    for i, (s, e) in enumerate(zip(scores, events)):
        ax.annotate(e, (i, s), textcoords="offset points", xytext=(0, 14),
                    ha="center", fontsize=6.5, color="#c0392b",
                    arrowprops=dict(arrowstyle="-", color="#c0392b", lw=0.5))
    ax.set_xticks(range(5)); ax.set_xticklabels(phases, fontsize=7)
    ax.set_ylabel("Cumulative score (%)")
    ax.set_ylim(-5, 25)
    ax.set_title("Fig. 8.  Provider dropout timeline — A-user-proposed (0.56%)", fontsize=9, pad=8)
    ax.axhline(0, color="#999", ls=":", lw=0.5)
    plt.tight_layout()
    plt.savefig(FIG / "fig8_dropout.pdf")
    plt.savefig(FIG / "fig8_dropout.png", dpi=300)
    plt.close()
    print("fig8 done")

# ── Run all ───────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    fig1_architecture()
    fig2_round1()
    fig3_trackA()
    fig4_alltracks()
    fig5_speed()
    fig6_scatter()
    fig7_heatmap()
    fig8_dropout()
    print(f"All figures saved to {FIG}")
