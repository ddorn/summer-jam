import random
from typing import List

from engine import *
from objects import Card, Transition, Player, Ennemy


class CardTestState(State):
    BG_COLORS = [
        0x134180,
        0x9463aa,
        0x3c926e,
    ]
    def __init__(self):
        super().__init__()

        card_num = random.randint(3, 7)
        self.cards: List[Card] = []
        spacing = 50
        rotation = 4
        card_size = (60, 100)
        frame_count = 25

        for i in range(card_num):
            image = pygame.Surface(card_size, pygame.SRCALPHA)
            image.fill(random_rainbow_color(60))
            pygame.draw.circle(image, "white", (30, 50), 15, 4)

            x = (
                (W // 2 - card_num * (spacing / 2))
                + (i * spacing)
                - (card_size[0] - spacing) / 2
            )
            if card_num % 2 == 0:
                r = (card_num / 2 - (i + 0.5)) * rotation
            else:
                r = (card_num // 2 - i) * rotation

            pos1 = pygame.Vector2(x, H // 4 * 3.2)
            pos2 = pygame.Vector2(W // 2 - (card_size[0] // 2), H * 1.2)

            card = Card(pos2, image)
            card.Z = card_num - i
            card.add_transition(
                "show",
                Transition(
                    card,
                    frame_count,
                    start_pos=pos2,
                    end_pos=pos1,
                    start_rotation=0,
                    end_rotation=r,
                ),
            )
            card.add_transition(
                "hide",
                Transition(
                    card,
                    frame_count,
                    start_pos=pos1,
                    end_pos=pos2,
                    start_rotation=r,
                    end_rotation=0,
                ),
            )
            self.cards.append(self.add(card))

        self.player = self.add(Player())
        self.spawn()

    def spawn(self):
        for x in range(30):
            self.add(Ennemy((30, -30 - 40* x)))

    def show_cards(self, _):
        for card in self.cards:
            if not card.shown:
                card.start_transition("show")
                card.shown = True

    def hide_cards(self, _):
        for card in self.cards:
            if card.shown:
                card.start_transition("hide")
                card.shown = False

    def create_inputs(self) -> Inputs:
        inputs = super().create_inputs()

        inputs["show_cards"] = Button(pygame.K_UP, pygame.K_w)
        inputs["show_cards"].on_press(self.show_cards)

        inputs["hide_cards"] = Button(pygame.K_DOWN, pygame.K_s)
        inputs["hide_cards"].on_press(self.hide_cards)

        return inputs

    def draw(self, gfx: "GFX"):
        super().draw(gfx)
        pygame.draw.line(gfx.surf, (200, 200, 200), (W // 2, 0), (W // 2, H))
