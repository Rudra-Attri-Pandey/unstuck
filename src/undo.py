"""Fix 4: undo button. Auto-save before every edit, restore in 1 click."""

import hashlib
import shutil
from pathlib import Path


class CheckpointManager:
    """Simple backup + restore. No git required, git-friendly if present.

    Backups live in <file's folder>/.unstuck_backups/ by default.
    """

    def __init__(self, backup_dir=None):
        self.backup_dir = Path(backup_dir) if backup_dir else None
        self._memory = {}  # path -> bytes, for fast restore in tests

    def _backup_path(self, path):
        p = Path(path)
        base = self.backup_dir or (p.parent / ".unstuck_backups")
        digest = hashlib.sha256(str(p.resolve()).encode()).hexdigest()[:10]
        return base / f"{p.name}.{digest}.bak"

    def checkpoint(self, path):
        """Save current file. Call BEFORE editing."""
        p = Path(path)
        if not p.exists():
            self._memory[str(p)] = None
            return None
        data = p.read_bytes()
        self._memory[str(p)] = data
        bak = self._backup_path(p)
        bak.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(p, bak)
        return str(bak)

    def restore(self, path):
        """Restore last checkpoint. Returns True if restored."""
        p = Path(path)
        key = str(p)
        if key in self._memory:
            data = self._memory[key]
            if data is None:
                if p.exists():
                    p.unlink()
                return True
            p.parent.mkdir(parents=True, exist_ok=True)
            p.write_bytes(data)
            return True
        bak = self._backup_path(p)
        if bak.exists():
            p.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(bak, p)
            return True
        return False

    def file_hash(self, path):
        p = Path(path)
        if not p.exists():
            return "missing"
        return hashlib.sha256(p.read_bytes()).hexdigest()[:16]
