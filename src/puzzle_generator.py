import random
from game.gameState import GameState

DIFICULTY_CONFIGS = {
   "easy": {"bottles": 3, "capacity": 3, "colors": 3, "empty": 2},
   "medium": {"bottles": 5, "capacity": 4, "colors": 5, "empty": 2},
   "hard": {"bottles": 10, "capacity": 4, "colors": 10, "empty": 2}
}

COLOR_NAMES = [
   "red", "blue", "green", "orange", "yellow", "purple", "brown", "white", "pink", "cyan"
]

def generate_puzzle(difficulty="easy", seed=None):
   if seed is not None:
      random.seed(seed)
   
   config = DIFICULTY_CONFIGS[difficulty]
   bottles = config["bottles"]
   capacity = config["capacity"]
   colors = config["colors"]
   empty_bottles = config["empty"]

   units = [c for c in range(1, colors + 1) for _ in range(capacity)]
   random.shuffle(units)

   filled = [units[i * capacity:(i + 1) * capacity] for i in range(colors)]
   empty_bottles = [[] for _ in range(empty_bottles)]
   all_bottles = filled + empty_bottles

   return GameState(all_bottles, capacity)