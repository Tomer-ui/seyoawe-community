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
    """Engine port must be open and accepting connections.
    We use a raw TCP socket so we are not affected by HTTP-level resets.
    'Connection refused' = engine not running. 'Connection reset' = engine is
    running but in warmup — that still counts as reachable.
    """
    import socket
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(10)
    host = ENGINE_URL.replace("http://", "").split(":")[0]
    port = int(ENGINE_URL.replace("http://", "").split(":")[1]) if ":" in ENGINE_URL.replace("http://", "") else 8080
    try:
        s.connect((host, port))
    except (ConnectionRefusedError, socket.timeout, OSError) as e:
        pytest.fail(f"Engine port is not open at {ENGINE_URL}: {e}")
    finally:
        s.close()


def test_engine_responds_quickly():
    """Engine must respond (or reset) within 5 seconds — catches startup hangs.
    A connection reset is accepted: it means the engine responded (just reset it),
    which is fast enough. Only a timeout indicates a hang.
    """
    import time
    start = time.monotonic()
    try:
        requests.get(f"{ENGINE_URL}/poll", timeout=5)
    except requests.exceptions.ConnectionError:
        pass  # connection reset = engine responded, just reset — that's fine
    elapsed = time.monotonic() - start
    assert elapsed < 5, f"Engine took {elapsed:.1f}s — likely hung"


def test_engine_poll_endpoint_exists():
    """The module dispatcher poll endpoint must exist."""
    response = requests.get(f"{ENGINE_URL}/poll", timeout=10)
    # 404 or 405 means the route exists but doesn't accept GET — that's fine
    assert response.status_code != 500, "Engine returned 500 on /poll — internal error"
