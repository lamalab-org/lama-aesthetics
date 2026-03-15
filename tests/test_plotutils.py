import matplotlib.pyplot as plt
import numpy as np

from lama_aesthetics.plotutils import add_identity, decompose_figure, range_frame, ylabel_top


def test_range_frame():
    """Test that range_frame sets axis limits correctly."""
    fig, ax = plt.subplots()
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([0, 2, 4, 6, 8])

    range_frame(ax, x, y, pad=0.1)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # Check that limits include all data points
    assert xlim[0] < x.min()
    assert xlim[1] > x.max()
    assert ylim[0] < y.min()
    assert ylim[1] > y.max()

    plt.close(fig)


def test_range_frame_per_axis_pad():
    """Test that pad_x and pad_y override the default pad independently."""
    fig, ax = plt.subplots()
    x = np.array([0, 1, 2, 3, 4])
    y = np.array([0, 2, 4, 6, 8])

    # pad_x controls padding near x-axis (vertical / y-limits)
    # pad_y controls padding near y-axis (horizontal / x-limits)
    range_frame(ax, x, y, pad_x=0.2, pad_y=0.0)

    xlim = ax.get_xlim()
    ylim = ax.get_ylim()

    # pad_y=0.0 → x-limits equal data range (no horizontal padding)
    assert xlim[0] == x.min()
    assert xlim[1] == x.max()

    # pad_x=0.2 → y-limits have vertical padding
    y_range = y.max() - y.min()
    assert ylim[0] < y.min()
    assert ylim[1] > y.max()
    assert abs(ylim[0] - (y.min() - 0.2 * y_range)) < 1e-10
    assert abs(ylim[1] - (y.max() + 0.2 * y_range)) < 1e-10

    plt.close(fig)


def test_range_frame_non_numeric_x_axis():
    """Non-numeric x values should use 0..len(x)-1 for the range frame."""
    fig, ax = plt.subplots()
    x = ["a", "b", "c", "d"]
    y = np.array([0, 2, 4, 6])

    ax.plot(x, y)
    range_frame(ax, x, y, pad=0.1)

    xlim = ax.get_xlim()

    assert xlim == (0.0, float(len(x) - 1))
    assert ax.spines["bottom"].get_bounds() == (0, len(x) - 1)

    plt.close(fig)


def test_range_frame_non_numeric_y_axis():
    """Non-numeric y values should use 0..len(y)-1 for the range frame."""
    fig, ax = plt.subplots()
    x = np.array([0, 1, 2, 3])
    y = ["low", "mid", "high", "top"]

    ax.plot(x, y)
    range_frame(ax, x, y, pad=0.1)

    ylim = ax.get_ylim()

    assert ylim == (0.0, float(len(y) - 1))
    assert ax.spines["left"].get_bounds() == (0, len(y) - 1)

    plt.close(fig)


def test_ylabel_top():
    """Test that ylabel_top sets ylabel without errors."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2])

    # Should not raise an exception
    ylabel_top("Test Label", ax=ax)

    # Check that ylabel was set
    assert ax.get_ylabel() == "Test Label"

    plt.close(fig)


def test_ylabel_top_no_ax():
    """Test that ylabel_top works without explicit axes argument."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2])

    # Should use current axes
    ylabel_top("Test Label")

    assert ax.get_ylabel() == "Test Label"

    plt.close(fig)


def test_add_identity():
    """Test that add_identity adds a 1:1 line to the plot."""
    fig, ax = plt.subplots()
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)

    result = add_identity(ax)

    # Should return the axes object
    assert result == ax

    plt.close(fig)


# --- decompose_figure tests ------------------------------------------------


def test_decompose_figure_lines():
    """decompose_figure should return one figure per labelled line."""
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 4], label="Linear")
    ax.plot([0, 1, 2], [0, 2, 8], label="Steep")
    ax.set_xlabel("x")
    ax.set_ylabel("y")
    ax.set_title("My Plot")

    parts = decompose_figure(fig)

    assert len(parts) == 2
    assert parts[0][0] == "Linear"
    assert parts[1][0] == "Steep"

    # Each returned figure should have exactly one line on its axes
    for label, part_fig in parts:
        part_ax = part_fig.get_axes()[0]
        labelled_lines = [line for line in part_ax.get_lines() if not line.get_label().startswith("_")]
        assert len(labelled_lines) == 1
        assert labelled_lines[0].get_label() == label
        # Axes metadata preserved
        assert part_ax.get_xlabel() == "x"
        assert part_ax.get_ylabel() == "y"
        assert part_ax.get_title() == "My Plot"

    for _, f in parts:
        plt.close(f)
    plt.close(fig)


def test_decompose_figure_scatter():
    """decompose_figure should handle scatter plots."""
    fig, ax = plt.subplots()
    ax.scatter([0, 1], [2, 3], label="Group A")
    ax.scatter([4, 5], [6, 7], label="Group B")

    parts = decompose_figure(fig)

    assert len(parts) == 2
    assert {p[0] for p in parts} == {"Group A", "Group B"}

    for _, f in parts:
        plt.close(f)
    plt.close(fig)


def test_decompose_figure_bars():
    """decompose_figure should handle bar plots."""
    fig, ax = plt.subplots()
    ax.bar([0, 1, 2], [3, 4, 5], label="Series 1")
    ax.bar([0, 1, 2], [1, 2, 3], bottom=[3, 4, 5], label="Series 2")

    parts = decompose_figure(fig)

    assert len(parts) == 2
    assert parts[0][0] == "Series 1"
    assert parts[1][0] == "Series 2"

    for _, f in parts:
        plt.close(f)
    plt.close(fig)


def test_decompose_figure_skips_unlabelled():
    """Artists without a label or with _-prefixed labels should be skipped."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1])  # no label
    ax.plot([0, 1], [0, 2], label="_hidden")
    ax.plot([0, 1], [0, 3], label="Visible")

    parts = decompose_figure(fig)

    assert len(parts) == 1
    assert parts[0][0] == "Visible"

    for _, f in parts:
        plt.close(f)
    plt.close(fig)


def test_decompose_figure_accepts_axes():
    """decompose_figure should accept a single Axes object."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], label="A")
    ax.plot([0, 1], [0, 2], label="B")

    parts = decompose_figure(ax)  # pass Axes, not Figure

    assert len(parts) == 2

    for _, f in parts:
        plt.close(f)
    plt.close(fig)


def test_decompose_figure_no_legend():
    """When show_legend=False no legend should be present."""
    fig, ax = plt.subplots()
    ax.plot([0, 1], [0, 1], label="A")

    parts = decompose_figure(fig, show_legend=False)

    assert len(parts) == 1
    part_ax = parts[0][1].get_axes()[0]
    assert part_ax.get_legend() is None

    for _, f in parts:
        plt.close(f)
    plt.close(fig)


def test_decompose_figure_preserves_limits():
    """Axis limits should be the same as the original plot."""
    fig, ax = plt.subplots()
    ax.plot([0, 10], [0, 100], label="A")
    ax.plot([0, 10], [100, 0], label="B")
    original_xlim = ax.get_xlim()
    original_ylim = ax.get_ylim()

    parts = decompose_figure(fig)

    for _, part_fig in parts:
        part_ax = part_fig.get_axes()[0]
        assert part_ax.get_xlim() == original_xlim
        assert part_ax.get_ylim() == original_ylim

    for _, f in parts:
        plt.close(f)
    plt.close(fig)
