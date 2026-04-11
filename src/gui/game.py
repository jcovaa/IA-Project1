import pygame
from .components import Button, DifficultySelector, Dropdown, InputBox, Confetti
from .bottles import draw_bottles, get_bottles
from src.game.gameState import pour, solve, solution, goal_state, has_possible_moves, run_solver, calculate_score, choose_best_heuristic_algorithm
import time
from src.puzzle_generator import generate_puzzle
import math
from .draw import draw_panel, draw_win_screen
import threading

from src.search.algorithms import (
    breadth_first_search,
    depth_first_search,
    depth_limited_search,
    iterative_deepening_search,
    greedy_search,
    a_star_search,
    weighted_a_star_search,
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
    "Greedy": greedy_search,
    "A*": a_star_search,
    "Weighted A*": weighted_a_star_search,
} # atualizar

#melhorar nomes
heuristics_map = {
    "Heuristic 1": heuristic1,
    "Heuristic 2": heuristic2,
    "Heuristic 3": heuristic3,
    "Heuristic 4": heuristic4
} 

def init_game():

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
    algorithms_dropdown = Dropdown(panel_x + 20, 300, 160, 40, algorithms)
    heuristics_dropdown = Dropdown(panel_x + 20, 350, 160, 40, heuristics)
    solve_button = Button(x=panel_x + 20, y=600, width=160, height=45, text="Solve", color=(50, 180, 50), hover_color=(70, 210, 70))
    return_btn = Button(x=panel_x + 20, y=650, width=160, height=45, text="Return", color=(180, 50, 50), hover_color=(210, 70, 70)) 
    hint_btn = Button(x=panel_x + 20, y=550, width=160, height=45, text="Hint", color=(200, 180, 50), hover_color=(220, 210, 70))
    btn_next_move = Button(x=panel_x + 110, y=20, width=80, height=80, text=">", color=(50, 180, 50), hover_color=(70, 210, 70)) 
    btm_prev_move = Button(x=panel_x + 20, y=20, width=80, height=80, text="<", color=(50, 180, 50), hover_color=(70, 210, 70))
    weight_input = InputBox(panel_x + 20, 400, 160, 45, placeholder="Weight")
    depth_limit_input = InputBox(panel_x + 20, 350, 160, 45, placeholder="Limit")
    
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
    best_result = choose_best_heuristic_algorithm(game_state)
    hint_count=0

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
            if btn_generate.is_clicked(event):
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
                hint_count=0

                computing_best = True
                state_copy = game_state
                def worker():
                    global best_result, computing_best
                    best_result = choose_best_heuristic_algorithm(state_copy)
                    computing_best = False
                    print(f"{best_result[0]}:{best_result[1]}:{best_result[2]}")

                threading.Thread(target=worker).start()
                
        
            #Buttons for computer mode
            if btm_prev_move.is_clicked(event) and solving and current_move > 0:
                current_move -= 1
                game_state = solution_path[current_move]
                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
            
            if btn_next_move.is_clicked(event) and solving and current_move < len(solution_path) - 1:
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


            if algorithm in ["A*", "Greedy", "Weighted A*"] and not event_consumed:
                if heuristics_dropdown.handle_click(event):
                    event_consumed = True

            if algorithm in ["DLS", "IDS"] and not event_consumed:
                if depth_limit_input.handle_event(event):
                    event_consumed = True

            if algorithm == "Weighted A*" and not event_consumed:
                if weight_input.handle_event(event):
                    event_consumed = True

            heuristic = heuristics_dropdown.selected
            
            #Hint button
            if hint_btn.is_clicked(event) and not solving and not event_consumed:
                func = algorithms_map[algorithm]
                heuristic_func = heuristics_map.get(heuristic)
            
                sol = run_solver(func, algorithm, game_state, heuristic_func, weight_input, depth_limit_input)

                if sol is not None:
                    solution_path = solution(sol) 
                    if len(solution_path) > 1:
                        game_state = solution_path[1]
                        steps_count += 1 
                        hint_count += 1
                    bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                    if goal_state(game_state):          
                        puzzle_solved = True
                        final_time = int(time.time() - start_time)
                else:
                    puzzle_stuck = True
                event_consumed = True

            #Solve button
            if solve_button.is_clicked(event) and not event_consumed:
                func = algorithms_map[algorithm]
                heuristic_func = heuristics_map.get(heuristic)

                sol = run_solver(func, algorithm, game_state, heuristic_func, weight_input, depth_limit_input)

                if(sol is not None):
                    solution_path = solution(sol)
                    solving = True
                else:
                    puzzle_stuck = True
                event_consumed = True

            #Return button
            if return_btn.is_clicked(event) and not event_consumed:
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
                animation_time = 0
                event_consumed = True
                hint_count=0

        #Draw
        screen.fill((30, 30, 30))

        jump_offset = 0
        if puzzle_solved:
            #animating bottles
            animation_time += 0.08
            jump_offset = int(abs(math.sin(animation_time)) * 12)
  
            if final_time is None:
                final_time = 0
            score = calculate_score(steps_count,final_time,best_result[2],hint_count)
            elapsed_time = final_time
            text = f"Time: {elapsed_time}s   Steps: {steps_count}"
            draw_win_screen(screen,font_big,font_small,steps_count,final_time,score,confetti)
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
            
            if algorithm in ["DLS", "IDS"]:
                depth_limit_input.draw(screen)
        
            if algorithm == "Weighted A*":
                weight_input.draw(screen)

            if algorithm in ["A*", "Greedy", "Weighted A*"]:
                heuristics_dropdown.draw(screen)

            algorithms_dropdown.draw(screen) 
        elif solving:
            btn_next_move.draw(screen)
            btm_prev_move.draw(screen)

        if puzzle_stuck: #melhorar maybe 
            stuck_text = font_big.render("No moves possible!",True,(255,80,80))
            screen.blit(stuck_text,stuck_text.get_rect(center=(SCREEN_W//2, 80)))
            
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()