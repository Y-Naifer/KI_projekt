# Turm & Wächter Move Generator

A move generator for the Turm & Wächter board game. This tool takes a FEN string representation of a game position and outputs all legal moves according to the implemented game rules.

## Usage

```
python main.py "FEN_STRING"
```

Example:
```
python main.py "b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b"
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

To view the starting position:
```
python show_initial.py
```

## FEN Format

The FEN string represents the board state and current player:
- Board is 7x7
- Empty squares are represented by numbers
- Pieces are represented by characters:
  - 'r': Red tower
  - 'R': Red watcher (Guardian)
  - 'b': Blue tower
  - 'B': Blue watcher (Guardian)
- Stack heights are represented by numbers after the piece
- Current player is represented by 'r' (red) or 'b' (blue) at the end

Example: `b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b`

## Debugging Tools

For debugging and visualization purposes, you can use:

```
python debug.py "FEN_STRING"
```

This will show a visualization of the board and list all legal moves.

To test jumping rules:
```
python jump_test.py
```

## Note on Move Generation

The move generator follows the game rules as implemented in the codebase. All moves include a height suffix (e.g., `-1`) indicating how many pieces are moved, even for Guardian moves that always move a single piece. Due to potential differences in FEN string interpretation, the generated moves may vary from other implementations. 