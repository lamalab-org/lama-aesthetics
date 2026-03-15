from typing import List, Optional, Tuple, Union

import matplotlib.pyplot as plt
import numpy as np
from matplotlib.collections import PathCollection, PolyCollection
from matplotlib.container import BarContainer
from matplotlib.figure import Figure
from matplotlib.lines import Line2D
from matplotlib.ticker import MaxNLocator


def _get_axis_bounds(values):
    """Return axis bounds for numeric or categorical values."""
    arr = np.asarray(values)

    try:
        numeric_arr = np.asarray(values, dtype=float)
    except (TypeError, ValueError):
        return 0, max(len(arr) - 1, 0), False

    return numeric_arr.min(), numeric_arr.max(), True


def _nice_tick_bounds(data_min, data_max):
    """Return nice tick positions and spine bounds that strictly bracket the data.

    Uses matplotlib's ``MaxNLocator`` to compute tick positions for the
    data range and then selects the outermost ticks as spine bounds.
    The returned bounds are guaranteed to satisfy
    ``bound_lo <= data_min`` and ``bound_hi >= data_max``, and every
    tick between the bounds (inclusive) is included.

    Args:
        data_min: Minimum value present in the data.
        data_max: Maximum value present in the data.

    Returns:
        ``(bound_lo, bound_hi, ticks)`` where *ticks* is a 1-D array of
        the tick positions that fall within ``[bound_lo, bound_hi]``.
    """
    if data_min == data_max:
        # Degenerate case — expand symmetrically so the locator has a range.
        if data_min == 0:
            data_min, data_max = -0.5, 0.5
        else:
            delta = abs(data_min) * 0.1
            data_min, data_max = data_min - delta, data_max + delta

    locator = MaxNLocator(nbins="auto", steps=[1, 2, 2.5, 5, 10])
    ticks = np.asarray(locator.tick_values(data_min, data_max))

    # The locator already returns values that bracket [data_min, data_max],
    # but enforce the invariant explicitly.
    bound_lo = float(ticks[ticks <= data_min + 1e-12].max()) if np.any(ticks <= data_min + 1e-12) else float(ticks[0])
    bound_hi = float(ticks[ticks >= data_max - 1e-12].min()) if np.any(ticks >= data_max - 1e-12) else float(ticks[-1])

    # Keep only ticks within the chosen bounds.
    mask = (ticks >= bound_lo - 1e-12) & (ticks <= bound_hi + 1e-12)
    ticks = ticks[mask]

    return bound_lo, bound_hi, ticks


def range_frame(ax, x, y, pad=0.1, pad_x=None, pad_y=None, nice=True):
    """
    Set the limits of the axes to include all data points with a padding of
    `pad` times the range of the data. This is useful to ensure that the data
    points are not cut off by the axes.

    Per-axis padding can be controlled with ``pad_x`` and ``pad_y``.  When
    either is *None* (the default) the value of ``pad`` is used instead.

    When ``nice`` is *True* (the default) and the axis carries numerical
    data, the spine bounds are snapped to nice tick positions that bracket
    the data, so that the axis line starts and ends exactly at tick marks.
    Tick positions are computed via matplotlib's ``MaxNLocator`` and
    explicitly set on the axes so there is no drift between ticks and
    spine endpoints.  The ``pad`` / ``pad_x`` / ``pad_y`` parameters are
    ignored for any axis that receives nice bounds.

    Args:
        ax: The axes object.
        x: The x-coordinates of the data points.
        y: The y-coordinates of the data points.
        pad: The default padding factor applied to both axes.
        pad_x: Padding near the x-axis (vertical direction). Overrides ``pad`` when set.
        pad_y: Padding near the y-axis (horizontal direction). Overrides ``pad`` when set.
        nice: If *True* (default), snap numeric spine bounds to nice tick
            positions that bracket the data.
    """
    if pad_x is None:
        pad_x = pad
    if pad_y is None:
        pad_y = pad

    y_min, y_max, y_is_numeric = _get_axis_bounds(y)
    x_min, x_max, x_is_numeric = _get_axis_bounds(x)

    # --- Y axis ------------------------------------------------------------
    if y_is_numeric:
        if nice:
            y_bound_min, y_bound_max, y_ticks = _nice_tick_bounds(y_min, y_max)
            ax.set_yticks(y_ticks)
            ax.set_ylim(y_bound_min, y_bound_max)
        else:
            y_bound_min = y_min
            y_bound_max = y_max
            ax.set_ylim(y_min - pad_x * (y_max - y_min), y_max + pad_x * (y_max - y_min))
    else:
        y_bound_min, y_bound_max = y_min, y_max
        ax.set_ylim(y_min, y_max)

    # --- X axis ------------------------------------------------------------
    if x_is_numeric:
        if nice:
            x_bound_min, x_bound_max, x_ticks = _nice_tick_bounds(x_min, x_max)
            ax.set_xticks(x_ticks)
            ax.set_xlim(x_bound_min, x_bound_max)
        else:
            x_bound_min = x_min
            x_bound_max = x_max
            ax.set_xlim(x_min - pad_y * (x_max - x_min), x_max + pad_y * (x_max - x_min))
    else:
        x_bound_min, x_bound_max = x_min, x_max
        ax.set_xlim(x_min, x_max)

    ax.spines["left"].set_position(("outward", 10))
    ax.spines["bottom"].set_position(("outward", 10))

    ax.spines["bottom"].set_bounds(x_bound_min, x_bound_max)
    ax.spines["left"].set_bounds(y_bound_min, y_bound_max)


