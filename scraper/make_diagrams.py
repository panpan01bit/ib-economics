#!/usr/bin/env python3
"""Generate clean, uncrowded diagram images for the diagram module.

Design: strong visuals, minimal short English labels (IB notation). Chinese
explanations live in the HTML layer. One PNG per diagram id -> site/assets/diagrams/.
"""
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.font_manager as fm

for _f in ("/System/Library/Fonts/Hiragino Sans GB.ttc",
           "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"):
    try:
        fm.fontManager.addfont(_f)
    except Exception:
        pass
plt.rcParams["font.family"] = ["Hiragino Sans GB", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

HERE = Path(__file__).resolve().parent
PROJECT = HERE.parent
SITE = PROJECT / "site"
OUT = SITE / "assets" / "diagrams"
sys.path.insert(0, str(HERE))
import content  # noqa: E402

TEAL = "#0ea5a4"; ORANGE = "#f97316"; RED = "#ef4444"; GREEN = "#22c55e"
SKY = "#38bdf8"; VIOLET = "#8b5cf6"; AMBER = "#f59e0b"; INK = "#334155"
GREY = "#94a3b8"


def new_ax():
    fig, ax = plt.subplots(figsize=(5.2, 3.7), dpi=160)
    ax.set_xlim(-0.10, 1.10)
    ax.set_ylim(-0.10, 1.10)
    ax.axis("off")
    ax.annotate("", xy=(1.06, 0), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.4, color=INK))
    ax.annotate("", xy=(0, 1.06), xytext=(0, 0), arrowprops=dict(arrowstyle="-|>", lw=1.4, color=INK))
    return fig, ax


def curve(ax, x1, y1, x2, y2, color, lw=3, ls="-", z=3):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, linestyle=ls, zorder=z, solid_capstyle="round")


def lbl(ax, x, y, text, color=INK, fs=12, ha="center", va="center", weight="bold", z=6, rotation=None):
    ax.text(x, y, text, color=color, fontsize=fs, ha=ha, va=va, fontweight=weight,
            zorder=z, rotation=rotation)


def dot(ax, x, y, color=INK, ms=6, z=5):
    ax.plot([x], [y], "o", color=color, ms=ms, zorder=z)


def vline(ax, x, y1=0, y2=1, color=GREY, ls="--", lw=1.2):
    ax.plot([x, x], [y1, y2], color=color, lw=lw, linestyle=ls, zorder=2)


def hline(ax, y, x1=0, x2=1, color=GREY, ls="--", lw=1.2):
    ax.plot([x1, x2], [y, y], color=color, lw=lw, linestyle=ls, zorder=2)


def fill(ax, xs, ys, color, alpha=0.25):
    ax.fill(xs, ys, color=color, alpha=alpha, zorder=1, linewidth=0)


def save(fig, ax, sid):
    OUT.mkdir(parents=True, exist_ok=True)
    fig.savefig(OUT / (sid + ".png"), bbox_inches="tight", facecolor="white", pad_inches=0.06)
    plt.close(fig)


def axis_labels(ax, x="Q", y="P"):
    lbl(ax, 1.07, -0.03, x, INK, fs=12, ha="left", weight="normal")
    lbl(ax, -0.04, 1.07, y, INK, fs=12, va="bottom", weight="normal")


# ---------------------------------------------------------------------------

def d_ppc(ax):
    xs = [0.1, 0.38, 0.66, 0.9]
    ys = [0.92, 0.66, 0.34, 0.08]
    curve(ax, xs[0], ys[0], xs[1], ys[1], TEAL); curve(ax, xs[1], ys[1], xs[2], ys[2], TEAL); curve(ax, xs[2], ys[2], xs[3], ys[3], TEAL)
    lbl(ax, 0.92, 0.17, "PPC", TEAL)
    dot(ax, 0.42, 0.42, VIOLET); lbl(ax, 0.42, 0.33, "A\n(inside)", VIOLET, fs=10)
    dot(ax, 0.3, 0.74, RED); lbl(ax, 0.3, 0.82, "B (on)", RED, fs=10)
    dot(ax, 0.78, 0.76, ORANGE); lbl(ax, 0.78, 0.84, "C (outside)", ORANGE, fs=10)
    axis_labels(ax, "Good X", "Good Y")


