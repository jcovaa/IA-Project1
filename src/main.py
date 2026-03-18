from game.gameState import GameState, pour, game_states, goal_state
from search.algorithms import breadth_first_search, depth_first_search, depth_limited_search, iterative_deepening_search, greedy_search, a_star_search

def print_solution(node):
    path = []
    current = node
    while current:
        path.append(current.state)
        current = current.parent

    for state in reversed(path):
        print(state)
        
def main():
	# Example starting bottles (each list: bottom -> top)
	bottles = [
		[1, 2, 1],
		[2, 2, 1],
		[3, 3, 2],
		[],
		[]
	]
	capacity = 3

	s = GameState(bottles, capacity)
	print("Initial state:")
	print(s)

	print()

	goal_bfs = breadth_first_search(s, goal_state, game_states)
	print("BFS solution")
	print_solution(goal_bfs)
      
	goal_dfs = depth_first_search(s, goal_state, game_states)
	print("DFS solution")
	print_solution(goal_dfs)

	goal_dls = depth_limited_search(s, goal_state, game_states, depth_limit=10)
	print("DLS solution")
	print_solution(goal_dls)

	goal_ids = iterative_deepening_search(s, goal_state, game_states, depth_limit=10)
	print("IDS solution")
	print_solution(goal_ids)


if __name__ == "__main__":
	main()

