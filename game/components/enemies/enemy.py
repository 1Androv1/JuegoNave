import pygame
import random

from pygame.sprite import  Sprite
from game.utils.constants import ENEMY_1,ENEMY_2,ENEMY_3,SCREEN_HEIGHT, SCREEN_WIDTH
from game.components.bullets.bullet import Bullet


class Enemy(Sprite):
    Y_POS = 10
    X_POST_LIST = [50, 100, 150, 200, 250, 300, 350, 400, 450, 500, 550]
    SPEED_X = 5
    SPEED_Y = 1
    MOV_X = {
        0: 'LEFT',
        1: 'RIGTH',
    }

    def __init__(self, type_enemy):
        self.type_enemy = type_enemy
        
        if self.type_enemy == 1:
            self.image = ENEMY_1
        elif self.type_enemy == 2:
            self.image = ENEMY_2
        else:
            self.image = ENEMY_3


        self.image = pygame.transform.scale(self.image, (40,60))
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, SCREEN_WIDTH - 40)
        self.rect.y = self.Y_POS

        self.type = 'enemy'

        self.speed_x = self.SPEED_X
        self.speed_y = self.SPEED_Y

        self.movement_x = self.MOV_X[random.randint(0,1)]
        self.move_x_for = random.randint(30,100)
        self.index = 0
        self.shooting_time = random.randint(30,50)

    def change_movement_x(self):
        self.index += 1
        if (self.index >= self.move_x_for and self.movement_x == 'RIGTH') or (self.rect.x >= SCREEN_WIDTH -40):
            self.movement_x = 'LEFT'
        elif (self.index >= self.move_x_for and self.movement_x == 'LEFT') or (self.rect.x <= 10):
            self.movement_x = 'RIGTH'
        if self.index >= self.move_x_for:
            self.index = 0

    def update(self, ships, game):
        self.rect.y += self.speed_y
        self.shoot(game.bullet_manager)

        if self.movement_x == 'LEFT':
            self.rect.x -= self.speed_x
            self.change_movement_x()
        else:
            self.rect.x += self.speed_x
            self.change_movement_x()
        if self.rect.y >= SCREEN_HEIGHT:
            ships.remove(self)

    def shoot(self, bullet_manager):
        current_time = pygame.time.get_ticks()
        if self.shooting_time <= current_time:
            bullet = Bullet(self)
            bullet_manager.add_bullet(bullet, self.type)
            self.shooting_time += random.randint(20,50)

    def draw(self,screen):
        screen.blit(self.image,(self.rect.x, self.rect.y))