#!/usr/bin/env python3
"""
AI Game Demo for Turm & Wächter.
This script demonstrates AI playing a game against itself (Random vs Random).
"""

import sys
import os
import subprocess
from typing import List, Tuple, Optional

def call_dummy_ki(fen_str: str) -> str:
    """
    Call dummy_ki.py with a FEN string to get a random move.
    Returns the move in algebraic notation (e.g., 'A7-B7-1')
    """
    # Path to dummy_ki.py
    dummy_ki_path = os.path.abspath(os.path.join(
        os.path.dirname(__file__), '..', 'dummy_ki.py'))
    
    try:
        # Run dummy_ki.py with the FEN string
        env = os.environ.copy()
        env["PYTHONPATH"] = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        result = subprocess.run(
            ["python3", dummy_ki_path, fen_str], 
            capture_output=True, 
            text=True, 
            env=env
        )
        
        if result.returncode != 0:
            print(f"Error from dummy_ki.py: {result.stderr}", file=sys.stderr)
            return None
        
        # Return the move (should be a single line like "A7-B7-1")
        return result.stdout.strip()
    
    except Exception as e:
        print(f"Error calling dummy_ki.py: {e}", file=sys.stderr)
        return None

def visualize_board(fen_str: str) -> None:
    """
    Visualize the current board state using direct core module imports.
    """
    # Add parent directory to sys.path to allow imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.fen import FenParser
    
    parser = FenParser()
    board, current_player = parser.parse_fen(fen_str)
    
    # Print column headers
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
                
                if piece_type and piece_type.value == 'W':
                    piece_char = "R" if owner == 1 else "B"
                else:  # TURM
                    piece_char = "r" if owner == 1 else "b"
                
                # Add height number for stacks higher than 1
                if stack_height > 1:
                    row += f"{piece_char}{stack_height}   "
                else:
                    row += f"{piece_char}    "
        print(row + f" {7-y}")
        print("")  # Add an empty line between each row
    print("   A    B    C    D    E    F    G  ")
    print("")  # Add empty line after the board
    
    player_name = "Red" if current_player == 1 else "Blue"
    print(f"Current player: {player_name}")

def get_next_fen(current_fen: str, move: str) -> str:
    """
    Calculate the next FEN string after applying a move.
    Uses direct core module imports.
    """
    # Add parent directory to sys.path to allow imports
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    from core.fen import FenParser
    from core.bitboard_rules import BitboardRules
    
    parser = FenParser()
    board, current_player = parser.parse_fen(current_fen)
    
    # Create rules engine
    rules = BitboardRules(board)
    rules.current_player = current_player
    
    # Parse the move string (e.g. "A7-B7-1")
    from_str, to_str, height_str = move.split('-')
    
    # Convert algebraic notation to coordinates
    from_col = ord(from_str[0]) - ord('A')
    from_row = 7 - int(from_str[1])
    to_col = ord(to_str[0]) - ord('A')
    to_row = 7 - int(to_str[1])
    height = int(height_str)
    
    # Apply the move
    rules.make_move((from_col, from_row), (to_col, to_row), height)
    
    # Get the new FEN (player is already switched in make_move)
    new_fen = board.to_fen(rules.current_player)
    
    return new_fen

def play_ai_game(max_moves=50):
    """
    Have the AI play a game against itself.
    Returns the game history and result.
    """
    # Start with the initial position FEN string
    initial_fen = "r1r11RG1r1r1/2r11r12/3r13/7/3b13/2b11b12/b1b11BG1b1b1 r"
    current_fen = initial_fen
    
    move_history = []
    
    print("Starting AI vs AI game: Random AI (Red) vs Random AI (Blue)")
    print("-----------------------------------------------------------")
    
    # Visualize initial board state
    visualize_board(current_fen)
    
    for move_num in range(1, max_moves + 1):
        # Get the current player from the FEN string
        current_player = "Red" if current_fen.split()[-1] == "r" else "Blue"
        
        # Get AI move by calling dummy_ki.py with the current FEN string
        move_desc = call_dummy_ki(current_fen)
        
        if not move_desc:
            print(f"Player {current_player} has no valid moves!")
            break
        
        # Add move to history
        move_history.append(move_desc)
        
        # Print move with clear separation
        print("\n-----------------------------------------------------------")
        print(f"Move {move_num}: {current_player} plays {move_desc}")
        
        # Apply the move and get the new FEN string
        current_fen = get_next_fen(current_fen, move_desc)
        if not current_fen:
            print("Error applying move, stopping game.")
            break
        
        # Visualize the board after the move
        visualize_board(current_fen)
        
        # Check for game over (would need to implement this based on the game rules)
        # For now, just play for max_moves
    
    # Report game result
    print("-----------------------------------------------------------")
    print("\nGame reached maximum number of moves without a winner.")
    
    return move_history

def main():
    print("Turm & Wächter AI Demonstration")
    print("==============================\n")
    
    # AI vs AI game
    play_ai_game(max_moves=15)  # Reduced to 15 moves for brevity
    
    print("\nAdditional Tools:")
    print("- To run benchmark tests: python benchmark.py")

if __name__ == "__main__":
    main() 