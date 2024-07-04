import pygame
import sys

COLOR_WHITE = (255, 255, 255)
COLOR_BLACK = (0, 0, 0)
COLOR_BLUE_GREEN = (0, 255, 255)
BUTTON_TRANSPARENT = (0, 0, 0, 0)

# Dimensions de l'écran
SCREEN_WIDTH = 960
SCREEN_HEIGHT = 720

def draw_rounded_rect(surface, rect, color, radius=0.4):
    """
    Draw a rectangle with rounded corners.
    """
    rect = pygame.Rect(rect)
    color = pygame.Color(*color)
    alpha = color.a
    color.a = 0
    pos = rect.topleft
    rect.topleft = 0, 0
    rectangle = pygame.Surface(rect.size, pygame.SRCALPHA)

    circle = pygame.Surface([min(rect.size) * 3] * 2, pygame.SRCALPHA)
    pygame.draw.ellipse(circle, color, circle.get_rect(), 0)
    circle = pygame.transform.smoothscale(circle, [int(min(rect.size) * radius)] * 2)
    radius = rectangle.blit(circle, (0, 0))
    radius.bottomright = rect.bottomright
    rectangle.blit(circle, radius.topleft)
    radius.topright = rect.topright
    rectangle.blit(circle, radius.topleft)
    radius.bottomleft = rect.bottomleft
    rectangle.blit(circle, radius.topleft)

    rectangle.fill(color, rect.inflate(-radius.w * 2, 0))
    rectangle.fill(color, rect.inflate(0, -radius.h * 2))
    rectangle.blit(rectangle, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
    surface.blit(rectangle, pos)

def show_menu(screen):
    background_image = pygame.image.load('background.jpg')
    background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.SysFont('Consolas', 36)

    button_play = pygame.Rect(380, 225, 200, 50)
    button_options = pygame.Rect(380, 325, 200, 50)
    button_scores = pygame.Rect(380, 425, 200, 50)

    play_button_text = font.render("Jouer", True, COLOR_WHITE)
    option_button_text = font.render("Options", True, COLOR_WHITE)
    scores_button_text = font.render("Scores", True, COLOR_WHITE)

    clock = pygame.time.Clock()
    while True:
        screen.blit(background_image, (0, 0))
        mouse_pos = pygame.mouse.get_pos()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if button_play.collidepoint(mouse_pos):
                    return "play"
                elif button_options.collidepoint(mouse_pos):
                    return "options"
                elif button_scores.collidepoint(mouse_pos):
                    return "scores"

        # Draw buttons
        for button in [button_play, button_options, button_scores]:
            if button.collidepoint(mouse_pos):
                draw_rounded_rect(screen, button, COLOR_BLUE_GREEN, 0.4)
                draw_eclair(screen, button)
            else:
                draw_rounded_rect(screen, button, COLOR_WHITE, 0.4)

        screen.blit(play_button_text, (button_play.x + 50, button_play.y + 10))
        screen.blit(option_button_text, (button_options.x + 35, button_options.y + 10))
        screen.blit(scores_button_text, (button_scores.x + 35, button_scores.y + 10))

        pygame.display.flip()
        clock.tick(60)

def draw_eclair(surface, button):
    """
    Draw an eclair effect across the button.
    """
    start_pos = (button.left, button.centery)
    end_pos = (button.right, button.centery)
    pygame.draw.line(surface, COLOR_BLUE_GREEN, start_pos, end_pos, 3)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    show_menu(screen)
    pygame.quit()
