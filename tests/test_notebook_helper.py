import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import vizlint


def test_lint_last_returns_report_for_current_figure(capsys):
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])

    report = vizlint.lint_last()

    from vizlint.core import Report

    assert isinstance(report, Report)

    captured = capsys.readouterr()
    assert captured.out.strip()


def test_lint_last_uses_latest_figure():
    fig1, ax1 = plt.subplots()
    ax1.plot([0, 1], [0, 1])

    fig2, ax2 = plt.subplots()
    ax2.bar(["A", "B"], [101, 103])
    ax2.set_ylim(100, 104)

    report = vizlint.lint_last()
    issue_ids = {issue.id for issue in report.issues}

    assert isinstance(issue_ids, set)
