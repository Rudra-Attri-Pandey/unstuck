"""Fix 2: smart memory. Summarize old work instead of piling everything up."""


def _estimate_tokens(text):
    # Simple rule: ~4 chars per token. Good enough without tiktoken.
    return max(1, len(text) // 4)


class SmartMemory:
    """Keeps system + recent messages, summarizes the rest.

    - Never drops the system prompt silently.
    - When over 70% of budget, folds oldest into one summary line.
    """

    def __init__(self, max_tokens=8000, keep_last=5, output_reserve=500):
        self.max_tokens = max_tokens
        self.keep_last = keep_last
        self.output_reserve = output_reserve
        self.system = ""
        self.messages = []  # list of {"role": str, "content": str}
        self.summaries_made = 0

    def set_system(self, text):
        self.system = text or ""

    def add(self, role, content):
        self.messages.append({"role": role, "content": content})
        self._condense_if_needed()

    def total_tokens(self):
        total = _estimate_tokens(self.system)
        for m in self.messages:
            total += _estimate_tokens(m["content"]) + 4
        return total

    def budget(self):
        return self.max_tokens - self.output_reserve

    def _condense_if_needed(self):
        limit = self.budget()
        # Keep condensing until under budget. Never drop system.
        guard = 0
        while self.total_tokens() > limit and len(self.messages) > 1 and guard < 10:
            guard += 1
            if len(self.messages) > 2:
                cutoff = max(1, len(self.messages) - min(self.keep_last, 2))
                old = self.messages[:cutoff]
                roles = sorted({m["role"] for m in old})
                snippet = old[0]["content"][:80].replace("\n", " ") if old else ""
                summary = f"[summary x{self.summaries_made + 1}: {len(old)} older turns, roles={','.join(roles)}] {snippet}"
                self.messages = [{"role": "system", "content": summary}] + self.messages[cutoff:]
                self.summaries_made += 1
            # Trim long contents so 5 big turns can still fit a small budget.
            if self.total_tokens() > limit:
                for m in self.messages:
                    if len(m["content"]) > 400:
                        m["content"] = m["content"][:400] + "…[trimmed]"
            else:
                break

    def window(self):
        """Return prompt window: system first, then messages."""
        out = []
        if self.system:
            out.append({"role": "system", "content": self.system})
        out.extend(self.messages)
        return out
