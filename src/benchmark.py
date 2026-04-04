import time
import tracemalloc
import csv
import threading
from src.puzzle_generator import generate_puzzle
from src.game.gameState import goal_state, game_states
from src.search.algorithms import (
    breadth_first_search, depth_first_search,
    depth_limited_search, iterative_deepening_search,
    uniform_cost_search, greedy_search,
    a_star_search, weighted_a_star_search,
    iterative_deepening_a_star_search,
    heuristic1, heuristic2, heuristic3, heuristic4
)

# Algorithms that don't need a heuristic
UNIFORMED = [
    ("BFS", breadth_first_search, {}),
    ("DFS", depth_first_search, {}),
    ("DLS", depth_limited_search, {"limit": 50}),
    ("IDS", iterative_deepening_search, {"limit": 50}),
    ("UCS", uniform_cost_search, {})
]

# Algorithms that need a heuristic
INFORMED = [
    ("Greedy_H1", greedy_search, {"heuristic": heuristic1}),
    ("Greedy_H2", greedy_search, {"heuristic": heuristic2}),    
    ("Greedy_H3", greedy_search, {"heuristic": heuristic3}),
    ("Greedy_H4", greedy_search, {"heuristic": heuristic4}),
    ("A*_H1", a_star_search, {"heuristic": heuristic1}),
    ("A*_H2", a_star_search, {"heuristic": heuristic2}),
    ("A*_H3", a_star_search, {"heuristic": heuristic3}),
    ("A*_H4", a_star_search, {"heuristic": heuristic4}),
    ("WA*_H1(w=1.5)", weighted_a_star_search, {"heuristic": heuristic1, "weight": 1.5}),
    ("WA*_H2(w=1.5)", weighted_a_star_search, {"heuristic": heuristic2, "weight": 1.5}),
    ("WA*_H3(w=1.5)", weighted_a_star_search, {"heuristic": heuristic3, "weight": 1.5}),
    ("WA*_H4(w=1.5)", weighted_a_star_search, {"heuristic": heuristic4, "weight": 1.5}),
    ("WA_H4(w=2)", weighted_a_star_search, {"heuristic": heuristic4, "weight": 2}),
    ("IDA*_H1", iterative_deepening_a_star_search, {"heuristic": heuristic1}),
    ("IDA*_H2", iterative_deepening_a_star_search, {"heuristic": heuristic2}),
    ("IDA*_H3", iterative_deepening_a_star_search, {"heuristic": heuristic3}),
    ("IDA*_H4", iterative_deepening_a_star_search, {"heuristic": heuristic4})
]

# Count steps from root to goal node
def solution_length(node):
    length, current = 0, node
    while current.parent:
        length += 1
        current = current.parent
    return length

# Run one algorithm, measure time, memory and solution quality
def run_algorithms(name, func, game_state, kwargs, timeout=60):
    result_container = [None]
    exception_container = [None]

    def target():
        try:
            result_container[0] = func(game_state, goal_state, game_states, **kwargs)
        except Exception as e:
            exception_container[0] = e

    tracemalloc.start()
    start = time.perf_counter()

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout=timeout)
    
    elasped = time.perf_counter() - start
    _, peak_memory = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    if exception_container[0]:
        return {"algorithm": name, "error": str(exception_container[0])}

    if thread.is_alive():
        return {
            "algorithm": name,
            "solved": False,
            "status": "Timeout",
            "time_s": f">{timeout}s",
            "memory_kb": round(peak_memory / 1024, 2),
            "states_visited": "N/A",
            "solution_steps": None,
            "solution_cost": None,
            "timed_out": True
        }
    
    result, stats = result_container[0]

    if result is None:
        return {
            "algorithm": name,
            "solved": False,
            "status": "Cutoff" if stats.get("cutoff") else "No",
            "time_s": round(elasped, 4),
            "memory_kb": round(peak_memory / 1024, 2),
            "states_visited": stats["states_visited"],
            "solution_steps": None,
            "solution_cost": None,
        }

    return {
        "algorithm": name,
        "solved": True,
        "status": "Yes",
        "time_s": round(elasped, 4),
        "memory_kb": round(peak_memory / 1024, 2),
        "states_visited": stats["states_visited"],
        "solution_steps": solution_length(result),
        "solution_cost": result.cost,
    }

def benchmark(difficulty="easy", seed=42, output_file=None):
    game_state = generate_puzzle(difficulty, seed=seed)
    print(f"\n{'='*60}")
    print(f"Benchmarking difficulty={difficulty}, seed={seed}")
    print(f"{'='*60}")
    print(f"{'Algorithm':<20} {'Status':<8} {'Time(s)':<10} {'Memory(KB)':<12} {'States':<10} {'Steps':<8} {'Cost'}")
    print("-"*80)

    results = []
    for name, func, kwargs in UNIFORMED + INFORMED:
        row = run_algorithms(name, func, game_state, kwargs)
        results.append(row)

        if "error" in row:
            print(f"{row['algorif "erroithm']:<20} ERROR: {row['error']}")
            continue

        print(
            f"{row['algorithm']:<20}"
            f"{row['status']:<10}"
            f"{str(row['time_s']):<10}"
            f"{row['memory_kb']:<12}"
            f"{str(row['states_visited']):<10}"
            f"{str(row['solution_steps']):<8} "
            f"{row['solution_cost'] if row['solution_cost'] is not None else 'N/A'}"
        )
    
    if output_file:
        save_results(results, difficulty, seed, output_file)

    return results

# Save benchmark results to a CSV file
def save_results(results, difficulty, seed, filepath):
    with open(filepath, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=[
            "algorithm", "solved", "status", "time_s", "memory_kb",
            "states_visited", "solution_steps", "solution_cost"
        ])
        writer.writeheader()
        for row in results:
            if "error" not in row:
                writer.writerow({k: row.get(k, "N/A") for k in writer.fieldnames})
    print(f"\nResults saved to {filepath}")
