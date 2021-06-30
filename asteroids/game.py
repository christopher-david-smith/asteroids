#!/usr/bin/env python

import pygame
import constants
import random
import time

class Game:
    def __init__(self):
        pygame.init()
        self.display = pygame.display.set_mode(constants.SCREEN_SIZE)
        self.asteroids = [Asteroid(self)]
        self.ship = Ship(self, constants.SCREEN_WIDTH / 2, constants.SCREEN_HEIGHT / 2)
        self.clock = pygame.time.Clock()
        self.dt = 0

    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.dt = self.clock.tick(60)

    def handle_events(self):
        events = pygame.event.get()

    def update(self):
        self.ship.update()
        for asteroid in self.asteroids:
            asteroid.update()
        key_pressed = pygame.key.get_pressed()
        
        if key_pressed[pygame.K_RIGHT]:
            self.ship.rotate(clockwise=True)

        elif key_pressed[pygame.K_LEFT]:
            self.ship.rotate(clockwise=False)

        if key_pressed[pygame.K_UP]:
            self.ship.thrusting = True
        
        else:
            self.ship.thrusting = False
            self.ship.thrusting_frame = 0

    def draw(self):
        self.display.fill((0, 0, 0))
        for asteroid in self.asteroids:
            asteroid.draw()
        self.ship.draw()

    def wrap_position(self, position):
        x, y = position
        w, h = constants.SCREEN_SIZE
        return pygame.math.Vector2(x % w, y % h)

class Ship:
    def __init__(self, game, x, y):
        self.game = game
        self.position = pygame.math.Vector2(x, y)
        self.direction = pygame.math.Vector2(0, 1)
        self.velocity = pygame.math.Vector2(0, 0)
        self.thrusting = False
        self.acceleration = 0.25
        self.deceleration = 0.05
        self.maximum_speed = 10
        self.thrusting_frame = 0
        self.next_update_time = time.time()
        self.refresh_time = 0.1

        self.point1, self.point2, self.point3 = None, None, None

    def update(self):
        self.point1 = self.position - (self.direction * 50)
        self.point2 = pygame.math.Vector2(self.direction)
        self.point2.rotate_ip(-135)
        self.point2 = self.position - (self.point2 * 50)
        self.point3 = pygame.math.Vector2(self.direction)
        self.point3.rotate_ip(135)
        self.point3 = self.position - (self.point3 * 50)

        speed = self.velocity.length()
        if self.thrusting:
            new_velocity = self.velocity - (self.direction * self.acceleration)

            if speed > self.maximum_speed:
                scale = self.maximum_speed/speed
                new_velocity *= scale

            self.velocity = new_velocity

        else:
            if speed > 0:
                self.velocity += ((self.velocity.normalize() * -1) * self.deceleration)

        self.position = self.game.wrap_position(self.position + self.velocity)


    def rotate(self, clockwise=True):
        amount = 0.2 if clockwise else -0.2
        self.direction.rotate_ip(amount * self.game.dt)
        
    def draw(self):
        pygame.draw.line(self.game.display, 'white', self.point1, self.point2)
        pygame.draw.line(self.game.display, 'white', self.point1, self.point3)
        pygame.draw.line(self.game.display, 'white', self.point2, self.point3)

        # Thrusters
        if self.thrusting:
            
            if time.time() > self.next_update_time:
                self.next_update_time = time.time() + self.refresh_time
                
                self.thrusting_frame += 1
                if self.thrusting_frame > 2:
                    self.thrusting_frame = 0

            colour = 'red'
            colour = 'orange' if self.thrusting_frame == 1 else colour
            colour = 'yellow' if self.thrusting_frame == 2 else colour

            distance = 30 * (self.thrusting_frame + 2)
            pygame.draw.line(self.game.display, colour, self.position + (self.direction * distance), self.point2)
            pygame.draw.line(self.game.display, colour, self.position + (self.direction * distance), self.point3)


class Asteroid:
    def __init__(self, game, size=3):
        self.game = game
        self.position = pygame.math.Vector2(500, 500)
        self.rotation_speed = random.choice([-2, -1, 1, 2]) / 30
        self.velocity = pygame.math.Vector2(
            random.uniform(-1, 1), 
            random.uniform(-1, 1)
        ).normalize() * random.randint(1, 3)

        # Generate number of points asteroid should have
        number_of_points = random.randint(10, 20)
        degrees_per_point = 360 / number_of_points
        
        # Then generate their angle and distance from the centre
        self.points = []
        for r in range(number_of_points):
            start = int(degrees_per_point * r)
            end = int(degrees_per_point * (r + 1))
            angle = int(random.randint(start, end))
            distance = int(random.randint(50, 100)) * size
            self.points.append((distance, angle))

        self.size = max([p[0] for p in self.points])

    def update(self):
        for i, _ in enumerate(self.points):
            point = self.points[i]
            direction, angle = self.points[i]

            new_angle = angle + (self.rotation_speed * self.game.dt) % 360
            self.points[i] = (direction, new_angle)

        self.position = self.game.wrap_position(self.position + self.velocity)

    def wrap_position(self, position):
        pass
        # if (position - (max_size / 2, max_size / 2)) 

        # if position.x < (screen_size - (max_size / 2))

        #position = self.position - pygame.math.Vector2(self.size / 2, self.size / 2)
        # ==> any([l < 0 for l in list(v(1,-1))])


    def draw(self):
        for index, point in enumerate(self.points):
            try:
                next_point = self.points[index + 1]
            except IndexError:
                next_point = self.points[0]

            first_point = pygame.math.Vector2(self.position)
            first_point.from_polar(point)

            second_point = pygame.math.Vector2(self.position)
            second_point.from_polar(next_point)

            pygame.draw.line(
                self.game.display,
                (0, 255, 0),
                self.position + first_point, self.position + second_point)

