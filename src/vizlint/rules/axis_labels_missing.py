from __future__ import annotations

from typing import Optional

from ..core import Issue
from ..adapters.matplotlib import ChartSpec


def axis_labels_missing(chart: ChartSpec) -> Optional[Issue]:
    """Warn when a chart is missing descriptive axis labels."""
    missing = []
    if not chart.has_xlabel:
        missing.append("x-axis")
    if not chart.has_ylabel:
        missing.append("y-axis")

    if not missing:
        return None

    which = missing[0] if len(missing) == 1 else " and ".join(missing)
    return Issue(
        id="axis_labels_missing",
        severity="warn",
        message=f"Chart is missing a label for the {which}, which makes interpretation harder.",
        hint="Add descriptive axis labels (and units, if helpful) so viewers know what each axis represents.",
    )
