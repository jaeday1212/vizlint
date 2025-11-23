from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Optional, Tuple


@dataclass
class ChartSpec:
    kind: str  # "bar" | "line" | "scatter" | "hist" | "unknown"
    ylim: Tuple[float, float]
    has_bar_container: bool
    has_xlabel: bool
    has_ylabel: bool
    has_title: bool
    data_y_min: Optional[float]
    data_y_max: Optional[float]


def _detect_kind(ax: Any) -> Tuple[str, bool]:
    # Bars in matplotlib are stored as BarContainer objects in ax.containers
    has_bar = any(c.__class__.__name__ == "BarContainer" for c in getattr(ax, "containers", []))
    if has_bar:
        return "bar", True
    if getattr(ax, "lines", []):
        return "line", False
    if getattr(ax, "collections", []):
        return "scatter", False
    return "unknown", False


def to_chart_specs(fig_or_ax: Any) -> List[ChartSpec]:
    axes = fig_or_ax.axes if hasattr(fig_or_ax, "axes") else [fig_or_ax]
    specs: List[ChartSpec] = []
    for ax in axes:
        kind, has_bar = _detect_kind(ax)

        data_y_min: Optional[float] = None
        data_y_max: Optional[float] = None

        if has_bar:
            ys: List[float] = []
            for container in getattr(ax, "containers", []):
                for patch in getattr(container, "patches", []):
                    y0 = patch.get_y()
                    y1 = y0 + patch.get_height()
                    ys.append(y0)
                    ys.append(y1)
            if ys:
                data_y_min = min(ys)
                data_y_max = max(ys)
        elif kind == "line":
            ys = []
            for line in getattr(ax, "lines", []):
                ys.extend(line.get_ydata())
            if ys:
                data_y_min = min(ys)
                data_y_max = max(ys)

        specs.append(
            ChartSpec(
                kind=kind,
                ylim=ax.get_ylim(),
                has_bar_container=has_bar,
                has_xlabel=bool(ax.get_xlabel()),
                has_ylabel=bool(ax.get_ylabel()),
                has_title=bool(ax.get_title()),
                data_y_min=data_y_min,
                data_y_max=data_y_max,
            )
        )
    return specs
