from random import choice, choices
from typing import List

from pygame import Vector2

from engine import *
from objects import *


class ShopState(State):
    def __init__(self, wave: int, player: Player):
        self.player = player
        self.wave = wave
        super().__init__()

        # self.add(player)

        self.deck = self.add(Deck(True))

        for i in range(6):
            self.deck.add_card(self.new_card())

    def new_card(self):
        possibilities = [
            card for Card in ALL_CARDS if (card := Card(InShopCard)).level <= self.wave
        ]
        weights = [(5 - card.level) for card in possibilities]

        return choices(possibilities, weights)[0]

    def draw(self, gfx: "GFX"):
        super().draw(gfx)

        t = text(f"Wave {self.wave} Shop", 32, ORANGE, BIG_FONT)
        r = gfx.blit(t, topright=(W - 10, 10))

        offset = Vector2(0, 4)
        self.player.draw_coins(gfx, self.player.coins, topright=r.bottomright + offset)
        self.player.draw_score(gfx, self.player.score, topleft=r.bottomleft + offset)
