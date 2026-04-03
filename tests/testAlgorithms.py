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

   def assert_stats(self, stats):
      self.assertIsInstance(stats, dict)
      self.assertIn("states_visited", stats)
      self.assertIsInstance(stats["states_visited"], int)
      self.assertGreaterEqual(stats["states_visited"], 0)

   def test_breadth_first_search(self):
      result, stats = alg.breadth_first_search(self.initial_state, self.goal_state_func, self.operators_func)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_depth_first_search(self):
      result, stats = alg.depth_first_search(self.initial_state, self.goal_state_func, self.operators_func)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_depth_limited_search(self):
      result, stats = alg.depth_limited_search(
         self.initial_state,
         self.goal_state_func,
         self.operators_func,
         depth_limit=5,
      )
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_iterative_deepening_search(self):
      result, stats = alg.iterative_deepening_search(
         self.initial_state,
         self.goal_state_func,
         self.operators_func,
         depth_limit=5,
      )
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_uniform_cost_search(self):
      result, stats = alg.uniform_cost_search(self.initial_state, self.goal_state_func, self.operators_func)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_greedy_best_first_search(self):
      result, stats = alg.greedy_search(
         self.initial_state,
         self.goal_state_func,
         self.operators_func,
         heuristic_func=lambda state: 0,
      )
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_a_star_search(self):
      result, stats = alg.a_star_search(
         self.initial_state,
         self.goal_state_func,
         self.operators_func,
         heuristic_func=lambda state: 0,
      )
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_weighted_a_star_search(self):
      result, stats = alg.weighted_a_star_search(
         self.initial_state,
         self.goal_state_func,
         self.operators_func,
         heuristic_func=lambda state: 0,
         weight=2,
      )
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   def test_iterative_deepening_a_star_search(self):
      result, stats = alg.iterative_deepening_a_star_search(
         self.initial_state,
         self.goal_state_func,
         self.operators_func,
         heuristic_func=lambda state: 0,
      )
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)

   @unittest.skip("bidirectional_search not implemented yet")
   def test_bidirectional_search(self):
      result, stats = alg.bidirectional_search(self.initial_state, self.goal_state, self.operators_func)
      self.assertIsNotNone(result)
      self.assertEqual(result.state, self.goal_state)
      self.assert_stats(stats)
