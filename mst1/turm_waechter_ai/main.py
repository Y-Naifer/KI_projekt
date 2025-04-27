#!/usr/bin/env python3
"""
Simplified move generator for Turm & Wächter.

Usage:
    python main.py "b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b"
"""

import sys
import random
from core.fen import FenParser

def main():
    if len(sys.argv) < 2:
        print("Usage: python main.py \"<FEN_STRING>\"")
        print("Example: python main.py \"b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b\"")
        sys.exit(1)
        
    fen_str = sys.argv[1]
    parser = FenParser()
    
    try:
        # Get moves in algebraic notation
        moves = parser.get_move_descriptions(fen_str)
        
        if moves:
            # Select only one random move
            random_move = random.choice(moves)
            print(random_move)
        else:
            print("No legal moves available")
                
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 