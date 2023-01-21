import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SRC_DIR = Path(os.environ["SRC_DIR"])
TESTS = SRC_DIR / "src/tests"
SKIPS = [
    # slow, don't care
    "benchmark",
    # assumes sys.argv
    "e2e",
    # assumes source repo
    "find_project_root_missing_but_git",
    # maybe 3.10?
    "both_tests_and_tasks",
    # no idea
    "parsing_error",
    "setting_not_supported",
]

PYTEST_ARGS = ["pytest", "-vv", "-k", f"""not ({" or ".join(SKIPS)})"""]

COVERAGE_THRESHOLD = os.environ.get("COVERAGE_THRESHOLD")

if COVERAGE_THRESHOLD:
    PYTEST_ARGS += [
        "--no-cov-on-fail",
        "--cov=robocop",
        "--cov-report=term-missing:skip-covered",
        f"--cov-fail-under={COVERAGE_THRESHOLD}",
    ]

if __name__ == "__main__":
    # move the tests to a temporary dir to avoid $SRC_DIR path rewriting
    with tempfile.TemporaryDirectory() as td:
        shutil.copytree(TESTS, Path(td) / "tests")
        sys.exit(subprocess.call(PYTEST_ARGS, cwd=td))
