from __future__ import annotations

from typing import Optional

from ..core import Issue
from ..adapters.matplotlib import ChartSpec


def axis_range_overexpanded(chart: ChartSpec) -> Optional[Issue]:
    """Warn when the y-axis span dwarfs the actual data range, hiding real change."""
    data_y_min = chart.data_y_min
    data_y_max = chart.data_y_max

    if data_y_min is None or data_y_max is None:
        return None

    axis_min, axis_max = chart.ylim
    if axis_max <= axis_min or data_y_max <= data_y_min:
        return None

    axis_span = axis_max - axis_min
    data_span = data_y_max - data_y_min
    ratio = axis_span / data_span
    if ratio < 20.0:
        return None

    slack_low = (data_y_min - axis_min) / axis_span
    slack_high = (axis_max - data_y_max) / axis_span
    if slack_low < 0.1 or slack_high < 0.1:
        return None

    axis_name = "y-axis" if chart.value_axis == "y" else "x-axis"

    return Issue(
        id="axis_range_overexpanded",
        severity="warn",
        message=(
            f"{axis_name.capitalize()} range is much larger than the data range, which can make changes look smaller than they are."
        ),
        hint="Tighten the value-axis limits so they track the data range while leaving a small buffer.",
    )
