"""
Demo: automatic nice-number axis bounds in range_frame
======================================================

This script demonstrates the ``nice=True`` feature of ``range_frame``.
With ``nice=True`` (the default), spine bounds snap to tick positions so
that the axis line starts and ends exactly on round numbers.

The LEFT column uses nice=True  → spines always land on tick marks.
The RIGHT column uses nice=False → spines sit at raw data min/max
(the old behaviour, shown for comparison — tick misalignment is expected).
"""

import matplotlib.pyplot as plt
import numpy as np

from lama_aesthetics.aesthetics import get_style
from lama_aesthetics.plotutils import range_frame

# ── style ──────────────────────────────────────────────────────────────────
get_style("main")

# ── datasets ────────────────────────────────────────────────────────────────
# Each tuple: (title, x, y)
DATASETS = [
    (
        "Integers 0–4 vs 0–8\n(common case)",
        np.array([0, 1, 2, 3, 4]),
        np.array([0, 2, 4, 6, 8]),
    ),
    (
        "Messy floats\n(3.2 – 47.8)",
        np.linspace(3.2, 47.8, 12),
        np.linspace(3.2, 47.8, 12) * 1.3 - 1.5,
    ),
    (
        "Sub-unit range\n(0.031 – 0.097)",
        np.linspace(0.031, 0.097, 10),
        np.linspace(0.031, 0.097, 10) ** 0.5,
    ),
    (
        "Large numbers\n(12 400 – 98 700)",
        np.linspace(12_400, 98_700, 8),
        np.linspace(12_400, 98_700, 8) * 0.7 + 3_000,
    ),
    (
        "Negative range\n(−73 – −12)",
        np.linspace(-73, -12, 10),
        np.linspace(-73, -12, 10) * -0.5 - 5,
    ),
]

# ── figure layout ────────────────────────────────────────────────────────────
n_rows = len(DATASETS)
fig, axes = plt.subplots(n_rows, 2, figsize=(10, 2.8 * n_rows))

# Column headers
axes[0, 0].set_title(
    "nice=True  (NEW — spines snap to ticks)",
    fontsize=9,
    fontweight="bold",
    color="green",
    pad=8,
)
axes[0, 1].set_title(
    "nice=False  (OLD — spines at raw data min/max)",
    fontsize=9,
    fontweight="bold",
    color="red",
    pad=8,
)

for row, (title, x, y) in enumerate(DATASETS):
    for col, nice in enumerate([True, False]):
        ax = axes[row, col]

        ax.plot(x, y, marker="o", markersize=4, linewidth=1.5, label=title)
        range_frame(ax, x, y, nice=nice)

        # Show where the spines end relative to the ticks
        if row > 0:
            label = "spines = tick positions" if nice else "spines = data min/max (misaligned)"
            ax.set_title(label, fontsize=7, pad=4, color="green" if nice else "red")

        if col == 0:
            ax.set_ylabel(title, fontsize=7)

        # Annotate the spine end-points so the numbers are visible
        x_lo, x_hi = ax.spines["bottom"].get_bounds()
        y_lo, y_hi = ax.spines["left"].get_bounds()
        ax.set_xlabel(f"x-spine: [{x_lo:.4g}, {x_hi:.4g}]", fontsize=7)

fig.tight_layout()
out_path = "results/figures/nice_bounds_demo.png"
fig.savefig(out_path, dpi=150, bbox_inches="tight")
print(f"Figure saved → {out_path}")
plt.show()
