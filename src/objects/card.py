from random import gauss
from typing import Dict

import pygame
from pygame import Surface, Vector2

from src.engine import *

# TODO: add docstrings to this file

__all__ = ["Transition", "BaseCard", "Deck"]


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


class BaseCard(SpriteObject):
    FRAME_COUNT = 20
    SPACING = 85

    def __init__(self, image, name, description, effect, buy_cost, use_cost, pos=(0, 0)):
        self.name = name
        self.description = description
        self.effect = effect
        self.buy_cost = buy_cost
        self.use_cost = use_cost

        size = image.get_rect().size
        super().__init__(pos, image, offset=(0, 0), size=size, vel=(0, 0), rotation=0)
        self.transitions: Dict[str, Transition] = {}
        self.shown = False
        self.hovered = False
        self.used = False
        self.using_controller = False

    def create_transitions(self, i):
        card_num = 5
        x = (
            (W // 2 - card_num * (self.SPACING / 2))
            + (i * self.SPACING)
            - (self.size[0] - self.SPACING) / 2
        )

        pos1 = pygame.Vector2(W // 2 - (self.size[0] // 2), H * -0.4)
        pos2 = pygame.Vector2(x, H * -0.15)

        pos3 = pygame.Vector2(x, 10)
        pos4 = pygame.Vector2(SCREEN.center) - self.size // 2

        # Does not actually scale sprite size, just hitbox
        size1 = pygame.Vector2(self.size)
        size2 = pygame.Vector2(self.size)
        size2.y *= 1.2
        size2.x *= 1.14

        self.pos = pos2 if self.shown else pos1
        self.Z = card_num - i
        self.add_transition(
            "show", Transition(self, self.FRAME_COUNT, start_pos=pos1, end_pos=pos2,),
        )
        self.add_transition(
            "hover",
            Transition(
                self,
                self.FRAME_COUNT // 4,
                start_pos=pos2,
                end_pos=pos3,
                start_size=size1,
                end_size=size2,
            ),
        )
        self.add_transition(
            "use", Transition(self, self.FRAME_COUNT, start_pos=pos3, end_pos=pos4,),
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

        if pygame.mouse.get_rel() != (0, 0):
            self.using_controller = False
            for card in self.state.deck.cards:
                card.using_controller = False

        if not self.using_controller and not self.used and not self.transitions["show"].running:
            colliding = rect.collidepoint(pygame.mouse.get_pos())

            if colliding and not self.hovered and not self.transitions["hover"].running:
                self.hover(True)

            elif not colliding and self.hovered and not self.transitions["hover"].running:
                self.hover(False)

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
        if not self.shown or not self.hovered:
            return

        if self.effect:
            self.effect(self.state)

        self.start_transition("use")
        self.used = True

    def hover(self, on=True, controller=False):
        if not self.shown or self.transitions["hover"].running or on == self.hovered:
            return

        self.start_transition("hover", reverse=not on)
        self.hovered = on
        self.using_controller = controller

    def show(self, on=True):
        if self.hovered:
            self.hover(False)

        self.start_transition("show", reverse=not on)
        self.shown = on


class InGameCard(BaseCard):
    def __init__(self, icon_surface: Surface, name, descrition, effect, buy_cost, use_cost):
        img = self.compute_card_image(icon_surface, name, use_cost)

        super().__init__(img, name, descrition, effect, buy_cost, use_cost)

    def compute_card_image(self, icon_surface, name: str, use_cost):
        icon_surface = scale(icon_surface, 2)
        bg_color = icon_surface.get_at((0, 0))
        text_color = "black"
        font_size = 12
        w, h = 80, 120

        # Make the card transparent
        img = Surface((w, h))
        img.fill("pink")
        img.set_colorkey("pink")

        pygame.draw.rect(img, bg_color, (0, 0, w, h - 10), border_radius=9)
        pygame.draw.rect(img, ORANGE, (0, 0, w, h - 10), width=1, border_radius=9)

        r = icon_surface.get_rect()
        r.midbottom = (w / 2, h - 18)
        img.blit(icon_surface, r)

        t = wrapped_text(name, 15, text_color, w - 4)
        img.blit(t, t.get_rect(midtop=(40, 8)))

        # display cost
        coin = image("coin")
        t = text(str(use_cost), font_size, text_color, SMALL_FONT)
        t = auto_crop(t)

        r = pygame.Rect(11, 0, 9 + coin.get_width() + t.get_width() + 2, 16)
        r.centery = h - 10 - 1
        pygame.draw.rect(img, YELLOW, r, border_radius=9999)
        pygame.draw.rect(img, ORANGE, r, width=1, border_radius=9999)
        # coin icon
        r = img.blit(coin, coin.get_rect(midright=r.midright + Vector2(-4, 0)))
        # cost text
        img.blit(t, t.get_rect(midright=r.midleft - Vector2(2, 0)))

        # Level indication
        level = name.rpartition(" ")[2]
        level = ["I", "II", "III", "IV"].index(level) + 1
        star = auto_crop(image("star"))
        r = star.get_rect(midright=(w - 10, h - 11))
        # r = pygame.Rect(0, 0, 8 + t.get_width(), 14)
        # r.centery = h - 10 - 1
        # r.right = w - 12
        for i in range(level):
            img.blit(star, r)
            r.x -= r.w + 1
            if i == 2:
                r.right = w - 14
                r.y -= 6

        # t = auto_crop(text(str(level), font_size, text_color, SMALL_FONT))

        # pygame.draw.rect(img, YELLOW, r, border_radius=9999)
        # pygame.draw.rect(img, ORANGE, r, width=1, border_radius=9999)
        # img.blit(t, t.get_rect(center=r.center))

        return img


class Deck(Object):
    def __init__(self):
        super().__init__((0, 0))
        self.cards = []
        self.selected = 0
        self.shown = False

    def script(self):
        yield
        self.toggle_cards(0)

    def add_card(self, *cards):
        self.selected = 0
        self.cards.extend(cards)
        for card in cards:
            self.state.add(card)

        for i, card in enumerate(self.cards):
            card.create_transitions(i)

    def toggle_cards(self, _):
        self.shown = not self.shown
        for card in self.cards:
            card.show(not card.shown)

    def change_selected_r(self, _):
        if not self.cards or self.selected > len(self.cards) or not self.shown:
            return 

        try:
            if self.cards[self.selected].hovered:
                self.cards[self.selected].hover(False, True)
        except IndexError:
            pass
        self.selected = (self.selected + 1) % len(self.cards)
        self.cards[self.selected].hover(True, True)

    def change_selected_l(self, _):
        if not self.cards or self.selected > len(self.cards) or not self.shown:
            return

        try:
            if self.cards[self.selected].hovered:
                self.cards[self.selected].hover(False, True)
        except IndexError:
            pass
        self.selected = (self.selected - 1) % len(self.cards)
        self.cards[self.selected].hover(True, True)

    def use_card(self, _):
        if not self.cards or self.selected > len(self.cards) or not self.shown:
            return

        self.cards[self.selected].use()
        del self.cards[self.selected]
        try:
            self.selected = self.selected % len(self.cards)
            self.cards[self.selected].hover(True, True)
        except (ZeroDivisionError, IndexError):
            pass  # self.cards is empty after usage

    def create_inputs(self):
        toggle = Button(MouseButtonPress(3), JoyButton(3), pygame.K_e).on_press(self.toggle_cards)
        change_select_l = Button(JoyHatButton(1, -1, use_ps4_buttons=True), pygame.K_LEFT).on_press(
            self.change_selected_l
        )
        change_select_r = Button(JoyHatButton(1, 1, use_ps4_buttons=True), pygame.K_RIGHT).on_press(
            self.change_selected_r
        )
        use = Button(JoyButton(0), pygame.K_DOWN).on_press(self.use_card)
        return {
            "toggle cards": toggle,
            "change right": change_select_r,
            "change left": change_select_l,
            "use card": use,
        }

    def logic(self):
        super().logic()
        for i, card in enumerate(self.cards):
            if not card.alive:
                del self.cards[i]

    def draw(self, gfx: "GFX"):
        super().draw(gfx)
        if self.shown:
            label = text("E/Y/Triangle to hide cards", 16, (50, 50, 50))

            gfx.surf.blit(label, label.get_rect(bottomright=(W, H)))
