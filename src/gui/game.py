import pygame
import os
import queue
import threading
from .components import Button, DifficultySelector, Dropdown, InputBox, Confetti
from .bottles import draw_bottles, get_bottles
from src.game.gameState import pour, solution, goal_state, game_states, has_possible_moves, calculate_score
import time
from src.puzzle_generator import generate_puzzle
import math
from .draw import draw_panel, draw_win_screen
from src.benchmark import benchmark
from src.game.puzzle_io import load_level_file, save_solver_results
from src.game.solver_metrics import build_solver_result, run_solver, build_solver

from src.search.algorithms import (
    breadth_first_search,
    depth_first_search,
    depth_limited_search,
    iterative_deepening_search,
    uniform_cost_search,
    greedy_search,
    a_star_search,
    weighted_a_star_search,
    iterative_deepening_a_star_search,
    heuristic1,
    heuristic2,
    heuristic3,
    heuristic4
)

SCREEN_W, SCREEN_H = 1280, 720
PANEL_W = 200

algorithms_map = {
    "BFS": breadth_first_search,
    "DFS": depth_first_search, 
    "DLS": depth_limited_search,
    "IDS": iterative_deepening_search,
    "UCS": uniform_cost_search,
    "Greedy": greedy_search,
    "A*": a_star_search,
    "Weighted A*": weighted_a_star_search,
    "IDA*": iterative_deepening_a_star_search,
}

#melhorar nomes
heuristics_map = {
    "Heuristic 1": heuristic1,
    "Heuristic 2": heuristic2,
    "Heuristic 3": heuristic3,
    "Heuristic 4": heuristic4
} 


