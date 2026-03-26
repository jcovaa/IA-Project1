import pygame

COLOR_RGB = {
    "red": (255, 0, 0),
    "green": (0, 255, 0),
    "blue": (0, 0, 255),
    "orange": (230, 140, 30),
    "yellow": (220, 210, 50),
    "purple": (150, 50, 200),
    "brown": (140, 90, 40),
    "white": (230, 230, 230),
    "pink": (230, 100, 160),
    "cyan": (50, 200, 210)
}

def draw_bottles(screen, game_state, x_start, y_start, bottle_width, bottle_heigth, spacing, difficulty=None, row_spacing=80):
    bottles = game_state.bottles
    capacity = game_state.capacity
    total_bottles = len(bottles)

    two_rows_layout = difficulty == "hard" and total_bottles > 1
    bottles_per_row = (total_bottles + 1) // 2 if two_rows_layout else total_bottles

    for i, bottle in enumerate(bottles):
        if two_rows_layout:
            row = 0 if i < bottles_per_row else 1
            col = i if row == 0 else i - bottles_per_row
            x = x_start + col * (bottle_width + spacing)
            y = y_start + row * (bottle_heigth + row_spacing)
        else:
            x = x_start + i * (bottle_width + spacing)
            y = y_start

        pygame.draw.ellipse(screen, (200, 200, 200), (x, y-10, bottle_width, 20), 3)
        pygame.draw.line(screen, (200, 200, 200), (x, y), (x, y + bottle_heigth), 3)
        pygame.draw.line(screen, (200, 200, 200), (x + bottle_width, y), (x + bottle_width, y + bottle_heigth), 3)
        pygame.draw.line(screen, (200, 200, 200), (x, y + bottle_heigth), (x + bottle_width, y + bottle_heigth), 3)

        for j, color_id in enumerate(bottle):
            color_name = game_state.color_map.get(color_id)
            rgb = COLOR_RGB.get(color_name, (120, 120, 120))
            block_height = bottle_heigth // capacity
            block_y = y + bottle_heigth - (j + 1) * block_height
            pygame.draw.rect(screen, rgb, (x+3, block_y+3, bottle_width-6, block_height-6))
