from typing import List, Tuple, Optional
from core.piece import PieceType
from core.bitboard import BitboardBoard

class BitboardRules:
    """Rules implementation for Turm & Wächter game using bitboard representation."""
    
    def __init__(self, board: BitboardBoard):
        self.board = board
        self.current_player = 1  # Red starts by default
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
        stack_height = self.board.get_stack_height(from_x, from_y)
        if stack_height < height or height <= 0:
            return False
        
        # Check if the top piece belongs to the current player
        owner = self.board.get_stack_owner(from_x, from_y)
        if owner != self.current_player:
            return False
        
        # Calculate move distance
        dx, dy = to_x - from_x, to_y - from_y
        
        # Only orthogonal moves allowed (no diagonal)
        if dx != 0 and dy != 0:
            return False
        
        # Move distance must exactly equal the height of the moving pieces
        move_distance = max(abs(dx), abs(dy))
        if move_distance != height:
            return False
        
        # Check for obstacles in the path
        step_x = 0 if dx == 0 else (1 if dx > 0 else -1)
        step_y = 0 if dy == 0 else (1 if dy > 0 else -1)
        
        # Start checking from one step away from the origin
        current_x, current_y = from_x + step_x, from_y + step_y
        
        # Check each square in the path except the destination
        while (current_x, current_y) != (to_x, to_y):
            if self.board.get_stack_height(current_x, current_y) > 0:
                # Found an obstacle in the path
                return False
            current_x += step_x
            current_y += step_y
        
        return True
    
    def is_valid_capture(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Check if a capture is valid."""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # Get information about source and destination
        source_owner = self.board.get_stack_owner(from_x, from_y)
        target_owner = self.board.get_stack_owner(to_x, to_y)
        
        # Can't capture if destination is empty
        if target_owner is None:
            return False
        
        # Can't capture own pieces
        if target_owner == self.current_player:
            return False
        
        moving_piece_type = self.board.get_top_piece_type(from_x, from_y)
        target_piece_type = self.board.get_top_piece_type(to_x, to_y)
        
        # Watcher can capture any piece
        if moving_piece_type == PieceType.WAECHTER:
            return True
        
        # Tower can capture Watcher (win condition)
        if moving_piece_type == PieceType.TURM and target_piece_type == PieceType.WAECHTER:
            return True
        
        # Tower can capture Tower if the moved height is equal to or greater than the target stack height
        if (moving_piece_type == PieceType.TURM and 
            target_piece_type == PieceType.TURM):
            # Check if the moved stack height is equal to or greater than the target stack height
            target_height = self.board.get_stack_height(to_x, to_y)
            if height >= target_height:
                return True
            else:
                return False
        
        return False
    
    def is_valid_stack(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Check if stacking is valid."""
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        # Get information about source and destination
        target_owner = self.board.get_stack_owner(to_x, to_y)
        
        # Can only stack on own pieces
        if target_owner is None or target_owner != self.current_player:
            return False
        
        # Get the piece types
        moving_piece_type = self.board.get_top_piece_type(from_x, from_y)
        target_piece_type = self.board.get_top_piece_type(to_x, to_y)
        
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
        # Use a set to track moves we've already added to avoid duplicates
        added_moves = set()
        
        for y in range(self.board.SIZE):
            for x in range(self.board.SIZE):
                # Skip if the square is empty or belongs to the opponent
                owner = self.board.get_stack_owner(x, y)
                if owner != player:
                    continue
                
                stack_height = self.board.get_stack_height(x, y)
                # Try all possible heights to move
                for height in range(1, stack_height + 1):
                    # Try all four directions
                    for dx, dy in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                        # Move exactly the distance of the height
                        nx, ny = x + dx * height, y + dy * height
                        
                        # Skip if out of bounds
                        if not (0 <= nx < self.board.SIZE and 0 <= ny < self.board.SIZE):
                            continue
                        
                        # Check if we've already added this move
                        move_key = ((x, y), (nx, ny), height)
                        if move_key in added_moves:
                            continue
                        
                        # First check if the move is valid according to movement rules
                        saved_current_player = self.current_player
                        self.current_player = player  # Temporarily set current player for validation
                        
                        if self.is_valid_move((x, y), (nx, ny), height):
                            target_owner = self.board.get_stack_owner(nx, ny)
                            
                            # Empty destination or capture or stack
                            if (target_owner is None or 
                                self.is_valid_capture((x, y), (nx, ny), height) or
                                self.is_valid_stack((x, y), (nx, ny), height)):
                                legal_moves.append(((x, y), (nx, ny), height))
                                # Add to set of already added moves
                                added_moves.add(move_key)
                        
                        # Restore current player
                        self.current_player = saved_current_player
        
        return legal_moves
    
    def make_move(self, from_pos: Tuple[int, int], to_pos: Tuple[int, int], height: int) -> bool:
        """Execute a move if valid and check win conditions."""
        if not self.is_valid_move(from_pos, to_pos, height):
            return False
        
        from_x, from_y = from_pos
        to_x, to_y = to_pos
        
        target_owner = self.board.get_stack_owner(to_x, to_y)
        moving_piece_type = self.board.get_top_piece_type(from_x, from_y)
        
        # Handle capture
        if target_owner is not None and target_owner != self.current_player:
            target_piece_type = self.board.get_top_piece_type(to_x, to_y)
            
            # Check if capturing opponent's Watcher (win condition)
            if target_piece_type == PieceType.WAECHTER:
                self.game_over = True
                self.winner = self.current_player
            
            # Remove the captured piece
            self.board.capture_piece(to_pos)
            
            # Execute the move
            self.board.move_stack(from_pos, to_pos, height)
        
        # Handle stacking (move to friendly tower)
        elif target_owner == self.current_player:
            # Execute the move (will handle stacking)
            self.board.move_stack(from_pos, to_pos, height)
        
        # Handle normal move to empty space
        else:
            # Execute the move
            self.board.move_stack(from_pos, to_pos, height)
        
        # Check center field win condition
        center_x, center_y = self.board.SIZE // 2, self.board.SIZE // 2
        center_owner = self.board.get_stack_owner(center_x, center_y)
        center_piece_type = self.board.get_top_piece_type(center_x, center_y)
        
        if (center_owner == self.current_player and 
            center_piece_type == PieceType.WAECHTER):
            self.game_over = True
            self.winner = self.current_player
        
        # Switch player
        self.current_player = 3 - self.current_player  # Toggle between 1 and 2
        
        return True
    
    def is_game_over(self) -> bool:
        """Check if the game is over."""
        return self.game_over
    
    def get_winner(self) -> Optional[int]:
        """Get the winner if the game is over."""
        return self.winner if self.game_over else None 