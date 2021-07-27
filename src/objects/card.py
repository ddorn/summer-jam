from typing import Dict, List, Optional
import pygame

from src.engine import *

# TODO: add docstrings to this file

__all__ = ["Transition", "Card"]


class Transition:
    def __init__(
        self,
        obj,
        frame_count,
        *,
        end_pos=None,
        start_pos=None,
        start_rotation=None,
        end_rotation=None,
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
        self.obj: SpriteObject = obj
        self.running = False
        self.frame_counter = -1  # Current frame

        self.frames = frame_count  # length of transition

        self.vel = None
        if start_pos is None:
            start_pos = obj.pos
        if end_pos is not None:
            self.vel = (end_pos - start_pos) / frame_count

        self.rotation = None
        if start_rotation is None:
            start_rotation = obj.rotation
        if end_rotation is not None:
            self.rotation = (end_rotation - start_rotation) / frame_count

    def start(self):
        self.running = True
        self.frame_counter = self.frames

    def logic(self):
        if not self.running:
            return

        if self.vel is not None:
            self.obj.pos += self.vel

        if self.rotation is not None:
            self.obj.rotation += self.rotation

        self.frame_counter -= 1

        if self.frame_counter <= 0:
            self.running = False


class Card(SpriteObject):
    def __init__(
        self,
        pos,
        image,
        offset=(0, 0),
        size=(1, 1),
        vel=(0, 0),
        rotation=0,
    ):

        super().__init__(
            pos, image, offset=offset, size=size, vel=vel, rotation=rotation
        )
        self.transitions: Dict[str, Transition] = {}
        self.shown = False

    def add_transition(self, name: str, transition: Transition):
        self.transitions[name] = transition

    def start_transition(self, name: str):
        self.transitions[name].start()

    def logic(self):
        super().logic()
        for transition in self.transitions.values():
            transition.logic()
