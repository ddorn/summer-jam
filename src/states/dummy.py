from src.engine import *


class DummyState(State):
    def __init__(self):
        super().__init__()

        self.add(Title("The Game", "purple"))