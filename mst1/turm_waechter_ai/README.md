# Turm & Wächter Move Generator

A move generator for the Turm & Wächter board game. This tool takes a FEN string representation of a game position and outputs all legal moves according to the implemented game rules.

## Usage

```
python zuggenerator.py "FEN_STRING"
```

Example:
```
python zuggenerator.py "b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b"
```

## Output Format

The tool outputs one legal move per line in algebraic notation:
- Format: `{from_col}{from_row}-{to_col}{to_row}-{height}`
- `from_col` and `to_col` are columns (A-G)
- `from_row` and `to_row` are rows (1-7)
- `height` is the stack height being moved

Example output:
```
A7-B7-1
A7-C7-2
D6-C6-1
...
```

## Game Rules

The following rules have been implemented:

1. **Movement:**
   - Pieces move orthogonally (horizontally or vertically, not diagonally)
   - A piece or stack must move exactly as many spaces as its height
   - Pieces cannot jump over obstacles in their path
   
2. **Stacking Restrictions:**
   - Towers cannot stack on top of Wächters (Guardians)
   - Wächters cannot stack on top of Towers
   
3. **Capture Rules:**
   - Wächters can capture any opponent piece
   - Towers can capture opponent Towers if the moved height is equal to or greater than the opponent's stack height
   - Towers can capture opponent Wächters (instant win)

4. **Win Conditions:**
   - Capturing the opponent's Wächter (Guardian)
   - Moving your Wächter to the center field (D4)

## Starting Position

The standard starting position for Turm & Wächter:

- Red Wächter at position D7
- Red Towers at positions A7, B7, C6, D5, E6, F7, G7
- Blue Wächter at position D1
- Blue Towers at positions A1, B1, C2, D3, E2, F1, G1

FEN string for the initial starting position:
```
r1r11RG1r1r1/2r11r12/3r13/7/3b13/2b11b12/b1b11BG1b1b1 r
```

To view the starting position:
```
python demos/show_initial.py
```

## FEN Format

The FEN string represents the board state and current player:
- Board is 7x7
- Empty squares are represented by numbers
- Pieces are represented by characters:
  - 'r': Red tower
  - 'RG': Red Guardian (Wächter)
  - 'b': Blue tower
  - 'BG': Blue Guardian (Wächter)
- Stack heights are represented by numbers after tower pieces (r1, b1)
- Current player is represented by 'r' (red) or 'b' (blue) at the end

Example: `b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b`

## Implementation

The codebase uses a bitboard-based representation for the game board. Bitboards use single bits to represent piece positions, which allows for efficient move generation and board state manipulation.

The bitboard implementation:
- Uses separate bitboards for Red Guardians, Blue Guardians, and Tower stacks of different heights
- Implements efficient bit operations for board manipulations
- Provides a clean API for game state management

The implementation is optimized for:
1. Memory efficiency - using compact bit representations
2. Clean state transitions - using immutable bit operations
3. Logical clarity - separating concerns by piece type and player

## Tools and Scripts

### Debugging and Visualization

For debugging and visualization purposes, you can use:

```
PYTHONPATH=. python utils/debug.py "FEN_STRING"
```

This will show a visualization of the board and list all legal moves.

### Benchmarking

To evaluate the performance of the move generator, you can run:

```
PYTHONPATH=. python benchmarks/benchmark.py
```

This runs tests on three representative positions:
- Initial position: `r1r11RG1r1r1/2r11r12/3r13/7/3b13/2b11b12/b1b11BG1b1b1 r`
- Midgame position: `3RG1r11/3r33/r36/7/b32b33/7/3BG2b1 b`
- Endgame position: `RGBG5/7/7/7/7/7/7 r`

Each position is tested with 10,000 iterations to provide reliable performance metrics.

### AI Implementation

The project includes a simple AI implementation that selects a random legal move:

```
PYTHONPATH=. python Dummy_KI.py "FEN_STRING"
```

Example:
```
PYTHONPATH=. python Dummy_KI.py "3RG1r11/3r33/r36/7/b32b33/7/3BG2b1 b"
```

This will output a single randomly selected legal move in algebraic notation.

### Demo Applications

Several demo applications are provided in the `demos` directory:

- `show_initial.py` - Displays the initial board position
- `jump_test.py` - Tests if towers can jump over other pieces
- `ai_game.py` - Demonstrates AI playing a game against itself

Run these demos with:
```
PYTHONPATH=. python demos/<script_name>.py
```

## Testing

To run the unit tests:

```
PYTHONPATH=. python tests/unit_tests.py
```

These tests verify the correctness of move generation across different game positions and scenarios.

## Project Structure

- `core/` - Core game logic
  - `bitboard.py` - Bitboard implementation for board representation
  - `bitboard_rules.py` - Game rules implementation using bitboards
  - `fen.py` - FEN string parsing and generation
  - `piece.py` - Piece type definitions

- `benchmarks/` - Performance testing
  - `benchmark.py` - Benchmark scripts for move generation

- `utils/` - Utility functions
  - `debug.py` - Debugging and visualization tools

- `demos/` - Demo applications
  - `show_initial.py` - Display initial board position
  - `jump_test.py` - Test jumping mechanics
  - `ai_game.py` - AI vs AI demonstration

- `tests/` - Unit tests
  - `unit_tests.py` - Comprehensive tests for move generation

## Note on Move Generation

The move generator follows the game rules as implemented in the codebase. All moves include a height suffix (e.g., `-1`) indicating how many pieces are moved, even for Guardian moves that always move a single piece. Due to potential differences in FEN string interpretation, the generated moves may vary from other implementations. 