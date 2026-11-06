from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path
from zipfile import ZipFile

import pytest


SCRIPT = Path(__file__).parents[2] / ".github" / "verify_python_wheel.py"
BUILD_WORKFLOW = Path(__file__).parents[2] / ".github" / "workflows" / "build.yml"
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


def test_build_workflow_uploads_the_verified_candidate_wheel() -> None:
    workflow = BUILD_WORKFLOW.read_text()
    build_condition = "matrix.os == 'ubuntu-latest' && matrix.python == '3.12'"
    build_step = workflow.index("      - name: Build typed wheel")
    verify_step = workflow.index("      - name: Verify typed wheel")
    upload_step = workflow.index("      - name: Upload verified candidate wheel")

    assert build_step < verify_step < upload_step
    assert workflow.count("name: candidate-linux-py312") == 1
    assert workflow.count(f"if: {build_condition}") == 3

    upload = workflow[upload_step : workflow.index("\n\n", upload_step)]
    assert "actions/upload-artifact@043fb46d1a93c77aae656e7c1c64a875d1fc6a0a" in upload
    assert "path: ${{ runner.temp }}/compas-wheelhouse/*.whl" in upload
    assert "if-no-files-found: error" in upload
    assert "retention-days: 14" in upload
