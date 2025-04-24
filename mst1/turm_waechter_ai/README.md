# Turm & Wächter Move Generator

A simple move generator for the Turm & Wächter board game. This tool takes a FEN string representation of a game position and outputs all legal moves.

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

## FEN Format

The FEN string represents the board state and current player:
- Board is 7x7
- Empty squares are represented by numbers
- Pieces are represented by characters:
  - 'r': Red tower
  - 'R': Red watcher
  - 'b': Blue tower
  - 'B': Blue watcher
- Stack heights are represented by numbers after the piece
- Current player is represented by 'r' (red) or 'b' (blue) at the end

Example: `b36/3b12r3/7/7/1r2RG4/2/BG4/6r1 b`

## Debugging

For debugging and visualization purposes, you can use:

```
python debug.py "FEN_STRING"
```

This will show a visualization of the board and list all legal moves.

## Note on Move Generation

The move generator follows the game rules as implemented in the codebase. Due to potential differences in FEN string interpretation, the generated moves may vary from other implementations. If exact move compatibility is required for specific test cases, additional customization may be needed. 