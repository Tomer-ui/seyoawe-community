"""
Unit tests — Engine module structure validation.
Verifies that each expected module directory exists and contains
a Python file. If a module is missing, the engine will fail to load it.
"""
import os
import pytest

MODULES_PATH = os.path.join(
    os.path.dirname(__file__), "../../../modules"
)

EXPECTED_MODULES = [
    ("api_module", "api.py"),
    ("chatbot_module", "chatbot.py"),
    ("command_module", "command.py"),
    ("delegate_remote_workflow", "remote_delegator.py"),
    ("email_module", "email.py"),
    ("git_module", "git.py"),
    ("slack_module", "slack.py"),
    ("webform", "webform.py"),
]


def test_modules_directory_exists():
    assert os.path.isdir(MODULES_PATH), "modules/ directory is missing"


@pytest.mark.parametrize("module_dir,module_file", EXPECTED_MODULES)
def test_module_file_exists(module_dir, module_file):
    path = os.path.join(MODULES_PATH, module_dir, module_file)
    assert os.path.exists(path), f"Missing module file: modules/{module_dir}/{module_file}"


@pytest.mark.parametrize("module_dir,module_file", EXPECTED_MODULES)
def test_module_file_is_not_empty(module_dir, module_file):
    path = os.path.join(MODULES_PATH, module_dir, module_file)
    assert os.path.getsize(path) > 0, f"Module file is empty: modules/{module_dir}/{module_file}"
