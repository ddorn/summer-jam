from dataclasses import dataclass
from random import choice

import states
from engine import *
from objects import *


@dataclass
class GameValues:
    enemy_damage_boost = 1
    points_bonus = 1


class CardTestState(State):
    BG_COLORS = [
        0x134180,
        0x9463AA,
        0x3C926E,
    ]
    FPS = 60

    def __init__(self):
        super().__init__()

        self.game_values = GameValues()
        self.player = self.add(Player())
        self.deck = self.add(Deck())
        self.spawn()

    def spawn(self):
        for _ in range(5):
            image = pygame.Surface((80, 120), pygame.SRCALPHA)
            image.fill(random_rainbow_color(80, 40))
            image.blit(
                wrapped_text("Increase fire rate for 10 seconds", 10, (255, 255, 255), 70), (5, 40),
            )
            self.deck.add_card(choice(ALL_CARDS)())

        ai = EnemyBlockAI()
        for e in ai.spawn():
            self.add(e)

    def create_inputs(self) -> Inputs:
        inputs = super().create_inputs()

        inputs["pause"] = Button(pygame.K_p)
        inputs["pause"].on_press(self.push_state_callback(states.PauseState, self))

        return inputs
