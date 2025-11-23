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

## Current checks
- `bar_zero_baseline` (warning): Flags bar charts whose y-axis range does not include zero, because truncated baselines can exaggerate differences between bars.

## CLI
```bash
vizlint path/to/script_that_makes_plots.py
```
