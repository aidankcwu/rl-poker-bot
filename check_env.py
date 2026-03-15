"""
check_env.py — Step 1: Verify the environment is ready for Kuhn Poker exploration.

Tries to install and import open_spiel/pyspiel. If that fails (common on
Python 3.13 where no pre-built wheel exists), falls back to the pure-Python
implementation in kuhn_pure.py and prints equivalent info.
"""

import sys
import subprocess

print("=" * 60)
print("ENVIRONMENT CHECK")
print("=" * 60)
print(f"Python version: {sys.version}")
print()

# ------------------------------------------------------------------
# Step 1: Attempt to install open_spiel
# ------------------------------------------------------------------
print("Attempting to install open_spiel via pip...")
result = subprocess.run(
    [sys.executable, "-m", "pip", "install", "open_spiel", "--quiet"],
    capture_output=True,
    text=True,
)
if result.returncode == 0:
    print("  pip install succeeded (or package already present)")
else:
    print("  pip install failed — likely no wheel for this Python version")
    print(f"  stderr: {result.stderr.strip()[:200]}")
print()

# ------------------------------------------------------------------
# Step 2: Try to import pyspiel and load kuhn_poker
# ------------------------------------------------------------------
USING_OPENSPIEL = False
try:
    import pyspiel  # type: ignore
    game = pyspiel.load_game("kuhn_poker")
    USING_OPENSPIEL = True
    print("STATUS: OPENSPIEL READY")
    print()
    print("Game info (via OpenSpiel):")
    print(f"  Name:                 {game.get_type().short_name}")
    print(f"  Num players:          {game.num_players()}")
    print(f"  Num distinct actions: {game.num_distinct_actions()}")
    print(f"  Max game length:      {game.max_game_length()}")
    print(f"  Min utility:          {game.min_utility()}")
    print(f"  Max utility:          {game.max_utility()}")

except ImportError:
    print("STATUS: USING PURE-PYTHON FALLBACK (pyspiel not importable)")
    print()

    # Fall back to our own implementation
    from kuhn_pure import KuhnGame
    game = KuhnGame()

    print("Game info (via pure-Python fallback):")
    print(f"  Name:                 {game}")
    print(f"  Num players:          {game.num_players()}")
    print(f"  Num distinct actions: {game.num_distinct_actions()}")
    print(f"  Max game length:      {game.max_game_length()}")
    print(f"  Min utility:          {game.min_utility()}")
    print(f"  Max utility:          {game.max_utility()}")

# ------------------------------------------------------------------
# Step 3: Quick sanity check — play one hand manually
# ------------------------------------------------------------------
print()
print("Sanity check: deal cards and take a few actions...")

if USING_OPENSPIEL:
    state = game.new_initial_state()
    # Deal cards (chance actions)
    while state.is_chance_node():
        outcomes = state.chance_outcomes()
        action = outcomes[0][0]  # take the first outcome deterministically
        state.apply_action(action)
    print(f"  State after dealing: {state}")
    print(f"  Legal actions for P0: {state.legal_actions()}")
    state.apply_action(1)  # P0 bets
    print(f"  State after P0 bets: {state}")
    state.apply_action(0)  # P1 folds
    print(f"  Terminal: {state.is_terminal()}")
    print(f"  Returns: {state.returns()}")
else:
    from kuhn_pure import KuhnState, DEAL_ORDERINGS
    state = KuhnState()
    state.apply_action(0)  # deal ordering index 0 => (Jack, Queen)
    print(f"  State after dealing: {state}")
    print(f"  Legal actions for P0: {state.legal_actions()}")
    state.apply_action(1)  # P0 bets
    print(f"  State after P0 bets: {state}")
    state.apply_action(0)  # P1 folds
    print(f"  Terminal: {state.is_terminal()}")
    print(f"  Returns: {state.returns()}")

print()
print("All checks passed. Ready to explore!")
