import json
import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).parents[2]
FIXTURES = ROOT / "tests" / "typing"
EXPECTED_ERROR = re.compile(r"# expected-error: (?P<rule>[A-Za-z][A-Za-z0-9]+)\s*$")


def run_pyright(fixture):
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "pyright",
            "--outputjson",
            "--pythonpath",
            sys.executable,
            str(fixture),
        ],
        cwd=ROOT,
        check=False,
        capture_output=True,
        text=True,
    )
    assert result.returncode in {0, 1}, result.stderr
    return json.loads(result.stdout)["generalDiagnostics"]


def expected_diagnostics(fixture):
    expected = []
    for line_number, line in enumerate(fixture.read_text().splitlines(), start=1):
        match = EXPECTED_ERROR.search(line)
        if match:
            expected.append((str(fixture.resolve()), line_number, match.group("rule")))
    return sorted(expected)


def actual_diagnostics(diagnostics):
    return sorted(
        (
            str(Path(diagnostic["file"]).resolve()),
            diagnostic["range"]["start"]["line"] + 1,
            diagnostic.get("rule"),
        )
        for diagnostic in diagnostics
    )


def test_accepted_typing_fixture_has_no_diagnostics():
    fixture = FIXTURES / "accepted.py"

    assert run_pyright(fixture) == []


def test_expected_typing_errors_match_inline_markers():
    fixture = FIXTURES / "expected_errors.py"

    assert actual_diagnostics(run_pyright(fixture)) == expected_diagnostics(fixture)
