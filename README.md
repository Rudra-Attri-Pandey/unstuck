# Unstuck
![tests](https://github.com/Rudra-Attri-Pandey/unstuck/actions/workflows/tests.yml/badge.svg)

Agents that don't quit on you. No sudden stops, no endless loops, no forgetting, no broken files.

Built for builders. Free and open-source.

## The 4 pains we fix

1. **Polite waiting** — blocked by rate limits? Wait smartly and retry instead of crashing.
2. **Smart memory** — summarize old work instead of piling everything up.
3. **Loop alarm** — same action 3x = stop and ask a human.
4. **Undo button** — auto-save before every edit, restore in 1 click.

## 2-min quick-start

```bash
python -m venv .venv
.venv\Scripts\activate
python examples/quickstart.py
```

No keys needed. No internet needed. Stdlib only.

## Demo

![Unstuck demo: before gets stuck, after stays unstuck](assets/demo.svg)

*Animated transcript of real runs — regenerate anytime with `python examples/make_demo.py`.*

`examples/before_stuck.py` shows the classic fail: naive retry hammers the API,
memory grows forever, same command repeats, bad edit stays broken.

`examples/after_unstuck.py` runs the same task with Unstuck: waits politely,
condenses memory, halts the loop, restores the file.

## Run tests

```bash
python -m pytest tests/ -v
```

3 tests: burst, memory, undo.

## Use in your project

```python
from src.waiter import PoliteWaiter
from src.memory import SmartMemory
from src.loop_alarm import LoopAlarm
from src.undo import CheckpointManager
```

Copy `src/` into your agent. That's it.

## Roadmap

- [ ] Async waiter + token-bucket queue
- [ ] Embedding similarity for loop alarm
- [ ] Git-native checkpoints
- [ ] More examples from the community
