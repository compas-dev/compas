from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path
from zipfile import ZipFile

import pytest


SCRIPT = Path(__file__).parents[2] / ".github" / "verify_python_wheel.py"
SPEC = spec_from_file_location("verify_python_wheel", SCRIPT)
assert SPEC and SPEC.loader
verify_python_wheel = module_from_spec(SPEC)
SPEC.loader.exec_module(verify_python_wheel)


def make_wheel(tmp_path: Path, *, include_marker: bool = True) -> Path:
    wheel = tmp_path / "compas-3.0.0-py3-none-any.whl"
    with ZipFile(wheel, "w") as archive:
        archive.writestr("compas/__init__.py", "")
        if include_marker:
            archive.writestr("compas/py.typed", "")
    return wheel


def test_verify_wheel_accepts_pep561_marker(tmp_path: Path) -> None:
    verify_python_wheel.verify_wheel(make_wheel(tmp_path))


def test_verify_wheel_rejects_missing_pep561_marker(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="compas/py.typed"):
        verify_python_wheel.verify_wheel(make_wheel(tmp_path, include_marker=False))


def test_find_wheel_requires_exactly_one_artifact(tmp_path: Path) -> None:
    with pytest.raises(RuntimeError, match="Expected exactly one wheel"):
        verify_python_wheel.find_wheel(tmp_path)
