import pygame
from game.utils.constants import FONT_STYLE, SCREEN_HEIGHT, SCREEN_WIDTH

class Menu:
    HALF_SCREEN_HEIGHT = SCREEN_HEIGHT // 2
    HALF_SCREEN_WIDTH = SCREEN_WIDTH // 2

    def __init__(self, message, screen):
        screen.fill((0, 0, 0))
        self.font = pygame.font.SysFont(FONT_STYLE, 30)
        self.text = self.font.render(message, True, (0, 0, 0))
        self.text_rect = self.text.get_rect()
        self.text_rect.center = (self.HALF_SCREEN_WIDTH, self.HALF_SCREEN_HEIGHT)
        self.texts = []
        self.start = pygame.mixer.Sound("game/assets/Sountrack/start.mp3")
        self.start.set_volume(0.5)  # Ajusta el volumen del sonido (0.0 a 1.0)

    def handle_events_on_menu(self, game):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
                game.playing = False
            if event.type == pygame.KEYDOWN:
                self.start.play(1)
                game.run()

    def update(self, game):
        pygame.display.update()
        self.handle_events_on_menu(game)

    def draw(self, screen):
        screen.blit(self.text, self.text_rect)

    def update_message(self, message, position):
        rendered_text = self.font.render(message, False, (0, 0, 0))
        text_rect = rendered_text.get_rect()
        text_rect.center = (self.HALF_SCREEN_WIDTH, self.HALF_SCREEN_HEIGHT + position)
        self.texts.append((rendered_text, text_rect))

    def reset_message(self):
        self.texts = []

    def reset_screen_collor(self, screen):
        screen.fill((255, 255, 255))
