from game.state import GameState, pour, game_states


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

	# Try a single pour and show result
	result = pour(s, 0, 3)
	print("Result of pouring from bottle 0 to 3:")
	print(result[0] if result else result)

	print()

	# Show all immediate child states
	print("Immediate children of the initial state:")
	for child, _cost in game_states(s):
		print(child)


if __name__ == "__main__":
	main()

