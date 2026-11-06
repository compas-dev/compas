from importlib.util import module_from_spec
from importlib.util import spec_from_file_location
from pathlib import Path
import sys


spec = spec_from_file_location("compas_tasks", Path(__file__).parents[1] / "tasks.py")
assert spec
assert spec.loader
tasks = module_from_spec(spec)
spec.loader.exec_module(tasks)


class RecordingContext:
    def __init__(self):
        self.commands: list[str] = []

    def run(self, command: str) -> None:
        self.commands.append(command)


def test_lint_task_is_non_mutating_and_repository_wide():
    context = RecordingContext()

    tasks.ns["lint"].body(context)

    assert context.commands == [f'"{sys.executable}" -m ruff check .']


def test_check_task_matches_the_canonical_ruff_commands():
    context = RecordingContext()

    tasks.ns["check"].body(context)

    assert context.commands == [
        f'"{sys.executable}" -m ruff check .',
        f'"{sys.executable}" -m ruff format --check .',
    ]
