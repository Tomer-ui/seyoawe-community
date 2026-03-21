"""
E2E tests — Workflow submission against a live engine.
Simulates a real user triggering a workflow via the API.
Requires the engine container to be running.
"""
import os
import requests
import pytest

ENGINE_URL = os.environ.get("ENGINE_URL", "http://localhost:8080")

SAMPLE_WORKFLOW_TRIGGER = {
    "workflow": "run_pwd_and_notify",
    "context": {
        "channel": "#ci-test"
    }
}


def test_workflow_endpoint_is_reachable():
    """The /workflow/trigger endpoint must exist and accept POST requests."""
    response = requests.post(
        f"{ENGINE_URL}/workflow/trigger",
        json=SAMPLE_WORKFLOW_TRIGGER,
        timeout=10
    )
    # 400 (bad request) or 200 both mean the endpoint exists and the engine handled it
    # 404 means the route doesn't exist — that's a real failure
    assert response.status_code != 404, (
        "Workflow trigger endpoint not found — engine API may have changed"
    )
    assert response.status_code != 500, (
        f"Engine returned 500 on workflow trigger: {response.text}"
    )


def test_workflow_response_is_json():
    """Engine must respond with valid JSON on workflow trigger."""
    response = requests.post(
        f"{ENGINE_URL}/workflow/trigger",
        json=SAMPLE_WORKFLOW_TRIGGER,
        timeout=10
    )
    try:
        data = response.json()
        assert isinstance(data, dict), "Response body should be a JSON object"
    except Exception:
        pytest.fail(f"Engine did not return valid JSON: {response.text}")
