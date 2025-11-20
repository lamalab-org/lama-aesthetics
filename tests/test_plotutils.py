import matplotlib.pyplot as plt
import numpy as np

from lama_aesthetics.plotutils import add_identity, range_frame, ylabel_top


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
