import pygame
from src.main import rand_bottles, solve
from .draw_bottles import draw_bottles
def main():

    # pygame setup
    pygame.init()
    screen = pygame.display.set_mode((1280, 720)) # provsorio
    clock = pygame.time.Clock()
    running = True

    #game setup
    # provisorio 
    # #gerar diferentes dificuldades -> dar opçoes -> func para gerar que faça sentido
    bottles = rand_bottles(5,4) 
    capacity = 4
    #solve # dar opçoes

    animating = False # para ter animações das bootles, if false desenhar bottles no estado autual
    animation_data = None

    #Meter todas as checkboxs aqui pre defenidas e cria las abaixo

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False        
            #if event.type == pygame.MOUSEBUTTONDOWN and not animating:
            #    bottles = pour(bottles) 

        # if animating:
            #fazer animaçoes
            
        screen.fill((30, 30, 30)) 
        draw_bottles(screen, bottles, capacity)

        pygame.display.flip()

        clock.tick(60)  # limits FPS to 60

    pygame.quit()

if __name__ == "__main__":
    main()