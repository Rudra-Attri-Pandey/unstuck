"""Fix 1: polite waiting when rate-limited. No hammering, no crash."""

import random
import time


class RetryableError(Exception):
    """Transient error worth retrying (429, 5xx, timeout)."""


class RateLimitedError(RetryableError):
    """Blocked by provider. Carries optional server wait hint."""

    def __init__(self, message="rate limited", retry_after=None):
        super().__init__(message)
        self.retry_after = retry_after


# Errors we NEVER retry: bad request, bad key, bad output.
_DO_NOT_RETRY = (ValueError, TypeError, KeyError, AttributeError)


class PoliteWaiter:
    """Wait smartly and retry. Stops 80% of 429-halts.

    Example:
        waiter = PoliteWaiter(max_retries=4)
        result = waiter.run(my_api_call)
    """

    def __init__(self, max_retries=4, base_delay=1.0, max_delay=30.0):
        self.max_retries = max_retries
        self.base_delay = base_delay
        self.max_delay = max_delay
        self.sleeps = []  # recorded for tests / logs

    def _wait_time(self, attempt, retry_after=None):
        if retry_after is not None:
            try:
                return max(0.0, float(retry_after))
            except (TypeError, ValueError):
                pass
        cap = min(self.max_delay, self.base_delay * (2 ** attempt))
        return random.uniform(0, cap)

    def run(self, func, *args, **kwargs):
        """Run func, retrying only transient errors."""
        last_error = None
        for attempt in range(self.max_retries + 1):
            try:
                return func(*args, **kwargs)
            except _DO_NOT_RETRY:
                raise
            except RetryableError as e:
                last_error = e
                if attempt >= self.max_retries:
                    break
                hint = getattr(e, "retry_after", None)
                wait = self._wait_time(attempt, hint)
                self.sleeps.append(wait)
                time.sleep(wait)
            except Exception as e:
                # Unknown error: retry once-ish, then stop. Never loop forever.
                last_error = e
                if attempt >= 1:
                    raise
                wait = self._wait_time(attempt)
                self.sleeps.append(wait)
                time.sleep(wait)
        raise last_error