def ylabel_top(string: str, ax: Optional[plt.Axes] = None, x_pad: float = 0.01, y_pad: float = 0.02) -> None:
    """
    Rotate the ylabel (such that you can read it comfortably) and place it
    above the top ytick. This requires some logic, so it cannot be
    incorporated in `style`. See
    <https://stackoverflow.com/a/27919217/353337> on how to get the axes
    coordinates of the top ytick.

    Args:
        string: The string to be displayed as the ylabel.
        ax: The axes object.
        x_pad: The x-padding in axes coordinates.
        y_pad: The y-padding in axes coordinates.
    """
    if ax is None:
        ax = plt.gca()

    yticks_pos = ax.get_yticks()
    coords = np.column_stack([np.zeros_like(yticks_pos), yticks_pos])
    data_to_axis = ax.transData + ax.transAxes.inverted()
    yticks_pos_ax = data_to_axis.transform(coords)[:, 1]
    # filter out the ticks which aren't shown
    tol = 1.0e-5
    yticks_pos_ax = yticks_pos_ax[(-tol < yticks_pos_ax) & (yticks_pos_ax < 1.0 + tol)]
    if len(yticks_pos_ax) > 0:
        pos_y = yticks_pos_ax[-1] + 0.1
    else:
        pos_y = 1.0

    # Get the padding in axes coordinates. The below logic isn't quite correct, so keep
    # an eye on <https://stackoverflow.com/q/67872207/353337> and
    # <https://discourse.matplotlib.org/t/get-ytick-label-distance-in-axis-coordinates/22210>
    # and
    # <https://github.com/matplotlib/matplotlib/issues/20677>
    yticks = ax.yaxis.get_major_ticks()
    if len(yticks) == 0:
        pos_x = 0.0
    else:
        pad_pt = yticks[-1].get_pad()
        # https://stackoverflow.com/a/51213884/353337
        # ticklen_pt = ax.yaxis.majorTicks[0].tick1line.get_markersize()
        # dist_in = (pad_pt + ticklen_pt) / 72.0
        dist_in = pad_pt / 72.0
        # get axes width in inches
        # https://stackoverflow.com/a/19306776/353337
        bbox = ax.get_window_extent().transformed(plt.gcf().dpi_scale_trans.inverted())
        pos_x = -dist_in / bbox.width

    yl = ax.set_ylabel(string, horizontalalignment="right", multialignment="right")
    # place the label 10% above the top tick
    ax.yaxis.set_label_coords(pos_x - x_pad, pos_y + y_pad)
    yl.set_rotation(0)


