"""
Unit tests — Engine configuration validation.
These run without the engine running. They verify that config.yaml
is structurally correct and won't cause the engine to crash on startup.
"""
import os
import yaml
import pytest

CONFIG_PATH = os.path.join(
    os.path.dirname(__file__), "../../../configuration/config.yaml"
)


@pytest.fixture
def config():
    with open(CONFIG_PATH, "r") as f:
        return yaml.safe_load(f)


def test_config_file_exists():
    assert os.path.exists(CONFIG_PATH), "configuration/config.yaml is missing"


def test_config_has_required_top_level_keys(config):
    required = ["logging", "directories", "app", "module_dispatcher"]
    for key in required:
        assert key in config, f"Missing required top-level key: '{key}'"


def test_app_port_is_defined(config):
    port = config["app"]["port"]
    assert isinstance(port, int), "app.port must be an integer"
    assert 1024 <= port <= 65535, f"app.port {port} is out of valid range"


def test_module_dispatcher_port_is_defined(config):
    port = config["module_dispatcher"]["port"]
    assert isinstance(port, int), "module_dispatcher.port must be an integer"


def test_directories_are_defined(config):
    required_dirs = ["workdir", "modules", "workflows", "logs"]
    for d in required_dirs:
        assert d in config["directories"], f"Missing directory config: '{d}'"


def test_logging_level_is_valid(config):
    valid_levels = {"DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"}
    level = config["logging"]["level"]
    assert level in valid_levels, f"Invalid logging level: '{level}'"
