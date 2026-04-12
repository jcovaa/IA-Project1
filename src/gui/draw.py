import pygame

SCREEN_W, SCREEN_H = 1280, 720
PANEL_W = 200

def draw_panel(screen, panel_x):
    pygame.draw.rect(screen, (40, 40, 40), (panel_x, 0, PANEL_W, SCREEN_H))
    pygame.draw.line(screen, (80, 80, 80), (panel_x, 0), (panel_x, SCREEN_H), 2)

def draw_win_screen(screen, font_big, font_small, steps, final_time, score, confetti,solved_by_solver):

    confetti.update()
    confetti.draw(screen)

    overlay = pygame.Surface((SCREEN_W, SCREEN_H))
    overlay.set_alpha(170)
    overlay.fill((0, 0, 0))
    screen.blit(overlay, (0, 0))

    title = font_big.render("Puzzle Solved!", True, (255, 255, 255))
    stats = font_small.render(
        f"Steps: {steps}   Time: {final_time}s",
        True,
        (220, 220, 220)
    )

    score_text = font_small.render(
        f"Score: {score}",
        True,
        (220,220,220)
    )
    if solved_by_solver:
        hint = font_small.render(
            "Click Play again",
            True,
            (180, 180, 180)
        )
    else:
        hint = font_small.render(
            "Click Generate to play again",
            True,
            (180, 180, 180)
        )

    screen.blit(title, title.get_rect(center=(SCREEN_W//2, SCREEN_H//2 - 40)))
    screen.blit(stats, stats.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 10)))
    screen.blit(score_text,score_text.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 50)))
    screen.blit(hint, hint.get_rect(center=(SCREEN_W//2, SCREEN_H//2 + 90)))

