from collections import defaultdict
from typing import Set

from pygame import Vector2

from engine import *

__all__ = ["Ennemy", "EnemyBlockAI", "SnakeAI"]


class Ennemy(Entity):
    EDGE = 30
    SPEED = 1
    SCALE = 2
    INITIAL_LIFE = 100

    FIRE_DAMAGE = 100

    IMAGE = Assets.Images.enemies(0)
    IMAGE.set_palette_at(1, (255, 255, 255))
    IMAGE = auto_crop(IMAGE)

    def __init__(self, pos, ai):
        super().__init__(pos, self.IMAGE, size=None, vel=(self.SPEED, 0))
        self.ai = ai
        ai.add(self)

    def fire(self):
        from objects import Bullet

        boost = self.state.game_values.enemy_damage_boost
        self.state.add(Bullet(self.center, damage=self.FIRE_DAMAGE * boost, friend=False))

    def logic(self):
        self.ai.logic(self)
        super().logic()
        if randrange(500) == 42:
            self.fire()

    def push_back(self, rows, duration=30):
        @self.add_script_decorator
        def script():
            target = rows * self.ai.ROW_HEIGHT
            k = 3
            scale = exp_impluse_integral(k) * duration
            print(scale)
            for i in range(duration):
                dy = exp_impulse(i / duration, k) / scale * target
                self.pos.y -= dy
                yield

    def on_death(self):
        self.state.particles.add_explosion(self.center,)


class AI:
    EDGE = 45  # min distance to sides
    ROW_HEIGHT = 30

    def __init__(self):
        # All the enemies controled by the same AI
        self.controled: Set[Ennemy] = set()

        # Hack to have the logic called only once per frame
        self.called_on = set()

    def logic(self, enemy):
        self.controled = {e for e in self.controled if e.alive}

    def set_direction(self, x_direction, y_direction):
        for enemy in self.controled:
            enemy.vel = Vector2(enemy.SPEED * x_direction, enemy.SPEED * y_direction)

    def add(self, enemy):
        self.controled.add(enemy)

    def call_once_per_frame(self, enemy) -> bool:
        # The logic will run only when called with an enemy
        # which is in the called_on set, which should mean
        # that it has been called on every enemy in between, and thus
        # it is the next frame.
        if enemy in self.called_on or not self.called_on:
            self.called_on = {enemy}
            return True
        else:
            self.called_on.add(enemy)
            return False


class EnemyBlockAI(AI):
    def __init__(self):
        super().__init__()
        self.go_down_duration = 0

        self.max_controled = 0
        self.direction = 1  # right / -1 left

    def logic(self, enemy):

        if not self.call_once_per_frame(enemy):
            return

        self.max_controled = max(self.max_controled, len(self.controled))

        min_x = min(e.pos.x for e in self.controled)
        max_x = max(e.pos.x + e.size.x for e in self.controled)

        wall_left = min_x < self.EDGE
        wall_right = max_x > W - self.EDGE

        speed_boost = chrange(
            len(self.controled), (0, self.max_controled), (1, 3), power=3, flipped=True
        )

        self.go_down_duration -= 1
        if self.go_down_duration > 0:
            pass
        elif self.go_down_duration == 0:
            self.set_direction(self.direction, 0)
        elif wall_left or wall_right:
            self.direction *= -1  # swap direction for next row
            self.go_down_duration = int(self.ROW_HEIGHT / speed_boost / Ennemy.SPEED)
            self.set_direction(0, 1)  # down

        for enemy in self.controled:
            enemy.vel.scale_to_length(enemy.SPEED * speed_boost)

        # We call super only later, because sometimes the AI logic is called
        # even if the enemy is dead, because it was killed in the same frame
        # and before its logic. This causes a problem for the last enemy.
        # As min() and max() have empty collections.
        super().logic(enemy)

    def spawn(self, rows=4, cols=10):
        for row in range(rows):
            for col in range(cols):
                x = chrange(col, (0, cols - 1), (self.EDGE * 3, W - self.EDGE * 3))
                y = self.EDGE + row * self.ROW_HEIGHT
                yield Ennemy((x, y), self)


class SnakeAI(AI):
    def __init__(self):
        super().__init__()
        self.goals = list(self.checkpoints())
        self.current_goals = defaultdict(int)

    def logic(self, enemy):
        super().logic(enemy)

        current = self.current_goals[enemy]

        try:
            if enemy.pos.distance_to(self.goals[current]) < enemy.SPEED:
                self.current_goals[enemy] += 1
            goal = self.goals[current]
        except IndexError:
            # No more goal.
            enemy.alive = False
            return

        self.vel = (goal - enemy.pos).normalize() * (enemy.SPEED)

    def checkpoints(self):
        y = self.EDGE
        while y < H + self.ROW_HEIGHT:
            yield self.EDGE, y
            yield W - self.EDGE, y
            yield W - self.EDGE, y + self.ROW_HEIGHT
            yield self.EDGE, y + self.ROW_HEIGHT
            y += 2 * self.ROW_HEIGHT

    def add(self, enemy):
        super().add(enemy)
