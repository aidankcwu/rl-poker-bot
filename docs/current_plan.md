# Current Plan

## Status
Initial setup complete. Exploratory scripts (check_env.py, explore_tree.py,
info_sets.py, nash_verify.py, exploit_demo.py) are working in scripts/.

## Working
- Kuhn Poker game tree explorer
- Information set inspector
- Basic exploit demo showing EV difference vs scripted opponents

## Next step
Begin Step 2: implement a baseline DQN or PPO agent in Leduc Hold'em
using RLCard. Verify it trains without crashing before adding complexity.

## Punted issues
- OpenSpiel not installable on Python 3.13, using kuhn_pure.py fallback
- CFR convergence issues in nash_verify.py — not a priority, skip for now
