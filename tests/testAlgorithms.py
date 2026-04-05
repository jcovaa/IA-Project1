import unittest
import init
import src.search.algorithms as alg

class TestAlgorithms(unittest.TestCase):
   def setUp(self):
      self.initial_state = "initial"
      self.goal_state = "goal"

      # Simple goal function
      self.goal_state_func = lambda state: state == self.goal_state

      # Simple operators function
      self.operators_func = lambda state: [(self.goal_state, 1)] if state == self.initial_state else []
   
   def test_breadth_first_search(self):
      result = alg.breadth_first_search(self.initial_state, self.goal_state_func, self.operators_func)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_breadth_first_search(self):
      result = alg.depth_first_search(self.initial_state, self.goal_state_func, self.operators_func)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_depth_limited_search(self):
      result = alg.depth_limited_search(self.initial_state, self.goal_state_func, self.operators_func, depth_limit=5)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_iterative_deepening_search(self):
      result = alg.iterative_deepening_search(self.initial_state, self.goal_state_func, self.operators_func, depth_limit=5)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_uniform_cost_search(self):
      result = alg.uniform_cost_search(self.initial_state, self.goal_state_func, self.operators_func)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_greedy_best_first_search(self):
      result = alg.greedy_search(self.initial_state, self.goal_state_func, self.operators_func, heuristic_func=lambda state: 0)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_a_star_search(self):
      result = alg.a_star_search(self.initial_state, self.goal_state_func, self.operators_func, heuristic_func=lambda state: 0)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_weighted_a_star_search(self):
      result = alg.weighted_a_star_search(self.initial_state, self.goal_state_func, self.operators_func, heuristic_func=lambda state: 0, weight=2)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

   def test_iterative_deepening_a_star_search(self):
      result = alg.iterative_deepening_a_star_search(self.initial_state, self.goal_state_func, self.operators_func, heuristic_func=lambda state: 0, depth_limit=5)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)

