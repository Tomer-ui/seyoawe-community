"""
Unit tests — CLI schema file validation.
Verifies that the schema files the CLI depends on exist and are valid JSON.
"""
import os
import json
import pytest

SAWECTL_DIR = os.path.join(os.path.dirname(__file__), "../../../sawectl")


def test_dsl_schema_exists():
    assert os.path.exists(os.path.join(SAWECTL_DIR, "dsl.schema.json"))


def test_module_schema_exists():
    assert os.path.exists(os.path.join(SAWECTL_DIR, "module.schema.json"))


def test_dsl_schema_is_valid_json():
    with open(os.path.join(SAWECTL_DIR, "dsl.schema.json")) as f:
        data = json.load(f)
    assert "$schema" in data or "properties" in data


def test_module_schema_is_valid_json():
    with open(os.path.join(SAWECTL_DIR, "module.schema.json")) as f:
        data = json.load(f)
    assert isinstance(data, dict)
