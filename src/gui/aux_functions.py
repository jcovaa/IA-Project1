from src.game.gameState import solve

def calculate_score(steps, time_elapsed, difficulty):

    difficulty_multiplier = {
        "easy": 1,
        "medium": 1.5,
        "hard": 2
    }

    base_score = 1000

    score = base_score \
        - (steps * 15) \
        - (time_elapsed * 2)

    return int(score * difficulty_multiplier[difficulty])

def run_solver(func, algorithm, game_state, heuristic_func, weight_input, depth_input):
    if algorithm in ("A*", "Greedy"):
        return solve(func, game_state, heuristic_func)
    elif algorithm == "Weighted A*":
        return solve(func, game_state, heuristic_func=heuristic_func, weight=int(weight_input.text or 2))
    elif algorithm in ("DLS", "IDS"):
        return solve(func, game_state, depth_limit=int(depth_input.text or 10))
    return solve(func, game_state)

    """elif algorithm == "Bidirectional":
                    #temos q fazer uma func nova
                else: """
