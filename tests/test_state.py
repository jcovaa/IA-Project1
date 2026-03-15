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

   def test_hash(self):
      state1 = GameState([[1, 2], [2, 1], [], []], 3)
      state2 = GameState([[1, 2], [2, 1], [], []], 3)
      self.assertEqual(hash(state1), hash(state2))

   def test_str(self):
      expected_str = "GameState(bottles=[[1, 2, 1, 3], [2, 2, 1, 1], [3, 3, 2, 3], [], []], capacity=4)"
      self.assertEqual(str(self.state), expected_str)

   def test_pour_valid(self):
      result = pour(self.state, 0, 3)
      self.assertIsNotNone(result)
      new_state, cost = result
      self.assertEqual(cost, 1)
      self.assertEqual(new_state.bottles[0], [1, 2, 1])
      self.assertEqual(new_state.bottles[3], [3])

   def test_pour_invalid_same_bottle(self):
      self.assertIsNone(pour(self.state, 0, 0))
      
   def test_pour_source_empty(self):
      self.assertIsNone(pour(self.state, 3, 0))

   def test_pour_source_complete(self):
      state1 = GameState([[1, 1, 1, 1], [2, 2, 1, 1], [3, 3, 2, 3], [], []], 4)
      self.assertIsNone(pour(state1, 0, 3))

   def test_pour_color_mismatch(self):
      state1 = GameState([[1, 2, 1], [2, 2, 1, 1], [3, 3, 2, 3], [3], []], 4)
      self.assertIsNone(pour(state1, 1, 3))

   def test_pour_multiple_color(self):
      result = pour(self.state, 1, 4)
      self.assertIsNotNone(result)
      new_state, cost = result
      self.assertEqual(cost, 1)
      self.assertEqual(new_state.bottles[1], [2, 2])
      self.assertEqual(new_state.bottles[4], [1, 1])

   def test_is_goal_state(self):
      goal = GameState([[1, 1, 1, 1], [2, 2, 2, 2], [3, 3, 3, 3], [], []], 4)
      self.assertTrue(goal_state(goal))
   
   def test_is_goal_state_empty(self):
      empty_goal = GameState([[], [], [], [], []], 4)
      self.assertTrue(goal_state(empty_goal))

   def test_is_goal_state_mixed(self):
      mixed_goal = GameState([[], [2, 2, 2, 2], [3, 3, 3, 3], [], [1, 1, 1, 1]], 4)
      self.assertTrue(goal_state(mixed_goal))

   def test_is_not_goal_state(self):
      self.assertFalse(goal_state(self.state))
      

if __name__ == '__main__':
   unittest.main()
   