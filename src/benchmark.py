import csv
import threading
from src.puzzle_generator import generate_puzzle
from src.game.gameState import goal_state, game_states
from src.game.solver_metrics import build_solver_result, run_solver, solution_length
from src.search.algorithms import (
    breadth_first_search, depth_first_search,
    depth_limited_search, iterative_deepening_search,
    uniform_cost_search, greedy_search,
    a_star_search, weighted_a_star_search,
    iterative_deepening_a_star_search,
    heuristic1, heuristic2, heuristic3, heuristic4, heuristic5, heuristic6, heuristic7
)

# Algorithms that don't need a heuristic
UNIFORMED = [
    ("BFS", breadth_first_search, {}),
    ("DFS", depth_first_search, {}),
    ("DLS(limit=40)", depth_limited_search, {"limit": 40}),
    ("IDS(limit=40)", iterative_deepening_search, {"limit": 40}),
    ("DLS(limit=50)", depth_limited_search, {"limit": 50}),
    ("IDS(limit=50)", iterative_deepening_search, {"limit": 50}),
    ("UCS", uniform_cost_search, {})
]

# Algorithms that need a heuristic
INFORMED = [
    ("Greedy_H1", greedy_search, {"heuristic": heuristic1}),
    ("Greedy_H2", greedy_search, {"heuristic": heuristic2}),
    ("Greedy_H3", greedy_search, {"heuristic": heuristic3}),
    ("Greedy_H4", greedy_search, {"heuristic": heuristic4}),
    ("Greedy_H5", greedy_search, {"heuristic": heuristic5}),
    ("Greedy_H6", greedy_search, {"heuristic": heuristic6}),
    ("Greedy_H7", greedy_search, {"heuristic": heuristic7}),
    ("A*_H1", a_star_search, {"heuristic": heuristic1}),
    ("A*_H2", a_star_search, {"heuristic": heuristic2}),
    ("A*_H3", a_star_search, {"heuristic": heuristic3}),
    ("A*_H4", a_star_search, {"heuristic": heuristic4}),
    ("A*_H4", a_star_search, {"heuristic": heuristic5}),
    ("A*_H6", a_star_search, {"heuristic": heuristic6}),
    ("A*_H7", a_star_search, {"heuristic": heuristic7}),
    ("WA*_H1(w=1.5)", weighted_a_star_search, {"heuristic": heuristic1, "weight": 1.5}),
    ("WA*_H2(w=1.5)", weighted_a_star_search, {"heuristic": heuristic2, "weight": 1.5}),
    ("WA*_H3(w=1.5)", weighted_a_star_search, {"heuristic": heuristic3, "weight": 1.5}),
    ("WA*_H4(w=1,5)", weighted_a_star_search, {"heuristic": heuristic4, "weight": 1.5}),
    ("WA*_H5(w=1,5)", weighted_a_star_search, {"heuristic": heuristic5, "weight": 1.5}),
    ("WA*_H6(w=1,5)", weighted_a_star_search, {"heuristic": heuristic6, "weight": 1.5}),
    ("WA*_H7(w=1,5)", weighted_a_star_search, {"heuristic": heuristic7, "weight": 1.5}),
    ("WA*_H1(w=2)", weighted_a_star_search, {"heuristic": heuristic1, "weight": 2}),
    ("WA*_H2(w=2)", weighted_a_star_search, {"heuristic": heuristic2, "weight": 2}),
    ("WA*_H3(w=2)", weighted_a_star_search, {"heuristic": heuristic3, "weight": 2}),
    ("WA*_H4(w=2)", weighted_a_star_search, {"heuristic": heuristic4, "weight": 2}),
    ("WA*_H5(w=2)", weighted_a_star_search, {"heuristic": heuristic5, "weight": 2}),
    ("WA*_H6(w=2)", weighted_a_star_search, {"heuristic": heuristic6, "weight": 2}),
    ("WA*_H7(w=2)", weighted_a_star_search, {"heuristic": heuristic7, "weight": 2}),
    ("IDA*_H1", iterative_deepening_a_star_search, {"heuristic": heuristic1}),
    ("IDA*_H2", iterative_deepening_a_star_search, {"heuristic": heuristic2}),
    ("IDA*_H3", iterative_deepening_a_star_search, {"heuristic": heuristic3}),
    ("IDA*_H4", iterative_deepening_a_star_search, {"heuristic": heuristic4}),
    ("IDA*_H5", iterative_deepening_a_star_search, {"heuristic": heuristic5}),
    ("IDA*_H6", iterative_deepening_a_star_search, {"heuristic": heuristic6}),
    ("IDA*_H7", iterative_deepening_a_star_search, {"heuristic": heuristic7}),
]

def run_algorithms(name, func, game_state, kwargs, timeout=120):
    result_container = [None]
    exception_container = [None]

    def target():
        try:
            result_container[0] = run_solver(func, game_state, goal_state, game_states, kwargs)
        except Exception as e:
            exception_container[0] = e

    thread = threading.Thread(target=target, daemon=True)
    thread.start()
    thread.join(timeout=timeout)

    if exception_container[0]:
        return {"algorithm": name, "error": str(exception_container[0])}

    if thread.is_alive() or result_container[0][0] is False:
        return {
            "algorithm": name,
            "solved": False,
            "status": "Timeout",
            "time_s": f">{timeout}s",
            "memory_kb": "N/A",
            "states_visited": "N/A",
            "solution_steps": None,
            "solution_cost": None,
            "timed_out": True
        }
    
    result, stats, elapsed, peak_memory = result_container[0]

    if result is None:
        return build_solver_result(
            algorithm=name,
            solved=False,
            status="Cutoff" if stats.get("cutoff") else "No",
            elapsed=elapsed,
            memory_kb=peak_memory,
            stats=stats,
        )

    return build_solver_result(
        algorithm=name,
        solved=True,
        status="Yes",
        elapsed=elapsed,
        memory_kb=peak_memory,
        stats=stats,
        solution_steps=solution_length(result),
        solution_cost=result.cost,
    )

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
            print(f"{row['algorithm']:<20} ERROR: {row['error']}")
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
