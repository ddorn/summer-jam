from dataclasses import dataclass
import random

import states
from engine import *
from objects import *
from objects.levels import level


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
        self.wave = 0
        self.level_ended = False
        self.go_next_level()

    def spawn(self):
        for _ in range(5):
            self.deck.add_card(random.choice(ALL_CARDS)())

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
                for _ in range(0):
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

                self.push_state(states.ShopState(self.wave, self.player))
                self.go_next_level()

    def go_next_level(self):
        self.wave += 1
        self.level_ended = False
        self.player.go_next_level()

        for enemy in EnemyBlockAI().spawn_wave(self.wave):
            self.add(enemy)

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
