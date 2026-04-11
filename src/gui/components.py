import pygame
import random
import time

SCREEN_W, SCREEN_H = 1280, 720

class Button:

    def __init__(self, x, y, width, height, text, color=(70, 70, 70), hover_color=(100, 100, 100)):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = hover_color
        self.font = pygame.font.SysFont("Arial", 18)
        self.loading = False
        self._spinner_chars = ["◐", "◓", "◑", "◒"]

    def draw(self, screen):
        mouse = pygame.mouse.get_pos()
        color = self.hover_color if self.rect.collidepoint(mouse) and not self.loading else self.color
        pygame.draw.rect(screen, color, self.rect, border_radius=8)
        pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=8)

        if self.loading:
            spinner = self._spinner_chars[int(time.time() * 6) % 4]
            label = self.font.render(f"{spinner}", True, (255, 255, 255))
        else:
            label = self.font.render(self.text, True, (255, 255, 255))

        screen.blit(label, label.get_rect(center=self.rect.center))

    def handle_click(self, event):
        if self.loading:
            return False
        return event.type == pygame.MOUSEBUTTONDOWN and self.rect.collidepoint(event.pos)
   

class DifficultySelector:

    def __init__(self, x, y, width=160):
        self.options = ["easy", "medium", "hard"]
        self.selected = "easy"
        self.font = pygame.font.SysFont("Arial", 18)
        self.title_font = pygame.font.SysFont("Arial", 20, bold=True)
        self.x, self.y = x, y
        self.width = width
        self.buttons = {
            opt: pygame.Rect(x, y + 40 + i * 50, width, 38) for i, opt in enumerate(self.options)
        }

    def draw(self, screen):
        title = self.title_font.render("Difficulty", True, (220, 220, 220))
        screen.blit(title, (self.x, self.y))

        for opt, rect in self.buttons.items():
            is_selected = opt == self.selected
            bg = (60, 120, 60) if is_selected else (60, 60, 60)
            border = (100, 220, 100) if is_selected else (150, 150, 150)
            pygame.draw.rect(screen, bg, rect, border_radius=8)
            pygame.draw.rect(screen, border, rect, 2, border_radius=8)
            label = self.font.render(opt.capitalize(), True, (255, 255, 255))
            screen.blit(label, label.get_rect(center=rect.center))

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            for opt, rect in self.buttons.items():
                if rect.collidepoint(event.pos):
                    self.selected = opt
                    return True
        return False

class Bottle:
    def __init__(self, bottle, x, y, width, height, capacity, index):
        self.bottle = bottle
        self.x = x  
        self.y = y
        self.width = width
        self.height = height
        self.capacity = capacity
        self.index = index

    def draw(self, screen, game_state, COLOR_RGB, selected=False):

        y_offset = -20 if selected else 0
        y = self.y + y_offset
    
        pygame.draw.ellipse(screen, (200, 200, 200), (self.x, y-10, self.width, 20), 3)
        pygame.draw.line(screen, (200, 200, 200), (self.x, y), (self.x, y + self.height), 3)
        pygame.draw.line(screen, (200, 200, 200), (self.x + self.width, y), (self.x + self.width, y + self.height), 3)
        pygame.draw.line(screen, (200, 200, 200), (self.x, y + self.height), (self.x + self.width, y + self.height), 3)

        for j, color_id in enumerate(self.bottle):
            color_name = game_state.color_map.get(color_id)
            rgb = COLOR_RGB.get(color_name, (120, 120, 120))
            block_height = self.height // self.capacity
            block_y = y + self.height - (j + 1) * block_height
            pygame.draw.rect(screen, rgb, (self.x+3, block_y+3, self.width-6, block_height-6))

    def handle_click(self, event):      
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            if self.x <= mx <= self.x + self.width and self.y <= my <= self.y + self.height:
                return True
        return False
   
class Dropdown:
    def __init__(self, x, y, width, height, options, selected_index=0):
        self.rect = pygame.Rect(x, y, width, height)
        self.options = options
        self.selected_index = selected_index
        self.open = False
        self.font = pygame.font.SysFont("Arial", 18)

    def draw(self, screen):
        pygame.draw.rect(screen, (60, 60, 60), self.rect)
        pygame.draw.rect(screen, (150, 150, 150), self.rect, 2)
        label = self.font.render(self.options[self.selected_index], True, (255, 255, 255))
        screen.blit(label, label.get_rect(center=self.rect.center))

        if self.open:
            for i, option in enumerate(self.options):
                option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height, self.rect.width, self.rect.height)
                pygame.draw.rect(screen, (80, 80, 80), option_rect)
                pygame.draw.rect(screen, (150, 150, 150), option_rect, 2)
                label = self.font.render(option, True, (255, 255, 255))
                screen.blit(label, label.get_rect(center=option_rect.center))

    def handle_click(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.open = not self.open
                return True
            if self.open:
                for i, option in enumerate(self.options):
                    option_rect = pygame.Rect(self.rect.x, self.rect.y + (i+1)*self.rect.height, self.rect.width, self.rect.height)
                    if option_rect.collidepoint(event.pos):
                        self.selected_index = i
                        self.open = False
                        return True
                self.open = False
        return False

    @property
    def selected(self):
        return self.options[self.selected_index]

class InputBox:
    def __init__(self, x, y, w, h, placeholder='', font_size=18):
        self.rect = pygame.Rect(x, y, w, h)
        self.color_inactive = (60, 60, 60)
        self.color_active = (100, 180, 250)
        self.color = self.color_inactive
        self.text = ''
        self.placeholder = placeholder
        self.font = pygame.font.SysFont("Arial", font_size)
        self.active = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.active = not self.active
                self.color = self.color_active if self.active else self.color_inactive
                return True
            else:
                self.active = False
                self.color = self.color_inactive
           
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                value = self.text
                self.text = ''
                return value
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif event.unicode.isdigit():
                self.text += event.unicode

        return False

    def draw(self, screen):
        if self.text:
            txt_surface = self.font.render(self.text, True, (255, 255, 255))
        else:
            txt_surface = self.font.render(self.placeholder, True, (130, 130, 130))
        
        screen.blit(txt_surface, (self.rect.x + 5, self.rect.y + 5))
        pygame.draw.rect(screen, self.color, self.rect, 2)


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