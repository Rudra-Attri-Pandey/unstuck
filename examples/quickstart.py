"""10-line happy path. Run me first."""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.waiter import PoliteWaiter
from src.memory import SmartMemory
from src.loop_alarm import LoopAlarm
from src.undo import CheckpointManager

waiter = PoliteWaiter()
mem = SmartMemory(max_tokens=2000)
alarm = LoopAlarm()
undo = CheckpointManager()

mem.set_system("You are a coding helper.")
mem.add("user", "Fix the typo in hello().")
print(alarm.record_action("str_replace", {"path": "a.py"}))
print("memory tokens:", mem.total_tokens())
print("Unstuck OK: waiter + memory + alarm + undo ready.")
