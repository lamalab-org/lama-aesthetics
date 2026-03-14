# Lama-Aesthetics

[![Build status](https://img.shields.io/github/actions/workflow/status/lamalab-org/lama-aesthetics/main.yml?branch=main)](https://github.com/lamalab-org/lama-aesthetics/actions/workflows/main.yml?query=branch%3Amain)
[![Supported Python versions](https://img.shields.io/badge/python-3.9_%7C_3.10_%7C_3.11_%7C_3.12_%7C_3.13-blue?labelColor=grey&color=blue)](https://github.com/lamalab-org/lama-aesthetics/blob/main/pyproject.toml)
[![Docs](https://img.shields.io/badge/docs-gh--pages-blue)](https://lamalab-org.github.io/lama-aesthetics/)
[![License](https://img.shields.io/github/license/lamalab-org/lama-aesthetics)](https://img.shields.io/github/license/lamalab-org/lama-aesthetics)

Plotting styles and helpers by LamaLab

- **Github repository**: <https://github.com/lamalab-org/lama-aesthetics/>
- **Documentation** <https://lamalab-org.github.io/lama-aesthetics/>

## Installation

```bash
# Clone the repository
git clone https://github.com/lamalab-org/lama-aesthetics.git
cd lama-aesthetics

# Install with uv (recommended)
uv pip install -e .

# Or install with make (which uses uv)
make install
```

## Usage

### Styles

The library provides three main plotting styles:

- **main**: Optimized for publications, reports, and other documents.
- **presentation**: Features larger fonts and thicker lines for better visibility in presentations.
- **dark**: Same as main but with a black background and white text/lines, ideal for dark-themed presentations or interfaces.

```python
import matplotlib.pyplot as plt
import numpy as np
import lama_aesthetics

lama_aesthetics.get_style("main")  # or lama_aesthetics.get_style("presentation") or lama_aesthetics.get_style("dark")
```

<div align="center">
  <div style="display: flex; flex-direction: row;">
    <img src="docs/static/main.png" alt="Main style" width="48%"/>
    <img src="docs/static/presentation.png" alt="Presentation style" width="48%"/>
  </div>
  <p><em>Left: Main style; Right: Presentation style</em></p>
</div>

### Helpers

The package includes several plotting utilities to enhance your visualizations:

- **range_frame**: Draws a frame around the data range.
- **ylabel_top**: Places the y-label at the top of the y-axis.
- **add_identity**: Adds a diagonal reference line.
- **decompose_figure**: Splits a figure into individual figures, one per labeled artist.

### Figure Dimensions

The package provides predefined figure dimension constants based on common journal column widths and the golden ratio:

```python
from lama_aesthetics import (
    ONE_COL_WIDTH,
    TWO_COL_WIDTH,
    ONE_COL_HEIGHT,
    TWO_COL_HEIGHT,
)

# Create a single-column figure with golden ratio proportions
fig, ax = plt.subplots(figsize=(ONE_COL_WIDTH, ONE_COL_HEIGHT))

# Create a two-column figure with golden ratio proportions
fig, ax = plt.subplots(figsize=(TWO_COL_WIDTH, TWO_COL_HEIGHT))
```

Available constants:

- `ONE_COL_WIDTH`: 3 inches (typical single-column width)
- `TWO_COL_WIDTH`: 7.25 inches (typical two-column width)
- `ONE_COL_HEIGHT`: Single-column height based on golden ratio
- `TWO_COL_HEIGHT`: Two-column height based on golden ratio

### Plotting Utilities Examples

```python
import matplotlib.pyplot as plt
import numpy as np
from lama_aesthetics.plotutils import range_frame, ylabel_top, add_identity

# Create sample data
x = np.linspace(0, 10, 100)
y = np.sin(x)

# Create a figure
fig, axes = plt.subplots(1, 3, figsize=(12, 4))

# Example 1: Range frame - only shows axes within the data range
axes[0].plot(x, y)
range_frame(axes[0], x, y)
axes[0].set_title("Range Frame")

# Example 2: Top Y-label - places ylabel at top of y-axis
axes[1].plot(x, y)
ylabel_top("sin(x)", axes[1])
axes[1].set_title("Top Y-Label")

# Example 3: Identity line - adds a diagonal reference line
x_scatter = np.linspace(0, 1, 20)
y_scatter = x_scatter + 0.1*np.random.randn(20)
axes[2].scatter(x_scatter, y_scatter)
add_identity(axes[2], linestyle="--", color="gray")
axes[2].set_title("Identity Line")

plt.tight_layout()
plt.show()
```

<div align="center"> <img src="docs/static/plotting_functions.png" alt="Helper function examples" width="100%"/> <p><em>Left: Range Frame; Center: Top Y-Label; Right: Identity Line</em></p> </div>

### Decomposing a Figure by Legend Entries

`decompose_figure` takes a figure (or axes) that contains multiple labeled series and returns a list of `(label, figure)` tuples — one separate figure per legend entry.  This is useful when you want to highlight individual series from a combined plot, e.g. to include them separately in a paper or presentation.

```python
import matplotlib.pyplot as plt
import numpy as np
from lama_aesthetics import decompose_figure, get_style

get_style("main")

# Build a figure with several series
fig, ax = plt.subplots()
x = np.linspace(0, 2 * np.pi, 50)
ax.plot(x, np.sin(x), label="sin(x)")
ax.plot(x, np.cos(x), label="cos(x)")
ax.plot(x, np.sin(x) + np.cos(x), label="sin(x)+cos(x)")
ax.set_xlabel("x")
ax.set_ylabel("f(x)")
ax.set_title("Trigonometric Functions")
ax.legend()

# Split into individual figures — one per labeled series
parts = decompose_figure(fig)  # also accepts an Axes directly

for label, part_fig in parts:
    part_fig.savefig(f"{label}.png")
    plt.close(part_fig)
```

Each decomposed figure inherits the axis labels, title, limits, and scale of the original.  Pass `show_legend=False` to omit the legend from the individual figures.

Supported artist types: line plots, scatter plots, bar charts, and `fill_between` regions.

Repository initiated with [lamalab-org/cookiecutter-uv](https://github.com/lamalab-org/cookiecutter-uv).