def add_identity(axes, *line_args, **line_kwargs):
    """
    Add a 1:1 line to the axes. This is useful to compare the data to a

    Args:
        axes: The axes object.
        line_args: The positional arguments for the line.
        line_kwargs: The keyword arguments for the line.
    """
    (identity,) = axes.plot([], [], *line_args, **line_kwargs)

    def callback(axes):
        low_x, high_x = axes.get_xlim()
        low_y, high_y = axes.get_ylim()
        low = max(low_x, low_y)
        high = min(high_x, high_y)
        identity.set_data([low, high], [low, high])

    callback(axes)
    axes.callbacks.connect("xlim_changed", callback)
    axes.callbacks.connect("ylim_changed", callback)
    return axes


def _setup_axes_like(source_ax: plt.Axes, target_ax: plt.Axes) -> None:
    """Copy axis labels, title, limits, scales, and spine visibility from *source_ax* to *target_ax*."""
    target_ax.set_xlim(source_ax.get_xlim())
    target_ax.set_ylim(source_ax.get_ylim())
    target_ax.set_xlabel(source_ax.get_xlabel())
    target_ax.set_ylabel(source_ax.get_ylabel())
    target_ax.set_title(source_ax.get_title())
    target_ax.set_xscale(source_ax.get_xscale())
    target_ax.set_yscale(source_ax.get_yscale())

    # Copy tick parameters
    target_ax.set_xticks(source_ax.get_xticks())
    target_ax.set_yticks(source_ax.get_yticks())
    try:
        target_ax.set_xticklabels([t.get_text() for t in source_ax.get_xticklabels()])
        target_ax.set_yticklabels([t.get_text() for t in source_ax.get_yticklabels()])
    except Exception:
        pass

    # Re-apply limits after setting ticks (ticks can change limits)
    target_ax.set_xlim(source_ax.get_xlim())
    target_ax.set_ylim(source_ax.get_ylim())

    # Copy spine visibility
    for spine_name in ("top", "bottom", "left", "right"):
        target_ax.spines[spine_name].set_visible(source_ax.spines[spine_name].get_visible())
        target_ax.spines[spine_name].set_bounds(*source_ax.spines[spine_name].get_bounds()) if source_ax.spines[spine_name].get_bounds() else None
        target_ax.spines[spine_name].set_position(source_ax.spines[spine_name].get_position())

    # Copy grid state
    target_ax.grid(source_ax.xaxis.get_gridlines()[0].get_visible() if source_ax.xaxis.get_gridlines() else False)


def _replay_line(source_line: Line2D, target_ax: plt.Axes) -> None:
    """Re-draw a Line2D artist onto *target_ax*."""
    target_ax.plot(
        source_line.get_xdata(),
        source_line.get_ydata(),
        color=source_line.get_color(),
        linestyle=source_line.get_linestyle(),
        linewidth=source_line.get_linewidth(),
        marker=source_line.get_marker(),
        markersize=source_line.get_markersize(),
        markerfacecolor=source_line.get_markerfacecolor(),
        markeredgecolor=source_line.get_markeredgecolor(),
        markeredgewidth=source_line.get_markeredgewidth(),
        alpha=source_line.get_alpha(),
        label=source_line.get_label(),
    )


def _replay_scatter(source_coll: PathCollection, target_ax: plt.Axes, label: str) -> None:
    """Re-draw a scatter PathCollection onto *target_ax*."""
    offsets = source_coll.get_offsets()
    if len(offsets) == 0:
        return
    facecolors = source_coll.get_facecolor()
    edgecolors = source_coll.get_edgecolor()
    sizes = source_coll.get_sizes()
    target_ax.scatter(
        offsets[:, 0],
        offsets[:, 1],
        color=facecolors if len(facecolors) > 1 else facecolors[0],
        edgecolors=edgecolors if len(edgecolors) > 1 else edgecolors[0],
        s=sizes if len(sizes) > 1 else sizes[0],
        alpha=source_coll.get_alpha(),
        label=label,
    )


