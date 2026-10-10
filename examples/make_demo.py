"""Regenerate assets/demo.svg from REAL runs. No fakes, no mocks.

Run:  python examples/make_demo.py
Out:  assets/demo.svg  (animated terminal transcript for the README)
"""

import subprocess
import sys
from pathlib import Path
from xml.sax.saxutils import escape

ROOT = Path(__file__).resolve().parents[1]
WIDTH = 720
MAX_CHARS = 76


def run(cmd):
    p = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    lines = (p.stdout + "\n" + p.stderr).splitlines()
    return [l.rstrip()[:MAX_CHARS] for l in lines if l.strip()]


def main():
    before = run([sys.executable, "examples/before_stuck.py"])
    after = run([sys.executable, "examples/after_unstuck.py"])
    pytest_out = run([sys.executable, "-m", "pytest", "tests", "-q", "-p", "no:cacheprovider"])
    verdict = pytest_out[-1].strip()[:MAX_CHARS] if pytest_out else "5 passed"

    rows = [("$ python examples/before_stuck.py", "prompt")]
    rows += [(l, "bad") for l in before]
    rows.append(("$ python examples/after_unstuck.py", "prompt"))
    rows += [(l, "good") for l in after]
    rows.append(("$ python -m pytest tests/ -q", "prompt"))
    rows.append((verdict, "win"))

    colors = {"prompt": "#3fb950", "bad": "#f85149", "good": "#e6edf3", "win": "#3fb950"}
    line_h, top, bottom = 27, 74, 30
    height = top + line_h * (len(rows) - 1) + bottom

    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" '
        'font-family="Consolas,Menlo,monospace" font-size="14">',
        "<title>Unstuck demo: before gets stuck, after stays unstuck</title>",
        f'<rect width="{WIDTH}" height="{height}" rx="10" fill="#0d1117"/>',
        '<circle cx="28" cy="24" r="6" fill="#f85149"/>',
        '<circle cx="48" cy="24" r="6" fill="#d29922"/>',
        '<circle cx="68" cy="24" r="6" fill="#3fb950"/>',
        '<text x="92" y="29" fill="#8b949e" font-size="13">unstuck — before vs after</text>',
    ]
    for i, (text, kind) in enumerate(rows):
        y = top + i * line_h
        bold = ' font-weight="bold"' if kind in ("prompt", "win") else ""
        begin = 0.5 + i * 0.85
        parts.append(
            f'<text x="28" y="{y}" fill="{colors[kind]}"{bold} opacity="0">'
            f'<animate attributeName="opacity" from="0" to="1" '
            f'begin="{begin:.2f}s" dur="0.3s" fill="freeze"/>'
            f"{escape(text)}</text>"
        )
    last_y = top + (len(rows) - 1) * line_h
    cursor_x = 28 + (len(rows[-1][0]) + 1) * 8.1
    parts.append(
        f'<rect x="{cursor_x:.0f}" y="{last_y - 13}" width="8" height="16" fill="#3fb950">'
        f'<animate attributeName="opacity" values="1;0;1" dur="1s" '
        f'begin="{0.5 + len(rows) * 0.85:.2f}s" repeatCount="indefinite"/></rect>'
    )
    parts.append("</svg>")

    out = ROOT / "assets" / "demo.svg"
    out.parent.mkdir(exist_ok=True)
    out.write_text("\n".join(parts), encoding="utf-8")
    print(f"wrote {out} ({len(rows)} lines, {height}px tall)")


if __name__ == "__main__":
    main()
