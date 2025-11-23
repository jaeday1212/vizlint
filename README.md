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

## CLI
```bash
vizlint path/to/script_that_makes_plots.py
```
