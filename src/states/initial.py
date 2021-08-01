from random import randint

import pygame

from engine import *
from engine.state_transitions import *


class InitialState(State):
    BG_COLOR = 0x321254

    def __init__(self):
        super().__init__()
        self.data = [
            (random_in_rect(SCREEN), random_rainbow_color(70, 80), randint(4, 25))
            for _ in range(100)
        ]

    def draw(self, gfx: "GFX"):
        super().draw(gfx)

        for center, color, radius in self.data:
            pygame.draw.circle(gfx.surf, color, center, radius)

    def logic(self):
        super().logic()
        if self.timer > 30:
            next_ = GameState()
            self.replace_state(SquarePatternTransition.random(self, next_))
