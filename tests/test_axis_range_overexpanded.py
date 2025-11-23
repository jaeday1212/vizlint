import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import vizlint


def test_overexpanded_axis_reports_issue():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [56, 57, 59])
    ax.set_ylim(0, 200)

    report = vizlint.lint(fig)
    issues = [i for i in report.issues if i.id == "axis_range_overexpanded"]

    assert issues, "Expected axis_range_overexpanded issue for extremely over-expanded y-axis"
    issue = issues[0]
    assert issue.severity == "warn"
    assert "y-axis" in issue.message.lower()


def test_tight_axis_is_clean():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [56, 57, 59])
    ax.set_ylim(55, 60)

    report = vizlint.lint(fig)
    assert all(i.id != "axis_range_overexpanded" for i in report.issues)


def test_flat_data_does_not_trigger_overexpanded_axis():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [5, 5, 5])
    ax.set_ylim(0, 10)

    report = vizlint.lint(fig)
    assert all(i.id != "axis_range_overexpanded" for i in report.issues)