def d_demand(ax):
    curve(ax, 0.12, 0.86, 0.92, 0.14, TEAL)
    lbl(ax, 0.94, 0.1, "D", TEAL)
    curve(ax, 0.3, 0.88, 0.96, 0.36, TEAL, ls="--", lw=2)
    dot(ax, 0.4, 0.55, INK, 5); dot(ax, 0.66, 0.3, INK, 5)
    ax.annotate("movement", xy=(0.66, 0.3), xytext=(0.42, 0.66),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2), fontsize=10, color=GREY)
    ax.annotate("shift", xy=(0.66, 0.6), xytext=(0.72, 0.82),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2), fontsize=10, color=GREY)
    axis_labels(ax)


def d_supply(ax):
    curve(ax, 0.12, 0.14, 0.92, 0.86, ORANGE)
    lbl(ax, 0.94, 0.9, "S", ORANGE)
    curve(ax, 0.3, 0.12, 0.96, 0.82, ORANGE, ls="--", lw=2)
    ax.annotate("shift", xy=(0.62, 0.52), xytext=(0.5, 0.22),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2), fontsize=10, color=GREY)
    axis_labels(ax)


def d_equilibrium(ax):
    curve(ax, 0.12, 0.86, 0.92, 0.14, TEAL)
    curve(ax, 0.12, 0.14, 0.92, 0.86, ORANGE)
    ix, iy = 0.5, 0.5
    vline(ax, ix, 0, iy); hline(ax, iy, 0, ix)
    fill(ax, [0.12, ix, ix], [0.86, iy, iy], TEAL, 0.22)
    fill(ax, [0.12, ix, ix], [0.14, iy, iy], ORANGE, 0.18)
    dot(ax, ix, iy, INK, 6); lbl(ax, ix + 0.035, iy + 0.05, "E", INK)
    lbl(ax, 0.27, 0.72, "CS", "#0f766e", fs=12)
    lbl(ax, 0.25, 0.27, "PS", "#c2410c", fs=12)
    lbl(ax, ix, -0.055, "Q*", INK, fs=11, weight="normal")
    lbl(ax, -0.05, iy, "P*", INK, fs=11, weight="normal")
    lbl(ax, 0.94, 0.1, "D", TEAL, fs=11); lbl(ax, 0.94, 0.9, "S", ORANGE, fs=11)


def d_ped(ax):
    curve(ax, 0.12, 0.9, 0.5, 0.14, TEAL)
    curve(ax, 0.6, 0.85, 0.92, 0.42, VIOLET)
    lbl(ax, 0.5, 0.1, "D elastic", TEAL, fs=11, ha="right")
    lbl(ax, 0.6, 0.92, "D inelastic", VIOLET, fs=11, ha="left")
    axis_labels(ax)


def d_pes(ax):
    curve(ax, 0.12, 0.1, 0.5, 0.86, ORANGE)
    curve(ax, 0.6, 0.28, 0.92, 0.82, RED)
    lbl(ax, 0.5, 0.92, "S elastic", ORANGE, fs=11, ha="right")
    lbl(ax, 0.6, 0.2, "S inelastic", RED, fs=11, ha="left")
    axis_labels(ax)


def d_tax(ax):
    curve(ax, 0.12, 0.86, 0.92, 0.14, TEAL)
    curve(ax, 0.12, 0.14, 0.92, 0.86, ORANGE)
    curve(ax, 0.2, 0.3, 0.94, 0.96, ORANGE, ls="--", lw=2.4)
    dot(ax, 0.5, 0.5, GREY, 5)
    dot(ax, 0.42, 0.58, INK, 6); lbl(ax, 0.42, 0.66, "P2", INK, fs=11)
    vline(ax, 0.42, 0, 0.58)
    hline(ax, 0.58, 0, 0.42)
    fill(ax, [0.42, 0.5, 0.5, 0.42], [0.58, 0.58, 0.5, 0.5], AMBER, 0.22)
    lbl(ax, 0.46, 0.45, "tax", "#b45309", fs=10)
    lbl(ax, 0.94, 0.1, "D", TEAL, fs=11); lbl(ax, 0.94, 0.9, "S", ORANGE, fs=11)
    lbl(ax, 0.96, 0.99, "S+tax", ORANGE, fs=11, ha="right")
    axis_labels(ax)


