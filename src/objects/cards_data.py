from engine import *
from .card import InGameCard

__all__ = ["ALL_CARDS"]

ALL_CARDS = []
SECOND = 60


def card(name, cost, use_cost, descrition, image_name, *, data=None):
    def decorator(effect):
        def partial_card(cls=InGameCard):
            return cls(
                image(image_name),
                name,
                descrition,
                effect=lambda state: effect(state, data),
                buy_cost=cost,
                use_cost=use_cost,
            )

        ALL_CARDS.append(partial_card)

        return effect

    return decorator


@card(
    "Firerate I", 200, 5, "Double the firerate for 15 seconds", "fire_rate", data=(2, 15),
)
@card(
    "Firerate II", 350, 9, "Triple the firerate for 10 seconds", "fire_rate", data=(3, 10),
)
@card(
    "Firerate III", 500, 12, "Triple the firerate for 20 seconds", "fire_rate", data=(3, 20),
)
def change_fire_rate(state, data):

    state.player.fire_cooldown.auto_lock /= data[0]

    @state.do_later(data[1] * SECOND)
    def change_back():
        state.player.fire_cooldown.auto_lock *= data[0]
