#!/usr/bin/env python

import sys
from pathlib import Path



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

sys.path.append(str((Path(__file__).parent / "src").absolute()))

# It is important not to import from SRC
from states.game import GameState
from states.card_test import CardTestState
from engine import SIZE, App, IntegerScaleScreen

if __name__ == "__main__":
    # App(GameState, IntegerScaleScreen(SIZE)).run()
    App(CardTestState, IntegerScaleScreen(SIZE)).run()
