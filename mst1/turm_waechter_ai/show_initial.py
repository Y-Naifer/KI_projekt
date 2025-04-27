#!/usr/bin/env python3
"""
Script to show the initial board position.
"""

from core.board import Board
from core.piece import PieceType

def visualize_board(board):
    """Visualize the board."""
    print("Initial Board Position:")
    print("   A  B  C  D  E  F  G ")
    for y in range(board.SIZE):
        print(f"{7-y} ", end="")
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
        print(f" {7-y}")
    print("   A  B  C  D  E  F  G ")

def main():
    # Create a new board with the initial setup
    board = Board(setup_initial=True)
    
    # Visualize the board
    visualize_board(board)
    
    # Print explanation of pieces
    print("\nPiece Legend:")
    print("R - Red Wächter (Guardian)")
    print("B - Blue Wächter (Guardian)")
    print("r - Red Turm (Tower)")
    print("b - Blue Turm (Tower)")
    print("Pieces with numbers (e.g., r3) indicate stack height")

if __name__ == "__main__":
    main() 