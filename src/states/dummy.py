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
                random_rainbow_color(70, 80),
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
            next_ = DummyState() if isinstance(self, DummyState2) else DummyState2()
            self.replace_state(
                SquarePatternTransition.random(self, next_)
            )

class DummyState2(DummyState):
    BG_COLOR = 0x541232

