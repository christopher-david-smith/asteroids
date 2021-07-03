import pygame
import utils

class Bullet:
    def __init__(self, game, position, direction, speed=800, size=5):
        self.game = game
        self.position = self.game.wrap_position(position, 1)
        self.speed = speed
        self.size = self.game.scale(size)
        self.position = self.position.elementwise() - (self.size / 2)
        self.velocity = direction * self.speed
        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.size,
            self.size)

    def update(self):
        previous_position = self.position
        self.position = self.position + (self.velocity * self.game.dt)
        self.rect = pygame.Rect(
            self.position.x,
            self.position.y,
            self.size,
            self.size)

        # Check to see if our bullet has hit an asteroid
        # Because the bullet travels fairly quickly we need to get all points
        # between when we last updated the bullets position, and its current
        # position. We then create a "dummy" bullet at each position and check
        # to see if a collision has occurred
        points = [p for p in utils.bresenham(previous_position, self.position)]
        rects = [pygame.Rect(p[0], p[1], self.size, self.size) for p in points]
        for asteroid in self.game.current_scene.asteroids:
            for line in utils.points_to_lines(asteroid.position, asteroid.points):
                for rect in rects:
                    if rect.clipline(line):
                        self.game.current_scene.bullets.remove(self)
                        asteroid.split()
                        self.game.current_scene.score += 100
                        return

        # Delete bullet if its out of bounds
        if self.position.x < 0 or self.position.x > self.game.screen_width:
            self.game.current_scene.bullets.remove(self)
            return

        if self.position.y < 0 or self.position.y > self.game.screen_height:
            self.game.current_scene.bullets.remove(self)
            return

    def draw(self):
        pygame.draw.rect(self.game.display, 'white', self.rect)
