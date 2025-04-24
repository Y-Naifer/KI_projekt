from typing import List, Tuple
from core.piece import Piece, PieceType

class Board:
    SIZE = 7

    def __init__(self, setup_initial=True):
        self.grid = [[[] for _ in range(self.SIZE)] for _ in range(self.SIZE)]
        if setup_initial:
            self.setup_starting_position()

    def setup_starting_position(self):
        self.grid[0][3].append(Piece(PieceType.WAECHTER, 1))
        self.grid[6][3].append(Piece(PieceType.WAECHTER, 2))

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
