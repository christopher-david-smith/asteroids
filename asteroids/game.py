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
        self.bullets = []
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
        for event in events:
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.ship.fire()

    def update(self):
        self.ship.update()
        for asteroid in self.asteroids:
            asteroid.update()

        for bullet in self.bullets:
            bullet.update()

            if not bullet.active:
                self.bullets.remove(bullet)

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

        for bullet in self.bullets:
            bullet.draw()

        self.ship.draw()

    def wrap_position(self, position, size):
        x, y = position
        w, h = constants.SCREEN_SIZE

        new_position_x = x
        new_position_y = y

        if x < -size:
            new_position_x = w + size
        elif x > w + size:
            new_position_x = -size

        if y < -size:
            new_position_y = h + size
        elif y > h + size:
            new_position_y = -size

        return pygame.math.Vector2(new_position_x, new_position_y)
        
        if x < -size or y < -size or x > w + size or y > h + size:
            print(x, y, x % (w+(size*2)), y % (h+(size*2)))
            return pygame.math.Vector2(x % (w + (size *2 )), y % (h + (size * 2)))

        return position

#        if position.x < -size or position.y <- size or position.x >
 #       return pygame.math.Vector2(x % w, y % h)

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
        self.size = 100 # This shouldn't be hardcoded
        self.colour = "white"

        self.point1, self.point2, self.point3 = None, None, None

    def update(self):
        self.point1 = self.position - (self.direction * 50)
        self.point2 = pygame.math.Vector2(self.direction)
        self.point2.rotate_ip(-135)
        self.point2 = self.position - (self.point2 * 50)
        self.point3 = pygame.math.Vector2(self.direction)
        self.point3.rotate_ip(135)
        self.point3 = self.position - (self.point3 * 50)
        self.check_for_collisions()

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

        self.position = self.game.wrap_position(self.position + self.velocity, self.size)

    def check_for_collisions(self):

        # The following functions are taken without understanding from 
        # https://stackoverflow.com/a/9997374
        # vvv

        def ccw(a, b, c):
            return (c.y - a.y) * (b.x - a.x) > (b.y - a.y) * (c.x - a.x)

        def intersect(a, b, c, d):
            return ccw(a, c, d) != ccw(b, c, d) and ccw(a, b, c) != ccw(a, b, d)

        # ^^^
        
        collision = False
        for asteroid in self.game.asteroids:
            if collision:
                break

            points = asteroid.points
            for i, point in enumerate(asteroid.points):
                try:
                    next_point = asteroid.points[i+1]

                except IndexError:
                    next_point = asteroid.points[0]

                # TODO - We're already doing all of this in the draw
                # function! 
                ap1 = pygame.math.Vector2(asteroid.position)
                ap1.from_polar(point)
                ap1= asteroid.position + ap1 
            
                ap2 = pygame.math.Vector2(asteroid.position)
                ap2.from_polar(next_point)
                ap2 = asteroid.position + ap2 

                collision = True if intersect(ap1, ap2, self.point1, self.point2) else collision 
                collision = True if intersect(ap1, ap2, self.point1, self.point3) else collision 
                collision = True if intersect(ap1, ap2, self.point2, self.point3) else collision 

                self.colour = "white"
                if collision:
                    self.colour = "red"
                    break

    def fire(self):
        self.game.bullets.append(
            Bullet(self.game, self.position, self.direction * -1)
        )

    def rotate(self, clockwise=True):
        amount = 0.2 if clockwise else -0.2
        self.direction.rotate_ip(amount * self.game.dt)
        
    def draw(self):
        pygame.draw.line(self.game.display, self.colour, self.point1, self.point2)
        pygame.draw.line(self.game.display, self.colour, self.point1, self.point3)
        pygame.draw.line(self.game.display, self.colour, self.point2, self.point3)

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


class Bullet:
    def __init__(self, game, position, direction):
        self.game = game
        self.position = position
        self.velocity = direction * 15
        self.active = True 
        self.distance_covered = pygame.math.Vector2()

    def update(self):
        self.position = self.game.wrap_position(self.position + self.velocity, 1) 
        self.distance_covered = self.distance_covered + self.velocity

        if self.distance_covered.length() > 2000:
            self.active = False

    def draw(self):
        pygame.draw.rect(
            self.game.display,
            'white',
            (self.position.x + 5, self.position.y + 5, 10, 10))

class Asteroid:
    def __init__(self, game, size=3):
        self.game = game
        self.size = size
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

        self.draw_size = max([p[0] for p in self.points])

        spawn_position = random.randint(0,3)
        if spawn_position == 0: # Top
            x = random.randint(0, constants.SCREEN_WIDTH)
            y = -self.draw_size

        elif spawn_position == 1: # Right
            x = constants.SCREEN_WIDTH + self.draw_size
            y = random.randint(0, constants.SCREEN_HEIGHT)

        elif spawn_position == 2: # Bottom
            x = random.randint(0, constants.SCREEN_WIDTH)
            y = constants.SCREEN_HEIGHT + self.draw_size

        else: # Left
            x = -self.draw_size
            y = random.randint(0, constants.SCREEN_HEIGHT)

        self.position = pygame.math.Vector2(x, y)
        
        # Uncomment for debugging
        #self.position = pygame.math.Vector2(500, 500)
        #self.rotation_speed = 0
        #self.velocity = pygame.math.Vector2()

    def update(self):
        for i, _ in enumerate(self.points):
            point = self.points[i]
            direction, angle = self.points[i]

            new_angle = angle + (self.rotation_speed * self.game.dt) % 360
            self.points[i] = (direction, new_angle)

        self.position = self.game.wrap_position(self.position + self.velocity, self.draw_size)

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

