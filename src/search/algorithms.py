# File containing all the search algorithms for the game
from collections import deque
from .node import TreeNode

def breadth_first_search(initial_state, goal_state_func, operators_func):
   root = TreeNode(initial_state)   # create the root node in the search tree
   queue = deque([root])   # initialize the queue to store the nodes
   visited = set()

   while queue:
         node = queue.popleft()   # get first element in the queue
         if goal_state_func(node.state):   # check goal state
            return node
         
         if node.state in visited:
            continue

         visited.add(node.state)

         for state, _ in operators_func(node.state):   # go through next states
            # create tree node with the new state
            state_node = TreeNode(state)

            # link child node to its parent in the tree
            node.add_child(state_node)


            # enqueue the child node
            queue.append(state_node)


   return None

def depth_first_search(initial_state, goal_state_func, operators_func):
   root = TreeNode(initial_state)
   stack = [root]
   visited = set()

   while stack:
      node = stack.pop()
      if goal_state_func(node.state):
         return node

      if node.state in visited:
         continue

      visited.add(node.state)

      for state, _ in operators_func(node.state):
         state_node = TreeNode(state)
         node.add_child(state_node)
         stack.append(state_node)

   return None

def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)
    stack = [(root, 0)]

    while stack:
        node, depth = stack.pop()

        if goal_state_func(node.state):
            return node

        if depth < depth_limit:
            for state, _ in operators_func(node.state):
                state_node = TreeNode(state)
                node.add_child(state_node)
                stack.append((state_node, depth + 1))

    return None

def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit):
   for depth in range(depth_limit):
      goal = depth_limited_search(initial_state, goal_state_func, operators_func, depth)
      if goal:
         return goal

   return None

def uniform_cost_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    queue = [(root, 0)]

    visited = set()

    while queue:
        node, cost = queue.pop(0)
        if goal_state_func(node.state):
            return node

        if node.state in visited:
            continue
        
        visited.add(node.state)
        
        for state, step_cost in operators_func(node.state):
            state_node = TreeNode(state)
            node.add_child(state_node)
            total_cost = cost + step_cost
            queue.append((state_node, total_cost))
        
        queue.sort(key=lambda x: x[1])

    return None

def greedy_search(initial_state, goal_state_func, operators_func, heuristic_func):
   root = TreeNode(initial_state)   # create the root node in the search tree
   queue = [(root, heuristic_func(root.state))]   # initialize the queue to store the nodes

   visited = set()

   while queue:
      (node, _) = queue.pop(0)   # get first element in the queue
      if goal_state_func(node.state):   # check goal state
         return node

      if node.state in visited:
         continue

      visited.add(node.state)

      for state, _ in operators_func(node.state):   # go through next states
         # create tree node with the new state
         tree = TreeNode(state,node)

         # link child node to its parent in the tree
         node.add_child(tree)

         # enqueue the child node
         queue.append((tree, heuristic_func(state))) 

      # sort the queue by state heuristic value
      queue.sort(key=lambda x: x[1])

   return None

def a_star_search(initial_state, goal_state_func, operators_func, heuristic_func):
   root = TreeNode(initial_state)   # create the root node in the search tree
   queue = [(root, heuristic_func(root.state))]   # initialize the queue to store the nodes

   visited = set()

   while queue:

      (node, _) = queue.pop(0)
      if goal_state_func(node.state):   # check goal state
         return node

      if node.state in visited:
         continue

      visited.add(node.state)

      for state, step_cost in operators_func(node.state):   # go through next states
         # create tree node with the new state
         tree = TreeNode(state,node)

         # link child node to its parent in the tree, including the operator cost
         node.add_child(tree)

         # enqueue the child node
         tree.cost = node.cost + step_cost

         cost = tree.cost + heuristic_func(state)

         queue.append((tree, cost))

      # sort the queue by state full cost (path cost + heuristic value)
      queue = sorted(queue, key=lambda x: x[1])

   return None

def weighted_a_star_search(initial_state, goal_state_func, operators_func, heuristic_func, weight):
    root = TreeNode(initial_state)
    queue = [(root, heuristic_func(root.state) * weight)]

    visited = set()

    while queue:
        
        (node, _) = queue.pop(0)
        if goal_state_func(node.state):
            return node

        if node.state in visited:
            continue

        visited.add(node.state)

        for state, step_cost in operators_func(node.state):
            
            tree = TreeNode(state, node)

            node.add_child(tree)
            
            tree.cost = node.cost + step_cost

            cost = tree.cost + weight * heuristic_func(state)

            queue.append((tree, cost))

        queue = sorted(queue, key=lambda x: x[1])

    return None

def iterative_deepening_a_star_search(initial_state, goal_state_func, operators_func, heuristic_func):
    def search(node, g, threshold):
        f = g + heuristic_func(node.state)
        if f > threshold:
            return f
        if goal_state_func(node.state):
            return node, f
        
        min_threshold = float('inf')
        for state, step_cost in operators_func(node.state):
            child = TreeNode(state, node)
            node.add_child(child)
            result, new_f = search(child, g + step_cost, threshold)
            if result:
                return result, new_f
            min_threshold = min(min_threshold, new_f)
        
        return None, min_threshold
    
    root = TreeNode(initial_state)
    threshold = heuristic_func(root.state)

    while True:
        result, new_threshold = search(root, 0, threshold)
        if result:
            return result
        if new_threshold == float('inf'):
            return None
        threshold = new_threshold


def heuristic1(state):
    score = 0
    for bottle in state.bottles:
        if not bottle:
            continue
        if len(bottle) != state.capacity or len(set(bottle)) != 1:
            score += 1
    return score

def heuristic2(state):
    score = 0
    for bottle in state.bottles:
        if not bottle:
            continue
        top_color = bottle[-1]
        for color in bottle:
            if color != top_color:
                score += 1
    return score

def heuristic3(state):
    score = 0
    for bottle in state.bottles:
        if not bottle:
            continue
        
        # penaliza mistura
        score += len(set(bottle)) - 1
        
        # penaliza não estar cheia
        if len(bottle) != state.capacity:
            score += 1

    return score

def heuristic4(state):
    score = 0
    for bottle in state.bottles:
        if not bottle:
            continue
        if len(set(bottle)) == 1 and len(bottle) == state.capacity:
            continue

        groups = 1
        for k in range(1, len(bottle)):
            if bottle[k] != bottle[k - 1]:
                groups += 1
        score += groups - 1
    
    return score