import pygame
from .bullet import Bullet
import utils
import time
from scenes import GameOver 
from scenes import Pause

class Player:
    def __init__(self, game):
        self.game = game

        # Position player in the middle of the screen
        self.position = pygame.math.Vector2(
            (self.game.screen_width / 2),
            (self.game.screen_height / 2))

        # Store some information about how the player should move
        self.size = self.game.scale(20)
        self.direction = pygame.math.Vector2(0, -1)
        self.velocity = pygame.math.Vector2()
        self.rotation_speed = 300
        self.acceleration = 400
        self.deceleration = self.acceleration / 4
        self.maximum_speed = 400
        self.thrusting = False
        self.lives = 3
        self.invincible = True 
        self.invincible_time = 2
        self.spawn_time = time.time()

        # Store coordinates that will be used to draw the player
        # These will be generated when the update function is called
        self.points = []

    def die(self):
        self.spawn_time = time.time()
        self.invincible = True
        self.lives -= 1
        if self.lives == 0:
            self.game.current_scene = GameOver(self.game, score=self.game.current_scene.score) 

        self.velocity = pygame.math.Vector2()
        self.direction = pygame.math.Vector2(0, -1)
        self.position = pygame.math.Vector2(
            (self.game.screen_width / 2),
            (self.game.screen_height / 2))

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if len(self.game.current_scene.bullets) > 6:
                    return

                self.game.current_scene.bullets.append(
                    Bullet(
                        self.game,
                        self.position + (self.direction * self.size),
                        self.direction))


    def handle_key_press(self, key_pressed):
        if key_pressed[pygame.K_RIGHT]:
            self.direction.rotate_ip(self.rotation_speed * self.game.dt)

        elif key_pressed[pygame.K_LEFT]:
            self.direction.rotate_ip(-self.rotation_speed * self.game.dt)

        self.thrusting = False
        if key_pressed[pygame.K_UP]:
            self.thrusting = True

    def update(self):

        if self.invincible:
            if time.time() - self.spawn_time > self.invincible_time:
                self.invincible = False

        # Move the player
        current_speed = self.velocity.length()
        if self.thrusting:
            acceleration = self.acceleration * (self.game.dt)
            self.velocity = self.velocity + (self.direction * acceleration)

            # Ensure the player doesn't go too fast
            if current_speed > self.maximum_speed:
                scale = self.maximum_speed / current_speed
                self.velocity = self.velocity * scale

        # If we're not thrusting, and we've almost come to a stop, stop!
        elif current_speed < 0.1:
            self.velocity = pygame.math.Vector2()

        # Otherwise, slowly decelerate
        elif current_speed > 0:
            deceleration = self.deceleration * (self.game.dt)
            self.velocity += (self.velocity.normalize() * -1) * deceleration

        self.position = self.position + (self.velocity * self.game.dt)
        self.position = self.game.wrap_position(self.position, self.size)

        # Generate coordinates to use to draw the player and detect collisions
        self.points = []
        for rotation in [0, -135, 135]:
            angle = pygame.math.Vector2(0, -1).angle_to(self.direction) - 90
            angle = (angle + rotation) % 360
            self.points.append((self.size, angle))

    def draw(self):

        colour = "white"
        paused = isinstance(self.game.current_scene, Pause)
        if self.invincible and not paused:
            t = round(time.time() - self.spawn_time, 1)
            t = t * 10 % 2
            if t == 0:
                colour = "green"
        # Draw our player
        for line in utils.points_to_lines(self.position, self.points):
            pygame.draw.line(self.game.display, colour, *line, 3)
