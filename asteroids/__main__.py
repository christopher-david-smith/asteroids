import sys
import pygame
import scenes
import time

class Game:
    def __init__(self):
        pygame.init()

        # Set up display
        self.display_scale = 1.5
        self.screen_width = self.scale(1400)
        self.screen_height = self.scale(800)
        self.display = pygame.display.set_mode((
            self.screen_width,
            self.screen_height))

        # Maintain constant framerate
        self.fps = 60
        self.clock = pygame.time.Clock()
        self.previous_time = time.time()
        self.dt = 0
        
        # Set up currennt scene
        self.current_scene = scenes.MainMenu(self)
        self.previous_scene = None

    def run(self):
        while True:

            self.clock.tick(self.fps)
            current_time = time.time()
            self.dt = current_time - self.previous_time
            self.previous_time = current_time

            # Handle events
            events = pygame.event.get()
            for event in events:
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                self.current_scene.handle_event(event)

            self.current_scene.handle_key_press(pygame.key.get_pressed())
            self.current_scene.update()

            self.display.fill((0, 0, 0))
            self.current_scene.draw()
            pygame.display.flip()

    def scale(self, size):
        """
        This function is designed to scale UI elements relative to the
        screen size
        """
        return int(size * self.display_scale)

    def wrap_position(self, position, size):
        """
        This function takes a pair of x,y coordinates and wraps them around
        the screen - but crucially - only if the object is entirely off screen
        """
        x, y = position
        w, h = self.screen_width, self.screen_height

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

if __name__ == '__main__':
    game = Game()
    game.run()
