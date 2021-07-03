import pygame
from .base import Scene

class Pause(Scene):
    def init(self, *args, **kwargs):
        self.entities = kwargs.get('entities')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.current_scene = self.game.previous_scene

    def handle_key_press(self, key):
        pass

    def update(self):
        pass

    def draw(self):
        for entity_type in self.entities:
            for entity in entity_type:
                entity.draw()

        startx, starty = 60, 30
        for life in range(self.game.previous_scene.player.lives):
            x, y = startx * (life + 1), starty
            pygame.draw.line(self.game.display, 'white', (x, y), (x - 20, y + 60), 2)
            pygame.draw.line(self.game.display, 'white', (x, y), (x + 20, y + 60), 2)
            pygame.draw.line(self.game.display, 'white', (x - 20, y + 60), (x + 20, y + 60), 2)
