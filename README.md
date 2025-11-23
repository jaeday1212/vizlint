# vizlint

Super-fast linting for Python visualizations so misleading charts never leave your notebook.

[![PyPI](https://img.shields.io/pypi/v/vizlint.svg)](https://pypi.org/project/vizlint/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Overview
vizlint inspects Matplotlib figures for easy-to-miss quality problems such as truncated bar charts or missing labels. Use it directly from Python, in a notebook, or via a CLI that runs headless by default (Agg backend) so it is safe in CI.

## Features
- Single-call API: `vizlint.lint(fig)` returns a `Report` you can print or serialize.
- Matplotlib adapter included; install `vizlint[mpl]` for the plotting extra.
- CLI that executes your plotting script, lints every open figure, and supports per-rule toggles via `--disable`.
- Notebook helper `vizlint.lint_last()` to lint the figure you just rendered.
- Default rules catch truncated bar charts, unlabeled axes, stretched ranges, and missing titles.

## Install
```bash
pip install vizlint
pip install "vizlint[mpl]"  # Matplotlib extra
```

## Quickstart (Python)
```python
import matplotlib.pyplot as plt
import vizlint

fig, ax = plt.subplots()
ax.bar(["A", "B"], [101, 103])
ax.set_ylim(100, 104)

report = vizlint.lint(fig)
print(report.summary())
```

## Example output
```text
vizlint report:
- WARN [bar_zero_baseline] Bar chart y-axis does not include zero, which can exaggerate differences between bars. Hint: Consider starting the y-axis at zero or switch to a different chart type if you need to zoom in.
```

## CLI usage
The CLI runs your plotting script, forces the Agg backend for headless safety, and lints every open figure:

```bash
vizlint path/to/script.py
```

Disable individual rules by name (rule function names) without editing code:

```bash
vizlint path/to/script.py --disable axis_labels_missing --disable bar_zero_baseline
```

Exit code is `0` when all figures are clean, `1` when any warning is emitted, and `2` if the user script or Matplotlib import fails.

## Jupyter / notebooks
Lint the most recently drawn Matplotlib figure from a notebook cell:

```python
import vizlint

# after plotting
report = vizlint.lint_last()
display(report.summary())
```

## Current checks
- `bar_zero_baseline` *(warning)* – Flags bar charts whose y-axis range excludes zero, making differences look larger than they are.
- `axis_labels_missing` *(warning)* – Reports charts missing an x-axis label, y-axis label, or both.
- `axis_range_overexpanded` *(warning)* – Detects y-axes that span far beyond the data range, which can minimize apparent variation.
- `title_missing` *(warning)* – Reminds you to add a descriptive chart title to aid quick interpretation.

## Configuration & custom rules
`vizlint.lint(fig, rules=None)` uses `vizlint.rules.DEFAULT_RULES` when `rules` is `None`. Pass your own list to customize behavior:

```python
from vizlint import lint
from vizlint.rules import DEFAULT_RULES, axis_labels_missing

custom = [rule for rule in DEFAULT_RULES if rule is not axis_labels_missing]
report = lint(fig, rules=custom)

# Structured output (e.g., for JSON APIs)
payload = report.to_dict()
```

In the CLI, use `--disable rule_name` to skip specific default checks. For richer integrations, the `Report` object exposes `.issues`, `.is_clean()`, `.summary()`, and `.to_dict()`.

## Development
```bash
git clone https://github.com/jaeday1212/vizlint.git
cd vizlint
pip install -e .
pip install -e .[mpl]
python -m pytest
```

You can also run the CLI locally via `python -m vizlint.cli path/to/script.py`.

## Roadmap
- Add more visualization rules (e.g., stacked bars, dual-axis charts).
- Support additional backends beyond Matplotlib.
- Provide optional JSON output mode in the CLI.
- Deepen notebook widgets for inline remediation hints.

## Looking Ahead
Upcoming explorations include native adapters for Seaborn and Plotly plus hooks that let LLM-based assistants recommend fixes based on the `Report` output.

## Contributing
Bug reports and pull requests are welcome. Please run `python -m pytest` before submitting and keep changes focused with clear descriptions.

## License
vizlint is available under the [MIT License](LICENSE).
