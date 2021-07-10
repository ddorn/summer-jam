from random import randint

import pygame

from src.engine import *
from src.engine.state_transitions import *


class DummyState(State):
    BG_COLOR = 0x321254

    def __init__(self):
        super().__init__()
        self.data = [
            (
                random_in_rect(SCREEN),
                random_rainbow_color(),
                randint(4, 25)
            )
            for _ in range(100)
        ]

    def draw(self, gfx: "GFX"):
        super().draw(gfx)

        for center, color, radius in self.data:
            pygame.draw.circle(gfx.surf, color, center, radius)

    def logic(self):
        super().logic()
        if self.timer > 30:
            self.replace_state(
                SquareSpawnTransistion(self, DummyState())
            )
