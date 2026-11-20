from pathlib import Path
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

ROOT = Path(__file__).resolve().parents[1]
fig, ax = plt.subplots(figsize=(13, 8))
ax.set(xlim=(0, 13), ylim=(0, 8))
ax.axis("off")


def box(x, y, w, h, text, color="#eff5f9"):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                               edgecolor="#173e58", facecolor=color))
    ax.text(x+w/2, y+h/2, text, ha="center", va="center", fontsize=16)


def arrow(a, b, label=None, xy=None):
    ax.add_patch(FancyArrowPatch(a, b, arrowstyle="-|>", mutation_scale=15, color="#173e58"))
    if label:
        ax.text(*xy, label, ha="center", fontsize=9,
                bbox={"facecolor": "white", "edgecolor": "none", "pad": 2})


ax.text(6.5, 7.65, "Project 7: model-directed review, enforced safety, unchanged mathematics",
        ha="center", fontsize=18, weight="bold")
box(.35, 5.8, 3.2, 1.05, "User task + persona\nregistered bike-share CSV")
box(4.55, 5.65, 3.8, 1.35, "Project 6: LLM + LangGraph\nchoose tool or final answer\nread returned observation", "#e6f1e8")
box(9.3, 5.8, 3.2, 1.05, "Fresh messages + state\n7 tools · 16 model turns")
box(.35, 3.25, 3.2, 1.3, "Python execution guards\nallowlist · arguments\nprerequisites · holds\nbudgets · no repeats")
box(4.55, 3.25, 3.8, 1.3, "Local numerical tools\nload · quality · split · model\nProject 3: forest + baseline")
box(9.3, 3.05, 3.2, 1.65, "Project 2: diagnostics\nhourly errors\ndaily rank association\ndemand stress")
box(3.25, .35, 6.5, 1.25, "Human evidence review\ncomputed evidence + model explanation + limits\nno source edits or automatic bike allocation", "#fff3df")
arrow((3.6, 6.35), (4.45, 6.35))
arrow((8.45, 6.6), (9.2, 6.6), "store", (8.8, 6.8))
arrow((9.2, 6.1), (8.45, 6.1), "read", (8.8, 5.85))
arrow((4.5, 5.75), (2.8, 4.65), "LLM request", (3.25, 5.25))
arrow((3.6, 3.9), (4.45, 3.9), "permit", (4.0, 4.15))
arrow((8.45, 3.9), (9.2, 3.9), "predictions", (8.8, 4.15))
arrow((6.45, 4.65), (6.45, 5.55), "aggregate observation", (6.55, 4.95))
arrow((10.9, 4.8), (8.4, 5.65), "aggregate observation", (10.2, 5.1))
arrow((2.0, 3.15), (3.2, 1.0), "hold / failure", (1.65, 2.1))
arrow((6.45, 3.15), (6.45, 1.7), "final evidence", (6.55, 2.3))
arrow((10.9, 2.95), (9.85, 1.0), "diagnostics", (11.5, 1.9))
fig.tight_layout()
fig.savefig(ROOT / "outputs/architecture_diagram.png", dpi=180, bbox_inches="tight")
plt.close(fig)
