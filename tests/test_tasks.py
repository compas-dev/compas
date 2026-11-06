import sys

import tasks


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
