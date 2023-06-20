import pygame
import random
from pygame.sprite import Sprite
from game.utils.constants import FIREBALL, FIREBALL_TYPE, SHIELD, SHIELD_TYPE, SCREEN_HEIGHT, SCREEN_WIDTH
from game.components.bullets.bullet import Bullet

Y_POS = 10
SPEED_Y = 5

class Power(Sprite):
    def __init__(self, image, power_type):
        self.image = image
        self.image = pygame.transform.scale(self.image, (20, 30))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = Y_POS
        self.type = power_type
        self.speed_y = SPEED_Y
        self.index = 0

    def update(self, ships, game):
        self.rect.y += self.speed_y
        if self.rect.y >= SCREEN_HEIGHT:
            ships.remove(self)

        self.check_collision(game.player)

    def check_collision(self, player):
        if pygame.sprite.collide_rect(self, player):
            if self.type == SHIELD_TYPE:
                print("activo escudo")
                player.activate_shield()
            else:
                print("activo multidisparo")
                player.activate_shot()

    def draw(self, screen):
        screen.blit(self.image, (self.rect.x, self.rect.y))
