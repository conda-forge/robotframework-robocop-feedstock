from subprocess import call
import sys

COVERAGE_THRESHOLD = 41
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

TEST_ARGS = [
    "coverage",
    "run",
    "--source=robocop",
    "--branch-mpytest",
    "src/tests",
    "-vv",
    "--color=yes",
    "--tb=long",
    "-k",
    f"""not ({" or ".join(SKIPS)})""",
]

REPORT_ARGS = [
    "coverage",
    "report",
    "--show-missing",
    "--skip-covered",
    f"--fail-under={COVERAGE_THRESHOLD}",
]

if __name__ == "__main__":
    sys.exit(call(TEST_ARGS) or call(REPORT_ARGS))
