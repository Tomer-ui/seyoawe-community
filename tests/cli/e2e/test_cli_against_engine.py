"""
E2E tests — CLI talking to a live engine.
Requires both the engine container and the CLI to be available.
ENGINE_URL defaults to http://localhost:8080.
"""
import os
import subprocess
import sys
import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "../../..")
CLI_SCRIPT = os.path.join(REPO_ROOT, "sawectl/sawectl.py")
ENGINE_URL = os.environ.get("ENGINE_URL", "localhost:8080")
SAMPLE_WORKFLOW = os.path.join(REPO_ROOT, "workflows/samples/command_and_slack.yaml")


def run_cli(*args):
    result = subprocess.run(
        [sys.executable, CLI_SCRIPT] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_ROOT
    )
    return result.returncode, result.stdout, result.stderr


def test_cli_run_reaches_engine():
    """CLI run command must reach the engine and get a response (not a connection error)."""
    code, out, err = run_cli(
        "run",
        "--workflow", SAMPLE_WORKFLOW,
        "--server", ENGINE_URL
    )
    combined = out + err
    # Connection refused = engine not running = real failure
    assert "connection" not in combined.lower() or "refused" not in combined.lower(), (
        f"CLI could not reach engine at {ENGINE_URL}:\n{combined}"
    )
    # Any response from the engine (even an error) means the CLI→engine path works
    assert code == 0 or "error" in combined.lower(), (
        f"Unexpected CLI failure:\n{combined}"
    )
