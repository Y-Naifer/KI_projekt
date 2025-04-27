#!/usr/bin/env python3
"""
Debug script for Turm & Wächter.
Visualizes the board from a FEN string.
"""

import sys
import os
import random

# Add the project root directory to the path to allow importing modules
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from core.fen import FenParser
from core.piece import PieceType
from core.bitboard import BitboardBoard

def visualize_board(fen_str):
    """Visualize the board from a FEN string."""
    parser = FenParser()
    board, current_player = parser.parse_fen(fen_str)
    
    print(f"FEN: {fen_str}")
    print(f"Current player: {'Red' if current_player == 1 else 'Blue'}")
    
    # Print column headers
    print("  ", end="")
    for col in range(board.SIZE):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Print board
    for y in range(board.SIZE):
        print(f"{7-y} ", end="")
        for x in range(board.SIZE):
            owner = board.get_stack_owner(x, y)
            if owner is None:
                print(" . ", end="")
            else:
                piece_type = board.get_top_piece_type(x, y)
                stack_height = board.get_stack_height(x, y)
                
                piece_char = "?"
                if piece_type == PieceType.TURM:
                    piece_char = "r" if owner == 1 else "b"
                else:  # WAECHTER
                    piece_char = "R" if owner == 1 else "B"
                
                if stack_height > 1:
                    print(f"{piece_char}{stack_height}", end=" ")
                else:
                    print(f" {piece_char} ", end="")
        print(f" {7-y}")
    
    # Print column headers again
    print("  ", end="")
    for col in range(board.SIZE):
        print(f" {chr(ord('A') + col)} ", end="")
    print()
    
    # Get all legal moves
    moves = parser.get_move_descriptions(fen_str)
    
    print(f"\nLegal moves: {len(moves)}")
    if moves:
        # Select and display only one random move
        random_move = random.choice(moves)
        print(f"  Selected move: {random_move}")
    else:
        print("  No legal moves available")

def main():
    if len(sys.argv) < 2:
        print("Usage: python debug.py \"<FEN_STRING>\"")
        print("Example: python debug.py \"b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b\"")
        sys.exit(1)
        
    fen_str = sys.argv[1]
    visualize_board(fen_str)

if __name__ == "__main__":
    main() 