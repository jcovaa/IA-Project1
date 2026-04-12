'''
Bottles defined as list of colors, where the last color is the top of the bottle. For example:
bottles = [
   [1, 2, 1, 3] # R G R B
   [2, 2, 1, 1] # G G R R
   [3, 3, 2, 3] # B B G B
   []
   []
]
Capacity defined as the maximum number of colors a bottle can hold. For example:
capacity = 3
'''
import time

from src.search.algorithms import (
    greedy_search,
    a_star_search,
    weighted_a_star_search,
    heuristic1,
    heuristic2,
    heuristic3,
    heuristic4
)

import multiprocessing as mp

class GameState:
   def __init__(self, bottles, capacity, color_map=None):
      # hashable tuple for storing bottles in a set
      self.bottles = [list(b) for b in bottles]
      self.capacity = capacity
      self.color_map = color_map or {}

   def convert_color_names(self, bottle):
      return [self.color_map.get(c, str(c)) for c in bottle]

   '''Needed for the visited list'''
   def __eq__(self, other):
      return self.bottles == other.bottles
   
   def __hash__(self):
      return hash(tuple(tuple(b) for b in self.bottles))
   
   def __str__(self):
      return f"GameState(bottles={self.bottles}, capacity={self.capacity})"
   

def pour(game_state, bottle1, bottle2):
   bottles = game_state.bottles
   src, dest = bottles[bottle1], bottles[bottle2]

   # Check if source bottle is different from destination bottle
   if bottle1 == bottle2:
      return None
   # Check if source is valid
   if not src:
      return None

   # Check if source bottle is complete with the same color (can't pour from a bottle that is already complete)
   if len(set(src)) == 1 and len(src) == game_state.capacity:
      return None
   
   if len(dest)  == game_state.capacity: 
      return None
   
   pour_color = src[-1]
   # Check if the last color in the source bottle is the same as the last color in the destination bottle
   if dest and pour_color != dest[-1]:
      return None

  
   # Count only the contiguous top block of the same color
   units_to_pour = 0
   for c in reversed(src):
      if c != pour_color:
         break
      units_to_pour += 1

   if units_to_pour == 0:
      return None
   
   # Calculate how many units can be poured into the destination bottle
   space = game_state.capacity - len(dest)

   units_to_pour = min(units_to_pour, space)

   new_bottles = [list(b) for b in bottles]
   for _ in range(units_to_pour):
      new_bottles[bottle2].append(new_bottles[bottle1].pop())

   return GameState(new_bottles, game_state.capacity, game_state.color_map), 1

def game_states(game_state):
   new_states = []
   for i in range(len(game_state.bottles)):
      for j in range(len(game_state.bottles)):
         if i == j:
            continue
         result = pour(game_state, i, j)
         if result:
            new_states.append(result)
   return new_states

def goal_state(game_state):
   # Every bottle empty or full with the same color
   for bottle in game_state.bottles:
      # Empty bottle
      if not bottle:
         continue
      # Bottle is not full
      if len(bottle) != game_state.capacity:
         return False
      # Bottle is not full with the same color
      if len(set(bottle)) != 1:
         return False
   return True

def solution(node):
    path = []
    current = node
    while current:
        path.append(current.state)
        current = current.parent

    return list(reversed(path))

def solve(func, state, *args, **kwargs):
   start = time.time()
   result = func(state, goal_state, game_states, start, *args, **kwargs)

   # Search functions return (goal_node, stats); GUI only needs the node.
   if isinstance(result, tuple):
      return result[0]
   return result

def has_possible_moves(state): #rever ciclo in finito
    bottles = state.bottles
    capacity = state.capacity

    for i, source in enumerate(bottles):
        if len(source) == 0:
            return True
      
        top_color = source[-1]
        # contar quantos blocos da mesma cor estão no topo
        same_color_count = 1
        for color in reversed(source[:-1]):
            if color == top_color:
                same_color_count += 1
            else:
                break
            
        for j, target in enumerate(bottles):
            if i == j:
                continue
            # destino cheio
            if len(target) == capacity:
                continue
            # destino vazio - sempre possível mover
            if len(target) == 0:
                return True
            # cor do topo tem de coincidir
            if target[-1] != top_color:
                continue
            # verificar espaço disponível
            space_available = capacity - len(target)
            if space_available >= same_color_count :
                return True

    return False


def parse_int_or_default(value, default):
      try:
         text = (value or "").strip()
         return int(text) if text else default
      except ValueError:
         return default
      
def calculate_score(steps, time_elapsed, steps_ai, hint_count):
    base_score = 500
    
    if time_elapsed <= 0:
        time_elapsed = 1

    if steps <= 0:
        steps = 1

    score = base_score*(steps_ai/steps)+base_score*((steps_ai*(1+steps_ai*0.02))/time_elapsed) - hint_count*100

    return int(score)

def run_solver_choose_best_heuristic_algorithm(queue, algo_func, state, h_func):
    try:
        sol = solve(
            algo_func,
            state,
            h_func
        )

        if sol is None:
            queue.put(None)
            return

        path = solution(sol)
        steps = len(path) - 1
        queue.put(steps)

    except Exception:
        queue.put(None)


def choose_best_heuristic_algorithm(state, time_limit_per_run=1):

    algo_func = greedy_search
    h_func = heuristic4

    queue = mp.Queue()

    p = mp.Process(
        target=run_solver_choose_best_heuristic_algorithm,
        args=(queue, algo_func, state, h_func)
    )

    p.start()
    p.join(timeout=time_limit_per_run)

    if p.is_alive():
        p.terminate()
        p.join()
        return None, None, None

    if queue.empty():
        return None, None, None

    steps = queue.get()

    print(f"Greedy:Heuristic4:{steps}")

    return steps