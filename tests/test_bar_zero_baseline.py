import matplotlib.pyplot as plt
import vizlint as vl


def test_bar_zero_baseline_flags_truncation():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [101, 103])
    ax.set_ylim(100, 104)
    report = vl.lint(fig)
    assert any(i.id == "bar_zero_baseline" for i in report.issues)


def test_bar_zero_baseline_allows_zero():
    fig, ax = plt.subplots()
    ax.bar(["A", "B"], [101, 103])
    ax.set_ylim(0, 104)
    report = vl.lint(fig)
    assert report.is_clean()
