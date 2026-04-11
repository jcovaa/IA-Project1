import time
import tracemalloc


def solution_length(node):
   length = 0
   current = node

   while current.parent:
      length += 1
      current = current.parent

   return length


def run_solver_with_metrics(func, game_state, goal_state_func, operators_func, solver_kwargs):
   tracemalloc.start()
   start = time.perf_counter()
   result = None
   error = None

   try:
      result = func(game_state, goal_state_func, operators_func, **solver_kwargs)
   except Exception as exc:
      error = exc
   finally:
      elapsed = time.perf_counter() - start
      _, peak_memory = tracemalloc.get_traced_memory()
      tracemalloc.stop()

   if error is not None:
      raise error

   if isinstance(result, tuple):
      node, stats = result
   else:
      node, stats = result, {"states_visited": 0}

   return node, stats, elapsed, round(peak_memory / 1024, 2)


def build_solver_result(
   algorithm,
   heuristic="N/A",
   solved=False,
   status="No",
   elapsed=0,
   memory_kb=0,
   stats=None,
   solution_steps=None,
   solution_cost=None,
   difficulty=None,
   initial_state=None,
   final_state=None,
   score=None,
):
   result = {
      "algorithm": algorithm,
      "heuristic": heuristic,
      "solved": solved,
      "status": status,
      "time_s": round(elapsed, 4),
      "memory_kb": memory_kb,
      "states_visited": stats["states_visited"] if stats and "states_visited" in stats else "N/A",
      "solution_steps": solution_steps,
      "solution_cost": solution_cost,
   }

   if difficulty is not None:
      result["difficulty"] = difficulty
   if initial_state is not None:
      result["initial_state"] = initial_state
   if final_state is not None:
      result["final_state"] = final_state
   if score is not None:
      result["score"] = score

   return result