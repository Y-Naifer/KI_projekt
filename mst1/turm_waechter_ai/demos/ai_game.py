#!/usr/bin/env python3
"""
AI Game Demo for Turm & Wächter.
This script demonstrates AI playing a game against itself (Random vs Random).
"""

import time
import random
from typing import List, Tuple, Optional
from core.board import Board
from core.piece import Piece, PieceType
from core.rules import GameRules
from core.fen import FenParser
from ai.dummy_ai import dummy_ai_choose_move

def play_ai_game(max_moves=50):
    """
    Have the AI play a game against itself.
    Returns the game history and result.
    """
    board = Board(setup_initial=True)
    rules = GameRules(board)
    current_player = 1  # Start with Red player
    
    move_history = []
    
    print("Starting AI vs AI game: Random AI (Red) vs Random AI (Blue)")
    print("-----------------------------------------------------------")
    
    for move_num in range(1, max_moves + 1):
        if rules.is_game_over():
            break
        
        # Get AI move - both players use random AI
        ai_move = dummy_ai_choose_move(board, current_player)
        
        if not ai_move:
            print(f"Player {current_player} has no valid moves!")
            break
        
        from_pos, to_pos, height = ai_move
        player_name = "Red" if current_player == 1 else "Blue"
        from_col = chr(from_pos[0] + ord('A'))
        from_row = 7 - from_pos[1]
        to_col = chr(to_pos[0] + ord('A'))
        to_row = 7 - to_pos[1]
        
        move_desc = f"{from_col}{from_row}-{to_col}{to_row}-{height}"
        move_history.append(move_desc)
        
        print(f"Move {move_num}: {player_name} plays {move_desc}")
        
        # Make the move
        rules.make_move(from_pos, to_pos, height)
        
        # Print a simple board representation after each move
        print_board_state(board)
        
        # Switch player for next turn
        current_player = 3 - current_player
    
    # Report game result
    if rules.is_game_over():
        winner = "Red" if rules.get_winner() == 1 else "Blue"
        print(f"\nGame over! {winner} wins!")
    else:
        print("\nGame reached maximum number of moves without a winner.")
    
    return move_history, rules.get_winner()

def print_board_state(board: Board):
    """Print a simple representation of the board"""
    print("  A B C D E F G")
    for y in range(board.SIZE):
        row = f"{7-y} "
        for x in range(board.SIZE):
            stack = board.get_stack(x, y)
            if not stack:
                row += ". "
            else:
                top_piece = stack[-1]
                if top_piece.piece_type == PieceType.TURM:
                    piece_char = "r" if top_piece.player == 1 else "b"
                else:  # WAECHTER
                    piece_char = "R" if top_piece.player == 1 else "B"
                row += piece_char + " "
        print(row)
    print()

def main():
    print("Turm & Wächter AI Demonstration")
    print("==============================\n")
    
    # AI vs AI game
    play_ai_game(max_moves=15)  # Reduced to 15 moves for brevity
    
    print("\nAdditional Tools:")
    print("- To run benchmark tests: python benchmark.py")
    print("- To run unit tests: python unit_tests.py")

if __name__ == "__main__":
    main() 