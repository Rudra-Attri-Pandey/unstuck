"""Undo test: bad edit restores byte-identical file. Loop halts on 3rd repeat."""

import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from src.undo import CheckpointManager
from src.loop_alarm import LoopAlarm


def test_undo_restores():
    with tempfile.TemporaryDirectory() as d:
        target = Path(d) / "a.py"
        target.write_text("def hello():\n    return True\n")
        undo = CheckpointManager(backup_dir=Path(d) / "backups")
        before = undo.file_hash(target)
        undo.checkpoint(target)
        target.write_text("BROKEN ((((")
        assert undo.file_hash(target) != before
        assert undo.restore(target) is True
        assert undo.file_hash(target) == before
        assert "return True" in target.read_text()


def test_loop_halts_on_third_repeat():
    alarm = LoopAlarm()
    assert alarm.record_action("bash", {"cmd": "cat file"}) == "ok"
    assert alarm.record_action("bash", {"cmd": "cat file"}) == "ok"
    decision = alarm.record_action("bash", {"cmd": "cat file"})
    assert decision.startswith("halt")
