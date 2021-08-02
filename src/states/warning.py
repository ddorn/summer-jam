from pygame import Vector2

import states
from engine import *


class WarningState(State):
    def draw(self, gfx: "GFX"):
        super().draw(gfx)

        r = gfx.text("Warning", 64, RED, midtop=(W / 2, 32))
        r = gfx.text("This game is incomplete.", 32, ORANGE, midtop=r.midbottom)
        r = gfx.wrap_text(
            "It was made in under ~2 days and many things are not glued together well. There are bugs and and we had bigger ideas for the project, so take it as a proof of concept.",
            16,
            WHITE,
            W / 2,
            midtop=r.midbottom,
        )

        if self.timer % 100 > 15 and self.timer > 200:
            r = gfx.text(
                "Press space to continue", 16, GREEN, center=(W / 2, (r.bottom + H - 42) / 2)
            )

        r = gfx.text("A game by", 16, YELLOW, SMALL_FONT, midtop=(W / 2, H - 42))
        gfx.text("CozyFractal - Zoldalma - Felix", 16, WHITE, midtop=r.midbottom + Vector2(0, 4))

    def create_inputs(self) -> Inputs:
        inputs = super().create_inputs()
        inputs["skip"] = Button(pygame.K_SPACE, pygame.K_RETURN, JoyButton(JOY_A)).on_press(
            self.replace_state_callback(states.MenuState)
        )
        return inputs
