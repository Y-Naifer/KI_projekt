#!/usr/bin/env python3
"""
Alpha-Beta AI for Turm & Wächter.

Usage:
    python intelligent_ki.py "FEN_STRING"
"""

import sys
from copy import deepcopy
from core.fen import FenParser
from core.bitboard_rules import BitboardRules
from core.piece import PieceType
from evaluate import evaluate
MAX_DEPTH = 3  # Adjust search depth here





def simulate_move(fen_str: str, move: str) -> str:
    """
    Simulate a move and return the resulting FEN string.
    """
    parser = FenParser()
    board, current_player = parser.parse_fen(fen_str)

    # Deepcopy so original board is not changed
    board_copy = deepcopy(board)
    rules = BitboardRules(board_copy)
    rules.current_player = current_player

    from_str, to_str, height_str = move.split("-")
    fx = ord(from_str[0]) - ord("A")
    fy = 7 - int(from_str[1])
    tx = ord(to_str[0]) - ord("A")
    ty = 7 - int(to_str[1])
    height = int(height_str)

    if not rules.make_move((fx, fy), (tx, ty), height):
        raise ValueError(f"Invalid move attempted: {move}")

    return board_copy.to_fen(rules.current_player)


def is_terminal(fen_str: str) -> bool:
    parser = FenParser()
    return len(parser.get_move_descriptions(fen_str)) == 0


def alpha_beta(fen_str: str, depth: int, alpha: float, beta: float, maximizing: bool, indent=0) -> float:
    parser = FenParser()
    current_player = 1 if fen_str.strip().split()[1] == 'r' else 2
    legal_moves = parser.get_move_descriptions(fen_str)

    prefix = "  " * indent

    if depth == 0 or not legal_moves:
        score = evaluate(fen_str)
        # Flip score if Blue to move, because evaluate is Red-centric
        if current_player == 2:
            score = -score
        print(f"{prefix}Eval at depth {depth}, player {'Red' if current_player == 1 else 'Blue'}: score={score}")
        return score

    if maximizing:
        max_eval = float("-inf")
        print(f"{prefix}Maximizing at depth {depth}, player {'Red' if current_player == 1 else 'Blue'}, moves: {len(legal_moves)}")
        for move in legal_moves:
            print(f"{prefix}Trying move {move}")
            next_fen = simulate_move(fen_str, move)
            eval = alpha_beta(next_fen, depth - 1, alpha, beta, False, indent + 1)
            max_eval = max(max_eval, eval)
            alpha = max(alpha, eval)
            print(f"{prefix}Move {move} eval={eval}, alpha={alpha}, beta={beta}")
            if beta <= alpha:
                print(f"{prefix}Beta cutoff")
                break
        print(f"{prefix}Maximizing returns {max_eval}")
        return max_eval
    else:
        min_eval = float("inf")
        print(f"{prefix}Minimizing at depth {depth}, player {'Red' if current_player == 1 else 'Blue'}, moves: {len(legal_moves)}")
        for move in legal_moves:
            print(f"{prefix}Trying move {move}")
            next_fen = simulate_move(fen_str, move)
            eval = alpha_beta(next_fen, depth - 1, alpha, beta, True, indent + 1)
            min_eval = min(min_eval, eval)
            beta = min(beta, eval)
            print(f"{prefix}Move {move} eval={eval}, alpha={alpha}, beta={beta}")
            if beta <= alpha:
                print(f"{prefix}Alpha cutoff")
                break
        print(f"{prefix}Minimizing returns {min_eval}")
        return min_eval


def choose_best_move(fen_str: str) -> str:
    parser = FenParser()
    legal_moves = parser.get_move_descriptions(fen_str)

    if not legal_moves:
        print("No legal moves available")
        return "No legal moves available"

    current_player = 1 if fen_str.strip().split()[1] == 'r' else 2
    maximizing = current_player == 1

    best_move = None
    best_score = float("-inf") if maximizing else float("inf")

    print(f"Choosing best move for player {'Red' if maximizing else 'Blue'} with {len(legal_moves)} moves")

    for move in legal_moves:
        print(f"Evaluating move {move}")
        next_fen = simulate_move(fen_str, move)
        score = alpha_beta(next_fen, MAX_DEPTH - 1, float("-inf"), float("inf"), not maximizing, indent=1)

        # Flip score if current player is Blue (since evaluate is Red-centric)
        if current_player == 2:
            score = -score

        print(f"Move {move} has score {score}")

        if maximizing and score > best_score:
            best_score = score
            best_move = move
        elif not maximizing and score < best_score:
            best_score = score
            best_move = move

        print(f"Current best move: {best_move} with score {best_score}")

    print(f"Best move chosen: {best_move} with score {best_score}")
    return best_move



def main():
    if len(sys.argv) < 2:
        print("Usage: python intelligent_ki.py \"FEN_STRING\"")
        sys.exit(1)

    fen_str = sys.argv[1]
    move = choose_best_move(fen_str)
    print(move)


if __name__ == "__main__":
    main()