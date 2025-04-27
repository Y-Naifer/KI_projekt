#!/usr/bin/env python3
"""
Random move selector for Turm & Wächter.
Uses the zuggenerator to get all legal moves and selects a random one.

Usage:
    python random_move.py "b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b"
"""

import sys
import random
import subprocess
from pathlib import Path

def get_all_moves(fen_str):
    """Use zuggenerator to get all legal moves."""
    # Get the directory of this script
    script_dir = Path(__file__).parent.absolute()
    
    # Run the zuggenerator with the provided FEN string
    try:
        result = subprocess.run(
            ["python3", f"{script_dir}/zuggenerator.py", fen_str],
            capture_output=True,
            text=True,
            check=True,
            env={"PYTHONPATH": str(script_dir)}
        )
        
        # Parse the output to get the moves
        lines = result.stdout.strip().split('\n')
        
        # Filter out the total count line and any empty lines
        moves = [line for line in lines if line and not line.startswith('Total:')]
        
        return moves
    except subprocess.CalledProcessError as e:
        print(f"Error running zuggenerator: {e}")
        if e.stderr:
            print(f"STDERR: {e.stderr}")
        sys.exit(1)

def main():
    if len(sys.argv) < 2:
        print("Usage: python random_move.py \"<FEN_STRING>\"")
        print("Example: python random_move.py \"b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b\"")
        sys.exit(1)
        
    fen_str = sys.argv[1]
    
    # Get all legal moves
    moves = get_all_moves(fen_str)
    
    # Select a random move
    if moves:
        random_move = random.choice(moves)
        print(random_move)
    else:
        print("No legal moves available")

if __name__ == "__main__":
    main() 