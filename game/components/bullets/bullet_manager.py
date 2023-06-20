import pygame
pygame.mixer.init()

class BulletManager:
    def __init__(self):
        self.bullets = []
        self.enemy_bullets = []
        self.player_bullets = []
        self.lives = 3  # vidas iniciales
        self.fire = 1

        self.death_sound = pygame.mixer.Sound("game/assets/Sountrack/death.mp3")
        self.death_sound.set_volume(1.0)
        
        self.shot = pygame.mixer.Sound("game/assets/Sountrack/shot.mp3")
        
        
    def update(self, game):
        for bullet in self.enemy_bullets:
            bullet.update(self.enemy_bullets)

            if bullet.rect.colliderect(game.player.rect) and bullet.owner == 'enemy':
                self.enemy_bullets.remove(bullet)
                self.lives -= 1
                if self.lives == 0:
                    game.playing = False
                    self.death_sound.play()
                    game.update_death_count()
                    pygame.time.delay(1000)
                    break
            
        for bullet in self.player_bullets:
            bullet.update(self.player_bullets)
            for enemy in game.enemy_manager.enemies:
                if bullet.rect.colliderect(enemy.rect) and bullet.owner != 'enemy':
                    game.enemy_manager.enemies.remove(enemy)
                    self.player_bullets.remove(bullet)
                    game.update_score()
    
    def draw(self, screen):
        for bullet in self.enemy_bullets:
            bullet.draw(screen)

        for bullet in self.player_bullets:
            bullet.draw(screen)
    
    def add_bullet(self, bullet, owner):
        if owner == 'enemy' and len(self.enemy_bullets) < 1:
            self.enemy_bullets.append(bullet)
            
        if owner == 'player' and len(self.player_bullets) < self.fire:
            self.shot.play(1)
            self.shot.set_volume(0.2)
            self.player_bullets.append(bullet)
