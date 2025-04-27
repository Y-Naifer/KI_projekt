#!/usr/bin/env python3
"""
Benchmark tests for Turm & Wächter.
This script runs performance tests for the move generator and AI.
"""

import time
import random
from typing import List, Tuple
from core.board import Board
from core.rules import GameRules
from core.fen import FenParser
from ai.dummy_ai import dummy_ai_choose_move

def run_benchmark_tests():
    """Run benchmark tests for move generation performance"""
    print("\nBenchmark Tests for Turm & Wächter")
    print("=================================\n")
    
    # Test 1: Generate moves from initial position
    print("Test 1: Initial position move generation")
    board = Board(setup_initial=True)
    rules = GameRules(board)
    
    start_time = time.time()
    moves = rules.get_legal_moves(1)  # Red player
    end_time = time.time()
    
    print(f"  Result: {len(moves)} legal moves")
    print(f"  Time: {(end_time - start_time)*1000:.2f} ms\n")
    
    # Test 2: Generate moves from a complex mid-game position
    print("Test 2: Complex position move generation")
    parser = FenParser()
    fen_str = "3RG1r11/3r33/r36/7/b32b33/7/3BG2b1 r"
    board, current_player = parser.parse_fen(fen_str)
    rules = GameRules(board)
    
    start_time = time.time()
    moves = rules.get_legal_moves(current_player)
    end_time = time.time()
    
    print(f"  Position: {fen_str}")
    print(f"  Result: {len(moves)} legal moves")
    print(f"  Time: {(end_time - start_time)*1000:.2f} ms\n")
    
    # Test 3: Random AI move selection benchmark
    print("Test 3: Random AI performance")
    board = Board(setup_initial=True)
    
    start_time = time.time()
    iterations = 1000
    for _ in range(iterations):
        dummy_ai_choose_move(board, 1)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time * 1000 / iterations
    
    print(f"  Iterations: {iterations}")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average: {avg_time:.2f} ms per move\n")
    
    # Test 4: Large number of move generations
    print("Test 4: Performance under load (10,000 move generations)")
    board = Board(setup_initial=True)
    rules = GameRules(board)
    
    start_time = time.time()
    iterations = 10000
    for _ in range(iterations):
        _ = rules.get_legal_moves(1 if random.random() > 0.5 else 2)
    end_time = time.time()
    
    total_time = end_time - start_time
    avg_time = total_time * 1000 / iterations
    
    print(f"  Iterations: {iterations}")
    print(f"  Total time: {total_time:.2f} seconds")
    print(f"  Average: {avg_time:.2f} ms per generation\n")
    
    print("Benchmark tests completed")

if __name__ == "__main__":
    run_benchmark_tests() 