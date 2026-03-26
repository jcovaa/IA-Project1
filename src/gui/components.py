import pygame

class Button:

   def __init__(self, x, y, width, heigth, text, color=(70, 70, 70), hover_color=(100, 100, 100)):
      self.rect = pygame.Rect(x, y, width, heigth)
      self.text = text
      self.color = color
      self.hover_color = hover_color
      self.font = pygame.font.SysFont("Arial", 18)

   def draw(self, screen):
      mouse = pygame.mouse.get_pos()
      color = self.hover_color if self.rect.collidepoint(mouse) else self.color
      pygame.draw.rect(screen, color, self.rect, border_radius=8)
      pygame.draw.rect(screen, (200, 200, 200), self.rect, 2, border_radius=8)
      label = self.font.render(self.text, True, (255, 255, 255))
      screen.blit(label, label.get_rect(center=self.rect.center))

   def is_clicked(self, event):
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