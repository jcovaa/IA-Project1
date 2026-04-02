import pygame
from .components import Button, DifficultySelector, Dropdown, InputBox
from .bottles import draw_bottles, get_bottles
from src.game.gameState import pour, solve, solution, goal_state, has_possible_moves
import time
from src.puzzle_generator import generate_puzzle
import random, math

from src.search.algorithms import (
    breadth_first_search,
    depth_first_search,
    depth_limited_search,
    iterative_deepening_search,
    greedy_search,
    a_star_search,
    weighted_a_star_search,
    bidirectional_search,
    heuristic1,
    heuristic2,
    heuristic3,
    heuristic4
)

SCREEN_W, SCREEN_H = 1280, 720
PANEL_W = 200

def draw_panel(screen, panel_x):
    pygame.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_W, SCREEN_H))
    pygame.draw.line(screen, (80, 80, 80), (panel_x, 0), (panel_x, SCREEN_H), 2)

algorithms_map = {
    "BFS": breadth_first_search,
    "DFS": depth_first_search, 
    "DLS": depth_limited_search,
    "IDS": iterative_deepening_search,
    "Greedy": greedy_search,
    "A*": a_star_search,
    "Weighted A*": weighted_a_star_search,
    "Bidirectional": bidirectional_search
} # atualizar

#melhorar nomes
heuristics_map = {
    "Heuristic 1": heuristic1,
    "Heuristic 2": heuristic2,
    "Heuristic 3": heuristic3,
    "Heuristic 4": heuristic4
} 

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

def draw_win_screen(screen, font_big, font_small, steps, time_elapsed,score,confetti):

    confetti.update()
    confetti.draw(screen)

    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(170)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font_big.render("Puzzle Solved!", True, (255, 255, 255))
    stats = font_small.render(
        f"Steps: {steps}   Time: {time_elapsed}s",
        True,
        (220, 220, 220)
    )

    score_text = font_small.render(
        f"Score: {score}",
        True,
        (220,220,220)
    )

    hint = font_small.render(
        "Click Generate to play again",
        True,
        (180, 180, 180)
    )

    screen.blit(title, title.get_rect(center=(SCREEN_W//2, SCREEN_H//2 - 40)))
    screen.blit(stats, stats.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 10)))
    screen.blit(score_text,score_text.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 50)))
    screen.blit(hint, hint.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 90)))

