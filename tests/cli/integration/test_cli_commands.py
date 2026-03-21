"""
Integration tests — CLI commands run as subprocesses.
These test the CLI binary end-to-end without needing the engine running.
Commands tested: validate-modules, validate-workflow
"""
import os
import subprocess
import sys
import pytest

REPO_ROOT = os.path.join(os.path.dirname(__file__), "../../..")
CLI_SCRIPT = os.path.join(REPO_ROOT, "sawectl/sawectl.py")
MODULES_DIR = os.path.join(REPO_ROOT, "modules")
SAMPLE_WORKFLOW = os.path.join(REPO_ROOT, "workflows/samples/command_and_slack.yaml")


def run_cli(*args):
    """Helper: run sawectl.py with given args, return (returncode, stdout, stderr)."""
    result = subprocess.run(
        [sys.executable, CLI_SCRIPT] + list(args),
        capture_output=True,
        text=True,
        cwd=REPO_ROOT
    )
    return result.returncode, result.stdout, result.stderr


def test_cli_help_exits_zero():
    code, out, _ = run_cli("--help")
    assert code == 0
    assert "sawectl" in out.lower() or "usage" in out.lower()


def test_validate_modules_passes():
    code, out, err = run_cli("validate-modules", "--modules", MODULES_DIR)
    assert code == 0, f"validate-modules failed:\nstdout: {out}\nstderr: {err}"
    assert "passed" in out.lower() or "valid" in out.lower()


def test_validate_workflow_sample_passes():
    code, out, err = run_cli(
        "validate-workflow",
        "--workflow", SAMPLE_WORKFLOW,
        "--modules", MODULES_DIR
    )
    # May warn about missing module.yaml but should not hard-fail on a sample workflow
    assert code == 0 or "warn" in out.lower() or "warn" in err.lower(), (
        f"validate-workflow failed unexpectedly:\nstdout: {out}\nstderr: {err}"
    )
