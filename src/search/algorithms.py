# File containing all the search algorithms for the game
from collections import deque
from .node import TreeNode


def breadth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = deque([root])  # initialize the queue to store the nodes
    visited = set()
    stats = {"states_visited": 0}

    while queue:
        node = queue.popleft()  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, _ in operators_func(node.state):  # go through next states
        # create tree node with the new state
            state_node = TreeNode(state)

            # link child node to its parent in the tree
            node.add_child(state_node)

            # enqueue the child node
            queue.append(state_node)

    return None, stats


def depth_first_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    stack = [root]
    visited = set()
    stats = {"states_visited": 0}

    while stack:
        node = stack.pop()
        if goal_state_func(node.state):
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, _ in operators_func(node.state):
            state_node = TreeNode(state)
            node.add_child(state_node)
            stack.append(state_node)

    return None, stats


def depth_limited_search(initial_state, goal_state_func, operators_func, depth_limit):
    root = TreeNode(initial_state)
    stack = [(root, 0)]
    stats = {"states_visited": 0}

    while stack:
        node, depth = stack.pop()

        if goal_state_func(node.state):
            return node, stats

        # counts every pop, including revisits
        stats["states_visited"] += 1

        if depth < depth_limit:
            for state, _ in operators_func(node.state):
                state_node = TreeNode(state)
                node.add_child(state_node)
                stack.append((state_node, depth + 1))

    return None, stats


def iterative_deepening_search(initial_state, goal_state_func, operators_func, depth_limit):
    total_stats = {"states_visited": 0}
    for depth in range(depth_limit):
        goal, stats = depth_limited_search(initial_state, goal_state_func, operators_func, depth)
        total_stats["states_visited"] += stats["states_visited"]
        if goal:
            return goal, total_stats

    return None, total_stats


def uniform_cost_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    queue = [(root, 0)]
    stats = {"states_visited": 0}

    visited = set()

    while queue:
        node, cost = queue.pop(0)
        if goal_state_func(node.state):
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, step_cost in operators_func(node.state):
            state_node = TreeNode(state)
            node.add_child(state_node)
            total_cost = cost + step_cost
            queue.append((state_node, total_cost))

        queue.sort(key=lambda x: x[1])

    return None, stats


def greedy_search(initial_state, goal_state_func, operators_func, heuristic_func):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [(root, heuristic_func(root.state))]  # initialize the queue to store the nodes
    stats = {"states_visited": 0}

    visited = set()

    while queue:
        (node, _) = queue.pop(0)  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, _ in operators_func(node.state):  # go through next states
            # create tree node with the new state
            tree = TreeNode(state, node)

            # link child node to its parent in the tree
            node.add_child(tree)

            # enqueue the child node
            queue.append((tree, heuristic_func(state)))

        # sort the queue by state heuristic value
        queue.sort(key=lambda x: x[1])

    return None, stats


def a_star_search(initial_state, goal_state_func, operators_func, heuristic_func):
    root = TreeNode(initial_state)  # create the root node in the search tree
    queue = [(root, heuristic_func(root.state))]  # initialize the queue to store the nodes
    stats = {"states_visited": 0}

    visited = set()

    while queue:

        (node, _) = queue.pop(0)
        if goal_state_func(node.state):  # check goal state
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, step_cost in operators_func(node.state):  # go through next states
            # create tree node with the new state
            tree = TreeNode(state, node)

            # link child node to its parent in the tree, including the operator cost
            node.add_child(tree)

            # enqueue the child node
            tree.cost = node.cost + step_cost

            cost = tree.cost + heuristic_func(state)

            queue.append((tree, cost))

        # sort the queue by state full cost (path cost + heuristic value)
        queue = sorted(queue, key=lambda x: x[1])

    return None, stats



# not tested
def weighted_a_star_search(initial_state, goal_state_func, operators_func, heuristic_func, weight):
    root = TreeNode(initial_state)
    queue = [(root, heuristic_func(root.state) * weight)]
    stats = {"states_visited": 0}

    visited = set()

    while queue:
        (node, _) = queue.pop(0)
        if goal_state_func(node.state):
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, step_cost in operators_func(node.state):
            tree = TreeNode(state, node)

            node.add_child(tree)

            tree.cost = node.cost + step_cost

            cost = tree.cost + weight * heuristic_func(state)

            queue.append((tree, cost))

        queue = sorted(queue, key=lambda x: x[1])

    return None, stats


def iterative_deepening_a_star_search(initial_state, goal_state_func, operators_func, heuristic_func):
    stats = {"states_visited": 0}

    def search(node, g, threshold):
        stats["states_visited"] += 1

        f = g + heuristic_func(node.state)
        if f > threshold:
            return None, f
        if goal_state_func(node.state):
            return node, f

        min_threshold = float("inf")
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
            return result, stats
        if new_threshold == float("inf"):
            return None, stats
        threshold = new_threshold

# not tested
def bidirectional_search(initial_state, goal_state, operators_func):
    if initial_state == goal_state:
        return TreeNode(initial_state), {"states_visited": 0}

    front_queue = deque([TreeNode(initial_state)])
    back_queue = deque([TreeNode(goal_state)])

    front_visited = {TreeNode(initial_state)}
    back_visited = {TreeNode(goal_state)}

    stats = {"states_visited": 0}

    while front_queue and back_queue:
        node = front_queue.popleft()
        stats["states_visited"] += 1

        for state, _ in operators_func(node.state):
            if state not in front_visited:
                tree = TreeNode(state)
                node.add_child(tree)
                front_visited.add(tree)
                front_queue.append(tree)

            if state in back_visited:
                return front_visited[state]

        node = back_queue.popleft()

        for state, _ in operators_func(node.state):
            if state not in back_visited:
                tree = TreeNode(state)
                node.add_child(tree)
                back_visited[state] = tree
                back_queue.append(tree)

            if state in front_visited:
                return front_visited[state]

    return None, stats


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