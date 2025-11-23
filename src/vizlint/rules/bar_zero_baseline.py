from __future__ import annotations
from typing import Optional

from ..core import Issue
from ..adapters.matplotlib import ChartSpec


def bar_zero_baseline(chart: ChartSpec) -> Optional[Issue]:
    """Bar charts should include zero on the y-axis unless explicitly justified."""
    if chart.kind != "bar" or not chart.has_bar_container:
        return None

    y0, _ = chart.ylim
    if y0 > 0:
        return Issue(
            id="bar_zero_baseline",
            severity="error",
            message=f"Bar chart y-axis starts at {y0:.3g} instead of 0; may exaggerate differences.",
            hint="Set ylim bottom to 0 (e.g., ax.set_ylim(bottom=0)) or add an axis-break annotation.",
        )

    return None
