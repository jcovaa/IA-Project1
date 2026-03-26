import pygame
from src.main import rand_bottles, solve
from .components import Button, DifficultySelector
from .draw_bottles import draw_bottles
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
    btn_generate = Button(x=panel_x + 20, y=225, width=160, heigth=45, text="Generate", color=(50, 100, 180), hover_color=(70, 130, 210))

    #game setup
    # provisorio 
    current_difficulty = "easy"
    game_state = generate_puzzle(current_difficulty, seed=42)
    #solve # dar opçoes

    running = True

    #animating = False # para ter animações das bootles, if false desenhar bottles no estado autual
    #animation_data = None

    #Meter todas as checkboxs aqui pre defenidas e cria las abaixo

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        
            #if event.type == pygame.MOUSEBUTTONDOWN and not animating:
            #    bottles = pour(bottles) 

            selector.handle_click(event)

            if btn_generate.is_clicked(event):
                current_difficulty = selector.selected
                game_state = generate_puzzle(current_difficulty)

        # if animating:
            #fazer animaçoes
            
        screen.fill((30, 30, 30)) 
        draw_bottles(screen, game_state, x_start=60, y_start=200, difficulty=current_difficulty)

        draw_panel(screen, panel_x)
        selector.draw(screen)
        btn_generate.draw(screen)

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()