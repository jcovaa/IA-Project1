# File containing all the search algorithms for the game
import heapq
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
            state_node = TreeNode(state, node)

            # link child node to its parent in the tree
            node.add_child(state_node, operator_cost=1)

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
            node.add_child(state_node, operator_cost=1)
            stack.append(state_node)

    return None, stats


def depth_limited_search(initial_state, goal_state_func, operators_func, limit):
    root = TreeNode(initial_state)
    stack = [(root, 0, {initial_state})] #aumenta muito a memoria, mas evita ciclos, rever
    stats = {"states_visited": 0, "cutoff": False}

    while stack:
        node, depth, path_visited = stack.pop()

        if goal_state_func(node.state):
            return node, stats

        # counts every pop, including revisits
        stats["states_visited"] += 1

        if depth < limit:
            for state, _ in operators_func(node.state):
                if state in path_visited:
                    continue
                state_node = TreeNode(state)
                node.add_child(state_node, operator_cost=1)
                stack.append((state_node, depth + 1, path_visited | {state}))
        else:
            stats["cutoff"] = True

    return None, stats


def iterative_deepening_search(initial_state, goal_state_func, operators_func, limit):
    total_stats = {"states_visited": 0, "cutoff": False}
    for depth in range(limit + 1):
        goal, stats = depth_limited_search(initial_state, goal_state_func, operators_func, depth)
        total_stats["states_visited"] += stats["states_visited"]
        total_stats["cutoff"] = total_stats["cutoff"] or stats["cutoff"]
        if goal:
            return goal, total_stats

    return None, total_stats


def uniform_cost_search(initial_state, goal_state_func, operators_func):
    root = TreeNode(initial_state)
    heap = [(0, id(root), root)]
    stats = {"states_visited": 0}

    visited = set()

    while heap:
        cost, _, node = heapq.heappop(heap)
        if goal_state_func(node.state):
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, step_cost in operators_func(node.state):
            state_node = TreeNode(state)
            node.add_child(state_node, operator_cost=step_cost)
            heapq.heappush(heap, (cost + step_cost, id(state_node), state_node))

    return None, stats


def greedy_search(initial_state, goal_state_func, operators_func, heuristic):
    root = TreeNode(initial_state)  # create the root node in the search tree
    h = heuristic(root.state)
    heap = [(h, id(root), root)]
    stats = {"states_visited": 0}

    visited = set()

    while heap:
        _, _, node = heapq.heappop(heap)  # get first element in the queue
        if goal_state_func(node.state):  # check goal state
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, _ in operators_func(node.state):  # go through next states
            tree = TreeNode(state, node)
            node.add_child(tree, operator_cost=1)
            heapq.heappush(heap, (heuristic(state), id(tree), tree))

    return None, stats


def a_star_search(initial_state, goal_state_func, operators_func, heuristic):
    root = TreeNode(initial_state)  # create the root node in the search tree
    h = heuristic(root.state)
    heap = [(h, id(root), root)]
    stats = {"states_visited": 0}

    visited = set()

    while heap:

        _, _, node = heapq.heappop(heap)  # get first element in the queue
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
            node.add_child(tree, operator_cost=step_cost)

            # enqueue the child node
            tree.cost = node.cost + step_cost

            f = tree.cost + heuristic(state)

            heapq.heappush(heap, (f, id(tree), tree))

    return None, stats



# not tested
def weighted_a_star_search(initial_state, goal_state_func, operators_func, heuristic, weight):
    root = TreeNode(initial_state)
    heap = [(heuristic(root.state) * weight, id(root), root)]
    stats = {"states_visited": 0}

    visited = set()

    while heap:
        _, _, node = heapq.heappop(heap)
        if goal_state_func(node.state):
            return node, stats

        if node.state in visited:
            continue

        visited.add(node.state)
        stats["states_visited"] += 1

        for state, step_cost in operators_func(node.state):
            tree = TreeNode(state, node)

            node.add_child(tree, operator_cost=step_cost)

            tree.cost = node.cost + step_cost

            f = tree.cost + weight * heuristic(state)

            heapq.heappush(heap, (f, id(tree), tree))

    return None, stats


def iterative_deepening_a_star_search(initial_state, goal_state_func, operators_func, heuristic):
    stats = {"states_visited": 0}

    def search(node, g, threshold, path_visited):
        f = g + heuristic(node.state)
        if f > threshold:
            return None, f
        if goal_state_func(node.state):
            return node, f

        stats["states_visited"] += 1
        min_threshold = float("inf")

        for state, step_cost in operators_func(node.state):
            if state in path_visited:
                continue

            child = TreeNode(state, node)
            node.add_child(child, operator_cost=step_cost)
            path_visited.add(state)
            result, new_f = search(child, g + step_cost, threshold, path_visited)
            path_visited.remove(state)
            if result:
                return result, new_f
            min_threshold = min(min_threshold, new_f)

        return None, min_threshold

    root = TreeNode(initial_state)
    threshold = heuristic(root.state)

    while True:
        path_visited = {initial_state}
        result, new_threshold = search(root, 0, threshold, path_visited)
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