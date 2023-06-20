import pygame
import random

from pygame.sprite import Sprite
from game.utils.constants import SPACESHIP,SPACESHIP_SHIELD, SCREEN_HEIGHT, SCREEN_WIDTH
from game.components.bullets.bullet_manager import BulletManager

from game.components.bullets.bullet import Bullet
REST = 10
class Spaceship(Sprite):
    X_POS = (SCREEN_WIDTH // 2) - 40
    Y_POS = 500
    SHIELD_DURATION = 5000  # 5 segundos (en milisegundos)
    SHOT_DURATION = 5000  # 10 segundos (en milisegundos)

    def __init__(self):
        self.original_image = SPACESHIP
        self.original_image = pygame.transform.scale(self.original_image, (40, 60))
        self.image = self.original_image.copy()
        self.rect = self.image.get_rect()
        self.rect.x = self.X_POS
        self.rect.y = self.Y_POS
        self.type = 'player'
        self.shield_active = False
        self.fireshot = False

        self.shield_timer = 0
        self.bullet_manager = BulletManager()
        self.shielsound = pygame.mixer.Sound("game/assets/Sountrack/shield.mp3")

    def reduce_life(self):
        if self.lives > 0:
            self.lives -= 1

    def update(self, user_input, game):
        self.update_shield()
        self.update_shot()
        if user_input[pygame.K_LEFT]:
            self.move_left()
        if user_input[pygame.K_RIGHT]:
            self.move_right()
        if user_input[pygame.K_UP]:
            self.move_up()
        if user_input[pygame.K_DOWN]:
            self.move_down()
        if user_input[pygame.K_SPACE]:
            self.shoot(game)
        if user_input[pygame.K_ESCAPE]:
            pygame.quit()
    
    def move_left(self):
        if self.rect.left > 0:
            self.rect.x -= REST
        elif self.rect.left < REST:
            self.rect.x = SCREEN_WIDTH - REST    

    def move_right(self):
        if self.rect.right < SCREEN_WIDTH:
            self.rect.x += REST
        elif self.rect.right > SCREEN_WIDTH - REST:
            self.rect.x = 0 + REST

    def move_up(self):
        if self.rect.y > SCREEN_HEIGHT // 2:
            self.rect.y -= REST

    def move_down(self):
        if self.rect.y < SCREEN_HEIGHT - 70:
            self.rect.y += REST

    # Resto de los métodos de movimiento...

    def shoot(self, game):
        if not self.shield_active:  # Solo puede disparar si el escudo no está activo
            bullet = Bullet(self)
            game.bullet_manager.add_bullet(bullet, self.type)

    def draw(self, screen):
        if self.shield_active:
            # Escalar la imagen con el escudo activado
            scaled_width = int(self.original_image.get_width() * 1.5)  # Ajusta el factor de escala según sea necesario
            scaled_height = int(self.original_image.get_height() * 1.5)
            scaled_image = pygame.transform.scale(SPACESHIP_SHIELD, (60, 70))
            screen.blit(scaled_image, (self.rect.x - (scaled_width - self.rect.width) // 2, self.rect.y - (scaled_height - self.rect.height) // 2))
        else:
            # Dibujar la imagen original sin cambios
            screen.blit(self.original_image, (self.rect.x, self.rect.y))

    def activate_shield(self):
        self.shielsound.play()
        self.shielsound.set_volume(0.5)
        if not self.shield_active:  # Activar el escudo solo si no está activo
            self.shield_active = True
            self.shield_timer = pygame.time.get_ticks()

    def update_shield(self):
        if self.shield_active:
            current_time = pygame.time.get_ticks()
            if current_time - self.shield_timer >= self.SHIELD_DURATION:
                self.shield_active = False

    def activate_shot(self):
        if not self.fireshot:  # Activar el escudo solo si no está activo
            self.fireshot = True
            self.shot_timer = pygame.time.get_ticks()

    def update_shot(self):
        if self.fireshot:
            current_time = pygame.time.get_ticks()
            if current_time - self.shot_timer >= self.SHOT_DURATION:
                self.fireshot = False