def game():

    # pygame setup 
    pygame.init() #passar para a main
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H)) # provsorio
    pygame.display.set_caption("Water Sort Puzzle")
    clock = pygame.time.Clock()

    algorithms = list(algorithms_map.keys())
    heuristics = list(heuristics_map.keys())


    #Painel
    panel_x = SCREEN_W - PANEL_W
    selector = DifficultySelector(x=panel_x + 20, y=20)
    btn_generate = Button(x=panel_x + 20, y=225, width=160, height=45, text="Generate level", color=(50, 100, 180), hover_color=(70, 130, 210)) # Mudar a posição do botão para baixo do selector de dificuldade, e mudar o texto para "Generate Puzzle" ou algo do tipo 
    btn_load = Button(x=panel_x + 20, y=280, width=160, height=45, text="Load level", color=(60, 130, 160), hover_color=(80, 160, 190))
    algorithms_dropdown = Dropdown(panel_x + 20, 335, 160, 40, algorithms)
    heuristics_dropdown = Dropdown(panel_x + 20, 385, 160, 40, heuristics)
    solve_button = Button(x=panel_x + 20, y=600, width=160, height=45, text="Solve", color=(50, 180, 50), hover_color=(70, 210, 70))
    return_btn = Button(x=panel_x + 20, y=650, width=160, height=45, text="Return", color=(180, 50, 50), hover_color=(210, 70, 70)) 
    hint_btn = Button(x=panel_x + 20, y=550, width=160, height=45, text="Hint", color=(200, 180, 50), hover_color=(220, 210, 70))
    btn_next_move = Button(x=panel_x + 110, y=20, width=80, height=80, text=">", color=(50, 180, 50), hover_color=(70, 210, 70)) 
    btm_prev_move = Button(x=panel_x + 20, y=20, width=80, height=80, text="<", color=(50, 180, 50), hover_color=(70, 210, 70))
    weight_input = InputBox(panel_x + 20, 435, 160, 45, placeholder="Weight")
    limit_input = InputBox(panel_x + 20, 435, 160, 45, placeholder="Limit")
    benchmark_btn = Button(x=panel_x + 20, y=490, width=160, height=45, text="Benchmark", color=(100, 100, 200), hover_color=(120, 120, 220))
    save_results_btn = Button(x=SCREEN_W // 2 - 90, y=SCREEN_H // 2 + 130, width=180, height=45, text="Save results", color=(50, 120, 180), hover_color=(70, 150, 210))
    
    #valores provisorios bottles - por macro
    x_start = 100
    y_start = 100
    bottle_width = 60
    bottle_height = 200
    spacing = 40

    #Game Setup - confirmar se é tudo resetado sempre
    #Geral
    running = True
    current_difficulty = "easy"
    game_state = generate_puzzle(current_difficulty, seed=42)
    bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
    #Control state
    puzzle_solved = False
    puzzle_stuck=False
    timeout = False
    solution_path = []
    #Player mode
    selected_bottle = None
    #Computer mode
    solving = False
    #Return state
    current_puzzle = game_state
    #Solver state
    current_move = 0
    #Dropdowns
    algorithm = None
    heuristic = None
    #Win Screeen - isto não devia estar aqui
    font_big = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 32)
    animation_time = 0
    confetti = Confetti()
    #Score
    start_time = time.time()
    final_time = None
    steps_count = 0
    font = pygame.font.SysFont(None, 36) #nao devia estar aqui
    #Benchmark
    benchmark_status_font = pygame.font.SysFont(None, 24)
    benchmark_running = False
    benchmark_status = ""
    benchmark_status_color = (210, 210, 210)
    benchmark_events = queue.Queue()
    benchmark_count = 1
    #solver results
    last_solver_result = None
    save_status = ""
    save_status_color = (210, 210, 210)
    #threading
    solver_result_queue = queue.Queue()
    solving_algo = False
    cancel_event = threading.Event()

    while running:
        
        #Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False    

            event_consumed = False #for overriding events in dropdowns and buttons

            #bottles
            if event.type == pygame.MOUSEBUTTONDOWN and not solving: 
                for bottle in bottles:
                    if bottle.handle_click(event):         
                        if selected_bottle is None:
                            selected_bottle = bottle.index
                        elif selected_bottle == bottle.index:
                            selected_bottle = None 
                        else:
                            result = pour(game_state, selected_bottle, bottle.index)
                            if result is not None:
                                game_state, _ = result
                                steps_count += 1
                                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                                if goal_state(game_state):
                                    puzzle_solved = True
                                    final_time = int(time.time() - start_time)
                                elif not has_possible_moves(game_state):
                                    puzzle_stuck = True
                            selected_bottle = None
                        break
            
            #difficulty
            selector.handle_click(event)

            #button generate
            if btn_generate.handle_click(event):
                current_difficulty = selector.selected
                game_state = generate_puzzle(current_difficulty)
                current_puzzle = game_state
                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                start_time = time.time()
                steps_count = 0
                selected_bottle = None
                solving = False
                solution_path = []
                current_move = 0
                puzzle_solved = False
                final_time = None
                puzzle_stuck=False
                animation_time = 0
                last_solver_result = None
                save_status = ""
                solving_algo = False
                solve_button.loading = False
                hint_btn.loading = False
                timeout = False
                cancel_event.set()
                cancel_event.clear()
                while not solver_result_queue.empty():
                    try: solver_result_queue.get_nowait()
                    except: pass

            if btn_load.handle_click(event):
                current_difficulty = selector.selected
                level_path = os.path.join(
                    os.path.dirname(os.path.dirname(__file__)),
                    "levels",
                    f"{current_difficulty}.txt",
                )

                try:
                    game_state = load_level_file(level_path)
                except Exception as exc:
                    benchmark_status = f"Load failed ({current_difficulty}): {exc}"
                    benchmark_status_color = (220, 120, 120)
                else:
                    current_puzzle = game_state
                    bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                    start_time = time.time()
                    steps_count = 0
                    selected_bottle = None
                    solving = False
                    solution_path = []
                    current_move = 0
                    puzzle_solved = False
                    final_time = None
                    puzzle_stuck = False
                    timeout = False
                    animation_time = 0
                    last_solver_result = None
                    save_status = ""
                    benchmark_status = f"Loaded {current_difficulty} level"
                    benchmark_status_color = (120, 220, 120)
                    solving_algo = False
                    solve_button.loading = False
                    hint_btn.loading = False
                    cancel_event.set()
                    cancel_event.clear()
                    while not solver_result_queue.empty():
                        try: solver_result_queue.get_nowait()
                        except: pass
                event_consumed = True
        
            #Buttons for computer mode
            if btm_prev_move.handle_click(event) and solving and current_move > 0:
                current_move -= 1
                game_state = solution_path[current_move]
                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
            
            if btn_next_move.handle_click(event) and solving and current_move < len(solution_path) - 1:
                current_move += 1
                game_state = solution_path[current_move]
                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                if goal_state(game_state):
                    puzzle_solved = True
                    final_time = int(time.time() - start_time)
                    steps_count = len(solution_path) - 1

            
            #Dropdown algorithm and heuristic selection
            if not event_consumed:
                if algorithms_dropdown.handle_click(event):
                    event_consumed = True
                algorithm = algorithms_dropdown.selected  

            if algorithm in ["A*", "Greedy", "Weighted A*", "IDA*",] and not event_consumed:
                heuristics_dropdown.handle_click(event)

            if algorithm in ["DLS", "IDS"] and not event_consumed:
                if limit_input.handle_event(event):
                    event_consumed = True

            if algorithm == "Weighted A*" and not event_consumed:
                if weight_input.handle_event(event):
                    event_consumed = True

            heuristic = heuristics_dropdown.selected
            
            #Hint button
            if hint_btn.handle_click(event) and not solving and not event_consumed and not puzzle_solved and not puzzle_stuck and not solving_algo:
                func = algorithms_map[algorithm]
                heuristic_func = heuristics_map.get(heuristic)
                hint_btn.loading = True
                solving_algo = True

                def run_hint_task():
                    solver_kwargs = build_solver(algorithm, heuristic_func, weight_input, limit_input)
                    sol, _, _, _ = run_solver(func, game_state, goal_state, game_states, solver_kwargs)
                    if not cancel_event.is_set():
                        solver_result_queue.put((sol,True))

                threading.Thread(target=run_hint_task, daemon=True).start()

                event_consumed = True

            #Solve button
            if solve_button.handle_click(event) and not event_consumed and not solving and not puzzle_solved and not puzzle_stuck and not solving_algo:
                timeout = False
                puzzle_stuck = False
                solving_algo = True
                solve_button.loading = True

                func = algorithms_map[algorithm]
                heuristic_func = heuristics_map.get(heuristic)
                heuristic_label = heuristic if algorithm in ["A*", "Greedy", "Weighted A*", "IDA*"] else "N/A"
                initial_snapshot = [list(b) for b in game_state.bottles]

                def run_solve_task():
                    
                    solver_kwargs = build_solver(algorithm, heuristic_func, weight_input, limit_input)
                    sol, stats, elapsed, memory_kb = run_solver(func, game_state, goal_state, game_states, solver_kwargs)
                    if not cancel_event.is_set():
                        solver_result_queue.put((sol, False, stats, elapsed, memory_kb, heuristic_label, initial_snapshot))

                threading.Thread(target=run_solve_task, daemon=True).start()

                event_consumed = True

            if save_results_btn.handle_click(event) and puzzle_solved:
                if last_solver_result and last_solver_result.get("solved"):
                    score = calculate_score(steps_count, final_time or 0, current_difficulty)
                    last_solver_result["score"] = score
                    filename = f"solver_result_{last_solver_result['algorithm'].replace(' ', '_').lower()}.txt"
                    output_path = os.path.join("doc", filename)
                    save_solver_results(last_solver_result, output_path)
                    save_status = f"Saved: {output_path}"
                    save_status_color = (120, 220, 120)
                else:
                    save_status = "No solver result available to save."
                    save_status_color = (220, 120, 120)

            #Return button
            if return_btn.handle_click(event) and not event_consumed:
                solving = False
                solution_path = []
                current_move = 0
                game_state = current_puzzle
                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                start_time = time.time()
                steps_count = 0
                puzzle_solved = False
                final_time = None
                puzzle_stuck=False
                timeout = False
                animation_time = 0
                save_status = ""
                event_consumed = True
                solving_algo = False
                solve_button.loading = False
                hint_btn.loading = False

                cancel_event.set()
                cancel_event.clear()
                while not solver_result_queue.empty():
                    try: solver_result_queue.get_nowait()
                    except: pass
                

            if benchmark_btn.handle_click(event) and not benchmark_running and not solving and not event_consumed and not solving_algo:
                benchmark_running = True
                benchmark_difficulty = selector.selected
                benchmark_btn.text = "Running..."
                benchmark_status = f"Benchmark running ({benchmark_difficulty})"
                benchmark_status_color = (220, 220, 120)

                output_path = os.path.join("doc", f"benchmark_{benchmark_difficulty}_{benchmark_count}.csv")
                benchmark_count += 1

                def run_benchmark_task():
                    try:
                        results = benchmark(difficulty=benchmark_difficulty, seed=42, output_file=output_path)
                        solved_count = sum(1 for row in results if row.get("solved"))
                        total_count = len(results)
                        benchmark_events.put((
                            "success",
                            f"Done: {solved_count}/{total_count} solved. Saved in {output_path}"
                        ))
                    except Exception as exc:
                        benchmark_events.put(("error", f"Benchmark failed: {exc}"))

                
                event_consumed = True

                threading.Thread(target=run_benchmark_task, daemon=True).start()


        while not solver_result_queue.empty():
            item = solver_result_queue.get_nowait()
            sol, is_hint = item[0], item[1]
            solving_algo = False
            solve_button.loading = False
            hint_btn.loading = False

            if not is_hint:
                _, _, stats, elapsed, memory_kb, heuristic_label, initial_snapshot = item

            if sol is False:
                timeout = True
                if not is_hint:
                    last_solver_result = build_solver_result(
                        algorithm=algorithm, heuristic=heuristic_label,
                        solved=False, status="Timeout",
                        elapsed=elapsed, memory_kb=memory_kb, stats=stats,
                        difficulty=current_difficulty,
                        initial_state=initial_snapshot,
                        final_state=[list(b) for b in game_state.bottles],
                    )
            elif sol is None:
                puzzle_stuck = True
                if not is_hint:
                    last_solver_result = build_solver_result(
                        algorithm=algorithm, heuristic=heuristic_label,
                        solved=False, status="Cutoff" if stats.get("cutoff") else "No",
                        elapsed=elapsed, memory_kb=memory_kb, stats=stats,
                        difficulty=current_difficulty,
                        initial_state=initial_snapshot,
                        final_state=[list(b) for b in game_state.bottles],
                    )
            else:
                solution_path = solution(sol)
                if is_hint:
                    game_state = solution_path[1] if len(solution_path) > 1 else game_state
                    bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                    if goal_state(game_state):
                        puzzle_solved = True
                        final_time = int(time.time() - start_time)
                        steps_count = len(solution_path) - 1
                else:
                    solving = True
                    last_solver_result = build_solver_result(
                        algorithm=algorithm, heuristic=heuristic_label,
                        solved=True, status="Yes",
                        elapsed=elapsed, memory_kb=memory_kb, stats=stats,
                        solution_steps=len(solution_path) - 1,
                        solution_cost=sol.cost,
                        difficulty=current_difficulty,
                        initial_state=initial_snapshot,
                        final_state=[list(b) for b in solution_path[-1].bottles],
                    )
                    save_status = ""

        while not benchmark_events.empty():
            status, message = benchmark_events.get_nowait()
            benchmark_running = False
            benchmark_btn.text = "Benchmark"
            benchmark_status = message
            benchmark_status_color = (120, 220, 120) if status == "success" else (220, 120, 120)

        #Draw
        screen.fill((30, 30, 30))

        jump_offset = 0
        if puzzle_solved:
            #animating bottles
            animation_time += 0.08
            jump_offset = int(abs(math.sin(animation_time)) * 12)
            
            if final_time is None:
                final_time = 0
            score = calculate_score(steps_count,final_time,current_difficulty)
            elapsed_time = final_time
            text = f"Time: {elapsed_time}s   Steps: {steps_count}"
            draw_win_screen(screen,font_big,font_small,steps_count,final_time,score,confetti)
            save_results_btn.draw(screen)
            if save_status:
                save_surface = benchmark_status_font.render(save_status, True, save_status_color)
                screen.blit(save_surface, save_surface.get_rect(center=(SCREEN_W // 2, SCREEN_H // 2 + 190)))
        elif not puzzle_solved:
            elapsed_time = int(time.time() - start_time)
            text = f"Time: {elapsed_time}s   Steps: {steps_count}"

        draw_bottles(screen, game_state, bottles, selected_bottle,jump_offset)

        #Always draw
        draw_panel(screen, panel_x)
        return_btn.draw(screen)
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))

        if not solving:
            solve_button.draw(screen)
            hint_btn.draw(screen)
            selector.draw(screen)
            btn_generate.draw(screen)
            btn_load.draw(screen)
            benchmark_btn.draw(screen)

            if benchmark_status:
                benchmark_surface = benchmark_status_font.render(benchmark_status, True, benchmark_status_color)
                screen.blit(benchmark_surface, (20, SCREEN_H - 30))
            
            if algorithm in ["DLS", "IDS"]:
                limit_input.draw(screen)
        
            if algorithm == "Weighted A*":
                weight_input.draw(screen)

            if algorithm in ["A*", "Greedy", "Weighted A*", "IDA*"]:
                heuristics_dropdown.draw(screen)

            algorithms_dropdown.draw(screen) 
        elif solving:
            btn_next_move.draw(screen)
            btm_prev_move.draw(screen)

        if puzzle_stuck: #melhorar maybe 
            stuck_text = font_big.render("No moves possible!",True,(255,80,80))
            screen.blit(stuck_text,stuck_text.get_rect(center=(SCREEN_W//2, 80)))

        if timeout:
            timeout_text = font_big.render("Timeout!",True,(255,80,80))
            screen.blit(timeout_text,timeout_text.get_rect(center=(SCREEN_W//2, 80)))
            
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()