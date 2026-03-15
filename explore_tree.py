"""
explore_tree.py — Step 2: Walk and print the full Kuhn Poker game tree.

Recursively visits every node from the root, printing:
  - CHANCE nodes: the card-dealing outcomes
  - PLAYER nodes: which player acts, the current game state, legal actions
  - TERMINAL nodes: the final state and each player's payoff

The indentation depth shows where you are in the tree. Kuhn Poker is tiny
(~58 terminal nodes), so the entire tree fits on one screen.
"""

import sys

# Try OpenSpiel first, fall back to pure Python
try:
    import pyspiel  # type: ignore
    game = pyspiel.load_game("kuhn_poker")
    USING_OPENSPIEL = True
except ImportError:
    from kuhn_pure import KuhnGame, DEAL_ORDERINGS, CARD_NAMES, CHANCE_PLAYER
    game = KuhnGame()
    USING_OPENSPIEL = False

BACKEND = "OpenSpiel" if USING_OPENSPIEL else "pure-Python fallback"
print(f"=== Kuhn Poker Game Tree ({BACKEND}) ===")
print()

# Action labels for player nodes (Kuhn has only 2 actions)
ACTION_NAMES = {0: "check/fold", 1: "bet/call"}


def node_type_label(state):
    """Return a short string describing what kind of node this is."""
    if state.is_terminal():
        return "TERMINAL"
    if state.is_chance_node():
        return "CHANCE"
    return f"PLAYER {state.current_player()}"


def format_chance_action(action):
    """Describe a chance action (card deal) in a human-readable way."""
    if USING_OPENSPIEL:
        # OpenSpiel chance actions are just integers; description not easily
        # available without game-specific knowledge, so label generically.
        return f"deal({action})"
    else:
        # In our pure-Python engine, action is an index into DEAL_ORDERINGS
        c0, c1 = DEAL_ORDERINGS[action]
        return f"deal P0:{CARD_NAMES[c0]}, P1:{CARD_NAMES[c1]}"


def explore(state, depth=0):
    """Recursively print the game tree from `state`."""
    indent = "  " * depth
    label = node_type_label(state)

    if state.is_terminal():
        # Show the final game state and the payoff for each player
        ret = state.returns()
        print(f"{indent}[{label}]  {state}")
        print(f"{indent}           Returns: P0={ret[0]:+.1f}  P1={ret[1]:+.1f}")
        return

    if state.is_chance_node():
        print(f"{indent}[{label}]  (dealing cards...)")
        outcomes = state.chance_outcomes()
        for action, prob in outcomes:
            desc = format_chance_action(action)
            print(f"{indent}  -> {desc}  (prob={prob:.4f})")
            child = state.child(action) if not USING_OPENSPIEL else _os_child(state, action)
            explore(child, depth + 1)
    else:
        # Player node
        player = state.current_player()
        actions = state.legal_actions()
        action_desc = ", ".join(f"{a}={ACTION_NAMES[a]}" for a in actions)
        print(f"{indent}[{label}]  {state}")
        print(f"{indent}           Legal actions: [{action_desc}]")
        for action in actions:
            print(f"{indent}  -> action={action} ({ACTION_NAMES[action]})")
            child = state.child(action) if not USING_OPENSPIEL else _os_child(state, action)
            explore(child, depth + 1)


def _os_child(state, action):
    """Apply an action to an OpenSpiel state without mutating the original."""
    s = state.child(action)
    return s


# ------------------------------------------------------------------
# Entry point: start from the initial (root) state
# ------------------------------------------------------------------
root = game.new_initial_state()
explore(root)

print()
print("Tree walk complete.")
