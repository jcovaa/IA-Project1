import pygame
from src.main import rand_bottles, solve
from .draw_bottles import draw_bottles
from src.game.gameState import GameState, pour
import time

def main():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720)) # provsorio
    clock = pygame.time.Clock()
    running = True

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
    # provisorio 
    # #gerar diferentes dificuldades -> dar opçoes -> func para gerar que faça sentido
    bottles = rand_bottles(5,4) 
    capacity = 4

    state = GameState(bottles, capacity)

    #solve # dar opçoes

    animating = False # para ter animações das bootles, if false desenhar bottles no estado autual
    #animation_data = None

    #Meter todas as checkboxs aqui pre defenidas e cria las abaixo

    selected_bottle = None

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(len(state.bottles)):
                    x = x_start + i * (bottle_width + spacing)
                    y = y_start
                    if x <= mouse_x <= x + bottle_width and y <= mouse_y <= y + bottle_height:
                        if selected_bottle is None:
                            selected_bottle = i  
                        else:
                            result  = pour(state, selected_bottle, i) 
                            if result is not None:
                                state, _ = result
                                steps_count += 1
                            selected_bottle = None  
                        break
            

        # if animating:
            #fazer animaçoes

       

        screen.fill((30, 30, 30)) #?
        draw_bottles(screen, state.bottles, state.capacity, x_start, y_start, bottle_width, bottle_height, spacing)

        elapsed_time = int(time.time() - start_time)
        text = f"Time: {elapsed_time}s   Steps: {steps_count}"
        text_surface = font.render(text, True, (255, 255, 255))
        screen.blit(text_surface, (20, 20))

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()