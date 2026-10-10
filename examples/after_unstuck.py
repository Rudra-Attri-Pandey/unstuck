"""AFTER: same task with Unstuck. Run me to see the fix."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.waiter import PoliteWaiter, RateLimitedError
from src.memory import SmartMemory
from src.loop_alarm import LoopAlarm
from src.undo import CheckpointManager

# Fix 1: polite waiting survives 2x 429 then succeeds.
calls = {"n": 0}


def flaky():
    calls["n"] += 1
    if calls["n"] <= 2:
        raise RateLimitedError("429", retry_after=0.01)
    return "api OK"


print("waiter:", PoliteWaiter(max_retries=4, base_delay=0.01).run(flaky))

# Fix 2: memory condenses instead of growing forever.
mem = SmartMemory(max_tokens=2000)
mem.set_system("You are a helper.")
for i in range(10):
    mem.add("user", f"turn {i}: " + "x" * 2000)
print(f"memory: {len(mem.window())} items in window, summaries={mem.summaries_made}")

# Fix 3: loop halts on 3rd repeat.
alarm = LoopAlarm()
for _ in range(3):
    decision = alarm.record_action("bash", {"cmd": "cat file"})
print("loop:", decision)

# Fix 4: bad edit restores.
with tempfile.TemporaryDirectory() as d:
    target = Path(d) / "a.py"
    target.write_text("def hello():\n    return True\n")
    undo = CheckpointManager(backup_dir=Path(d) / "backups")
    undo.checkpoint(target)
    target.write_text("BROKEN ((((")
    undo.restore(target)
    print("undo restored:", "return True" in target.read_text())
