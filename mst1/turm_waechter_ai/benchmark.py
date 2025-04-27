#!/usr/bin/env python3
"""
Run benchmark tests for the Turm & Wächter move generator.

This script measures the performance of the move generator on three different positions:
1. Initial position
2. Midgame position
3. Endgame position

Each position is tested with 10,000 iterations to get reliable performance measurements.
"""

from benchmarks.move_generation import run_benchmark_tests

if __name__ == "__main__":
    run_benchmark_tests() 