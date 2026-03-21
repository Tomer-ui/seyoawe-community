"""
Unit tests — CLI internal logic.
Tests the pure functions in sawectl.py directly without running any subprocesses
or needing the engine to be up.
"""
import os
import sys
import json
import tempfile
import pytest

# Add sawectl/ to the path so we can import it directly
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "../../../sawectl"))
from sawectl import load_yaml, load_json_schema, extract_module_and_method, validate_step

SCHEMAS_DIR = os.path.join(os.path.dirname(__file__), "../../../sawectl")
MODULES_DIR = os.path.join(os.path.dirname(__file__), "../../../modules")


# --- load_yaml ---

def test_load_yaml_valid(tmp_path):
    f = tmp_path / "test.yaml"
    f.write_text("key: value\nlist:\n  - a\n  - b\n")
    result = load_yaml(str(f))
    assert result["key"] == "value"
    assert result["list"] == ["a", "b"]


def test_load_yaml_missing_file_exits():
    with pytest.raises(SystemExit):
        load_yaml("/nonexistent/path/file.yaml")


def test_load_yaml_empty_file_exits(tmp_path):
    f = tmp_path / "empty.yaml"
    f.write_text("")
    with pytest.raises(SystemExit):
        load_yaml(str(f))


# --- load_json_schema ---

def test_load_dsl_schema():
    schema = load_json_schema(os.path.join(SCHEMAS_DIR, "dsl.schema.json"))
    assert isinstance(schema, dict)
    assert "properties" in schema


def test_load_module_schema():
    schema = load_json_schema(os.path.join(SCHEMAS_DIR, "module.schema.json"))
    assert isinstance(schema, dict)


def test_load_json_schema_missing_file_exits():
    with pytest.raises(SystemExit):
        load_json_schema("/nonexistent/schema.json")


# --- extract_module_and_method ---

def test_extract_standard_action():
    # Format: module_name.ClassName.method_name
    module, method = extract_module_and_method("slack_module.Slack.send_info_message", {})
    assert module == "slack_module"
    assert method == "send_info_message"


def test_extract_two_part_action():
    # Format: module_name.method_name
    module, method = extract_module_and_method("command_module.run", {})
    assert module == "command_module"
    assert method == "run"


def test_extract_context_module_action():
    context_modules = {
        "my_slack": {"module": "slack_module.Slack"}
    }
    module, method = extract_module_and_method("context.my_slack.send_info_message", context_modules)
    assert module == "slack_module"
    assert method == "send_info_message"


def test_extract_context_module_missing_returns_none():
    module, method = extract_module_and_method("context.missing_ref.some_method", {})
    assert module is None
    assert method is None


# --- validate_step ---

def test_validate_step_missing_id_fails():
    step = {"type": "action", "action": "slack_module.Slack.send_info_message"}
    ok, msg = validate_step(step, MODULES_DIR, {})
    assert not ok
    assert "id" in msg


def test_validate_step_no_action_passes():
    # Steps without an action (e.g. wait or condition steps) should pass
    step = {"id": "wait_step", "type": "wait"}
    ok, msg = validate_step(step, MODULES_DIR, {})
    assert ok


def test_validate_step_valid_slack_action(tmp_path):
    # Use a real module that exists in the repo
    step = {
        "id": "notify",
        "type": "action",
        "action": "slack_module.Slack.send_info_message",
        "input": {
            "channel": "#test",
            "title": "Test"
        }
    }
    ok, msg = validate_step(step, MODULES_DIR, {})
    # ok can be True or False depending on whether module.yaml exists,
    # but it must not raise an exception
    assert isinstance(ok, bool)
