# A generic definition of a tree node holding a state of the problem
class TreeNode:
   def __init__(self, state, parent=None):
      self.state = state
      self.parent = parent
      self.children = []
      self.cost = 0  # the path cost to get to this state

   def add_child(self, child_node, operator_cost=0):
      self.children.append(child_node)
      child_node.cost = self.cost + operator_cost # the path cost is the parent's cost plus this operator cost
      child_node.parent = self
