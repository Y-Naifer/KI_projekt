#!/usr/bin/env python3
"""
Benchmark tests for Turm & Wächter.
This script measures the speed of the move generator on different position types:
- Initial position
- Midgame position
- Endgame position

For each position, it runs 10,000 iterations and measures the total and average time.
"""

import time
from typing import List, Tuple
from core.board import Board
from core.rules import GameRules
from core.fen import FenParser

# Position FEN strings
INITIAL_POSITION = "r1r11RG1r1r1/2r11r12/3r13/7/3b13/2b11b12/b1b11BG1b1b1 r"
MIDGAME_POSITION = "3RG1r11/3r33/r36/7/b32b33/7/3BG2b1 b"
ENDGAME_POSITION = "RGBG5/7/7/7/7/7/7 r"

def benchmark_position(fen_str: str, label: str, iterations: int = 10000):
    """
    Benchmark the move generation speed for a specific position.
    
    Args:
        fen_str: FEN string representation of the position
        label: Description of the position type
        iterations: Number of times to generate legal moves
    """
    print(f"\nBenchmarking {label} position")
    print(f"Position: {fen_str}")
    
    parser = FenParser()
    board, current_player = parser.parse_fen(fen_str)
    rules = GameRules(board)
    rules.current_player = current_player  # Set the current player correctly
    
    # First check: get number of legal moves (for verification)
    moves = rules.get_legal_moves(current_player)
    print(f"Legal moves: {len(moves)}")
    
    # Main benchmark
    print(f"Running {iterations} iterations...")
    
    start_time = time.time()
    for _ in range(iterations):
        rules.get_legal_moves(current_player)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time * 1000 / iterations
    
    print(f"Total time: {total_time:.2f} seconds")
    print(f"Average time: {avg_time:.4f} ms per generation")
    
    return total_time, avg_time, len(moves)

def run_benchmark_tests():
    """Run benchmark tests for all position types"""
    print("\nBenchmark Tests for Turm & Wächter Move Generator")
    print("=================================================\n")
    
    iterations = 10000
    results = []
    
    # Test 1: Initial position
    initial_time, initial_avg, initial_moves = benchmark_position(
        INITIAL_POSITION, "Initial", iterations
    )
    results.append(("Initial", initial_time, initial_avg, initial_moves))
    
    # Test 2: Midgame position
    midgame_time, midgame_avg, midgame_moves = benchmark_position(
        MIDGAME_POSITION, "Midgame", iterations
    )
    results.append(("Midgame", midgame_time, midgame_avg, midgame_moves))
    
    # Test 3: Endgame position
    endgame_time, endgame_avg, endgame_moves = benchmark_position(
        ENDGAME_POSITION, "Endgame", iterations
    )
    results.append(("Endgame", endgame_time, endgame_avg, endgame_moves))
    
    # Summary
    print("\nSummary of Results")
    print("=================")
    print(f"{'Position':<10} | {'Legal Moves':<12} | {'Total Time (s)':<15} | {'Avg Time (ms)':<15}")
    print(f"{'-'*10:<10} | {'-'*12:<12} | {'-'*15:<15} | {'-'*15:<15}")
    
    for pos_type, total, avg, moves in results:
        print(f"{pos_type:<10} | {moves:<12} | {total:<15.2f} | {avg:<15.4f}")
    
    print("\nBenchmark tests completed.")

if __name__ == "__main__":
    run_benchmark_tests() 