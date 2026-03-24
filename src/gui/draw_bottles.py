import pygame
import random

# AI function
def generate_colors(n):
    random.seed(42)  # Para resultados reprodutíveis, pode remover se quiser aleatório sempre
    colors = []
    for i in range(n):
        hue = i / n
        r = int(255 * (1 + random.uniform(-0.2, 0.2)) * hue) % 256
        g = int(255 * (1 + random.uniform(-0.2, 0.2)) * (1 - hue)) % 256
        b = int(255 * (1 + random.uniform(-0.2, 0.2)) * (0.5 + hue/2)) % 256
        colors.append((r, g, b))
    return colors

# AI function
def draw_bottles(screen, bottles, capacity, x_start=100, y_start=100, bottle_width=60, bottle_height=200, spacing=40):

    colors = generate_colors(len(bottles) -2)
    for i, bottle in enumerate(bottles):
        x = x_start + i * (bottle_width + spacing)
        y = y_start

        #Tubo
        pygame.draw.ellipse(screen, (200, 200, 200), (x, y-10, bottle_width, 20), 3)
        pygame.draw.line(screen, (200, 200, 200), (x, y), (x, y + bottle_height), 3) 
        pygame.draw.line(screen, (200, 200, 200), (x + bottle_width, y), (x + bottle_width, y + bottle_height), 3)
        pygame.draw.line(screen, (200, 200, 200), (x, y + bottle_height), (x + bottle_width, y + bottle_height), 3) 

        for j, color_id in enumerate(reversed(bottle)):
            if color_id == 0:
                continue
            block_height = bottle_height // capacity
            block_y = y + bottle_height - (j + 1) * block_height
            pygame.draw.rect(screen, colors[color_id -1], (x+3, block_y+3, bottle_width-6, block_height-6)) # da para melhorar