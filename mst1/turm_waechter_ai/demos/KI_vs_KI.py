#!/usr/bin/env python3
"""
AI Game Demo for Turm & Wächter.
This script demonstrates AI playing a game against itself (Random vs Random).
"""

import time
import random
import sys
import os
from typing import List, Tuple, Optional

# Add parent directory to path for imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.bitboard import BitboardBoard
from core.piece import PieceType
from core.bitboard_rules import BitboardRules
from core.fen import FenParser

# Import from dummy_ki instead of ai.dummy_ai
def get_random_move(board: BitboardBoard, current_player: int):
    """Get a random legal move."""
    # Use FenParser to get moves (same as dummy_ki.py)
    parser = FenParser()
    
    # Convert board to FEN string
    fen_str = board.to_fen(current_player)
    
    # Get legal moves using the parser
    moves_desc = parser.get_move_descriptions(fen_str)
    
    if not moves_desc:
        return None
    
    # Select a random move description
    move_desc = random.choice(moves_desc)
    
    # Parse the move description back to coordinates
    from_str, to_str, height_str = move_desc.split('-')
    
    # Convert algebraic notation to coordinates
    from_col = ord(from_str[0]) - ord('A')
    from_row = 7 - int(from_str[1])
    to_col = ord(to_str[0]) - ord('A')
    to_row = 7 - int(to_str[1])
    height = int(height_str)
    
    # Return move in the format expected by the rest of the code
    return ((from_col, from_row), (to_col, to_row), height)

def play_ai_game(max_moves=50):
    """
    Have the AI play a game against itself.
    Returns the game history and result.
    """
    board = BitboardBoard(setup_initial=True)
    rules = BitboardRules(board)
    current_player = 1  # Start with Red player
    
    move_history = []
    
    print("Starting AI vs AI game: Random AI (Red) vs Random AI (Blue)")
    print("-----------------------------------------------------------")
    
    for move_num in range(1, max_moves + 1):
        if rules.is_game_over():
            break
        
        # Get AI move - both players use random AI
        ai_move = get_random_move(board, current_player)
        
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
        
        # Print move with clear separation
        if move_num > 1:
            print("\n-----------------------------------------------------------")
        print(f"Move {move_num}: {player_name} plays {move_desc}")
        
        # Make the move
        rules.make_move(from_pos, to_pos, height)
        
        # Print a simple board representation after each move
        print_board_state(board)
        
        # Switch player for next turn
        current_player = 3 - current_player
    
    # Report game result
    print("-----------------------------------------------------------")
    if rules.is_game_over():
        winner = "Red" if rules.get_winner() == 1 else "Blue"
        print(f"\nGame over! {winner} wins!")
    else:
        print("\nGame reached maximum number of moves without a winner.")
    
    return move_history, rules.get_winner()

def print_board_state(board: BitboardBoard):
    """Print a simple representation of the board with stack heights"""
    print("")  # Add empty line before the board
    print("   A    B    C    D    E    F    G  ")
    print("")
    for y in range(board.SIZE):
        row = f"{7-y}  "
        for x in range(board.SIZE):
            owner = board.get_stack_owner(x, y)
            if owner is None:
                row += ".    "
            else:
                piece_type = board.get_top_piece_type(x, y)
                stack_height = board.get_stack_height(x, y)
                
                if piece_type == PieceType.TURM:
                    piece_char = "r" if owner == 1 else "b"
                else:  # WAECHTER
                    piece_char = "R" if owner == 1 else "B"
                
                # Add height number for stacks higher than 1
                if stack_height > 1:
                    row += f"{piece_char}{stack_height}   "
                else:
                    row += f"{piece_char}    "
        print(row + f" {7-y}")
        print("")  # Add an empty line between each row
    print("   A    B    C    D    E    F    G  ")
    print("")  # Add empty line after the board

def main():
    print("Turm & Wächter AI Demonstration")
    print("==============================\n")
    
    # AI vs AI game
    play_ai_game(max_moves=15)  # Reduced to 15 moves for brevity
    
    print("\nAdditional Tools:")
    print("- To run benchmark tests: python benchmark.py")

if __name__ == "__main__":
    main() 