#!/usr/bin/env python3
"""
Dummy AI for Turm & Wächter.
Simple implementation that selects a random legal move.

Usage:
    python Dummy_KI.py "b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b"
"""

import sys
import random
from core.fen import FenParser
from core.bitboard import BitboardBoard
from core.bitboard_rules import BitboardRules

def get_random_move(fen_str):
    """Get a random legal move using BitboardRules directly."""
    # Parse the FEN string
    parser = FenParser()
    board, current_player = parser.parse_fen(fen_str)
    
    # Setup rules engine
    rules = BitboardRules(board)
    rules.current_player = current_player
    
    # Get all legal moves
    legal_moves = rules.get_legal_moves(current_player)
    
    if not legal_moves:
        return None
    
    # Select a random move
    random_move = random.choice(legal_moves)
    
    # Convert to algebraic notation
    from_pos, to_pos, height = random_move
    return parser.describe_move(from_pos, to_pos, height)

def main():
    if len(sys.argv) < 2:
        print("Usage: python Dummy_KI.py \"<FEN_STRING>\"")
        print("Example: python Dummy_KI.py \"b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b\"")
        sys.exit(1)
        
    fen_str = sys.argv[1]
    
    # Get a random legal move
    move = get_random_move(fen_str)
    
    if move:
        print(move)
    else:
        print("No legal moves available")

if __name__ == "__main__":
    main() 