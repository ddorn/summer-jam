from dataclasses import dataclass
import random

import states
from engine import *
from objects import *


@dataclass
class GameValues:
    enemy_damage_boost = 1
    points_bonus = 1


class GameState(State):
    FPS = 60

    def __init__(self):
        super().__init__()

        self.game_values = GameValues()
        self.player = self.add(Player())
        self.deck = self.add(Deck())
        self.spawn()
        self.level_ended = False

    def spawn(self):
        for _ in range(5):
            image = pygame.Surface((80, 120), pygame.SRCALPHA)
            image.fill(random_rainbow_color(80, 40))
            image.blit(
                wrapped_text("Increase fire rate for 10 seconds", 10, (255, 255, 255), 70), (5, 40),
            )
            self.deck.add_card(random.choice(ALL_CARDS)())

        ai = EnemyBlockAI()
        for e in ai.spawn():
            self.add(e)

    def create_inputs(self) -> Inputs:
        inputs = super().create_inputs()

        inputs["pause"] = Button(pygame.K_p)
        inputs["pause"].on_press(self.push_state_callback(states.PauseState, self))

        return inputs

    def logic(self):
        super().logic()

        if self.level_ended:
            return

        if not any(isinstance(e, Enemy) for e in self.objects):
            self.level_ended = True

            @self.add_script_decorator
            def fireworks():
                for _ in range(100):
                    yield from range(6)
                    center = random_in_rect(SCREEN)
                    color = random.choice([ORANGE, RED, GREEN, YELLOW])
                    for i in range(100):
                        self.particles.add(
                            SquareParticle(color)
                            .builder()
                            .at(center, a := uniform(0, 360))
                            # .hsv(a, 0.8)
                            .velocity(random.gauss(3, 0.5))
                            .acceleration(-0.05)
                            .anim_fade()
                            .living(60)
                            .sized(4)
                            .build()
                        )

                self.push_state(states.ShopState(self.player))

    def script(self):
        while True:
            self.particles.add(
                SquareParticle((255, 255, 255))
                .builder()
                .velocity(0)
                .at(random_in_rect(SCREEN))
                .sized(1)
                .anim_fade()
                .living(180)
                .build()
            )
            yield from particles.rrange(random.gauss(14, 4))
