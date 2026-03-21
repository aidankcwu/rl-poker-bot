---
name: add-opponent
description: Use when creating a new scripted opponent for training or
evaluation. Trigger phrases: "new opponent", "scripted opponent",
"add opponent", "always bluffs", "tight passive", "loose aggressive",
"opponent that never folds".
---

# Add Opponent

New opponents go in agents/opponents/.
Create that folder if it does not exist.

## Requirements for every opponent file

1. Implement exactly this interface:
   def get_action(info_state, legal_actions) -> action
   where action is one of the values in legal_actions.

2. Include a docstring at the top of the class describing:
   - The exploitable leak this opponent has
   - What the counter-strategy should be

3. Include a quick self-test at the bottom:
   if __name__ == "__main__":
       # instantiate opponent, call get_action 100 times, print action counts

4. Register the class in agents/opponents/__init__.py

## Naming convention
Use descriptive names: always_bluff.py, tight_passive.py, freq_based.py
Class name should match: AlwaysBluff, TightPassive, FreqBased
