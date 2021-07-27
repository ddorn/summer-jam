import pygame
from pygame import Vector2

from engine import *

__all__ = ["Player", "Ennemy", "Bullet"]


class Player(Object):
    VELOCITY = 4
    SPAWN = W / 2, H - 10
    FIRE_COOLDOWN = 8
    def __init__(self):
        super().__init__(self.SPAWN, (20, 12))
        self.fire_cooldown = self.FIRE_COOLDOWN

    def logic(self):
        super().logic()
        self.fire_cooldown -= 1

    def draw(self, gfx: "GFX"):
        gfx.rect(*self.pos, *self.size, "orange", anchor="center")

    def move(self, axis):
        self.pos.x += axis.value * self.VELOCITY

    def fire(self, button):
        if button.pressed and self.fire_cooldown < 0:
            self.state.add(Bullet(self.pos))
            self.fire_cooldown = self.FIRE_COOLDOWN

    def create_inputs(self):
        motion = Axis([pygame.K_a, pygame.K_LEFT], [pygame.K_d, pygame.K_RIGHT]).always_call(self.move)
        fire = Button(pygame.K_SPACE).always_call(self.fire)
        return {
            "player motion": motion,
            "fire": fire,
        }

class Bullet(Object):
    VELOCITY = 7

    def __init__(self, pos):
        super().__init__(pos, vel=(0, -self.VELOCITY))

    def logic(self):
        super().logic()
        if not SCREEN.inflate(10, 10).collidepoint(self.pos):
            self.alive = False

        for enemy in self.state.get_all(Ennemy):
            if enemy.rect.collidepoint(self.pos):
                enemy.alive = False
                self.alive = False
                return


    def draw(self, gfx: "GFX"):
        gfx.rect(*self.pos, 5, 5, "white", anchor="center")


class Ennemy(SpriteObject):
    EDGE = 30
    SPEED = 3
    ROW_HEIGHT = 45

    def __init__(self, pos):
        super().__init__(pos, scale(image("enemy"), 0.2), vel=(self.SPEED, 0))
        self.goals = list(self.checkpoints())

    def checkpoints(self):
        y = self.EDGE
        while y < H + self.ROW_HEIGHT:
            yield self.EDGE, y
            yield W - self.EDGE, y
            yield W - self.EDGE, y + self.ROW_HEIGHT
            yield self.EDGE, y + self.ROW_HEIGHT
            y += 2 * self.ROW_HEIGHT

    def logic(self):
        if self.goals and self.pos.distance_to(self.goals[0]) < self.SPEED:
            self.goals.pop(0)

        if not self.goals:
            self.alive = False
            return

        goal = self.goals[0]
        self.vel = (goal - self.pos).normalize() * (self.SPEED)

        super().logic()
