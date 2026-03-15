"""
info_sets.py — Step 3: Collect and display all information sets in Kuhn Poker.

An information set groups together all game states that a player cannot
distinguish from one another. In Kuhn Poker, a player sees only their own
card — not the opponent's. So "I hold a Jack and the action history is
[check]" is one information set, regardless of whether the opponent holds
a Queen or a King.

This script walks the full game tree and collects, for each player:
  - The information state string (what the player can observe)
  - Which distinct game states (histories) map to that info set
  - What actions are legal from that info set

Expected result: 6 info sets per player, 12 total.
"""

from collections import defaultdict

# Try OpenSpiel first, fall back to pure Python
try:
    import pyspiel  # type: ignore
    game = pyspiel.load_game("kuhn_poker")
    USING_OPENSPIEL = True
except ImportError:
    from kuhn_pure import KuhnGame, CHANCE_PLAYER
    game = KuhnGame()
    USING_OPENSPIEL = False

BACKEND = "OpenSpiel" if USING_OPENSPIEL else "pure-Python fallback"
print(f"=== Kuhn Poker Information Sets ({BACKEND}) ===")
print()
print("KEY CONCEPT: An information set groups states a player CANNOT distinguish.")
print("In Kuhn Poker, each player sees only their own card + the action history.")
print("Two states with the same (my card, action history) are indistinguishable")
print("even if the opponent's card differs.")
print()

# ------------------------------------------------------------------
# Data structures for collecting info sets
# ------------------------------------------------------------------

# For each player: info_state_str -> list of human-readable state descriptions
info_set_states = defaultdict(lambda: defaultdict(list))
# For each player: info_state_str -> legal actions (same for all states in the set)
info_set_actions = defaultdict(dict)


def walk(state, history="root"):
    """Recursively walk the tree and record info sets at every player node."""
    if state.is_terminal():
        return

    if state.is_chance_node():
        outcomes = state.chance_outcomes()
        for action, _ in outcomes:
            child = state.child(action)
            child_history = f"{history}->deal({action})"
            walk(child, child_history)
        return

    # It's a player node
    player = state.current_player()
    actions = state.legal_actions()

    if USING_OPENSPIEL:
        info_str = state.information_state_string(player)
        state_desc = str(state)
    else:
        info_str = state.information_state_string(player)
        state_desc = str(state)

    # Record this game state as belonging to this info set
    info_set_states[player][info_str].append(state_desc)
    info_set_actions[player][info_str] = actions

    for action in actions:
        child = state.child(action)
        child_history = f"{history}->{action}"
        walk(child, child_history)


root = game.new_initial_state()
walk(root)

# ------------------------------------------------------------------
# Print results, grouped by player
# ------------------------------------------------------------------

ACTION_NAMES = {0: "check/fold", 1: "bet/call"}

for player in sorted(info_set_states.keys()):
    sets = info_set_states[player]
    print(f"{'='*55}")
    print(f"  Player {player} — {len(sets)} information sets")
    print(f"{'='*55}")

    for info_str, state_descs in sorted(sets.items()):
        actions = info_set_actions[player][info_str]
        action_desc = ", ".join(f"{a}({ACTION_NAMES[a]})" for a in actions)
        num_states = len(state_descs)

        print(f"  Info set: \"{info_str}\"")
        print(f"    Distinct game states mapped here: {num_states}")
        for desc in state_descs:
            print(f"      - {desc}")
        print(f"    Legal actions: [{action_desc}]")

        # Explain WHY multiple states share this info set, when they do
        if num_states > 1:
            print(f"    ^ These {num_states} states look IDENTICAL to Player {player}:")
            print(f"      same card, same action history — opponent's card is hidden.")
        print()

# ------------------------------------------------------------------
# Summary
# ------------------------------------------------------------------
total = sum(len(v) for v in info_set_states.values())
print(f"Total information sets across all players: {total}")
print()
print("This is why imperfect-information games are hard:")
print("a strategy must map each INFO SET to an action, not each game state.")
print("The number of info sets (not states) determines strategy complexity.")
