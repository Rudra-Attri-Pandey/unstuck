"""Burst test: 5 fast calls don't crash. Polite waiting absorbs 429s."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.waiter import PoliteWaiter, RateLimitedError


def test_burst_survives_rate_limits():
    calls = {"n": 0}

    def flaky():
        calls["n"] += 1
        if calls["n"] <= 2:
            raise RateLimitedError("429 blocked", retry_after=0.01)
        return "ok"

    waiter = PoliteWaiter(max_retries=4, base_delay=0.01, max_delay=0.05)
    assert waiter.run(flaky) == "ok"
    assert calls["n"] == 3


def test_never_retries_bad_request():
    def bad():
        raise ValueError("bad schema")

    waiter = PoliteWaiter()
    try:
        waiter.run(bad)
        assert False, "should have raised"
    except ValueError:
        pass
