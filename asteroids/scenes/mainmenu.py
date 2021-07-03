import pygame
import time
from .game import Game
from .base import Scene

class MainMenu(Scene):
    def init(self, *args, **kwargs):
        font = pygame.font.SysFont(None, self.game.scale(200))
        self.title = font.render('Asteroids', True, 'white')

        font = pygame.font.SysFont(None, self.game.scale(100))
        self.play = font.render('Press enter to play', True, 'white')
        self.time_elapsed = self.game.dt 
        self.show_text = True

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.current_scene = Game(self.game)

    def update(self):
        self.time_elapsed += self.game.dt 

    def draw(self):
        self.game.display.blit(
            self.title, 
            (
                (self.game.screen_width / 2) - self.title.get_width() / 2, 
                self.game.scale(50)
            )
        )
        
        if self.time_elapsed > 0.5:
            self.show_text = not self.show_text
            self.time_elapsed = 0

        if self.show_text:
            self.game.display.blit(
                self.play, 
                (
                    (self.game.screen_width / 2) - self.title.get_width() / 2, 
                    self.game.scale(400)
                )
            )
