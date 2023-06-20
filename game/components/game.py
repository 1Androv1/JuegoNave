import pygame
import random

from game.utils.constants import HEART,BG,BG2,GAMEOVER,ICON,FIREBALL,SHIELD, SCREEN_HEIGHT, SCREEN_WIDTH ,  TITLE, FPS, FONT_STYLE

from game.components.spaceship import Spaceship
from game.components.enemies.enemy_manager import EnemyManager
from game.components.menus.menu import Menu
from game.components.bullets.bullet_manager import BulletManager
from game.components.powers.power_manager import PowerManager
#from game.components.powers.power_manager import PowerManager2


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode ((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()

        self.playing = False
        self.game_speed = 10

        self.x_pos_bg = 0
        self.y_pos_bg = 0
        self.player = Spaceship()
        self.enemy_manager = EnemyManager()
        self.bullet_manager = BulletManager()
        
        self.power_manager = PowerManager()
        self.listvalues = 0
        
        self.previous_lives = self.bullet_manager.lives

        self.running = False
        self.score = 0
        self.death_count = 0
        self.high_score = {'high_score': 0, 'death_count':0}
        self.menu = Menu('PRESS ANY KEY TO START THE GAME...', self.screen)
        self.inicio_sound = pygame.mixer.Sound("game/assets/Sountrack/intro.mp3")

    def execute(self):
        self.running = True
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.display.quit()
        pygame.quit()

    def run(self):
        self.enemy_manager.reset()
        self.power_manager.reset()

        self.score = 0
        self.menu.reset_message()
        self.bullet_manager.lives = 3
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):

        if self.player.shield_active:
            if self.previous_lives == 0:
                self.previous_lives = self.bullet_manager.lives  # Guarda el valor original de las vidas

            self.bullet_manager.lives = 99
        else:
            if self.previous_lives != 0:
                self.bullet_manager.lives = self.previous_lives  # Restaura el valor original de las vidas
                self.previous_lives = 0  # Restablece la variable a su estado inicial
                
        if self.player.fireshot: 
            self.bullet_manager.fire = 3
        else: 
            self.bullet_manager.fire = 1 
            
        self.enabledsountrack()
        user_iput = pygame.key.get_pressed()
        self.player.update(user_iput,self)
        self.enemy_manager.update(self)
        self.bullet_manager.update(self)
        #self.uplive()
        self.power_manager.update(self)        
        #self.power_manager2.update(self)        


    def enabledsountrack(self):
        if self.running: 
            self.inicio_sound.stop()

    def draw(self):
        self.clock.tick(FPS)
        self.screen.fill((255,255,255))

        self.draw_background()
        self.player.draw(self.screen)
        self.enemy_manager.draw(self.screen)
        self.bullet_manager.draw(self.screen)
        self.power_manager.draw(self.screen)
        #self.power_manager2.draw(self.screen)

        self.draw_score()
        pygame.display.update()
        pygame.display.flip()

    def draw_background(self):
        image = pygame.transform.scale(BG, (SCREEN_WIDTH, SCREEN_HEIGHT) )
        image_heigth = image.get_height()
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_heigth))

        if self.y_pos_bg >= SCREEN_HEIGHT:
            self.screen.blit(image, (self.x_pos_bg, self.y_pos_bg - image_heigth))
            self.y_pos_bg = 0
        self.y_pos_bg = self.y_pos_bg + self.game_speed

    def show_menu(self):
        self.inicio_sound.play()
        self.inicio_sound.set_volume(0.2)

        self.menu.reset_screen_collor(self.screen)
        half_screen_heigth = SCREEN_HEIGHT // 2
        half_screen_width = SCREEN_WIDTH // 2

        if self.death_count == 0:
            self.menu.draw(self.screen)
            icon = pygame.transform.scale(ICON, (80, 120))
            self.screen.blit(icon, (half_screen_width - 50, half_screen_heigth - 150))
        else:
            icon = pygame.transform.scale(GAMEOVER, (300, 100))
            self.screen.blit(icon, (400, 200))
            self.menu.update_message(f'You Score:  {self.score}', 40)  
            self.menu.update_message(f'Highest score: {int(self.high_score["high_score"])}', 70)
            self.menu.update_message(f'Total deaths: {int(self.high_score["death_count"])}', 100) 
            self.menu.draw(self.screen)
            
            for text, rect in self.menu.texts:
                self.screen.blit(text, rect)

        self.menu.update(self)
        
    def update_score(self):
        self.score += 1
        #self.increase_life()
        self.high_score['score']= self.score

        if self.score > self.high_score['high_score']:
            self.high_score['high_score'] = self.score
            self.high_score['death_count'] = self.death_count

    def update_death_count(self):
        self.death_count += 1
        self.high_score['death_count'] = self.death_count

    def draw_score(self):
        font = pygame.font.Font(FONT_STYLE, 30)
        text = font.render(f'Score: {self.score}', True, (255,255,255))
        pixel = 50
        text_rect = text.get_rect()
        vidas_rect = text.get_rect()
        power = text.get_rect()
        power2 = text.get_rect()
        """
            PINTAR LAS VIDAS DISPONIBLES
        """
    
        max_lives = min(self.bullet_manager.lives, 10)  # Obtener la cantidad máxima de vidas a mostrar (máximo 10)

        for i in range(max_lives):
            vidas_rect.center = (pixel, 50)
            pixel += 50
            vidas_img = pygame.transform.scale(HEART, (40, 40))
            vidas_rect.center = (pixel, 50)
            self.screen.blit(vidas_img, vidas_rect)
        
        if self.player.shield_active:
            power.center = (150, 100)
            power_img = pygame.transform.scale(SHIELD, (40, 40))
            self.screen.blit(power_img, power)
        
        if self.player.fireshot:
            power2.center = (100, 100)
            power2_img = pygame.transform.scale(FIREBALL, (40, 40))
            self.screen.blit(power2_img, power2)
        
        text_rect.center = (1000, 50)
    
        self.screen.blit(text, text_rect)
