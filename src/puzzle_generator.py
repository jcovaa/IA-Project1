import random
from src.game.gameState import GameState

#mudar niveis
DIFICULTY_CONFIGS = {
    "easy":   {"bottles": (5, 6),  "capacity": (3, 4)},
    "medium": {"bottles": (6, 8),  "capacity": (4, 5)},
    "hard":   {"bottles": (9, 12), "capacity": (5, 6)}
}

COLOR_NAMES = [
   "red", "green", "blue", "orange", "yellow", "purple", "brown", "white", "pink", "cyan",
]

def generate_puzzle(difficulty="easy", seed=None):
   if seed is not None:
      random.seed(seed)
   
   config = DIFICULTY_CONFIGS[difficulty]

   bottles = random.randint(*config["bottles"])
   capacity = random.randint(*config["capacity"])
   num_empty_bottles = 2
   colors = bottles - num_empty_bottles

   units = [c for c in range(1, colors + 1) for _ in range(capacity)]
   random.shuffle(units)

   filled = [units[i * capacity:(i + 1) * capacity] for i in range(colors)]
   empty_bottles = [[] for _ in range(num_empty_bottles)]
   all_bottles = filled + empty_bottles

   color_map = {i + 1: COLOR_NAMES[i] for i in range(colors)}

   return GameState(all_bottles, capacity, color_map=color_map)