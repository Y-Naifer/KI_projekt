#!/usr/bin/env python3
"""
Test script for `is_threatened` function in Turm & Wächter.

Usage:
    python threat_test.py
"""
from core.bitboard import BitboardBoard
from core.fen import FenParser
from core.bitboard_rules import BitboardRules


def is_threatened(board: BitboardBoard, pos: tuple, player: int) -> bool:
    """
    Check if the piece owned by `player` at `pos` is threatened by any opponent move.
    """
    rules = BitboardRules(board)
    opponent = 3 - player
    rules.current_player = opponent

    # Generate all opponent legal moves
    opponent_moves = rules.get_legal_moves(opponent)

    for from_pos, to_pos, height in opponent_moves:
        if to_pos == pos:
            # If it's a capturing move, pos was occupied by us
            if rules.is_valid_capture(from_pos, to_pos, height):
                return True
    return False


def pos_from_alg(alg: str) -> tuple:
    """
    Convert algebraic notation (e.g. 'D7') to zero-based (x, y).
    'A7' -> (0,0), 'G1' -> (6,6)
    """
    col = ord(alg[0].upper()) - ord('A')
    row = 7 - int(alg[1])
    return (col, row)


def test_position(fen: str, alg_pos: str, player: int, expected: bool):
    parser = FenParser()
    board, _ = parser.parse_fen(fen)
    pos = pos_from_alg(alg_pos)
    threatened = is_threatened(board, pos, player)
    status = "PASS" if threatened == expected else "FAIL"
    print(f"Test {status}: Player {player} at {alg_pos} in '{fen}' -> threatened? {threatened} (expected {expected})")


def main():
    # Test cases: (FEN, position, player, expected result)
    tests = [
        # Initial position: no one is threatened
        (
            "r1r11RG1r1r1/11r11r12/3r13/1b35/3b13/2b11b12/b1b11BG1b1b1 r",
            "B7", 1, True
        ),
        (
            "r1r11RG1r1r1/2r1b1r12/3b23/7/3b13/2b11b12/b1b11BG1b1b1 r",
            "D7", 2, True
        ),
        # Simple threat: Blue tower at A6 can move 1 to A7 to capture red tower
        (
            "r16/1b6/7/7/7/7/7 r",  # r at A7, b at B6
            "A7", 1, False
        ),
    ]
    for fen, alg, player, expected in tests:
        test_position(fen, alg, player, expected)


if __name__ == "__main__":
    main()
