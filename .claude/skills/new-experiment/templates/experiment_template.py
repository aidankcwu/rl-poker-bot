"""
Experiment template for poker AI project.
Copy this file to experiments/ and rename it.
Do not modify this template.
"""
import csv
import os
import time
import argparse

# ─── Config ───────────────────────────────────────────────────────────────────
def get_config():
    parser = argparse.ArgumentParser()
    parser.add_argument("--iterations", type=int, default=10000)
    parser.add_argument("--lr", type=float, default=0.001)
    parser.add_argument("--opponent", type=str, default="random")
    parser.add_argument("--experiment_name", type=str, default="experiment")
    return parser.parse_args()

# ─── Logging setup ────────────────────────────────────────────────────────────
def setup_logger(experiment_name):
    os.makedirs("logs", exist_ok=True)
    timestamp = time.strftime("%Y%m%d_%H%M%S")
    log_path = f"logs/{experiment_name}_{timestamp}.csv"
    f = open(log_path, "w", newline="")
    writer = csv.DictWriter(f, fieldnames=["iteration", "avg_return", "exploit_rate", "opponent_type"])
    writer.writeheader()
    print(f"Logging to {log_path}")
    return writer, f

# ─── Checkpoint ───────────────────────────────────────────────────────────────
def save_checkpoint(agent, iteration, experiment_name):
    os.makedirs("checkpoints", exist_ok=True)
    path = f"checkpoints/{experiment_name}_iter{iteration}.pkl"
    # replace with your agent's actual save method
    import pickle
    with open(path, "wb") as f:
        pickle.dump(agent, f)
    print(f"Checkpoint saved: {path}")

# ─── Main training loop ───────────────────────────────────────────────────────
def main():
    config = get_config()
    writer, log_file = setup_logger(config.experiment_name)

    # TODO: initialize your env and agent here
    env = None
    agent = None

    returns = []

    for i in range(config.iterations):
        # TODO: run one episode and get return
        episode_return = 0.0
        exploit_rate = 0.0
        returns.append(episode_return)

        # log every 100 iterations
        if i % 100 == 0:
            avg_return = sum(returns[-100:]) / len(returns[-100:])
            writer.writerow({
                "iteration": i,
                "avg_return": avg_return,
                "exploit_rate": exploit_rate,
                "opponent_type": config.opponent,
            })
            print(f"Iter {i:6d} | avg_return={avg_return:.4f} | exploit={exploit_rate:.4f}")

        # checkpoint every 1000 iterations
        if i % 1000 == 0 and i > 0:
            save_checkpoint(agent, i, config.experiment_name)

    log_file.close()

    # summary
    all_returns = returns
    print("\n=== Summary ===")
    print(f"  Total iterations: {config.iterations}")
    print(f"  Final avg return (last 1000): {sum(all_returns[-1000:]) / 1000:.4f}")
    print(f"  Opponent: {config.opponent}")

if __name__ == "__main__":
    main()
