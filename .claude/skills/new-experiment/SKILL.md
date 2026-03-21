---
name: new-experiment
description: Use when creating a new RL training script, agent variant,
or experiment file. Ensures consistent logging, checkpointing, and
reproducibility. Trigger phrases: "new experiment", "training script",
"train an agent", "set up training".
---

# New Experiment

Every experiment file must follow this structure:

1. Config dict or argparse at the top — no hardcoded hyperparameters
2. CSV logging to logs/{experiment_name}_{timestamp}.csv
   Required columns: iteration, avg_return, exploit_rate, opponent_type
3. Checkpoint saves to checkpoints/ every 1000 iterations
4. Summary printout at the end showing key metrics
5. Must be runnable standalone: python experiments/your_script.py

Use the template at templates/experiment_template.py as starting point.
Copy it — do not modify the template itself.
