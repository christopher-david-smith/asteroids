from .base import Scene
import scenes
import pygame

class GameOver(Scene):
    def init(self, *args, **kwargs):
        font = pygame.font.SysFont(None, self.game.scale(200))
        self.game_over = font.render('Game Over!', True, 'white')

        font = pygame.font.SysFont(None, self.game.scale(150))
        self.score = kwargs.get('score')
        self.score_text = font.render(f'Score: {self.score}', True, 'white')
        self.play_again = font.render('Press enter to play again', True, 'white')

    def handle_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.game.current_scene = scenes.Game(self.game)

    def handle_key_press(self, key):
        pass

    def update(self):
        pass

    def draw(self):

        self.game.display.blit(
            self.game_over,
            (
                (self.game.screen_width / 2) - self.game_over.get_width() / 2,
                self.game.scale(50)
            )
        )

        self.game.display.blit(
            self.score_text,
            (
                (self.game.screen_width / 2) - self.score_text.get_width() / 2,
                self.game.scale(250)
            )
        )

        self.game.display.blit(
            self.play_again,
            (
                (self.game.screen_width / 2) - self.play_again.get_width() / 2,
                self.game.scale(550)
            )
        )
