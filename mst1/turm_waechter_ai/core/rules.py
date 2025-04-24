from typing import List, Tuple, Optional
from core.board import Board
from core.piece import Piece, PieceType

class GameRules:
    def __init__(self, board: Board):
        self.board = board
        self.current_player = 1
        self.game_over = False
        self.winner = None
        
    def is_valid_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Check if a move is valid according to game rules."""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # Check if positions are within board
        if not (0 <= from_x < self.board.SIZE and 0 <= from_y < self.board.SIZE and
                0 <= to_x < self.board.SIZE and 0 <= to_y < self.board.SIZE):
            return False
        
        # Check if there are pieces to move
        from_stack = self.board.get_stack(from_x, from_y)
        if len(from_stack) < height or height <= 0:
            return False
            
        # Check if the top piece belongs to the current player
        if from_stack[-1].player != self.current_player:
            return False
            
        # Calculate move distance
        dx, dy = to_x - from_x, to_y - from_y
        
        # Only orthogonal moves allowed (no diagonal)
        if dx != 0 and dy != 0:
            return False
            
        # Move distance must exactly equal the stack height
        if abs(dx) != height and abs(dy) != height:
            return False
            
        # Check for obstacles in the path
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        # Start checking from one step away from the origin
        current_x, current_y = from_x + step_x, from_y + step_y
        
        # Check each square in the path except the destination
        while (current_x, current_y) != (to_x, to_y):
            if self.board.get_stack(current_x, current_y):
                # Found an obstacle in the path
                return False
            current_x += step_x
            current_y += step_y
            
        return True
    
    def is_valid_capture(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Check if a capture is valid."""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        from_stack = self.board.get_stack(from_x, from_y)
        to_stack = self.board.get_stack(to_x, to_y)
        
        # Can't capture if destination is empty
        if not to_stack:
            return False
            
        # Can't capture own pieces
        if to_stack[-1].player == self.current_player:
            return False
            
        moving_piece_type = from_stack[-1].piece_type
        target_piece_type = to_stack[-1].piece_type
        
        # Watcher can capture any piece
        if moving_piece_type == PieceType.WAECHTER:
            return True
            
        # Tower can capture Watcher (win condition)
        if moving_piece_type == PieceType.TURM and target_piece_type == PieceType.WAECHTER:
            return True
            
        # Tower can capture Tower of equal or greater height only if moving the entire tower
        if (moving_piece_type == PieceType.TURM and 
            target_piece_type == PieceType.TURM):
            # Check if we're moving the entire tower (height equals stack size)
            if height == len(from_stack) and len(to_stack) <= len(from_stack):
                return True
            else:
                return False
            
        return False
        
    def is_valid_stack(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Check if stacking is valid."""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        from_stack = self.board.get_stack(from_x, from_y)
        to_stack = self.board.get_stack(to_x, to_y)
        
        # Can only stack on own pieces
        if not to_stack or to_stack[-1].player != self.current_player:
            return False
        
        # Get the piece types
        moving_piece_type = from_stack[-1].piece_type
        target_piece_type = to_stack[-1].piece_type
        
        # Watchers can't go on top of towers
        if moving_piece_type == PieceType.WAECHTER and target_piece_type == PieceType.TURM:
            return False
            
        # Towers can't go on top of watchers
        if moving_piece_type == PieceType.TURM and target_piece_type == PieceType.WAECHTER:
            return False
            
        return True
        
    def get_legal_moves(self, player: int) -> List[Tuple[Tuple[int, int], Tuple[int, int], int]]:
        """Get all legal moves for a player."""
        legal_moves = []
        
        for y in range(self.board.SIZE):
            for x in range(self.board.SIZE):
                stack = self.board.get_stack(x, y)
                if not stack or stack[-1].player != player:
                    continue
                    
                # Try all possible heights to move
                for height in range(1, len(stack) + 1):
                    # Try all four directions
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        nx, ny = x + dx * height, y + dy * height
                        
                        if not (0 <= nx < self.board.SIZE and 0 <= ny < self.board.SIZE):
                            continue
                        
                        # First check if the move is valid according to movement rules
                        if not self.is_valid_move((x, y), (nx, ny), height):
                            continue
                        
                        target_stack = self.board.get_stack(nx, ny)
                        
                        # Empty destination or capture or stack
                        if (not target_stack or 
                            self.is_valid_capture((x, y), (nx, ny), height) or
                            self.is_valid_stack((x, y), (nx, ny), height)):
                            legal_moves.append(((x, y), (nx, ny), height))
                            
        return legal_moves
        
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Execute a move if valid and check win conditions."""
        if not self.is_valid_move(from_pos, to_pos, height):
            return False
            
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        to_stack = self.board.get_stack(to_x, to_y)
        from_stack = self.board.get_stack(from_x, from_y)
        
        # Handle capture
        if to_stack and to_stack[-1].player != self.current_player:
            # Check if capturing opponent's Watcher (win condition)
            if to_stack[-1].piece_type == PieceType.WAECHTER:
                self.game_over = True
                self.winner = self.current_player
                
            # Execute the capture (remove opponent piece)
            self.board.move_piece(from_pos, to_pos, height)
            
        # Handle stacking (move to friendly tower)
        elif to_stack and to_stack[-1].player == self.current_player:
            self.board.move_piece(from_pos, to_pos, height)
            
        # Handle normal move to empty space
        else:
            self.board.move_piece(from_pos, to_pos, height)
            
        # Check center field win condition
        center_x, center_y = self.board.SIZE // 2, self.board.SIZE // 2
        center_stack = self.board.get_stack(center_x, center_y)
        
        if (center_stack and center_stack[-1].player == self.current_player and 
            center_stack[-1].piece_type == PieceType.WAECHTER):
            self.game_over = True
            self.winner = self.current_player
            
        # Switch player
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        
        return True
        
    def unstack(self, pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Execute an unstacking operation."""
        x, y = pos
        to_x, to_y = to_pos
        
        # Check if positions are within board
        if not (0 <= x < self.board.SIZE and 0 <= y < self.board.SIZE and
                0 <= to_x < self.board.SIZE and 0 <= to_y < self.board.SIZE):
            return False
            
        stack = self.board.get_stack(x, y)
        
        # Can't unstack if no pieces or not enough pieces
        if len(stack) < height + 1:  # Need at least one piece left
            return False
            
        # Top piece must belong to current player
        if stack[-1].player != self.current_player:
            return False
            
        # Move the top 'height' pieces to the destination
        self.board.move_piece(pos, to_pos, height)
        
        # Switch player
        self.current_player = 3 - self.current_player
        
        return True
        
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_over
        
    def get_winner(self) -> Optional[int]:
        """Get the winner if the game is over."""
        return self.winner if self.game_over else None 