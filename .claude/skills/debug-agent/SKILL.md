---
name: debug-agent
description: Use when an RL agent is not converging, stuck on one action,
producing degenerate strategies, or showing training instability. Trigger
phrases: "agent not learning", "always folds", "always calls", "diverging",
"not working", "something is wrong with training", "why is it doing this".
---

# Debug Agent

Before touching any code, run through this checklist in order.
Do not skip steps. Do not start editing code until you have identified
which step reveals the problem.

## Checklist

1. Print the reward signal for 20 random episodes.
   Is it nonzero? Is it varying? If rewards are all zero, the env is broken.

2. Print action distribution over 100 episodes.
   Is the agent playing only one action? If so, it has collapsed to a
   deterministic policy — this is the non-stationarity problem.

3. Check whether the opponent is changing mid-training.
   If the opponent is also learning, the reward signal is non-stationary.
   Freeze the opponent and retrain from scratch first.

4. Check learning rate.
   If training is unstable: try 10x smaller.
   If training is completely flat: try 10x larger.

5. Run 200 episodes against a random opponent as a sanity baseline.
   The agent should beat a random opponent. If it cannot, the setup is wrong,
   not the algorithm.

## After identifying the problem
Write a one-line comment above any fix explaining what the bug was.
Example: # BUG: reward was always 0 because env.reset() was not called
