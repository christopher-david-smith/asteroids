import abc

class Scene:
    def __init__(self, game, *args, **kwargs):
        self.game = game
        self.init(*args, **kwargs)

    @abc.abstractmethod
    def init(self, *args, **kwargs):
        pass

    @abc.abstractmethod
    def handle_event(self, event):
        pass

    @abc.abstractmethod
    def handle_key_press(self, key):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self):
        pass
