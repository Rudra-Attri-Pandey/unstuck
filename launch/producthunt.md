# Unstuck — Product Hunt launch kit

> Status: DRAFT. Fill the thumbnail, pick a Tuesday–Thursday, launch at 00:01 PST.

## Tagline (pick one, max 60 chars)

1. Agents that don't quit — open-source reliability layer **(recommended)**
2. Stop AI coding agents from stalling, looping, breaking files
3. Four small fixes that keep coding agents alive

## Description

AI coding agents die the same four deaths: rate-limit blocks, memory blowups,
endless debug loops, broken files. I read two research reports on these failure
modes, then built the fixes as a tiny Python library:

1. **Polite waiting** — backs off smartly on 429s instead of hammering.
2. **Smart memory** — summarizes old turns instead of piling up context.
3. **Loop alarm** — same action 3x means stop and ask a human.
4. **Undo button** — auto-saves before every edit, restores in one click.

Stdlib only, no API keys to try, 5 tests green on every commit, animated demo
in the README generated from real runs. Copy `src/` into your own agent.

Free and open-source (MIT) — built so other builders stop losing runs.

## Maker comment (post this first, in your voice)

Hey PH! I'm Rudra. After shipping 4 AI apps, the thing that kept eating my
time wasn't features — it was my coding agents dying mid-run. Research talks
about agents burning millions of tokens across 34-iteration debug spirals, and
I'd lived it.

So I distilled the fixes into Unstuck: 4 small modules you can read in one
sitting and drop into any agent. The demo in the README is a real terminal
transcript, not a mock — before gets stuck, after stays unstuck.

I'd love feedback especially on: what's the failure mode that kills YOUR
agents most? That's what v0.2 targets.

## Launch checklist

- [ ] Thumbnail: export `assets/demo.svg` frame as PNG/GIF (1200x630), or record the 2-min terminal run
- [ ] Topics: Open Source, Developer Tools, Artificial Intelligence
- [ ] Links: GitHub repo + live demo section of README
- [ ] Maker badge claimed; hunter = yourself (as with the last 4 launches)
- [ ] Launch Tue–Thu at 00:01 PST; reply to every comment within 24h
- [ ] Cross-post the demo the same day (X, LinkedIn, relevant subreddits)
