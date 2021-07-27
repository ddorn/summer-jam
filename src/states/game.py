from objects import *
from engine import App, State


class GameState(State):
    BG_COLORS = [
        0x134180,
        0x9463aa,
        0x3c926e,
    ]
    def __init__(self):
        super().__init__()

        self.player = self.add(Player())
        self.spawn()

    def spawn(self):
        for x in range(30):
            self.add(Ennemy((30, -30 - 40* x)))

    def logic(self):
        super().logic()