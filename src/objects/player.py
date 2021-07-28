from engine import *

__all__ = ["Player", "Ennemy", "Bullet"]


class Player(Object):
    VELOCITY = 4
    SPAWN = W / 2, H - 10
    FIRE_COOLDOWN = 12

    def __init__(self):
        super().__init__(self.SPAWN, (20, 12))
        self.fire_cooldown = Cooldown(self.FIRE_COOLDOWN)

    def logic(self):
        super().logic()
        self.fire_cooldown.tick()

    def draw(self, gfx: "GFX"):
        gfx.rect(*self.pos, *self.size, "orange", anchor="center")

    def move(self, axis):
        self.pos.x += axis.value * self.VELOCITY
        self.pos.x = clamp(self.pos.x, self.size.x / 2, W - self.size.x / 2)

    def fire(self, _button):
        if self.fire_cooldown.fire():
            self.state.add(Bullet(self.pos))

    def create_inputs(self):
        motion = Axis([pygame.K_a, pygame.K_LEFT], [pygame.K_d, pygame.K_RIGHT]).always_call(
            self.move
        )
        fire = Button(pygame.K_SPACE).on_press(self.fire)
        return {
            "player motion": motion,
            "fire": fire,
        }


class Bullet(Object):
    VELOCITY = 7

    def __init__(self, pos, friend=True):
        super().__init__(pos, vel=(0, -self.VELOCITY))
        self.friend = friend

    def logic(self):
        super().logic()
        if not SCREEN.inflate(10, 10).collidepoint(self.pos):
            self.alive = False

        targets = self.state.get_all(Ennemy) if self.friend else [self.state.player]

        for target in targets:
            if target.rect.collidepoint(self.pos):
                target.alive = False
                self.alive = False

                if self.friend:
                    # Todo: increase score
                    pass
                return

    def draw(self, gfx: "GFX"):
        gfx.rect(*self.pos, 5, 5, "white", anchor="center")


class Ennemy(SpriteObject):
    EDGE = 30
    SPEED = 1
    ROW_HEIGHT = 45
    SCALE = 2

    IMAGE = Assets.Images.enemies(0)
    IMAGE.set_palette_at(1, (255, 255, 255))
    IMAGE = auto_crop(IMAGE)

    def __init__(self, pos):
        super().__init__(pos, self.IMAGE, vel=(self.SPEED, 0))
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

    def on_death(self):
        self.state.particles.add_explosion(self.center,)