def _replay_bar(container: BarContainer, target_ax: plt.Axes) -> None:
    """Re-draw a BarContainer onto *target_ax*."""
    for patch in container.patches:
        target_ax.bar(
            patch.get_x() + patch.get_width() / 2,
            patch.get_height(),
            width=patch.get_width(),
            bottom=patch.get_y(),
            color=patch.get_facecolor(),
            edgecolor=patch.get_edgecolor(),
            linewidth=patch.get_linewidth(),
            alpha=patch.get_alpha(),
            label=container.get_label() if patch is container.patches[0] else None,
        )


def _replay_fill(source_coll: PolyCollection, target_ax: plt.Axes, label: str) -> None:
    """Re-draw a PolyCollection (e.g. fill_between) onto *target_ax*."""
    for path in source_coll.get_paths():
        verts = path.vertices
        target_ax.fill(
            verts[:, 0],
            verts[:, 1],
            facecolor=source_coll.get_facecolor()[0],
            edgecolor=source_coll.get_edgecolor()[0] if len(source_coll.get_edgecolor()) > 0 else None,
            alpha=source_coll.get_alpha(),
            label=label,
        )
        label = None  # only label the first polygon


def decompose_figure(
    fig_or_ax: Union[Figure, plt.Axes],
    *,
    show_legend: bool = True,
) -> List[Tuple[str, Figure]]:
    """Decompose a matplotlib figure into individual figures, one per labeled artist.

    Each returned figure contains a single plotted element (line, scatter,
    bar group, fill, …) together with the same axis labels, limits, and
    title as the original.  Only artists that carry a label (and would
    therefore appear in a legend) are considered; artists whose label
    starts with ``_`` are skipped, following the matplotlib convention.

    Args:
        fig_or_ax: A :class:`~matplotlib.figure.Figure` or a single
            :class:`~matplotlib.axes.Axes` instance.  When a *Figure*
            is given the first ``Axes`` is used.
        show_legend: If *True* (default) a legend is added to every
            decomposed figure.

    Returns:
        A list of ``(label, figure)`` tuples where *label* is the
        legend text associated with the artist and *figure* is a new
        :class:`~matplotlib.figure.Figure` containing only that artist.

    Example::

        fig, ax = plt.subplots()
        ax.plot([0, 1], [0, 1], label="Linear")
        ax.plot([0, 1], [0, 2], label="Steep")

        parts = decompose_figure(fig)
        for label, part_fig in parts:
            part_fig.savefig(f"{label}.png")
    """
    # Resolve axes ----------------------------------------------------------
    if isinstance(fig_or_ax, Figure):
        axes_list = fig_or_ax.get_axes()
        if not axes_list:
            return []
        source_ax = axes_list[0]
        source_fig = fig_or_ax
    else:
        source_ax = fig_or_ax
        source_fig = fig_or_ax.get_figure()

    figsize = source_fig.get_size_inches()

    # Collect labelled artists ----------------------------------------------
    items: List[Tuple[str, object]] = []

    # 1. Lines
    for line in source_ax.get_lines():
        lbl = line.get_label()
        if lbl and not lbl.startswith("_"):
            items.append((lbl, line))

    # 2. Bar containers
    for container in source_ax.containers:
        if isinstance(container, BarContainer):
            lbl = container.get_label()
            if lbl and not lbl.startswith("_"):
                items.append((lbl, container))

    # 3. Collections (scatter / fill_between)
    for coll in source_ax.collections:
        lbl = coll.get_label()
        if lbl and not lbl.startswith("_"):
            items.append((lbl, coll))

    # Build one figure per item ---------------------------------------------
    results: List[Tuple[str, Figure]] = []
    for label, artist in items:
        new_fig, new_ax = plt.subplots(figsize=figsize)

        # Reproduce axes properties
        _setup_axes_like(source_ax, new_ax)

        # Replay the single artist
        if isinstance(artist, Line2D):
            _replay_line(artist, new_ax)
        elif isinstance(artist, BarContainer):
            _replay_bar(artist, new_ax)
        elif isinstance(artist, PathCollection):
            _replay_scatter(artist, new_ax, label)
        elif isinstance(artist, PolyCollection):
            _replay_fill(artist, new_ax, label)

        if show_legend:
            new_ax.legend()

        new_fig.tight_layout()
        results.append((label, new_fig))

    return results
