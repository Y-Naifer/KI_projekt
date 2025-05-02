#!/usr/bin/env python3
"""
Dummy AI for Turm & Wächter.
Simple implementation that selects a random legal move.

Usage:
    python dummy_ki.py "b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b"
"""

import sys
import random
import subprocess
import os
import importlib.util
from core.fen import FenParser

def get_random_move(fen_str):
    """
    Get a random legal move using zuggenerator.py.
    1. Pass FEN string to zuggenerator.py
    2. Get all legal moves as output
    3. Choose one randomly
    """
    # Use the FenParser directly
    parser = FenParser()
    moves = parser.get_move_descriptions(fen_str)
    
    if not moves:
        return None
    
    # Select a random move from the list
    return random.choice(moves)

def main():
    if len(sys.argv) < 2:
        print("Usage: python dummy_ki.py \"<FEN_STRING>\"")
        print("Example: python dummy_ki.py \"b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b\"")
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