from .game.gameState import game_states, goal_state
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

def solve(func, state):

	goal = func(state, goal_state, game_states) # temos q adaptar para cada tipo de funçao pq ha funçoes que exigem mais coisas
    
	return goal.state

#def calc_time



if __name__ == "__main__":
    solve()
