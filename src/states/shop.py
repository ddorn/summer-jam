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
        self.player.draw_score(gfx, self.player.score, topleft=r.bottomleft + offset)
        r2 = self.player.draw_coins(gfx, self.player.coins, topright=r.bottomright + offset)

        def blit(mult=1):
            nonlocal r2
            r2 = gfx.blit(t, topright=r2.bottomright + mult * offset)

        t = text("Selected card", 8, WHITE, SMALL_FONT)
        blit(20)

        card: InGameCard = self.deck.selected_card
        if card is None:
            t = text("None", 16, YELLOW, BIG_FONT)
            blit()
            return

        t = text(card.name, 24, YELLOW)
        blit(0)

        t = wrapped_text(card.description, 16, WHITE, r.width, align_right=True)
        blit(-1)

        t = text("Purchase cost", 8, WHITE, SMALL_FONT)
        blit()

        t = scale(image("coin"), 2)
        blit(0.5)
        color = RED if card.buy_cost > self.player.coins else GREEN
        t = text(str(card.buy_cost), 16, color)
        gfx.blit(t, topright=r2.topleft - offset.yx)

        t = text("Use cost", 8, WHITE, SMALL_FONT)
        blit()

        t = scale(image("coin"), 2)
        blit(0.5)
        t = text(str(card.use_cost), 16, YELLOW)
        gfx.blit(t, topright=r2.topleft - offset.yx)
