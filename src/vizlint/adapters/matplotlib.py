from __future__ import annotations
from dataclasses import dataclass
import math
from typing import Any, Iterable, List, Optional, Tuple


try:  # pragma: no cover - handled at runtime when matplotlib is present
    from matplotlib.axes import Axes  # type: ignore
    from matplotlib.container import BarContainer  # type: ignore
    from matplotlib.figure import Figure  # type: ignore
except Exception:  # pragma: no cover - matplotlib is optional until linting time
    Axes = Figure = BarContainer = None


@dataclass
class ChartSpec:
    kind: str  # "bar" | "line" | "scatter" | "hist" | "unknown"
    value_axis: str  # "x" or "y" depending on which axis encodes magnitudes
    ylim: Tuple[float, float]  # historical name; represents the value-axis limits
    has_bar_container: bool
    has_xlabel: bool
    has_ylabel: bool
    has_title: bool
    data_y_min: Optional[float]
    data_y_max: Optional[float]


def _detect_kind(ax: Any) -> Tuple[str, bool]:
    # Bars in matplotlib are stored as BarContainer objects in ax.containers
    has_bar = any(isinstance(c, BarContainer) if BarContainer else c.__class__.__name__ == "BarContainer" for c in getattr(ax, "containers", []))
    if has_bar:
        return "bar", True
    if getattr(ax, "lines", []):
        return "line", False
    if getattr(ax, "collections", []):
        return "scatter", False
    return "unknown", False


def _finite(values: Iterable[Any]) -> List[float]:
    clean: List[float] = []
    for value in values:
        try:
            as_float = float(value)
        except (TypeError, ValueError):
            continue
        if math.isfinite(as_float):
            clean.append(as_float)
    return clean


def _resolve_bar_orientation(container: Any) -> str:
    orientation = getattr(container, "orientation", None)
    if orientation in {"horizontal", "vertical"}:
        return orientation
    for patch in getattr(container, "patches", []):
        width = getattr(patch, "get_width", lambda: 0)()
        height = getattr(patch, "get_height", lambda: 0)()
        if abs(width) > abs(height):
            return "horizontal"
    return "vertical"


def to_chart_specs(fig_or_ax: Any) -> List[ChartSpec]:
    if Figure is not None and isinstance(fig_or_ax, Figure):
        axes = list(fig_or_ax.axes)
    elif Axes is not None and isinstance(fig_or_ax, Axes):
        axes = [fig_or_ax]
    else:
        axes_attr = getattr(fig_or_ax, "axes", None)
        if isinstance(axes_attr, (list, tuple)):
            axes = list(axes_attr)
        else:
            axes = [fig_or_ax]

    specs: List[ChartSpec] = []
    for ax in axes:
        kind, has_bar = _detect_kind(ax)

        value_axis = "y"
        axis_limits: Tuple[float, float] = ax.get_ylim()

        data_y_min: Optional[float] = None
        data_y_max: Optional[float] = None

        if has_bar:
            values: List[float] = []
            orientation = None
            for container in getattr(ax, "containers", []):
                orientation = orientation or _resolve_bar_orientation(container)
                for patch in getattr(container, "patches", []):
                    if (orientation or "vertical") == "horizontal":
                        start = getattr(patch, "get_x", lambda: 0)()
                        end = start + getattr(patch, "get_width", lambda: 0)()
                    else:
                        start = getattr(patch, "get_y", lambda: 0)()
                        end = start + getattr(patch, "get_height", lambda: 0)()
                    values.extend([start, end])

            clean_values = _finite(values)
            if clean_values:
                data_y_min = min(clean_values)
                data_y_max = max(clean_values)

            if (orientation or "vertical") == "horizontal":
                value_axis = "x"
                axis_limits = ax.get_xlim()
        elif kind == "line":
            ys = []
            for line in getattr(ax, "lines", []):
                ys.extend(line.get_ydata())
            clean_values = _finite(ys)
            if clean_values:
                data_y_min = min(clean_values)
                data_y_max = max(clean_values)

        specs.append(
            ChartSpec(
                kind=kind,
                value_axis=value_axis,
                ylim=axis_limits,
                has_bar_container=has_bar,
                has_xlabel=bool(ax.get_xlabel()),
                has_ylabel=bool(ax.get_ylabel()),
                has_title=bool(ax.get_title()),
                data_y_min=data_y_min,
                data_y_max=data_y_max,
            )
        )
    return specs
