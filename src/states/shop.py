from engine import *
from objects import *


class ShopState(State):
    def __init__(self, player: Player):
        self.player = player
        super().__init__()
