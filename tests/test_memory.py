"""Memory test: 10 big turns stay under budget with summaries."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.memory import SmartMemory


def test_memory_stays_under_budget():
    mem = SmartMemory(max_tokens=2000, keep_last=5)
    mem.set_system("You are a helper.")
    for i in range(10):
        mem.add("user", f"turn {i}: " + "x" * 2000)
    assert mem.total_tokens() <= mem.budget()
    assert mem.summaries_made >= 1
    # System never lost.
    roles = [m["role"] for m in mem.window()]
    assert "system" in roles
