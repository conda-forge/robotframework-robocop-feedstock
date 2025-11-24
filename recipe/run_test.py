from subprocess import call
import sys
import tempfile
import shutil
from pathlib import Path

COVERAGE_THRESHOLD = 63
SKIPS: list[str] = [
    # https://github.com/conda-forge/robotframework-robocop-feedstock/pull/48
    # expects a specific git layout
    "gitignore",
    # https://github.com/conda-forge/robotframework-robocop-feedstock/pull/60
    # expects version-dependent strings?
    "invalid_for_loop and (TestRuleAcceptance and (test_rule or test_extended))",
    # https://github.com/conda-forge/robotframework-robocop-feedstock/pull/71
    # missing config error message?
    "test_invalid_threshold",
    # https://github.com/conda-forge/robotframework-robocop-feedstock/pull/86
    # error message drift?
    "test_invalid_extends",
]

TEST_ARGS = [
    "coverage",
    "run",
    "--source=robocop",
    "--branch",
    "-m",
    "pytest",
    "-vv",
    "--color=yes",
    "--tb=long",
]

if SKIPS:
    TEST_ARGS += [
        "-k",
        f"not {SKIPS[0]}" if len(SKIPS) == 1 else f"""not ({" or ".join(SKIPS)})""",
    ]


REPORT_ARGS = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COVERAGE_THRESHOLD}",
]

if __name__ == "__main__":
    # move the tests to a temporary dir to avoid path assumption issues
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree("tests", Path(td) / "tests")
        shutil.copy2(Path("pyproject.toml"), Path(td) / "pyproject.toml")
        sys.exit(call(TEST_ARGS, cwd=td) or call(REPORT_ARGS, cwd=td))
