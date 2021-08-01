from engine import *
from .card import InGameCard

__all__ = ["ALL_CARDS"]

ALL_CARDS = []
SECOND = 60


def card(name, cost, use_cost, descrition, sprite_idx, *, data=None):
    def decorator(effect):
        def partial_card(cls=InGameCard):
            return cls(
                scale(auto_crop(Assets.Images.cards(sprite_idx)), 4),
                name,
                descrition,
                effect=lambda state: effect(state, data),
                buy_cost=cost,
                use_cost=use_cost,
                blueprint=partial_card,
            )

        ALL_CARDS.append(partial_card)

        return effect

    return decorator


@card(
    "Firerate I", 200, 5, "Double the firerate for 5 seconds", 7, data=(2, 5),
)
@card(
    "Firerate II", 350, 9, "Triple the firerate for 4 seconds", 7, data=(3, 4),
)
@card(
    "Firerate III", 500, 12, "Triple the firerate for 8 seconds", 7, data=(3, 8),
)
def change_fire_rate(state, data):

    state.player.fire_cooldown.auto_lock /= data[0]

    @state.do_later(data[1] * SECOND)
    def change_back():
        state.player.fire_cooldown.auto_lock *= data[0]


@card("Heal I", 100, 15, "Heal 100HP", 0, data=100)
@card("Heal II", 200, 30, "Heal 200HP", 0, data=200)
@card("Heal III", 300, 60, "Heal 500HP", 0, data=500)
@card("Heal IV", 200, 200, "Heal completely", 0, data=None)
def heal(state, data):
    if data is None:
        state.player.heal(state.player.max_life)
    else:
        state.player.heal(data)


@card("Bullet up I", 200, 10, "Two bullets per shot for 5 seconds", 6, data=(2, 5))
@card("Bullet up II", 350, 15, "Three bullets per shot for 4 seconds", 6, data=(3, 4))
@card("Bullet up III", 500, 20, "Three bullets per shot for 8 seconds", 6, data=(3, 8))
@card("Bullet up IV", 500, 200, "Permanently shoot one more bullet", 6, data=None)
def bullet_up(state, data):
    if data is None:
        state.player.bullets += 1
    else:
        state.player.bullets += data[0] - 1

        @state.do_later(data[1] * SECOND)
        def change_back():
            state.player.bullets -= data[0] - 1


@card("Push enemies I", 100, 10, "Push enemies back two rows", 3, data=2)
@card("Push enemies II", 200, 15, "Push enemies back three rows", 3, data=3)
@card("Push enemies III", 400, 20, "Push enemies back five rows", 3, data=5)
def push_enemies(state, data):
    for enemy in state.get_all("Enemy"):
        enemy.push_back(data)


@card(
    "Danger Zone I",
    100,
    10,
    "Enemies deal 10% more damage and give 10% more points (permanent)",
    4,
    data=(10, 10),
)
@card(
    "Danger Zone II",
    200,
    15,
    "Enemies deal 15% more damage and give 20% more points (permanent)",
    4,
    data=(15, 20),
)
@card(
    "Danger Zone III",
    400,
    20,
    "Enemies deal 20% more damage and give 30% more points (permanent)",
    4,
    data=(20, 30),
)
def danger_zone(state, data):
    state.game_values.enemy_damage_boost += data[0] / 100
    state.game_values.points_bonus += data[1] / 100


@card("Sacrifice I", 100, 0, "Sacrifice 100HP for 10 coins", 5, data=(100, 10))
@card("Sacrifice II", 200, 0, "Sacrifice 200HP for 25 coins", 5, data=(200, 25))
@card("Sacrifice III", 400, 0, "Sacrifice 300HP for 40 coins", 5, data=(300, 40))
def sacrifice(state, data):
    if state.player.life > data[0]:
        state.player.damage(data[0], True)
        state.player.coins += data[1]


@card("Life up I", 100, 50, "Permanently gain 100HP", 1, data=100)
@card("Life up II", 200, 100, "Permanently gain 250HP", 1, data=250)
@card("Life up III", 400, 200, "Permanently gain 600HP", 1, data=600)
def life_up(state, data):
    state.player.max_life += data
    state.player.heal(data)


@card("Bad news I", -100, 0, "Permanently loose 25HP", 2, data=25)
@card("Bad news II", -200, 0, "Permanently loose 50HP", 2, data=50)
@card("Bad news III", -400, 0, "Permanently loose 100HP", 2, data=100)
def bad_news(state, data):
    state.player.damage(data)
    state.player.max_life -= data
