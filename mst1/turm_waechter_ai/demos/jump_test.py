#!/usr/bin/env python3
"""
Test script to check if towers can jump over other pieces.
"""

import sys
from core.fen import FenParser
from core.board import Board
from core.rules import GameRules
from core.piece import Piece, PieceType

def create_test_board():
    """Create a test board with a tower that needs to jump over another piece."""
    # Create an empty board
    board = Board(setup_initial=False)
    
    # Add a tower of height 3 for the current player (Red)
    board.grid[3][1].append(Piece(PieceType.TURM, 1))
    board.grid[3][1].append(Piece(PieceType.TURM, 1))
    board.grid[3][1].append(Piece(PieceType.TURM, 1))
    
    # Add an opponent's piece in the way
    board.grid[3][2].append(Piece(PieceType.TURM, 2))
    
    # Add an empty space after the opponent's piece
    # (Position 3,3 is empty)
    
    # Add another opponent's piece further away
    board.grid[3][4].append(Piece(PieceType.TURM, 2))
    
    return board

def main():
    # Create a test board or use a FEN string
    if len(sys.argv) > 1:
        parser = FenParser()
        board, current_player = parser.parse_fen(sys.argv[1])
    else:
        board = create_test_board()
        current_player = 1  # Red player
    
    # Print the board
    print("Test Board:")
    print("   0  1  2  3  4  5  6")
    for y in range(board.SIZE):
        print(f"{y} ", end="")
        for x in range(board.SIZE):
            stack = board.get_stack(x, y)
            if not stack:
                print(" . ", end="")
            else:
                top_piece = stack[-1]
                piece_char = "r" if top_piece.player == 1 else "b"
                if top_piece.piece_type == PieceType.WAECHTER:
                    piece_char = piece_char.upper()
                
                stack_height = len(stack)
                if stack_height > 1:
                    print(f"{piece_char}{stack_height}", end=" ")
                else:
                    print(f" {piece_char} ", end="")
        print(f" {y}")
    print("   0  1  2  3  4  5  6")
    
    # Check legal moves
    rules = GameRules(board)
    rules.current_player = current_player
    legal_moves = rules.get_legal_moves(current_player)
    
    # Convert moves to readable format
    move_descriptions = []
    for from_pos, to_pos, height in legal_moves:
        move_descriptions.append(f"({from_pos[0]},{from_pos[1]})-({to_pos[0]},{to_pos[1]})-{height}")
    
    print(f"\nLegal moves for player {current_player}: {len(move_descriptions)}")
    for move in sorted(move_descriptions):
        print(f"  {move}")
    
    # Check specific moves for jumping
    test_moves = [
        ((1, 3), (3, 3), 2),  # Jump over piece at (2,3)
        ((1, 3), (4, 3), 3)   # Jump over pieces at (2,3) and (3,3)
    ]
    
    print("\nTesting specific moves for jumping:")
    for from_pos, to_pos, height in test_moves:
        is_valid = rules.is_valid_move(from_pos, to_pos, height)
        in_legal_moves = (from_pos, to_pos, height) in legal_moves
        print(f"  Move ({from_pos[0]},{from_pos[1]})-({to_pos[0]},{to_pos[1]})-{height}: Valid={is_valid}, In legal moves={in_legal_moves}")

if __name__ == "__main__":
    main() 