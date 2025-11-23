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

    ymin, ymax = chart.ylim

    # Degenerate limits show the user is doing something odd; skip to avoid noise.
    if ymax <= ymin:
        return None

    includes_zero = ymin <= 0 <= ymax
    if includes_zero:
        return None

    return Issue(
        id="bar_zero_baseline",
        severity="warn",
        message="Bar chart y-axis does not include zero, which can exaggerate differences between bars.",
        hint="Consider starting the y-axis at zero or switch to a different chart type if you need to zoom in.",
    )
