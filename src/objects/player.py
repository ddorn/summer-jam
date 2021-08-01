from engine import *
import states

__all__ = ["Player", "Bullet"]


class Player(Entity):
    VELOCITY = 4
    SPAWN = W / 2, H - 20
    FIRE_COOLDOWN = 0
    INITIAL_LIFE = 1000
    SIZE = (20, 12)
    FIRE_DAMAGE = 60

    def __init__(self):
        img = pygame.Surface(self.SIZE)
        img.fill(GREEN)
        super().__init__(self.SPAWN, img, size=self.SIZE)
        self.fire_cooldown = Cooldown(self.FIRE_COOLDOWN)
        self.health_bar = HealthBar((0, 0, 30, 1), RED, self)
        self.fire_power = self.FIRE_DAMAGE
        self.bullets = 2

    def logic(self):
        super().logic()
        self.fire_cooldown.tick()
        self.health_bar.logic()
        self.health_bar.center = self.center + (0, self.size.y / 2 + 6)

    def draw(self, gfx: "GFX"):
        super(Player, self).draw(gfx)
        self.health_bar.draw(gfx)

    def move(self, axis):
        self.pos.x += axis.value * self.VELOCITY
        self.pos.x = clamp(self.pos.x, self.size.x / 2, W - self.size.x / 2)

    def fire(self, _button):
        if self.fire_cooldown.fire():
            w = 5 * (self.bullets - 1)
            for i in range(self.bullets):
                x = chrange(i, (0, self.bullets - 1), (-w / 2, w / 2))
                y = abs(i - (self.bullets - 1) / 2) * 3 - 5
                self.state.add(Bullet(self.center + (x, y), damage=self.fire_power))

    def create_inputs(self):
        motion = Axis(pygame.K_a, pygame.K_d, JoyAxis(JOY_HORIZ_LEFT),).always_call(self.move)

        fire = Button(pygame.K_SPACE, MouseButtonPress(1), JoyButton(0)).on_press_repeated(
            self.fire, 0
        )
        return {
            "player motion": motion,
            "fire": fire,
        }

    def on_death(self):
        self.state.particles.add_explosion(self.center, 200, 1000, "red")

        @self.state.do_later(60)
        def new_game():
            self.state.replace_state(states.CardTestState())


class Bullet(Object):
    VELOCITY = 7
    SIZE = (2, 5)

    def __init__(self, pos, damage=100, friend=True):
        direction = -self.VELOCITY if friend else self.VELOCITY / 2
        super().__init__(pos, self.SIZE, vel=(0, direction))
        self.friend = friend
        self.damage = damage

    def logic(self):
        super().logic()
        if not SCREEN.inflate(10, 10).collidepoint(self.pos):
            self.alive = False

        targets = self.state.get_all("Ennemy") if self.friend else [self.state.player]

        target: Entity
        for target in targets:
            if target.rect.colliderect(self.rect):
                target.damage(self.damage)
                self.alive = False

                if self.friend:
                    # Todo: increase score
                    pass
                return

    def draw(self, gfx: "GFX"):
        color = "white" if self.friend else "red"
        gfx.rect(*self.rect, color)
