"""
nash_verify.py — Step 4: Run the known Kuhn Poker Nash equilibrium and observe the EV.

The Nash equilibrium for Kuhn Poker is known analytically (Kuhn, 1950).
We hardcode it here and simulate 10,000 hands to see what it produces.

Key probabilities:
  - P0 Jack:   bet (bluff) 1/3 of the time — makes P1 indifferent about calling
  - P0 Queen:  always check
  - P0 King:   always bet

  - P1 Jack:   always check after P0 check; always fold after P0 bet
  - P1 Queen:  bet (bluff) 1/3 after P0 check; fold after P0 bet
  - P1 King:   always bet; always call

Why mixed strategies? A deterministic strategy leaks information.
If P0 Jack never bets, P1 knows any P0 bet = King and always folds Queen,
denying P0 value. The 1/3 bluff frequency is the exact rate that makes
P1 indifferent between calling and folding with Queen.
"""

import random
from kuhn_pure import KuhnGame, DEAL_ORDERINGS, CARD_NAMES

random.seed(42)

# Nash strategy: info_state_string -> [prob_check/fold, prob_bet/call]
NASH = {
    # Player 0 first action (info set = just their card)
    "0": [2/3, 1/3],   # Jack:  check 2/3, bluff-bet 1/3
    "1": [1.0, 0.0],   # Queen: always check
    "2": [0.0, 1.0],   # King:  always bet

    # Player 0 response after: P0 checked, P1 bet
    "0 0 1": [1.0, 0.0],  # Jack:  fold (can't beat Queen or King)
    "1 0 1": [1.0, 0.0],  # Queen: fold
    "2 0 1": [0.0, 1.0],  # King:  call

    # Player 1 response after P0 checked
    "0 0": [1.0, 0.0],  # Jack:  check (don't bluff)
    "1 0": [2/3, 1/3],  # Queen: check 2/3, bluff-bet 1/3
    "2 0": [0.0, 1.0],  # King:  bet

    # Player 1 response after P0 bet
    "0 1": [1.0, 0.0],  # Jack:  fold
    "1 1": [1.0, 0.0],  # Queen: fold
    "2 1": [0.0, 1.0],  # King:  call
}

print("=== Nash Strategy ===")
print()
print("Player 0 (first to act):")
print(f"  Jack  ('0'):      check={NASH['0'][0]:.2f}  bet={NASH['0'][1]:.2f}  <- bluffs 1/3")
print(f"  Queen ('1'):      check={NASH['1'][0]:.2f}  bet={NASH['1'][1]:.2f}")
print(f"  King  ('2'):      check={NASH['2'][0]:.2f}  bet={NASH['2'][1]:.2f}")
print()
print("Player 0 response when P1 bets (after P0 checked):")
print(f"  Jack  ('0 0 1'):  fold={NASH['0 0 1'][0]:.2f}  call={NASH['0 0 1'][1]:.2f}")
print(f"  Queen ('1 0 1'):  fold={NASH['1 0 1'][0]:.2f}  call={NASH['1 0 1'][1]:.2f}")
print(f"  King  ('2 0 1'):  fold={NASH['2 0 1'][0]:.2f}  call={NASH['2 0 1'][1]:.2f}")
print()
print("Player 1 after P0 checked:")
print(f"  Jack  ('0 0'):    check={NASH['0 0'][0]:.2f}  bet={NASH['0 0'][1]:.2f}")
print(f"  Queen ('1 0'):    check={NASH['1 0'][0]:.2f}  bet={NASH['1 0'][1]:.2f}  <- bluffs 1/3")
print(f"  King  ('2 0'):    check={NASH['2 0'][0]:.2f}  bet={NASH['2 0'][1]:.2f}")
print()
print("Player 1 after P0 bet:")
print(f"  Jack  ('0 1'):    fold={NASH['0 1'][0]:.2f}  call={NASH['0 1'][1]:.2f}")
print(f"  Queen ('1 1'):    fold={NASH['1 1'][0]:.2f}  call={NASH['1 1'][1]:.2f}")
print(f"  King  ('2 1'):    fold={NASH['2 1'][0]:.2f}  call={NASH['2 1'][1]:.2f}")

# Simulate
game = KuhnGame()
N = 10_000
total_p0 = 0.0

for _ in range(N):
    state = game.new_initial_state()
    state.apply_action(random.randint(0, len(DEAL_ORDERINGS) - 1))
    while not state.is_terminal():
        player = state.current_player()
        info_str = state.information_state_string(player)
        probs = NASH[info_str]
        action = 0 if random.random() < probs[0] else 1
        state.apply_action(action)
    total_p0 += state.returns()[0]

avg = total_p0 / N
print()
print(f"=== Simulation: {N:,} hands of Nash vs Nash ===")
print(f"P0 average return: {avg:+.4f}  (theoretical: +{1/18:.4f})")
