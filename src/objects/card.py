from random import gauss
from typing import Dict
import pygame

from src.engine import *

# TODO: add docstrings to this file

__all__ = ["Transition", "Card", "Deck"]


class Transition:
    def __init__(
        self,
        obj,
        frame_count,
        *,
        start_pos=None,
        end_pos=None,
        start_rotation=None,
        end_rotation=None,
        start_size=None,
        end_size=None,
    ):
        """
        Args:
            obj (SpriteObject): The object to do the transition on

            frame_count (int): The number of frames it takes to finish the transiton

            end_pos (Vector2, optional): The position to finish on. Defaults to None.

            start_pos (Vector2, optional): The position to start on. If this is none
                (and end_pos is not None), it will use the object's current position.
                Defaults to None.

            start_rotation (int, optional): The rotation to finish on. Defaults to None.

            end_rotation (int, optional): The rotation to start on. If this is none (and
                end_rotation is not None), it will use the object's current rotation.
                Defaults to None.
        """
        self.obj = obj
        self.running = False
        self.frame_counter = -1  # Current frame

        self.frames = frame_count  # length of transition
        self.modifier = 1

        self.vel = None
        if start_pos is None:
            start_pos = obj.pos
        if end_pos is not None:
            self.vel = (end_pos - start_pos) / frame_count

        self.rotation = None
        if end_rotation is not None:
            if start_rotation is None:
                start_rotation = obj.rotation
            self.rotation = (end_rotation - start_rotation) / frame_count

        self.size = None
        if end_size is not None:
            if start_size is None:
                start_size = obj.size
            self.size = (end_size - start_size) / frame_count

    def start(self, reverse=False):
        if self.running:
            return
        self.running = True
        self.frame_counter = self.frames
        self.modifier = -1 if reverse else 1

    def logic(self):
        if not self.running:
            return

        if self.vel is not None:
            self.obj.pos += self.vel * self.modifier

        if self.rotation is not None:
            self.obj.rotation += self.rotation * self.modifier

        if self.size is not None:
            self.obj.size += self.size * self.modifier

        self.frame_counter -= 1

        if self.frame_counter <= 0:
            self.running = False


class Card(SpriteObject):
    FRAME_COUNT = 20
    SPACING = 55
    ROTATION = -4

    def __init__(self, image, pos=(0, 0), f=None):
        size = image.get_rect().size
        super().__init__(pos, image, offset=(0, 0), size=size, vel=(0, 0), rotation=0)
        self.transitions: Dict[str, Transition] = {}
        self.shown = False
        self.hovered = False
        self.used = False
        self.func = f

    def create_transitions(self, i):
        card_num = 5
        x = (
            (W // 2 - card_num * (self.SPACING / 2))
            + (i * self.SPACING)
            - (self.size[0] - self.SPACING) / 2
        )
        if card_num % 2 == 0:
            r = (card_num / 2 - (i + 0.5)) * self.ROTATION
        else:
            r = (card_num // 2 - i) * self.ROTATION

        pos1 = pygame.Vector2(x, H * -0.1)
        pos2 = pygame.Vector2(W // 2 - (self.size[0] // 2), H * -0.4)

        pos3 = pos2 + (pos1 - pos2) / 6
        pos4 = pos2 + (pos1 - pos2) / 1.4

        # Does not actually scale sprite size, just hitbox
        size1 = pygame.Vector2(self.size)
        size2 = pygame.Vector2(self.size)
        size2.x *= 1 + abs(r) / 12
        size2.y *= 1.1

        self.pos = pos1 if self.shown else pos2
        self.Z = card_num - i
        self.add_transition(
            "show",
            Transition(
                self,
                self.FRAME_COUNT,
                start_pos=pos2,
                end_pos=pos1,
                start_rotation=0,
                end_rotation=r,
            ),
        )
        self.add_transition(
            "hover",
            Transition(
                self,
                self.FRAME_COUNT // 2,
                start_pos=pos2,
                end_pos=pos3,
                start_size=size1,
                end_size=size2,
            ),
        )
        self.add_transition(
            "use",
            Transition(
                self,
                self.FRAME_COUNT,
                start_pos=pos3,
                end_pos=pos4,
            ),
        )

    def add_transition(self, name: str, transition: Transition):
        self.transitions[name] = transition

    def start_transition(self, name: str, reverse=False):
        self.transitions[name].start(reverse)

    def logic(self):
        super().logic()
        rect = pygame.Rect(0, 0, *self.size)
        rect.center = self.sprite_center
        self.state.debug.rectangle(rect, (0, 0, 0))

        if not self.used and not self.transitions["show"].running:
            colliding = rect.collidepoint(pygame.mouse.get_pos())

            if colliding and not self.hovered and not self.transitions["hover"].running:
                self.start_transition("hover")
                self.hovered = True

            elif (
                not colliding and self.hovered and not self.transitions["hover"].running
            ):
                self.start_transition("hover", reverse=True)
                self.hovered = False

            if self.hovered and pygame.mouse.get_pressed(3)[0]:
                self.use()

        elif self.used:
            if not self.transitions["use"].running:
                for _ in particles.rrange(gauss(15, 5)):
                    self.state.particles.add(
                        CircleParticle()
                        .builder()
                        .at(self.sprite_center, gauss(0, 180))
                        .velocity(gauss(1.2, 0.4))
                        .sized(uniform(2, 4))
                        .living(45)
                        .hsv(0, 0.1, 100)
                        .anim_fade()
                        .build()
                    )
                self.alive = False

        for transition in self.transitions.values():
            transition.logic()

    def use(self):
        if self.func:
            self.func(self.state)

        self.start_transition("use")
        self.used = True


class Deck(Object):
    def __init__(self):
        super().__init__((0, 0))
        self.cards = []

    def add_card(self, *cards):
        self.cards.extend(cards)
        for card in cards:
            self.state.add(card)

        for i, card in enumerate(self.cards):
            card.create_transitions(i)
            print(i)

    def show_cards(self, _):
        for card in self.cards:
            if not card.shown:
                card.start_transition("show")
                card.shown = True

    def hide_cards(self, _):
        for card in self.cards:
            if card.shown:
                card.start_transition("show", reverse=True)
                card.shown = False

    def create_inputs(self):
        hide = Button(pygame.K_UP, pygame.K_w).on_press(self.hide_cards)
        show = Button(pygame.K_DOWN, pygame.K_s).on_press(self.show_cards)

        return {
            "show cards": show,
            "hide cards": hide,
        }