def d_subsidy(ax):
    curve(ax, 0.12, 0.86, 0.92, 0.14, TEAL)
    curve(ax, 0.12, 0.14, 0.92, 0.86, ORANGE)
    curve(ax, 0.06, 0.0, 0.9, 0.78, ORANGE, ls="--", lw=2.4)
    dot(ax, 0.58, 0.46, INK, 6); lbl(ax, 0.58, 0.36, "P1", INK, fs=11)
    vline(ax, 0.58, 0, 0.46)
    lbl(ax, 0.94, 0.1, "D", TEAL, fs=11); lbl(ax, 0.94, 0.9, "S", ORANGE, fs=11)
    lbl(ax, 0.9, 0.72, "S+subsidy", ORANGE, fs=11, ha="right")
    axis_labels(ax)


def d_ceiling(ax):
    curve(ax, 0.12, 0.86, 0.92, 0.14, TEAL)
    curve(ax, 0.12, 0.14, 0.92, 0.86, ORANGE)
    hline(ax, 0.3, 0.05, 0.98, RED, ls="-", lw=2.6)
    lbl(ax, 0.98, 0.3, "Pc", RED, fs=11, ha="right")
    qd, qs = 0.68, 0.26
    vline(ax, qs, 0, 0.3); vline(ax, qd, 0, 0.3)
    ax.annotate("", xy=(qd, 0.3), xytext=(qs, 0.3), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
    lbl(ax, 0.47, 0.2, "shortage", INK, fs=11)
    lbl(ax, 0.94, 0.1, "D", TEAL, fs=11); lbl(ax, 0.94, 0.9, "S", ORANGE, fs=11)
    axis_labels(ax)


def d_floor(ax):
    curve(ax, 0.12, 0.86, 0.92, 0.14, TEAL)
    curve(ax, 0.12, 0.14, 0.92, 0.86, ORANGE)
    hline(ax, 0.72, 0.05, 0.98, RED, ls="-", lw=2.6)
    lbl(ax, 0.98, 0.72, "Pf", RED, fs=11, ha="right")
    qd, qs = 0.26, 0.68
    vline(ax, qs, 0, 0.72); vline(ax, qd, 0, 0.72)
    ax.annotate("", xy=(qs, 0.72), xytext=(qd, 0.72), arrowprops=dict(arrowstyle="<->", color=INK, lw=1.4))
    lbl(ax, 0.47, 0.82, "surplus", INK, fs=11)
    lbl(ax, 0.94, 0.1, "D", TEAL, fs=11); lbl(ax, 0.94, 0.9, "S", ORANGE, fs=11)
    axis_labels(ax)


def d_neg_prod(ax):
    curve(ax, 0.12, 0.82, 0.92, 0.16, TEAL)
    curve(ax, 0.12, 0.1, 0.92, 0.72, ORANGE)
    curve(ax, 0.16, 0.34, 0.96, 0.98, RED)
    xm, xo = 0.55, 0.42
    vline(ax, xm, 0, 0.44); vline(ax, xo, 0, 0.34)
    fill(ax, [xo, xm, xm], [0.34, 0.34, 0.44], RED, 0.22)
    lbl(ax, 0.5, 0.25, "DWL", RED, fs=11)
    lbl(ax, xm, -0.055, "Qm", INK, fs=10, weight="normal")
    lbl(ax, xo, -0.055, "Q*", INK, fs=10, weight="normal")
    lbl(ax, 0.94, 0.12, "D=MSB", TEAL, fs=10); lbl(ax, 0.94, 0.78, "MPC", ORANGE, fs=10)
    lbl(ax, 0.96, 0.96, "MSC", RED, fs=10, ha="right")
    axis_labels(ax)


def d_neg_cons(ax):
    curve(ax, 0.12, 0.1, 0.92, 0.72, ORANGE)
    curve(ax, 0.12, 0.82, 0.92, 0.16, TEAL)
    curve(ax, 0.06, 0.6, 0.82, 0.0, GREEN)
    xm, xo = 0.55, 0.42
    vline(ax, xm, 0, 0.44); vline(ax, xo, 0, 0.34)
    fill(ax, [xo, xm, xm], [0.34, 0.34, 0.44], GREEN, 0.2)
    lbl(ax, 0.5, 0.25, "DWL", "#166534", fs=11)
    lbl(ax, xm, -0.055, "Qm", INK, fs=10, weight="normal")
    lbl(ax, xo, -0.055, "Q*", INK, fs=10, weight="normal")
    lbl(ax, 0.94, 0.78, "S=MSC", ORANGE, fs=10); lbl(ax, 0.94, 0.12, "MPB", TEAL, fs=10)
    lbl(ax, 0.06, 0.68, "MSB", GREEN, fs=10, ha="left")
    axis_labels(ax)


def d_pos_ext(ax):
    curve(ax, 0.12, 0.1, 0.92, 0.72, ORANGE)
    curve(ax, 0.12, 0.82, 0.92, 0.16, TEAL)
    curve(ax, 0.22, 0.9, 0.98, 0.26, GREEN)
    xm, xo = 0.42, 0.55
    vline(ax, xm, 0, 0.34); vline(ax, xo, 0, 0.44)
    fill(ax, [xm, xo, xo], [0.34, 0.34, 0.44], GREEN, 0.2)
    lbl(ax, 0.49, 0.25, "DWL", "#166534", fs=11)
    lbl(ax, xm, -0.055, "Qm", INK, fs=10, weight="normal")
    lbl(ax, xo, -0.055, "Q*", INK, fs=10, weight="normal")
    lbl(ax, 0.94, 0.78, "S=MSC", ORANGE, fs=10); lbl(ax, 0.94, 0.12, "MPB", TEAL, fs=10)
    lbl(ax, 0.98, 0.2, "MSB", GREEN, fs=10, ha="right")
    axis_labels(ax)


def d_monopoly(ax):
    curve(ax, 0.12, 0.88, 0.9, 0.18, TEAL)
    curve(ax, 0.12, 0.88, 0.6, 0.06, VIOLET)
    curve(ax, 0.16, 0.22, 0.92, 0.78, ORANGE)
    xm, y_mc = 0.46, 0.4
    dot(ax, xm, y_mc, INK, 5)
    vline(ax, xm, 0, 0.66)
    dot(ax, xm, 0.66, RED, 6); lbl(ax, xm - 0.045, 0.66, "Pm", RED, fs=11, ha="right")
    lbl(ax, xm, -0.055, "Qm", INK, fs=10, weight="normal")
    lbl(ax, 0.92, 0.14, "D=AR", TEAL, fs=10, ha="right")
    lbl(ax, 0.6, 0.0, "MR", VIOLET, fs=10, ha="right")
    lbl(ax, 0.94, 0.82, "MC", ORANGE, fs=10)
    axis_labels(ax)


def d_circular(ax):
    ax.text(0.27, 0.56, "Households", ha="center", va="center", fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#e0f7f3", ec=TEAL, lw=1.5))
    ax.text(0.73, 0.56, "Firms", ha="center", va="center", fontsize=12, fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.4", fc="#ffedd5", ec=ORANGE, lw=1.5))
    ax.annotate("", xy=(0.665, 0.62), xytext=(0.335, 0.62), arrowprops=dict(arrowstyle="->", color=TEAL, lw=2))
    lbl(ax, 0.5, 0.67, "spending", TEAL, fs=11)
    ax.annotate("", xy=(0.335, 0.5), xytext=(0.665, 0.5), arrowprops=dict(arrowstyle="->", color=ORANGE, lw=2))
    lbl(ax, 0.5, 0.45, "income", ORANGE, fs=11)
    lbl(ax, 0.5, 0.14, "Leakages: S, T, M      Injections: I, G, X", GREY, fs=10, weight="normal")


def d_ad(ax):
    curve(ax, 0.12, 0.86, 0.92, 0.16, SKY)
    curve(ax, 0.32, 0.82, 0.98, 0.3, SKY, ls="--", lw=2.2)
    lbl(ax, 0.94, 0.12, "AD", SKY, fs=11)
    ax.annotate("", xy=(0.72, 0.62), xytext=(0.6, 0.8),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.4))
    axis_labels(ax, "Real GDP", "Price level")


def d_sras(ax):
    curve(ax, 0.16, 0.1, 0.92, 0.86, TEAL)
    lbl(ax, 0.94, 0.9, "SRAS", TEAL)
    axis_labels(ax, "Real GDP", "Price level")


def d_lras(ax):
    vline(ax, 0.62, 0.05, 0.98, VIOLET, ls="-", lw=3)
    lbl(ax, 0.62, 1.03, "LRAS (neo)", VIOLET, fs=11)
    curve(ax, 0.12, 0.14, 0.3, 0.14, ORANGE, lw=2.4)
    curve(ax, 0.3, 0.14, 0.3, 0.8, ORANGE, lw=2.4)
    curve(ax, 0.3, 0.8, 0.56, 0.8, ORANGE, lw=2.4)
    curve(ax, 0.56, 0.8, 0.56, 0.98, ORANGE, lw=2.4)
    lbl(ax, 0.12, 0.22, "Keynesian", ORANGE, fs=10, ha="left")
    axis_labels(ax, "Real GDP", "Price level")


def d_adas_gap(ax):
    curve(ax, 0.12, 0.8, 0.8, 0.2, SKY)
    curve(ax, 0.18, 0.1, 0.9, 0.8, TEAL)
    vline(ax, 0.6, 0.05, 0.92, VIOLET, ls="--", lw=2.2)
    lbl(ax, 0.6, 1.0, "LRAS", VIOLET, fs=10)
    dot(ax, 0.48, 0.46, INK, 6); lbl(ax, 0.48, 0.38, "E", INK, fs=10)
    ax.annotate("", xy=(0.6, 0.36), xytext=(0.48, 0.36), arrowprops=dict(arrowstyle="<->", color=RED, lw=1.6))
    lbl(ax, 0.54, 0.28, "recessionary gap", RED, fs=10)
    lbl(ax, 0.82, 0.16, "AD", SKY, fs=10); lbl(ax, 0.92, 0.84, "SRAS", TEAL, fs=10)
    axis_labels(ax, "Real GDP", "Price level")


def d_business(ax):
    xs = [0.08, 0.3, 0.52, 0.74, 0.92]
    ys = [0.34, 0.74, 0.4, 0.8, 0.5]
    curve(ax, xs[0], ys[0], xs[1], ys[1], TEAL); curve(ax, xs[1], ys[1], xs[2], ys[2], TEAL)
    curve(ax, xs[2], ys[2], xs[3], ys[3], TEAL); curve(ax, xs[3], ys[3], xs[4], ys[4], TEAL)
    hline(ax, 0.56, 0.05, 0.95, GREY, ls="--", lw=1.4)
    lbl(ax, 0.95, 0.62, "trend", GREY, fs=10, ha="right", weight="normal")
    lbl(ax, 0.3, 0.82, "peak", INK, fs=10)
    lbl(ax, 0.52, 0.3, "trough", INK, fs=10)
    axis_labels(ax, "time", "Real GDP")


def d_lorenz(ax):
    curve(ax, 0.05, 0.05, 0.95, 0.95, GREY, lw=2)
    xs = [0.05, 0.3, 0.55, 0.8, 0.95]
    ys = [0.05, 0.15, 0.3, 0.52, 0.95]
    curve(ax, xs[0], ys[0], xs[1], ys[1], VIOLET); curve(ax, xs[1], ys[1], xs[2], ys[2], VIOLET)
    curve(ax, xs[2], ys[2], xs[3], ys[3], VIOLET); curve(ax, xs[3], ys[3], xs[4], ys[4], VIOLET)
    fill(ax, xs + [0.95, 0.05], ys + [0.05, 0.05], VIOLET, 0.18)
    lbl(ax, 0.72, 0.74, "45°", GREY, fs=10, rotation=43, weight="normal")
    lbl(ax, 0.85, 0.62, "Lorenz", VIOLET, fs=11)
    axis_labels(ax, "population %", "income %")


def d_monetary(ax):
    curve(ax, 0.12, 0.8, 0.8, 0.2, SKY)
    curve(ax, 0.32, 0.82, 0.96, 0.3, SKY, lw=2.4)
    curve(ax, 0.18, 0.1, 0.9, 0.8, TEAL)
    lbl(ax, 0.82, 0.16, "AD1", SKY, fs=10)
    lbl(ax, 0.98, 0.26, "AD2", SKY, fs=10, ha="right")
    lbl(ax, 0.92, 0.84, "SRAS", TEAL, fs=10)
    ax.annotate("", xy=(0.76, 0.64), xytext=(0.55, 0.86),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.4))
    axis_labels(ax, "Real GDP", "Price level")


def d_supply_side(ax):
    vline(ax, 0.45, 0.05, 0.92, VIOLET, ls="--", lw=2.2)
    vline(ax, 0.68, 0.05, 0.92, VIOLET, ls="-", lw=2.6)
    lbl(ax, 0.45, 1.0, "LRAS1", VIOLET, fs=10, ha="right")
    lbl(ax, 0.68, 1.0, "LRAS2", VIOLET, fs=10, ha="left")
    curve(ax, 0.12, 0.76, 0.82, 0.3, SKY)
    lbl(ax, 0.84, 0.26, "AD", SKY, fs=10)
    ax.annotate("", xy=(0.68, 0.56), xytext=(0.45, 0.56), arrowprops=dict(arrowstyle="->", color=TEAL, lw=1.8))
    axis_labels(ax, "Real GDP", "Price level")


def d_comparative(ax):
    curve(ax, 0.1, 0.88, 0.46, 0.12, TEAL)
    curve(ax, 0.1, 0.6, 0.46, 0.12, SKY)
    lbl(ax, 0.46, 0.08, "A", TEAL, fs=11, ha="right")
    lbl(ax, 0.46, 0.66, "B", SKY, fs=11, ha="right")
    axis_labels(ax, "Good X", "Good Y")


def d_tariff(ax):
    hline(ax, 0.28, 0.05, 0.98, AMBER, ls="-", lw=2.4)
    hline(ax, 0.5, 0.05, 0.98, RED, ls="-", lw=2.4)
    lbl(ax, 0.98, 0.28, "Pw", AMBER, fs=11, ha="right")
    lbl(ax, 0.98, 0.5, "Pw+t", RED, fs=11, ha="right")
    curve(ax, 0.1, 0.84, 0.92, 0.1, TEAL)
    curve(ax, 0.1, 0.1, 0.92, 0.84, ORANGE)
    q1, q2, q3, q4 = 0.17, 0.31, 0.57, 0.73
    for q, t in ((q1, "Q1"), (q2, "Q2"), (q3, "Q3"), (q4, "Q4")):
        vline(ax, q, 0, 0.5, GREY, lw=0.9)
        lbl(ax, q, -0.05, t, INK, fs=9, weight="normal")
    fill(ax, [q2, q3, q3, q2], [0.5, 0.5, 0.28, 0.28], AMBER, 0.2)
    lbl(ax, 0.44, 0.4, "tax revenue", "#b45309", fs=10)
    lbl(ax, 0.94, 0.06, "D", TEAL, fs=10); lbl(ax, 0.94, 0.88, "S", ORANGE, fs=10)
    axis_labels(ax, "Q", "P")


def d_exchange(ax):
    curve(ax, 0.12, 0.84, 0.9, 0.16, TEAL)
    curve(ax, 0.12, 0.16, 0.9, 0.84, ORANGE)
    dot(ax, 0.5, 0.5, INK, 6); lbl(ax, 0.5, 0.42, "e*", INK, fs=11)
    vline(ax, 0.5, 0, 0.5)
    lbl(ax, 0.92, 0.12, "D", TEAL, fs=11); lbl(ax, 0.92, 0.88, "S", ORANGE, fs=11)
    axis_labels(ax, "Q of currency", "Price of currency")


def d_jcurve(ax):
    xs = [0.08, 0.28, 0.48, 0.7, 0.92]
    ys = [0.7, 0.3, 0.16, 0.5, 0.88]
    curve(ax, xs[0], ys[0], xs[1], ys[1], TEAL); curve(ax, xs[1], ys[1], xs[2], ys[2], TEAL)
    curve(ax, xs[2], ys[2], xs[3], ys[3], TEAL); curve(ax, xs[3], ys[3], xs[4], ys[4], TEAL)
    hline(ax, 0.5, 0.05, 0.95, GREY, ls="--", lw=1.4)
    lbl(ax, 0.5, 0.08, "J-curve", TEAL, fs=11)
    lbl(ax, 0.95, 0.42, "0", GREY, fs=10, ha="right", weight="normal")
    lbl(ax, 0.03, 0.56, "+", GREY, fs=11, weight="normal")
    lbl(ax, 0.03, 0.44, "−", GREY, fs=11, weight="normal")
    axis_labels(ax, "time", "trade balance")


def d_poverty(ax):
    def box(x, y, t, fc, ec):
        ax.text(x, y, t, ha="center", va="center", fontsize=11, fontweight="bold",
                bbox=dict(boxstyle="round,pad=0.4", fc=fc, ec=ec, lw=1.5))
    box(0.28, 0.28, "Low income", "#e0f7f3", TEAL)
    box(0.72, 0.28, "Low saving", "#ffedd5", ORANGE)
    box(0.72, 0.72, "Low investment", "#fef3c7", AMBER)
    box(0.28, 0.72, "Low growth", "#ede9fe", VIOLET)
    ax.annotate("", xy=(0.655, 0.28), xytext=(0.345, 0.28), arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.annotate("", xy=(0.72, 0.655), xytext=(0.72, 0.345), arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.annotate("", xy=(0.345, 0.72), xytext=(0.655, 0.72), arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.annotate("", xy=(0.28, 0.345), xytext=(0.28, 0.655), arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))


FUNCS = {
    "ppc": d_ppc, "demand_curve": d_demand, "supply_curve": d_supply,
    "equilibrium": d_equilibrium, "ped": d_ped, "pes": d_pes,
    "tax": d_tax, "subsidy": d_subsidy, "price_ceiling": d_ceiling,
    "price_floor": d_floor, "neg_ext_prod": d_neg_prod, "neg_ext_cons": d_neg_cons,
    "pos_ext": d_pos_ext, "monopoly": d_monopoly, "circular_flow": d_circular,
    "ad": d_ad, "sras": d_sras, "lras": d_lras, "adas_gap": d_adas_gap,
    "business_cycle": d_business, "lorenz": d_lorenz, "monetary_transmission": d_monetary,
    "supply_side": d_supply_side, "comparative_advantage": d_comparative,
    "tariff": d_tariff, "exchange_rate": d_exchange, "jcurve": d_jcurve,
    "poverty_cycle": d_poverty,
}


def main():
    for d in content.DIAGRAMS:
        sid = d["id"]
        fn = FUNCS.get(sid)
        if not fn:
            continue
        fig, ax = new_ax()
        fn(ax)
        save(fig, ax, sid)
    print(f"generated {len(content.DIAGRAMS)} diagrams to {OUT}")


if __name__ == "__main__":
    main()
