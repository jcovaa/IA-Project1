import unittest
import init
from src.game.state import GameState, pour, game_states, goal_state

class TestGameState(unittest.TestCase):

   def setUp(self):
      self.bottles = [[1, 2, 1, 3], [2, 2, 1, 1], [3, 3, 2, 3], [], []]
      self.capacity = 4
      self.state = GameState(self.bottles, self.capacity)

   def test_init(self):
      self.assertEqual(self.state.bottles, self.bottles)
      self.assertEqual(self.state.capacity, self.capacity)
   
   def test_equality(self):
      state1 = GameState([[1, 2], [2, 1], [], []], 3)
      state2 = GameState([[1, 2], [2, 1], [], []], 3)
      self.assertEqual(state1, state2)

if __name__ == '__main__':
   unittest.main()
   