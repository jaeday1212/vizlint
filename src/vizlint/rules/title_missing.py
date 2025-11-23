from __future__ import annotations

from typing import Optional

from ..core import Issue
from ..adapters.matplotlib import ChartSpec


def title_missing(chart: ChartSpec) -> Optional[Issue]:
    """Warn when a chart omits a title."""
    if chart.has_title:
        return None

    return Issue(
        id="title_missing",
        severity="warn",
        message=(
            "Chart is missing a title, which can make it harder for viewers to quickly understand the visualization."
        ),
        hint="Add a concise title that summarizes what the chart shows.",
    )
