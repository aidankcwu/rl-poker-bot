# Poker AI — Exploitative RL Agent

## Project
Learning RL by building an exploitative poker agent.
Primary envs: Kuhn Poker → Leduc Hold'em. Python 3.13.
OpenSpiel unavailable (no wheel for 3.13) — use kuhn_pure.py fallback.

## Repo layout
- envs/        game environments (kuhn_pure.py, leduc/)
- agents/      RL agents, opponent models, opponents/
- experiments/ training scripts
- scripts/     exploratory one-offs (check_env.py etc.)
- docs/        theory notes, experiment logs, current_plan.md

## Rules — follow these always
- DO NOT implement CFR from scratch. Use library solvers or skip.
- DO NOT refactor working code unless explicitly asked.
- DO NOT spend more than 5 min debugging a single issue — note it, move on.
- Every experiment script must be runnable standalone: python script.py
- Every experiment must log to CSV: iteration, avg_return, exploit_rate

## Commands
- Lint: flake8 agents/ envs/ --select=E9,F821,F401
- Test: python -m pytest tests/ -x -q

## Session start
Read docs/current_plan.md before doing anything.
