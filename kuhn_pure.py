"""
Pure-Python implementation of Kuhn Poker.

Used as a fallback when open_spiel/pyspiel is not available.
The API mirrors OpenSpiel's game/state interface so the other scripts
can work against either backend with minimal branching.

Kuhn Poker rules:
  - 3-card deck: Jack=0, Queen=1, King=2
  - Each player antes 1 chip and receives 1 card.
  - Player 0 acts first: check(0) or bet(1).
  - If Player 0 checks, Player 1 acts: check(0) ends in showdown, bet(1)
    gives Player 0 another action: fold(0) or call(1).
  - If Player 0 bets, Player 1 acts: fold(0) or call(1).
  - At showdown, higher card wins the pot.

Chance player is represented as CHANCE_PLAYER = -1 (matching OpenSpiel).
"""

import itertools
from copy import deepcopy

CHANCE_PLAYER = -1
JACK, QUEEN, KING = 0, 1, 2
CARD_NAMES = {0: "Jack", 1: "Queen", 2: "King"}

# All 6 orderings of (card_for_player0, card_for_player1)
DEAL_ORDERINGS = list(itertools.permutations([JACK, QUEEN, KING], 2))


class KuhnState:
    """
    Represents a single node in the Kuhn Poker game tree.

    Internal action history (self._actions) stores deals and player actions
    in sequence:
      - First entry is the deal index (into DEAL_ORDERINGS), dealing both cards at once
      - Subsequent entries are player actions (0=check/fold, 1=bet/call)
    """

    def __init__(self):
        self._actions = []  # sequence of actions taken so far

    def clone(self):
        s = KuhnState()
        s._actions = self._actions[:]
        return s

    # ------------------------------------------------------------------
    # Node type queries
    # ------------------------------------------------------------------

    def is_chance_node(self):
        """True if we're still in the card-dealing phase."""
        return len(self._actions) < 1

    def is_terminal(self):
        """True if the hand is over."""
        if len(self._actions) < 1:
            return False
        # Player actions come after the single deal action
        pa = self._actions[1:]
        n = len(pa)
        if n == 0:
            return False
        # bet then fold/call => done
        if pa[0] == 1:           # P0 bets
            return n >= 2        # P1 responds (fold or call)
        # check then ...
        if n == 1:
            return False         # P1 hasn't acted yet
        if pa[1] == 0:
            return True          # both check => showdown
        # pa[1] == 1 (P1 bets after P0 check)
        return n >= 3            # P0 responds (fold or call)

    def current_player(self):
        """
        Returns the player to act, or CHANCE_PLAYER if dealing is unfinished.
        Raises if called on a terminal node.
        """
        if self.is_terminal():
            raise RuntimeError("current_player called on terminal node")
        if self.is_chance_node():
            return CHANCE_PLAYER
        pa = self._actions[1:]
        n = len(pa)
        if n == 0:
            return 0             # P0 acts first
        if pa[0] == 1:           # P0 bet => P1 responds
            return 1
        # P0 checked
        if n == 1:
            return 1             # P1 acts
        # pa[1] == 1 (P1 bet after P0 check) => P0 responds
        return 0

    # ------------------------------------------------------------------
    # Legal actions
    # ------------------------------------------------------------------

    def legal_actions(self, player=None):
        """
        Returns list of legal action ints.
          - Chance node: indices into DEAL_ORDERINGS (0..5)
          - Player node: [0, 1]  (check/fold or bet/call)
        """
        if self.is_terminal():
            return []
        if self.is_chance_node():
            return list(range(len(DEAL_ORDERINGS)))
        return [0, 1]

    def chance_outcomes(self):
        """Returns list of (action, probability) for chance nodes."""
        prob = 1.0 / len(DEAL_ORDERINGS)
        return [(a, prob) for a in range(len(DEAL_ORDERINGS))]

    # ------------------------------------------------------------------
    # Applying actions
    # ------------------------------------------------------------------

    def apply_action(self, action):
        """Apply an action (in-place). Use clone() first to avoid mutation."""
        self._actions.append(action)

    def child(self, action):
        """Return a new state with action applied."""
        s = self.clone()
        s.apply_action(action)
        return s

    # ------------------------------------------------------------------
    # Information state strings (what a player can observe)
    # ------------------------------------------------------------------

    def information_state_string(self, player):
        """
        Returns a string encoding what `player` can observe.

        Format: "<card> <visible_actions...>"
        where visible_actions are all player actions so far
        (both players' actions are public; only the dealt cards are private).

        Example: player 0 holds Jack(0), and the action sequence so far is
        [check, bet] => "0 0 1"
        """
        if len(self._actions) < 1:
            # Cards haven't been dealt yet; shouldn't be called
            return ""
        card = self._cards()[player]
        pa = self._actions[1:]   # player actions, all are public info
        parts = [str(card)] + [str(a) for a in pa]
        return " ".join(parts)

    # ------------------------------------------------------------------
    # Returns (payoffs)
    # ------------------------------------------------------------------

    def returns(self):
        """
        Returns [return_p0, return_p1] from the perspective of each player
        relative to their ante of 1. Ante is already paid, so:
          - win a bet:  +1
          - lose a bet: -1
          - win at showdown (no bets): +1 (win opponent's ante)
          - lose at showdown (no bets): -1
        """
        assert self.is_terminal(), "returns() called on non-terminal state"
        c0, c1 = self._cards()
        pa = self._actions[1:]

        if pa[0] == 1:
            # P0 bet
            if pa[1] == 0:
                # P1 folds => P0 wins P1's ante (+1 for P0)
                return [1.0, -1.0]
            else:
                # P1 calls => showdown, winner takes the pot (ante + bet each)
                # Pot = 4 chips total (1 ante + 1 bet each). Winner nets +2 from start,
                # loser nets -2. But relative to ante already paid:
                # winner gains opponent's ante+bet = +2, loser loses own bet = -2
                if c0 > c1:
                    return [2.0, -2.0]
                else:
                    return [-2.0, 2.0]
        else:
            # P0 checked
            if pa[1] == 0:
                # Both check => showdown, pot = 2 chips (antes only)
                if c0 > c1:
                    return [1.0, -1.0]
                else:
                    return [-1.0, 1.0]
            else:
                # P1 bet after P0 check
                if pa[2] == 0:
                    # P0 folds => P1 wins
                    return [-1.0, 1.0]
                else:
                    # P0 calls => showdown, pot = 4 chips
                    if c0 > c1:
                        return [2.0, -2.0]
                    else:
                        return [-2.0, 2.0]

    # ------------------------------------------------------------------
    # Human-readable representation
    # ------------------------------------------------------------------

    def __str__(self):
        if len(self._actions) < 1:
            return "[dealing cards]"
        c0, c1 = self._cards()
        pa = self._actions[1:]
        action_names = {0: "check/fold", 1: "bet/call"}
        history = ", ".join(action_names[a] for a in pa) if pa else "no actions yet"
        return f"P0:{CARD_NAMES[c0]} P1:{CARD_NAMES[c1]} | history=[{history}]"

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------

    def _cards(self):
        """Returns (card_p0, card_p1). Only valid after dealing is done."""
        deal_idx = self._actions[0] * len(DEAL_ORDERINGS) // len(DEAL_ORDERINGS)
        # The first action is a deal index into DEAL_ORDERINGS
        return DEAL_ORDERINGS[self._actions[0]]


class KuhnGame:
    """
    Thin wrapper providing game-level metadata, mirroring OpenSpiel's game object.
    """

    def __init__(self):
        self.num_players_ = 2
        self.num_distinct_actions_ = 2   # check/fold=0, bet/call=1
        # Chance actions (deals) are separate; player actions are 0 or 1

    def new_initial_state(self):
        return KuhnState()

    def num_players(self):
        return self.num_players_

    def num_distinct_actions(self):
        return self.num_distinct_actions_

    def max_game_length(self):
        # 1 deal action + at most 3 player actions
        return 4

    def min_utility(self):
        return -2.0

    def max_utility(self):
        return 2.0

    def __str__(self):
        return "kuhn_poker (pure-python fallback)"
