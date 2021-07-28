import random
from src.objects.card import Card
from typing import List

from engine import *
from objects import Deck, Player, Ennemy


class CardTestState(State):
    BG_COLORS = [
        0x134180,
        0x9463AA,
        0x3C926E,
    ]

    def __init__(self):
        super().__init__()
        self.player = self.add(Player())
        self.deck = self.add(Deck(self))
        self.spawn()

    def spawn(self):
        # for x in range(30):
        #     self.add(Ennemy((30, -30 - 40 * x)))

        for _ in range(5):
            image = pygame.Surface((60, 100), pygame.SRCALPHA)
            image.fill(random_rainbow_color(60))
            pygame.draw.circle(image, "white", (30, 50), 15, 4)
            self.deck.add_card(Card(image))
