from __future__ import annotations
from dataclasses import dataclass
from typing import Any, List, Tuple


@dataclass
class ChartSpec:
    kind: str  # "bar" | "line" | "scatter" | "hist" | "unknown"
    ylim: Tuple[float, float]
    has_bar_container: bool


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
        specs.append(
            ChartSpec(
                kind=kind,
                ylim=ax.get_ylim(),
                has_bar_container=has_bar,
            )
        )
    return specs
