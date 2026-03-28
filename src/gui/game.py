import pygame
from src.main import rand_bottles, solve
from .components import Button, DifficultySelector
from .bottles import draw_bottles, get_bottles
from src.game.gameState import GameState, pour
import time
from src.puzzle_generator import generate_puzzle

SCREEN_W, SCREEN_H = 1280, 720
PANEL_W = 200

def draw_panel(screen, panel_x):
    pygame.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_W, SCREEN_H))
    pygame.draw.line(screen, (80, 80, 80), (panel_x, 0), (panel_x, SCREEN_H), 2)

def main():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H)) # provsorio
    pygame.display.set_caption("Water Sort Puzzle")
    clock = pygame.time.Clock()

    panel_x = SCREEN_W - PANEL_W
    selector = DifficultySelector(x=panel_x + 20, y=20)
    btn_generate = Button(x=panel_x + 20, y=225, width=160, height=45, text="Generate", color=(50, 100, 180), hover_color=(70, 130, 210))

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

    #animating = False # para ter animações das bootles, if false desenhar bottles no estado autual
    #animation_data = None

    #Meter todas as checkboxs aqui pre defenidas e cria las abaixo


    while running:
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

        # if animating:
            #fazer animaçoes

        screen.fill((30, 30, 30)) #?
        draw_bottles(screen, game_state, bottles, selected_bottle)

        draw_panel(screen, panel_x)
        selector.draw(screen)
        btn_generate.draw(screen)

        elapsed_time = int(time.time() - start_time)
        text = f"Time: {elapsed_time}s   Steps: {steps_count}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()