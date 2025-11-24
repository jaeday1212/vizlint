from __future__ import annotations

from .core import Report, lint


def lint_last() -> Report:
    """Lint the current Matplotlib figure and print a summary."""
    try:
        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - requires notebook/runtime env
        raise RuntimeError("matplotlib is required to lint the active figure") from exc

    fig = plt.gcf()
    report = lint(fig)
    print(report.summary())
    return report
