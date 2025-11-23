from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Callable, List, Optional


@dataclass
class Issue:
    id: str
    severity: str  # "error" | "warn" | "info"
    message: str
    hint: Optional[str] = None


@dataclass
class Report:
    issues: List[Issue] = field(default_factory=list)

    def add(self, issue: Issue) -> None:
        self.issues.append(issue)

    def is_clean(self) -> bool:
        return not self.issues

    def summary(self) -> str:
        if not self.issues:
            return "vizlint: no issues found ✅"
        lines = ["vizlint report:"]
        for i in self.issues:
            hint_text = f" Hint: {i.hint}" if i.hint else ""
            lines.append(f"- {i.severity.upper()} [{i.id}] {i.message}{hint_text}")
        return "\n".join(lines)


# ---- Lint orchestration ----

RuleFn = Callable[[Any], Optional[Issue]]


def _is_matplotlib_obj(obj: Any) -> bool:
    return hasattr(obj, "axes") or obj.__class__.__module__.startswith("matplotlib.")


def lint(fig_or_ax: Any, rules: Optional[List[RuleFn]] = None) -> Report:
    """
    Lint a matplotlib Figure or Axes and return a Report.
    """
    report = Report()

    # Lazy import to avoid requiring matplotlib unless used
    if not _is_matplotlib_obj(fig_or_ax):
        report.add(
            Issue(
                id="unsupported_object",
                severity="error",
                message=f"Object of type {type(fig_or_ax)} not supported yet.",
                hint="Pass a matplotlib.figure.Figure or matplotlib.axes.Axes.",
            )
        )
        return report

    from .adapters.matplotlib import to_chart_specs
    from .rules.bar_zero_baseline import bar_zero_baseline
    from .rules.axis_labels_missing import axis_labels_missing

    chart_specs = to_chart_specs(fig_or_ax)
    active_rules = rules or [bar_zero_baseline, axis_labels_missing]

    for chart in chart_specs:
        for rule in active_rules:
            issue = rule(chart)
            if issue:
                report.add(issue)

    return report
