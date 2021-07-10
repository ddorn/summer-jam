from math import ceil
from random import shuffle

from .constants import *
from .gfx import GFX
from .state_machine import State


class StateTransition(State):
    def __init__(self, previous: State, next_: State, duration=None):
        if duration is None:
            duration = 60

        super().__init__()
        self.previous = previous
        self.next = next_
        self.duration = duration  # frames

    def next_surface(self, gfx):
        next_surface = pygame.Surface(gfx.surf.get_size())
        self.next.draw(GFX(next_surface))
        return next_surface

    def logic(self):
        super().logic()
        if self.progress == 1:
            self.replace_state(self.next)

    @property
    def progress(self):
        return min(1, self.timer / self.duration)


class FadeTransition(StateTransition):
    def __init__(self, previous, next_, duration=None):
        super().__init__(previous, next_, duration)

    def draw(self, gfx: "GFX"):
        super().draw(gfx)

        self.previous.draw(gfx)

        next_surface = self.next_surface(gfx)

        next_surface.set_alpha(int(255 * self.progress))
        gfx.blit(next_surface)


class SquareSpawnTransistion(StateTransition):
    def __init__(self, previous: State, next_: State, ):

        self.square_size = 32  # pixels
        self.delay = 64

        self.squares = [
            [None] * ceil(H / self.square_size)
            for x in range(0, W, self.square_size)
        ]

        self.order = [
            (x, y)
            for x in range(len(self.squares))
            for y in range(len(self.squares[0]))
        ]
        shuffle(self.order)

        duration = len(self.order) + 2 * self.square_size + self.delay
        super().__init__(previous, next_, duration)

    def logic(self):
        super().logic()

        if self.order:
            x, y = self.order.pop()
            self.squares[x][y] = self.timer

    def draw(self, gfx: "GFX"):
        super().draw(gfx)

        self.previous.draw(gfx)
        next_surface = self.next_surface(gfx)

        for x, column in enumerate(self.squares):
            for y, square in enumerate(column):
                if square is not None:
                    life = self.timer - square

                    new_surf_size = min(self.square_size, life - self.square_size - self.delay)
                    if new_surf_size > 0:
                        r = self.get_rect(x, y, 32)
                        gfx.surf.blit(next_surface, r.topleft, r)
                        life = self.square_size - new_surf_size

                    if life > 0:
                        black_size = min(self.square_size, life)
                        pygame.draw.rect(gfx.surf, 'black', self.get_rect(x, y, black_size))

    def get_rect(self, x, y, size):
        x = (x + 0.5) * self.square_size
        y = (y + 0.5) * self.square_size
        rect = pygame.Rect(0, 0, size, size)
        rect.center = x, y
        return rect
