import pygame
from src.main import solution, rand_bottles, solve
from .components import Button, DifficultySelector, Dropdown
from .bottles import draw_bottles, get_bottles
from src.game.gameState import pour
import time
from src.puzzle_generator import generate_puzzle

from src.search.algorithms import (
    breadth_first_search,
    depth_first_search,
    depth_limited_search,
    iterative_deepening_search,
    greedy_search,
    a_star_search,
    weighted_a_star_search,
    bidirectional_search,
)


SCREEN_W, SCREEN_H = 1280, 720
PANEL_W = 200

def draw_panel(screen, panel_x):
    pygame.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_W, SCREEN_H))
    pygame.draw.line(screen, (80, 80, 80), (panel_x, 0), (panel_x, SCREEN_H), 2)

algorithms_map = {
    "BFS": breadth_first_search,
    "DFS": depth_first_search, 
} # atualizar

def main():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H)) # provsorio
    pygame.display.set_caption("Water Sort Puzzle")
    clock = pygame.time.Clock()

    panel_x = SCREEN_W - PANEL_W
    selector = DifficultySelector(x=panel_x + 20, y=20)
    btn_generate = Button(x=panel_x + 20, y=225, width=160, height=45, text="Generate", color=(50, 100, 180), hover_color=(70, 130, 210)) # Mudar a posição do botão para baixo do selector de dificuldade, e mudar o texto para "Generate Puzzle" ou algo do tipo
    
    algorithms = list(algorithms_map.keys())

    algorithms_dropdown = Dropdown(panel_x + 20, 300, 160, 45, algorithms)
    #heuristcis_dropdown = Dropdown(panel_x + 20, 300, 160, 45, algorithms, text="Solve with")
    solve_button = Button(x=panel_x + 20, y=400, width=160, height=45, text="Solve", color=(180, 50, 50), hover_color=(210, 70, 70))

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

    #game setup
    #provisorio 
    current_difficulty = "easy"
    game_state = generate_puzzle(current_difficulty, seed=42)
    #solve # dar opçoes

    running = True
    selected_bottle = None
    bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
    
    #Computer Mode
    solution_path = []
    solving = False
    current_move = 0
    last_move_time = 0

    #animating = False # para ter animações das bootles, if false desenhar bottles no estado autual
    #animation_data = None

    #Meter todas as checkboxs aqui pre defenidas e cria las abaixo


    while running:
        if solving and solution_path:
            now = time.time()
            if now - last_move_time >= 1 and current_move < len(solution_path):
                game_state = solution_path[current_move]
                bottles = get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, current_difficulty)
                current_move += 1
                last_move_time = now
            if current_move >= len(solution_path):
                solving = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False      

            if event.type == pygame.MOUSEBUTTONDOWN: # se calhar mudar a mecanica para selecionar a garrafa e so aceitar quando acertar e se quero desistir de usar essa garrafa, clicar na mesma + ter algumacoisa a mostrar isso                
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

            algorithms_dropdown.handle_click(event)

            if solve_button.is_clicked(event):
                algorithm = algorithms_dropdown.selected
                func = algorithms_map[algorithm]
                sol = solve(func, game_state)
                solution_path = solution(sol) 
                solving = True
               



        # if animating:
            #fazer animaçoes

        screen.fill((30, 30, 30)) #?
        draw_bottles(screen, game_state, bottles, selected_bottle)

        draw_panel(screen, panel_x)
        selector.draw(screen)
        btn_generate.draw(screen)
        algorithms_dropdown.draw(screen)
        solve_button.draw(screen)

        elapsed_time = int(time.time() - start_time)
        text = f"Time: {elapsed_time}s   Steps: {steps_count}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()