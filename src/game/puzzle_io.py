from src.game.gameState import GameState

def save_puzzle(game_state, filename):
   with open(filename, 'w') as f:
      f.write(f"bottles={len(game_state.bottles)}\n")
      f.write(f"capacity={game_state.capacity}\n")
      for i, bottle in enumerate(game_state.bottles):
         colors = " ".join(map(str, bottle))
         f.write(f"bottle{i}={colors}\n")

def load_puzzle(filename):
   with open(filename, 'r') as f:
      lines = f.readlines()

   bottles_count = int(lines[0].split('=')[1])
   capacity = int(lines[1].split('=')[1])
   bottles = []
   for line in lines[2:2 + bottles_count]:
      parts = line.split('=', 1)[1].strip()
      bottle = list(map(int, parts.split())) if parts else []
      bottles.append(bottle)

   return GameState(bottles, capacity)


def save_solver_results(result_data, filename):
   with open(filename, 'w') as f:
      f.write("=== Water Sort Solver Result ===\n")
      f.write(f"Algorithm: {result_data.get('algorithm', 'N/A')}\n")
      f.write(f"Heuristic: {result_data.get('heuristic', 'N/A')}\n")
      f.write(f"Solved: {result_data.get('solved', False)}\n")
      f.write(f"Time (s): {result_data.get('time_s', 'N/A')}\n")
      f.write(f"Memory (KB): {result_data.get('memory_kb', 'N/A')}\n")
      f.write(f"States visited: {result_data.get('states_visited', 'N/A')}\n")
      f.write(f"Solution steps/cost: {result_data.get('solution_steps', 'N/A')}\n")
      f.write(f"Score: {result_data.get('score', 'N/A')}\n")
      f.write(f"Difficulty: {result_data.get('difficulty', 'N/A')}\n\n")

      f.write("Initial state:\n")
      initial_state = result_data.get('initial_state', [])
      for idx, bottle in enumerate(initial_state):
         f.write(f"  bottle{idx}: {bottle}\n")

      f.write("\nFinal state:\n")
      final_state = result_data.get('final_state', [])
      for idx, bottle in enumerate(final_state):
         f.write(f"  bottle{idx}: {bottle}\n")