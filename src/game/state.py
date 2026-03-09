class GameState:
   def __init__(self, bottles, capacity):
      # hashable tuple for storing bottles in a set
      self.bottles = tuple(tuple(b) for b in bottles)
      self.capacity = capacity

   '''Needed for the visited list'''
   def __eq__(self, other):
      return self.bottles == other.bottles
   
   def __hash__(self):
      return hash(self.bottles)
   
   def __str__(self):
      return f"GameState(bottles={self.bottles}, capacity={self.capacity})"
   

def pour(game_state, bottle1, bottle2):
   bottles = game_state.bottles
   src, dest = bottles[bottle1], bottles[bottle2]

   # Check if source bottle is different from destination bottle
   if bottle1 == bottle2:
      return None
   # Check if source and destination are valid and exist
   if not src or not dest:
      return None
   # Check if destination bottle is full
   if len(dest) == game_state.capacity:
      return None
   # Check if the last color in the source bottle is the same as the last color
   if src[-1] != dest[-1]:
      return None

   color = src[-1]
   # Count how many units of the same color are at the top of the source bottle
   units_to_pour = sum(1 for c in reversed(src) if c == color)
   # Calculate how many units can be poured into the destination bottle
   space = game_state.capacity - len(dest)

   units_to_pour = min(units_to_pour, space)

   new_bottles = [list(b) for b in bottles]
   for _ in range(units_to_pour):
      new_bottles[bottle2].append(new_bottles[bottle1].pop())

   return GameState(new_bottles, game_state.capacity), 1
