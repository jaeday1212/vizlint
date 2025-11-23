# vizlint

Lint Python charts for common misleading or low-quality patterns.

## Install
```bash
pip install vizlint
pip install "vizlint[mpl]"
```

## Quickstart (Matplotlib)
```python
import matplotlib.pyplot as plt
import vizlint as vl

fig, ax = plt.subplots()
ax.bar(["A", "B"], [101, 103])
ax.set_ylim(100, 104)

report = vl.lint(fig)
print(report.summary())
```

## Example output
For the truncated bar chart above, `report.summary()` might look like:

```text
vizlint report:
- WARN [bar_zero_baseline] Bar chart y-axis does not include zero, which can exaggerate differences between bars. Hint: Consider starting the y-axis at zero or switch charts if you need to zoom in.
```

Depending on your chart, you might also see warnings such as `axis_labels_missing` or `axis_range_overexpanded` alongside other issues.

## Current checks
- `bar_zero_baseline` (warning): Flags bar charts whose y-axis range does not include zero, which can exaggerate differences between bars.
- `axis_labels_missing` (warning): Warns when the x-axis, y-axis, or both are unlabeled, making the chart harder to interpret.
- `axis_range_overexpanded` (warning): Warns when the y-axis span is far larger than the data range and the data floats in the middle, which can visually minimize changes.

## CLI
```bash
vizlint path/to/script_that_makes_plots.py
```
