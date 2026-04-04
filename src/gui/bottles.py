import pygame
from .components import Bottle

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

def get_bottles(game_state, x_start, y_start, bottle_width, bottle_height, spacing, difficulty, row_spacing=80):
    total_bottles = len(game_state.bottles)
    two_rows_layout = difficulty == "hard" and total_bottles > 1
    bottles_per_row = (total_bottles + 1) // 2 if two_rows_layout else total_bottles

    bottles = []
    for i in range(total_bottles):
        if two_rows_layout:
            row = 0 if i < bottles_per_row else 1
            col = i if row == 0 else i - bottles_per_row
            x = x_start + col * (bottle_width + spacing)
            y = y_start + row * (bottle_height + row_spacing)
        else:
            x = x_start + i * (bottle_width + spacing)
            y = y_start
        bottles.append(Bottle(game_state.bottles[i],x, y, bottle_width, bottle_height, game_state.capacity, i))
    return bottles

def draw_bottles(screen, game_state, bottles, selected_bottle=None,jump_offset=0):

    for b in bottles:
        is_selected = (b.index == selected_bottle)
        #so aplica quando puzzle completo
        original_y = b.y
        b.y = original_y - jump_offset
        b.draw(screen, game_state, COLOR_RGB, is_selected)
        #restaura posiçao
        b.y = original_y


