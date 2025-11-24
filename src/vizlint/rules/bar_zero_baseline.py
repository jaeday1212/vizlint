from __future__ import annotations
from typing import Optional

from ..core import Issue
from ..adapters.matplotlib import ChartSpec


def bar_zero_baseline(chart: ChartSpec) -> Optional[Issue]:
    """
    Warn when a bar chart hides zero on the y-axis, which can exaggerate
    perceived deltas between bars.
    """
    if chart.kind != "bar" or not chart.has_bar_container:
        return None

    axis_min, axis_max = chart.ylim

    # Degenerate limits show the user is doing something odd; skip to avoid noise.
    if axis_max <= axis_min:
        return None

    includes_zero = axis_min <= 0 <= axis_max
    if includes_zero:
        return None

    axis_name = "y-axis" if chart.value_axis == "y" else "x-axis"

    return Issue(
        id="bar_zero_baseline",
        severity="warn",
        message=(
            f"Bar chart {axis_name} does not include zero, which can exaggerate differences between bars."
        ),
        hint=(
            "Consider starting the value axis at zero or switch to a different chart type if you need to zoom in."
        ),
    )
