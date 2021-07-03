import pygame
from .base import Scene
from .pause import Pause
from entities import Player
from entities import Asteroid
import utils
import time

class Game(Scene):
    def init(self, *args, **kwargs):
        self.level = 1
        self.player = Player(self.game)
        self.asteroids = [Asteroid(self.game) for _ in range(3 + self.level)]
        self.bullets = []
        self.elapsed = None
        self.score = 0
        self.font = pygame.font.SysFont(None, self.game.scale(50))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.previous_scene = self
                self.game.current_scene = Pause(
                    self.game,
                    entities=[
                        self.game.current_scene.asteroids, 
                        [self.game.current_scene.player], 
                        self.game.current_scene.bullets])

        self.player.handle_event(event)

    def handle_key_press(self, key):
        self.player.handle_key_press(key)

    def update(self):

        if len(self.asteroids) == 0:
            if not self.elapsed:
                self.elapsed = time.time()

            if time.time() - self.elapsed > 3:
                self.elapsed = None

                self.level += 1
                self.asteroids = [Asteroid(self.game) for _ in range(3 + self.level)]

        self.player.update()

        for bullet in self.bullets:
            bullet.update()
        
        # Check to see if the player has collided with an asteroid
        # Do this last as if its game over we change the game state which means
        # any code executed afterwards would almost certainly fail
        ship_lines = utils.points_to_lines(self.player.position, self.player.points)
        for asteroid in self.asteroids:
            asteroid.update()
            asteroid_lines = utils.points_to_lines(asteroid.position, asteroid.points)

            collision = False
            if not self.player.invincible:
                for asteroid_line in asteroid_lines:
                    for ship_line in ship_lines:
                        if utils.lines_intersect(asteroid_line, ship_line):
                            self.player.die()
                            collision = True
                            break

                    if collision:
                        break

    def draw(self):
        self.player.draw()

        for asteroid in self.asteroids:
            asteroid.draw()

        for bullet in self.bullets:
            bullet.draw()

        startx, starty = 60, 30
        for life in range(self.player.lives):
            x, y = startx * (life + 1), starty 
            pygame.draw.line(self.game.display, 'white', (x, y), (x - 20, y + 60), 2)
            pygame.draw.line(self.game.display, 'white', (x, y), (x + 20, y + 60), 2)
            pygame.draw.line(self.game.display, 'white', (x - 20, y + 60), (x + 20, y + 60), 2)

        text = self.font.render(f"Score: {self.score}", True, 'white')
        self.game.display.blit(text, (240, 35))
