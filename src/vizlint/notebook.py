from __future__ import annotations

import matplotlib.pyplot as plt

from .core import Report, lint


def lint_last() -> Report:
    """Lint the current Matplotlib figure and print a summary."""
    fig = plt.gcf()
    report = lint(fig)
    print(report.summary())
    return report
