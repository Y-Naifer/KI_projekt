#!/usr/bin/env python3
"""
Evaluation function for alpha-beta search in Turm & Wächter, combining previously defined metrics.

Weights:
    w_win     = 1_000_000   # terminal outcome
    w_center  =      50     # reward proximity to center
    w_danger  =     200     # penalty if your guardian is threatened
    w_Md      =      20     # penalty per your piece in danger
    w_E       =       5     # each enemy stack you subtract
    w_H       =      10     # each unit of your tower height you add
    w_diff    =      30     # net piece-count difference
    w_Eh      =      15     # penalty per enemy in your half
"""
from core.fen import FenParser
from core.bitboard_rules import BitboardRules
from core.bitboard import BitboardBoard

# Import utility functions (ensure these are available in your project)
from threat_test import is_threatened
from distance_test import distance_to_opponent_start
from piece_count_test import count_pieces, count_enemy_pieces, diff_of_pieces, count_enemy_pieces_in_half
from average_tower_height import average_tower_height

# Evaluation weights
w_win     = 1_000_000
w_center  = 50
w_danger  = 200
w_Md      = 20
w_E       = 5
w_H       = 10
w_diff    = 30
w_Eh      = 15


def evaluate(fen_str: str) -> float:
    """
    Compute evaluation score from the perspective of the side to move.
    Positive values favor the current player; negative values favor the opponent.
    """
    # Parse board and current player
    parser = FenParser()
    board, player = parser.parse_fen(fen_str)

    # Initialize rules engine for terminal detection
    rules = BitboardRules(board)
    rules.current_player = player

    # Terminal outcome
    if rules.is_game_over():
        winner = rules.get_winner()
        return w_win if winner == player else -w_win

    # Find guardian position and center proximity
    # Center square is (3,3)
    guard_bb = board.red_guardian if player == 1 else board.blue_guardian
    # Locate guardian bit
    guard_pos = None
    for bitpos in range(board.SIZE * board.SIZE):
        if guard_bb & (1 << bitpos):
            x = bitpos % board.SIZE
            y = bitpos // board.SIZE
            guard_pos = (x, y)
            break

    # Distance to center
    d_center = abs(guard_pos[0] - 3) + abs(guard_pos[1] - 3)
    F_center = 6 - d_center

    # Threat to guardian
    F_danger = 1 if is_threatened(board, guard_pos, player) else 0

    # Count own pieces in danger
    F_Md = 0
    for bitpos in range(board.SIZE * board.SIZE):
        x = bitpos % board.SIZE
        y = bitpos // board.SIZE
        if board.get_stack_owner(x, y) == player:
            if is_threatened(board, (x, y), player):
                F_Md += 1

    # Enemy stack count
    F_E = count_enemy_pieces(fen_str)

    # Own tower height sum
    F_H = 0
    for h in range(1, 8):
        tower_bb = board.red_towers[h] if player == 1 else board.blue_towers[h]
        F_H += h * bin(tower_bb).count('1')

    # Piece-count difference
    F_diff = diff_of_pieces(fen_str)

    # Enemy in your half
    F_Eh = count_enemy_pieces_in_half(fen_str)

    # Final evaluation
    score = (
        w_center * F_center
        - w_danger * F_danger
        - w_Md * F_Md
        - w_E * F_E
        + w_H * F_H
        + w_diff * F_diff
        - w_Eh * F_Eh
    )

    return score


if __name__ == "__main__":
    # Simple REPL for testing
    import sys
    if len(sys.argv) != 2:
        print("Usage: python evaluate.py \"FEN_STRING\"")
        sys.exit(1)
    fen = sys.argv[1]
    print(f"Eval score: {evaluate(fen)}")
