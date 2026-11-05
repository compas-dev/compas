"""Verify the contents required from a COMPAS Python wheel."""

from __future__ import annotations

import sys
from pathlib import Path
from zipfile import ZipFile


def find_wheel(path: Path) -> Path:
    """Resolve exactly one wheel from a file or directory."""
    if path.is_file():
        return path
    wheels = sorted(path.glob("*.whl"))
    if len(wheels) != 1:
        raise RuntimeError(f"Expected exactly one wheel in {path}, found {len(wheels)}.")
    return wheels[0]


def verify_wheel(path: Path) -> None:
    """Verify that a wheel contains the PEP 561 marker."""
    wheel = find_wheel(path)
    with ZipFile(wheel) as archive:
        names = set(archive.namelist())
    if "compas/py.typed" not in names:
        raise RuntimeError(f"{wheel.name} does not contain compas/py.typed.")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: verify_python_wheel.py WHEEL_OR_DIRECTORY")
    verify_wheel(Path(sys.argv[1]))
