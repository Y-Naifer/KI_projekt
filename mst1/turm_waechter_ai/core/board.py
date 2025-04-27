from typing import List, Tuple
from core.piece import Piece, PieceType

class Board:
    SIZE = 7

    def __init__(self, setup_initial=True):
        self.grid = [[[] for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        if setup_initial:
            self.setup_starting_position()

    def setup_starting_position(self):
        # Place Wächter (Guardians)
        self.grid[0][3].append(Piece(PieceType.WAECHTER, 1))  # Red at D7
        self.grid[6][3].append(Piece(PieceType.WAECHTER, 2))  # Blue at D1
        
        # Place Red Turm (Towers) - A7, B7, C6, D5, E6, F7, G7
        self.grid[0][0].append(Piece(PieceType.TURM, 1))  # A7
        self.grid[0][1].append(Piece(PieceType.TURM, 1))  # B7
        self.grid[1][2].append(Piece(PieceType.TURM, 1))  # C6
        self.grid[2][3].append(Piece(PieceType.TURM, 1))  # D5
        self.grid[1][4].append(Piece(PieceType.TURM, 1))  # E6
        self.grid[0][5].append(Piece(PieceType.TURM, 1))  # F7
        self.grid[0][6].append(Piece(PieceType.TURM, 1))  # G7
        
        # Place Blue Turm (Towers) - A1, B1, C2, D3, E2, F1, G1
        self.grid[6][0].append(Piece(PieceType.TURM, 2))  # A1
        self.grid[6][1].append(Piece(PieceType.TURM, 2))  # B1
        self.grid[5][2].append(Piece(PieceType.TURM, 2))  # C2
        self.grid[4][3].append(Piece(PieceType.TURM, 2))  # D3
        self.grid[5][4].append(Piece(PieceType.TURM, 2))  # E2
        self.grid[6][5].append(Piece(PieceType.TURM, 2))  # F1
        self.grid[6][6].append(Piece(PieceType.TURM, 2))  # G1

    def get_stack(self, x: int, y: int) -> List[Piece]:
        return self.grid[y][x]

    def move_piece(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int):
        stack = self.get_stack(*from_pos)
        moving = stack[-height:]
        self.grid[from_pos[1]][from_pos[0]] = stack[:-height]
        self.grid[to_pos[1]][to_pos[0]].extend(moving)

    def print_board(self):
        for row in self.grid:
            print([f"{len(cell)}" if cell else "." for cell in row])
