import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import vizlint


def test_bar_chart_with_non_zero_baseline_reports_issue():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [101, 103])
    ax.set_ylim(100, 104)

    report = vizlint.lint(fig)
    issues = [i for i in report.issues if i.id == "bar_zero_baseline"]

    assert issues, "Expected bar_zero_baseline issue for truncated y-axis"
    issue = issues[0]
    assert issue.severity == "warn"
    assert "axis" in issue.message.lower()


def test_bar_chart_with_zero_baseline_is_clean():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [101, 103])
    ax.set_ylim(0, 120)

    report = vizlint.lint(fig)
    assert all(i.id != "bar_zero_baseline" for i in report.issues)


def test_non_bar_charts_are_ignored():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [100, 101, 102])
    ax.set_ylim(100, 104)

    report = vizlint.lint(fig)
    assert all(i.id != "bar_zero_baseline" for i in report.issues)


def test_barh_chart_uses_x_axis_limits():
    fig, ax = plt.subplots()
    ax.barh(["A", "B"], [10, 12])
    ax.set_xlim(5, 15)

    report = vizlint.lint(fig)
    issues = [i for i in report.issues if i.id == "bar_zero_baseline"]
    assert issues, "Expected bar_zero_baseline to respect x-axis baseline"
    assert "x-axis" in issues[0].message.lower()


def test_lint_accepts_axes_objects():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [0, 1, 2])

    report = vizlint.lint(ax)
    assert isinstance(report, vizlint.Report)
