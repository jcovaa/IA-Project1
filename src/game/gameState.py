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

	goal = func(state, goal_state, game_states,  *args, **kwargs) 
    
	return goal

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

def run_solver(func, algorithm, game_state, heuristic_func, weight_input, depth_input):
      if algorithm in ("A*", "Greedy"):
         return solve(func, game_state, heuristic_func)
      elif algorithm == "Weighted A*":
         return solve(func, game_state, heuristic_func=heuristic_func, weight=int(weight_input.text or 2))
      elif algorithm in ("DLS", "IDS"):
         return solve(func, game_state, depth_limit=int(depth_input.text or 10))
      return solve(func, game_state)

def calculate_score(steps, time_elapsed, difficulty):

    difficulty_multiplier = {
        "easy": 1,
        "medium": 1.5,
        "hard": 2
    }

    base_score = 1000

    score = base_score \
        - (steps * 15) \
        - (time_elapsed * 2)

    return int(score * difficulty_multiplier[difficulty])