def init_game():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H)) # provsorio
    pygame.display.set_caption("Water Sort Puzzle")
    clock = pygame.time.Clock() # contar o timer bem

    panel_x = SCREEN_W - PANEL_W
    selector = DifficultySelector(x=panel_x + 20, y=20)
    btn_generate = Button(x=panel_x + 20, y=225, width=160, height=45, text="Generate level", color=(50, 100, 180), hover_color=(70, 130, 210)) # Mudar a posição do botão para baixo do selector de dificuldade, e mudar o texto para "Generate Puzzle" ou algo do tipo
    
    algorithms = list(algorithms_map.keys())
    hueristics = list(heuristics_map.keys())

    #Painel
    algorithms_dropdown = Dropdown(panel_x + 20, 300, 160, 45, algorithms)
    heuristics_dropdown = Dropdown(panel_x + 20, 350, 160, 45, hueristics)
    solve_button = Button(x=panel_x + 20, y=600, width=160, height=45, text="Solve", color=(50, 180, 50), hover_color=(70, 210, 70))
    return_btn = Button(x=panel_x + 20, y=650, width=160, height=45, text="Return", color=(180, 50, 50), hover_color=(210, 70, 70)) 
    hint_btn = Button(x=panel_x + 20, y=550, width=160, height=45, text="Hint", color=(200, 180, 50), hover_color=(220, 210, 70))
    btn_next_move = Button(x=panel_x + 110, y=20, width=80, height=80, text=">", color=(50, 180, 50), hover_color=(70, 210, 70)) 
    btm_prev_move = Button(x=panel_x + 20, y=20, width=80, height=80, text="<", color=(50, 180, 50), hover_color=(70, 210, 70))
    weigt_input = InputBox(panel_x + 20, 400, 160, 45, placeholder="Weight")
    depth_limit_input = InputBox(panel_x + 20, 350, 160, 45, placeholder="Limit")
    
    #Score
    start_time = time.time()
    steps_count = 0
    font = pygame.font.SysFont(None, 36)

    #valores provisorios
    x_start = 100
    y_start = 100
    bottle_width = 60
    bottle_height = 200
    spacing = 40

    #tela de vitoria
    font_big = pygame.font.SysFont(None, 64)
    font_small = pygame.font.SysFont(None, 32)
    puzzle_solved = False
    final_time = None
    animation_time = 0
    confetti = Confetti()

    #game setup
    current_difficulty = "easy"
    game_state = generate_puzzle(current_difficulty, seed=42)

    running = True
    selected_bottle = None
    bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
    puzzle_stuck=False
    
    #Computer Mode
    solution_path = []
    solving = False
    current_move = 0
    algorithm = None
    heuristic = None
    current_puzzle = game_state

    #animating = False # para ter animações das bootles, if false desenhar bottles no estado autual
    #animation_data = None

    #Meter todas as checkboxs aqui pre defenidas e cria las abaixo


    while running:
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False      

            if event.type == pygame.MOUSEBUTTONDOWN and not solving: # se calhar mudar a mecanica para selecionar a garrafa e so aceitar quando acertar e se quero desistir de usar essa garrafa, clicar na mesma + ter algumacoisa a mostrar isso                
                for bottle in bottles:
                    if bottle.handle_click(event):         # usa o método da classe
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

            selector.handle_click(event)

            if btn_generate.is_clicked(event):
                current_difficulty = selector.selected
                game_state = generate_puzzle(current_difficulty)
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

            if return_btn.is_clicked(event):
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
            
            if hint_btn.is_clicked(event) and not solving:
                algorithm = algorithms_dropdown.selected
                func = algorithms_map[algorithm]

                heuristic = heuristics_dropdown.selected
                heuristic_func = heuristics_map.get(heuristic)

                if algorithm == "A*" or algorithm == "Greedy":
                    sol = solve(func, game_state, heuristic_func)
                elif algorithm == "Weighted A*":
                    sol = solve(func, game_state, heuristic_func=heuristic_func, weight=int(weigt_input.text or 2)) #deviamos por mandatory
                elif algorithm == "DLS" or algorithm == "IDS":
                    sol = solve(func, game_state, depth_limit=int(depth_limit_input.text or 10)) #deviamos por mandatory
                else:
                    sol = solve(func, game_state)

                """elif algorithm == "Bidirectional":
                    #temos q fazer uma func nova
                else: """

                solution_path = solution(sol) 
                game_state = solution_path[1] if len(solution_path) > 1 else game_state
                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)

            algorithms_dropdown.handle_click(event)
            algorithm = algorithms_dropdown.selected 
            

            if algorithm in ["A*", "Greedy", "Weighted A*"]:
                heuristics_dropdown.handle_click(event)

            if algorithm in ["DLS", "IDS"]:
                depth_limit_input.handle_event(event)

            if algorithm == "Weighted A*":
                weigt_input.handle_event(event)

            if solve_button.is_clicked(event):
                algorithm = algorithms_dropdown.selected
                func = algorithms_map[algorithm]

                heuristic = heuristics_dropdown.selected
                heuristic_func = heuristics_map.get(heuristic)

                if algorithm == "A*" or algorithm == "Greedy":
                    sol = solve(func, game_state, heuristic_func)
                elif algorithm == "Weighted A*":
                    sol = solve(func, game_state, heuristic_func=heuristic_func, weight=int(weigt_input.text or 2)) #deviamos por mandatory
                elif algorithm == "DLS" or algorithm == "IDS":
                    sol = solve(func, game_state, depth_limit=int(depth_limit_input.text or 10)) #deviamos por mandatory
                else:
                    sol = solve(func, game_state)

                """elif algorithm == "Bidirectional":
                    #temos q fazer uma func nova
                else: """

                solution_path = solution(sol) 
                solving = True

        # if animating:
            #fazer animaçoes

        screen.fill((30, 30, 30)) #?
        jump_offset = 0
        #animating bottles
        if puzzle_solved:
            animation_time += 0.08
            jump_offset = int(abs(math.sin(animation_time)) * 12)

        draw_bottles(screen, game_state, bottles, selected_bottle,jump_offset)

        draw_panel(screen, panel_x)
        return_btn.draw(screen)

        if not solving:
            solve_button.draw(screen)
            hint_btn.draw(screen)
            selector.draw(screen)
            btn_generate.draw(screen)
            
            if algorithm in ["DLS", "IDS"]:
                depth_limit_input.draw(screen)
        
            if algorithm == "Weighted A*":
                weigt_input.draw(screen)

            if algorithm in ["A*", "Greedy", "Weighted A*"]:
                heuristics_dropdown.draw(screen)

            algorithms_dropdown.draw(screen)

            

        #falta os restantes diferes de algoritmos
        
        if solving:
            btn_next_move.draw(screen)
            btm_prev_move.draw(screen)

        elapsed_time = int(time.time() - start_time)
        text = f"Time: {elapsed_time}s   Steps: {steps_count}"
        if not solving:
            text_surface = font.render(text, True, (255, 255, 255))
            screen.blit(text_surface, (20, 20))

        if puzzle_solved:
            if final_time is None:
                final_time = 0
            elapsed_time = final_time if puzzle_solved else int(time.time() - start_time) 
            score = calculate_score(steps_count,final_time,current_difficulty)
            draw_win_screen(screen,font_big,font_small,steps_count,elapsed_time,score,confetti)

        if puzzle_stuck:
            stuck_text = font_big.render(
                "No moves possible!",
                True,
                (255,80,80)
            )
            screen.blit(
                stuck_text,
                stuck_text.get_rect(center=(SCREEN_W//2, 80))
            )
            
        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()



# confettis
class Confetti:
    def __init__(self):
        self.particles = []
        for _ in range(120):
            self.particles.append({
                "x": random.randint(0, SCREEN_W),
                "y": random.randint(-SCREEN_H, 0),
                "speed": random.uniform(2, 5),
                "size": random.randint(4, 8),
                "color": random.choice([
                    (255,50,50),
                    (50,255,50),
                    (50,50,255),
                    (255,255,50),
                    (255,50,255),
                    (50,255,255)
                ])
            })

    def update(self):
        for p in self.particles:
            p["y"] += p["speed"]
            if p["y"] > SCREEN_H:
                p["y"] = random.randint(-50, -10)

    def draw(self, screen):
        for p in self.particles:
            pygame.draw.rect(
                screen,
                p["color"],
                (p["x"], p["y"], p["size"], p["size"])
            )