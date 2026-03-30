from game.gameState import GameState, game_states, goal_state
from search.algorithms import breadth_first_search
import random

def print_solution(node):
    path = []
    current = node
    while current:
        path.append(current.state)
        current = current.parent

    for state in reversed(path):
        print(state)

def rand_bottles(num_bottles,capacity):
    bottles = [[] for _ in range(num_bottles)]

    colors = []
    
    for color in range(1, num_bottles - 1):
        colors.extend([color] * capacity)
    random.shuffle(colors)

    idx = 0
    for i in range(num_bottles - 2):
        for j in range(capacity):
            bottles[i].append(colors[idx])
            idx += 1

    return bottles

def solve(func=None, state=None):
    if func is None:
        func = breadth_first_search

    if state is None:
        state = GameState(rand_bottles(num_bottles=5, capacity=4), capacity=4)

    goal = func(state, goal_state, game_states)
    if goal is None:
        return None

    return goal.state

#def calc_time



if __name__ == "__main__":
    solution = solve()
    if solution is None:
        print("No solution found.")
    else:
        print(solution)
