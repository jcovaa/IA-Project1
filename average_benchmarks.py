import csv
import os
from collections import defaultdict

NUMERIC_FIELDS = ["time_s", "memory_kb", "states_visited", "solution_steps", "solution_cost"]
DIFFICULTIES = ["easy"]
NUM_FILES = 3

def parse_value(val):
    if val in ("N/A", "", None):
        return None
    try:
        return float(val)
    except ValueError:
        return None

def average_benchmarks(difficulty, doc_dir="doc"):
    all_rows = defaultdict(lambda: defaultdict(list)) 
    algo_meta = {} 
    
    for i in range(1, NUM_FILES + 1):
        filepath = os.path.join(doc_dir, f"benchmark_{difficulty}_{i}.csv")
        if not os.path.exists(filepath):
            print(f"  Warning: {filepath} not found, skipping.")
            continue

        with open(filepath, newline="") as f:
            reader = csv.DictReader(f)
            for row in reader:
                algo = row["algorithm"]
                algo_meta[algo] = {
                    "solved": row.get("solved", ""),
                    "status": row.get("status", ""),
                }
                for field in NUMERIC_FIELDS:
                    val = parse_value(row.get(field))
                    if val is not None:
                        all_rows[algo][field].append(val)

    if not all_rows:
        print(f"  No data found for difficulty={difficulty}")
        return []

    results = []
    for algo in all_rows:
        row_result = {
            "algorithm": algo,
            "solved": algo_meta[algo]["solved"],
            "status": algo_meta[algo]["status"],
        }
        for field in NUMERIC_FIELDS:
            values = all_rows[algo][field]
            if values:
                row_result[f"avg_{field}"] = round(sum(values) / len(values), 4)
            else:
                row_result[f"avg_{field}"] = "N/A"
        results.append(row_result)

    return results


def save_averages(results, difficulty, doc_dir="doc"):
    output_path = os.path.join(doc_dir, f"benchmark_{difficulty}_avg.csv")
    fieldnames = ["algorithm", "solved", "status"] + [f"avg_{f}" for f in NUMERIC_FIELDS]

    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(results)

    print(f"  Saved: {output_path}")
    return output_path


def print_results(results, difficulty):
    print(f"\n{'='*80}")
    print(f"Averages for difficulty={difficulty}")
    print(f"{'='*80}")
    print(f"{'Algorithm':<22} {'Status':<8} {'Time(s)':<10} {'Memory(KB)':<14} {'States':<10} {'Steps':<8} {'Cost'}")
    print("-" * 80)
    for row in results:
        print(
            f"{row['algorithm']:<22}"
            f"{row['status']:<10}"
            f"{str(row['avg_time_s']):<10}"
            f"{str(row['avg_memory_kb']):<14}"
            f"{str(row['avg_states_visited']):<10}"
            f"{str(row['avg_solution_steps']):<8}"
            f"{row['avg_solution_cost']}"
        )


if __name__ == "__main__":
    doc_dir = "doc"
    os.makedirs(doc_dir, exist_ok=True)

    for difficulty in DIFFICULTIES:
        print(f"\nProcessing {difficulty}...")
        results = average_benchmarks(difficulty, doc_dir)
        if results:
            print_results(results, difficulty)
            save_averages(results, difficulty, doc_dir)

    print("\nDone.")