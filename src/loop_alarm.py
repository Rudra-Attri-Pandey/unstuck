"""Fix 3: loop alarm. Repeat 3x = stop and ask a human."""

import difflib
import hashlib
import json


def _action_hash(tool, args):
    canonical = json.dumps({"tool": tool, "args": args or {}}, sort_keys=True, default=str)
    return hashlib.sha256(canonical.encode()).hexdigest()[:16]


def _similar(a, b):
    if not a or not b:
        return 0.0
    return difflib.SequenceMatcher(None, a, b).ratio()


class LoopAlarm:
    """3-layer guard: exact repeats, paraphrased repeats, zero progress.

    Usage:
        alarm = LoopAlarm()
        decision = alarm.record_action("bash", {"cmd": "cat file"})
        if decision.startswith("halt"):
            ask_human()
    """

    def __init__(self, max_exact_repeats=3, similarity_threshold=0.9, max_zero_progress=3):
        self.max_exact_repeats = max_exact_repeats
        self.similarity_threshold = similarity_threshold
        self.max_zero_progress = max_zero_progress
        self.action_counts = {}
        self.recent_texts = []  # last 5 (content + tool) for similarity
        self.zero_streak = 0

    def record_action(self, tool, args=None, text=""):
        key = _action_hash(tool, args)
        self.action_counts[key] = self.action_counts.get(key, 0) + 1
        if self.action_counts[key] >= self.max_exact_repeats:
            return "halt_exact: same action 3x"

        blob = f"{tool} {json.dumps(args or {}, sort_keys=True, default=str)} {text}"
        for old in self.recent_texts[-5:]:
            if _similar(blob, old) >= self.similarity_threshold and len(self.recent_texts) >= 2:
                return "halt_similar: paraphrased repeat"
        self.recent_texts.append(blob)
        self.recent_texts = self.recent_texts[-5:]
        return "ok"

    def record_progress(self, changed):
        """Call after each file/tool step. changed=True if files actually changed."""
        if changed:
            self.zero_streak = 0
            return "ok"
        self.zero_streak += 1
        if self.zero_streak >= self.max_zero_progress:
            return "halt_noprogress: files unchanged 3 steps"
        return "ok"

    def reset(self):
        self.action_counts.clear()
        self.recent_texts.clear()
        self.zero_streak = 0
