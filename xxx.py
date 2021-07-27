#!/usr/bin/env python

import sys


def abort_dependency(name, got=""):
    if got:
        # The leading space is important.
        got = f" but found {got}"
    print(f"XXX needs {name} to run{got}.")
    print("In case you have troubles to get the dependencies you can head to")
    print("\thttps://cozyfractal.itch.io/XXX")
    print("to find Linux and Windows executables.")
    sys.exit(1)


if sys.version_info < (3, 8):
    abort_dependency("python 3.8", "python " + sys.version.split()[0])

try:
    import pygame
except ImportError:
    abort_dependency("pygame 2.0.1")

if pygame.version.vernum < (2, 0, 1):
    abort_dependency(f"pygame 2.0.1", f"pygame {pygame.version.ver}")

from src.engine import SIZE, App, IntegerScaleScreen
from src.states.card_test import CardTestState

if __name__ == "__main__":
    App(CardTestState, IntegerScaleScreen(SIZE)).run()
