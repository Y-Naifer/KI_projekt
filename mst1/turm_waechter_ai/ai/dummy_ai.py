import random
from typing import List, Tuple, Optional
from core.board import Board
from core.piece import Piece
from core.rules import GameRules

def dummy_ai_legal_moves(board: Board, player: int) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """Get legal moves using the GameRules implementation."""
    rules = GameRules(board)
    rules.current_player = player  # Set the current player to get moves for
    return rules.get_legal_moves(player)

def dummy_ai_choose_move(board: Board, player: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """Choose a random legal move."""
    moves = dummy_ai_legal_moves(board, player)
    return random.choice(moves) if moves else None
