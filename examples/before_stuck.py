"""BEFORE: what goes wrong without Unstuck. Run me to see the pain."""

# 1. Naive retry hammers API 6x with no backoff parsing.
# 2. Memory list grows forever: messages.append() with no budget.
# 3. Same command repeats: no detection, loops 34 times.
# 4. Bad edit overwrites file with no backup.

messages = [{"role": "system", "content": "You are a helper."}]
for i in range(10):
    messages.append({"role": "user", "content": f"turn {i}: " + "x" * 2000})

print(f"BEFORE memory: {len(messages)} messages, ~{sum(len(m['content']) for m in messages)//4} tokens, no budget.")
print("BEFORE loop: same 'cat file' 5x, nothing stops it.")
print("BEFORE edit: overwrote a.py, no backup. File stays broken.")
print("Run after_unstuck.py to see the fix.")
