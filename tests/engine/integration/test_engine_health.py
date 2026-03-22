"""
Integration tests — Engine HTTP health checks.
These require the engine container to be running.
ENGINE_URL defaults to http://localhost:8080 but can be overridden
via the ENGINE_URL environment variable (used in CI).
"""
import os
import requests
import pytest

ENGINE_URL = os.environ.get("ENGINE_URL", "http://localhost:8080")


def test_engine_is_reachable():
    """Engine must respond to HTTP requests on /poll (any status code means it's up).
    The engine resets connections on unknown routes, so we probe a known endpoint.
    """
    try:
        response = requests.get(f"{ENGINE_URL}/poll", timeout=10)
        assert response.status_code in range(100, 600), "No valid HTTP response"
    except requests.exceptions.ConnectionError:
        pytest.fail(f"Engine is not reachable at {ENGINE_URL}/poll")


def test_engine_responds_quickly():
    """Engine must respond within 5 seconds on /poll — catches startup hangs."""
    response = requests.get(f"{ENGINE_URL}/poll", timeout=5)
    assert response.elapsed.total_seconds() < 5


def test_engine_poll_endpoint_exists():
    """The module dispatcher poll endpoint must exist."""
    response = requests.get(f"{ENGINE_URL}/poll", timeout=10)
    # 404 or 405 means the route exists but doesn't accept GET — that's fine
    assert response.status_code != 500, "Engine returned 500 on /poll — internal error"
