import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import vizlint


def test_missing_title_reports_issue():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])

    report = vizlint.lint(fig)
    issues = [i for i in report.issues if i.id == "title_missing"]

    assert issues, "Expected title_missing issue when no chart title is set"
    issue = issues[0]
    assert issue.severity == "warn"
    assert "title" in issue.message.lower()


def test_present_title_is_clean_for_title_missing():
    fig, ax = plt.subplots()
    ax.plot([0, 1, 2], [1, 2, 3])
    ax.set_title("Example chart")

    report = vizlint.lint(fig)
    assert all(i.id != "title_missing" for i in report.issues)
