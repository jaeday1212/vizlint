from __future__ import annotations
import argparse
import os
import runpy
import sys
from typing import List

from vizlint.rules import DEFAULT_RULES


def main(argv: List[str] | None = None) -> None:
    parser = argparse.ArgumentParser(
        prog="vizlint",
        description="Lint matplotlib charts in a Python script.",
    )
    parser.add_argument("script", help="Path to a Python script that generates matplotlib figures.")
    parser.add_argument(
        "--disable",
        action="append",
        default=[],
        help=(
            "Disable specific rule names (e.g. --disable axis_labels_missing). "
            "Rule names correspond to the rule function names."
        ),
    )
    args = parser.parse_args(argv)

    try:
        if not os.environ.get("MPLBACKEND"):
            os.environ["MPLBACKEND"] = "Agg"

        import matplotlib

        try:
            matplotlib.use("Agg", force=True)
        except TypeError:  # pragma: no cover - extremely old matplotlib
            matplotlib.use("Agg")

        import matplotlib.pyplot as plt
    except Exception as exc:  # pragma: no cover - user environment issue
        print(f"vizlint: matplotlib not available. Install vizlint[mpl]. ({exc})", file=sys.stderr)
        sys.exit(2)

    try:
        # Execute the user's script in its own namespace
        runpy.run_path(args.script, run_name="__main__")
    except Exception as exc:  # pragma: no cover - pass-thru for CLI
        print(f"vizlint: failed to run script: {exc}", file=sys.stderr)
        sys.exit(2)

    from .core import lint

    figs = list(map(plt.figure, plt.get_fignums()))
    if not figs:
        print("vizlint: no matplotlib figures found.")
        return

    disabled = set(args.disable or [])
    active_rules = [rule for rule in DEFAULT_RULES if rule.__name__ not in disabled]

    exit_code = 0
    for idx, fig in enumerate(figs, start=1):
        report = lint(fig, rules=active_rules)
        if not report.is_clean():
            exit_code = 1
            print(f"\nFigure {idx}:")
            print(report.summary())
        else:
            print(f"\nFigure {idx}: clean ✅")

    sys.exit(exit_code)
