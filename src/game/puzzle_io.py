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
      parts = line.split(':')[1].strip()
      bottle = list(map(int, parts.split())) if parts else []
      bottles.append(bottle)

   return GameState(bottles, capacity)