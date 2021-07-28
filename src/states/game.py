from objects.player import *
from engine import State


class GameState(State):
    BG_COLORS = [
        0x134180,
        0x9463AA,
        0x3C926E,
    ]

    def __init__(self):
        super().__init__()

        self.player = self.add(Player())
        self.spawn()

    def spawn(self):
        ai = EnemyBlockAI()
        for x in range(30):
            self.add(Ennemy((30, -30 - 40 * x), ai))

    def logic(self):
        super().logic()
