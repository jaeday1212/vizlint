import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import vizlint


def test_missing_axis_labels_reports_issue():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [1, 2])

    report = vizlint.lint(fig)
    issues = [i for i in report.issues if i.id == "axis_labels_missing"]
    assert issues, "Expected axis_labels_missing issue when both axis labels are missing"
    issue = issues[0]
    assert issue.severity == "warn"
    assert "label" in issue.message.lower()


def test_axis_labels_present_is_clean():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [1, 2])
    ax.set_xlabel("Category")
    ax.set_ylabel("Value")

    report = vizlint.lint(fig)
    assert all(i.id != "axis_labels_missing" for i in report.issues)


def test_single_missing_axis_is_still_reported():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [1, 2])
    ax.set_xlabel("Category")  # y-axis unlabeled

    report = vizlint.lint(fig)
    issues = [i for i in report.issues if i.id == "axis_labels_missing"]
    assert issues, "Expected axis_labels_missing when one axis label is missing"
