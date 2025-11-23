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
    assert "y-axis" in issue.message.lower()


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
