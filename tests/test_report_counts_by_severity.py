import pytest

from vizlint.core import Issue, Report


def test_counts_by_severity_empty_report():
    report = Report(issues=[])
    counts = report.counts_by_severity()
    assert counts == {}


def test_counts_by_severity_single_severity():
    report = Report(
        issues=[
            Issue(id="foo", severity="warn", message="m1"),
            Issue(id="bar", severity="warn", message="m2"),
        ]
    )

    counts = report.counts_by_severity()
    assert counts == {"warn": 2}


def test_counts_by_severity_mixed_severities():
    report = Report(
        issues=[
            Issue(id="a", severity="warn", message="w1"),
            Issue(id="b", severity="warn", message="w2"),
            Issue(id="c", severity="error", message="e1"),
        ]
    )

    counts = report.counts_by_severity()
    assert counts["warn"] == 2
    assert counts["error"] == 1
    assert set(counts.keys()) == {"warn", "error"}
