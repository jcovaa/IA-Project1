import random
from game.gameState import GameState

DIFICULTY_CONFIGS = {
   "easy": {"bottles": 5, "capacity": 3, "colors": 3},
   "medium": {"bottles": 7, "capacity": 4, "colors": 5},
   "hard": {"bottles": 12, "capacity": 4, "colors": 10}
}

COLOR_NAMES = [
   "red", "blue", "green", "orange", "yellow", "purple", "brown", "white", "pink", "cyan"
]