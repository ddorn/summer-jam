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
    "Firerate I", 200, 5, "Double the firerate for 5 seconds", "fire_rate", data=(2, 5),
)
@card(
    "Firerate II", 350, 9, "Triple the firerate for 4 seconds", "fire_rate", data=(3, 4),
)
@card(
    "Firerate III", 500, 12, "Triple the firerate for 8 seconds", "fire_rate", data=(3, 8),
)
def change_fire_rate(state, data):

    state.player.fire_cooldown.auto_lock /= data[0]

    @state.do_later(data[1] * SECOND)
    def change_back():
        state.player.fire_cooldown.auto_lock *= data[0]


@card("Heal I", 100, 15, "Heal 10% of life", "fire_rate", data=10)
@card("Heal II", 200, 30, "Heal 25% of life", "fire_rate", data=25)
@card("Heal III", 200, 200, "Heal completely", "fire_rate", data=100)
def heal(state, data):
    state.player.heal(state.player.max_life * data / 100)


@card("More bullets I", 200, 10, "Two bullets per shot for 5 seconds", "fire_rate", data=(2, 5))
@card("More bullets II", 350, 15, "Three bullets per shot for 4 seconds", "fire_rate", data=(3, 4))
@card("More bullets III", 500, 20, "Three bullets per shot for 8 seconds", "fire_rate", data=(3, 8))
@card("More bullets IIII", 500, 200, "Permanently shoot one more bullet", "fire_rate", data=None)
def heal(state, data):
    if data is None:
        state.player.bullets += 1
    else:
        state.player.bullets += data[0] - 1

        @state.do_later(data[1] * SECOND)
        def change_back():
            state.player.bullets -= data[0] - 1
