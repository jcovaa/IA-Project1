import unittest
import init
from src.search.node import TreeNode

class TestTreeNode(unittest.TestCase):
   def setUp(self):
      self.root_state = "root"
      self.child_state = "child"
      self.grandchild_state = "grandchild"

      self.root = TreeNode(self.root_state)
      self.child = TreeNode(self.child_state)
      self.grandchild = TreeNode(self.grandchild_state)

      self.root.add_child(self.child, operator_cost=5)
      self.child.add_child(self.grandchild, operator_cost=3)

   def test_init(self):
      self.assertEqual(self.root.state, self.root_state)
      self.assertEqual(self.child.state, self.child_state)
      self.assertEqual(self.grandchild.state, self.grandchild_state)
      self.assertIsNone(self.root.parent)

   def test_add_child(self):
      self.assertIn(self.child, self.root.children)
      self.assertEqual(self.child.parent, self.root)
      self.assertEqual(self.child.cost, 5)

      self.assertIn(self.grandchild, self.child.children)
      self.assertEqual(self.grandchild.parent, self.child)
      self.assertEqual(self.grandchild.cost, 8)