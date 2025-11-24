from __future__ import annotations

from importlib import metadata
from pathlib import Path

from .core import lint, Report, Issue

__all__ = ["lint", "Report", "Issue", "lint_last"]


def lint_last():  # noqa: D401 - forwarded docstring
	from .notebook import lint_last as _lint_last

	return _lint_last()


def _read_local_version() -> str:
	try:
		import tomllib
	except ModuleNotFoundError:  # pragma: no cover - Python <3.11 fallback not needed in CI
		return "0.0.0"

	pyproject = Path(__file__).resolve().parents[2] / "pyproject.toml"
	try:
		data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
		return data["project"]["version"]
	except Exception:
		return "0.0.0"


try:
	__version__ = metadata.version("vizlint")
except metadata.PackageNotFoundError:  # pragma: no cover - occurs in editable installs
	__version__ = _read_local_version()
