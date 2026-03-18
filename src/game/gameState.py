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
   def __init__(self, bottles, capacity):
      # hashable tuple for storing bottles in a set
      self.bottles = [list(b) for b in bottles]
      self.capacity = capacity

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
   if not dest:
      return None
   # Check if source bottle is complete 
   if len(src) == game_state.capacity:
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
   # Calculate how many units can be poured into the destination bottle
   space = game_state.capacity - len(dest)

   if not space:
      return None

   units_to_pour = min(units_to_pour, space)

   new_bottles = [list(b) for b in bottles]
   for _ in range(units_to_pour):
      new_bottles[bottle2].append(new_bottles[bottle1].pop())

   return GameState(new_bottles, game_state.capacity), 1


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