import random
from game.components.enemies.enemy import Enemy
from game.utils.constants import ENEMY_1, ENEMY_2, ENEMY_3


class EnemyManager:
    def __init__(self):
        self.enemies = []

    def update(self, game):
        self.add_enemy()
        for enemy in self.enemies:
            enemy.update(self.enemies, game)

    def add_enemy(self):
        enemy_types = [1, 2, 3]
        max_enemies = 5

        while len(self.enemies) < max_enemies:
            enemy_value = random.choice(enemy_types)
            if enemy_value == 1:
                enemy = Enemy(enemy_value)
            elif enemy_value == 2:
                enemy = Enemy(enemy_value)
            elif enemy_value == 3:
                enemy = Enemy(enemy_value)
            self.enemies.append(enemy)

    def draw(self, screen):
        for enemy in self.enemies:
            enemy.draw(screen)

    def reset(self):
        self.enemies = []
