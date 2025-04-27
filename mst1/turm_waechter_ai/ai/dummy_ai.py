import random
from typing import List, Tuple, Optional
from core.bitboard import BitboardBoard
from core.piece import PieceType
from core.bitboard_rules import BitboardRules

def dummy_ai_legal_moves(board: BitboardBoard, player: int) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """Get legal moves using the BitboardRules implementation."""
    rules = BitboardRules(board)
    rules.current_player = player  # Set the current player to get moves for
    return rules.get_legal_moves(player)

def dummy_ai_choose_move(board: BitboardBoard, player: int) -> Optional[Tuple[Tuple[int, int], Tuple[int, int], int]]:
    """Choose a random legal move."""
    moves = dummy_ai_legal_moves(board, player)
    return random.choice(moves) if moves else None
