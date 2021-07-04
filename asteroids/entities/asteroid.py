import random
import pygame
import utils

class Asteroid:
    def __init__(self, game, size=3, position=None):
        self.game = game
        self.size = size 
        self.rotation_speed = random.randint(10, 60)
        self.rotation_speed = self.rotation_speed * random.choice([-1, 1])
        self.velocity = pygame.math.Vector2(random.uniform(-1, 1), random.uniform(-1, 1))
        self.velocity = self.velocity.normalize() * (random.randint(3, 8) / size)
        self.sound_explode = pygame.mixer.Sound(f'{self.game.path}/assets/asteroid_explosion.wav')

        # Generate a number of points which we'll join together to draw
        # our asteroid
        points_count = random.randint(10, 20)
        degrees_pp = 360 / points_count
        self.points = []
        for r in range(points_count):
            start, end = int(degrees_pp * r), int(degrees_pp * (r + 1))
            angle = random.randint(start, end)
            distance = random.randint(self.game.scale(20), self.game.scale(25)) * self.size
            self.points.append((distance, angle))

        self.draw_size = max([p[0] for p in self.points])

        # Generate a random spawn position off screen
        self.position = position
        if self.position is None:
            spawn_point = random.randint(0, 3)
            if spawn_point in [0, 2]:
                x = random.randint(0, self.game.screen_width)
                y = -self.draw_size if spawn_point == 0 else self.game.screen_height + self.draw_size

            else:
                x = -self.draw_size if spawn_point == 3 else self.game.screen_width + self.draw_size
                y = random.randint(0, self.game.screen_height)

            self.position = pygame.math.Vector2(x, y)

    def split(self):
        if self.size != 1:
            for _ in range(2):
                self.game.current_scene.asteroids.append(
                    Asteroid(
                        self.game,
                        self.size - 1,
                        self.position))

        pygame.mixer.Sound.play(self.sound_explode)
        self.game.current_scene.asteroids.remove(self)

    def update(self):
        for i, _ in enumerate(self.points):
            distance, angle = self.points[i]
            new_angle = angle + (self.rotation_speed * self.game.dt) % 360
            self.points[i] = (distance, new_angle)

        self.position = self.position + self.velocity
        self.position = self.game.wrap_position(self.position, self.draw_size)

    def draw(self):
        for lines in utils.points_to_lines(self.position, self.points):
            pygame.draw.line(
                self.game.display,
                (175, 99, 87), 
                lines[0], lines[1], 8)
