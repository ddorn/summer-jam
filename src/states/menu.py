import pygame
from engine import *
from objects import *
from states import *


class MenuState(State):
    def __init__(self):
        super().__init__()

        self.add(Text(GAME_NAME, GREEN, 72, midtop=(W / 2, 8)))
        self.add(
            Menu(
                (W / 2, 150),
                {
                    "Play": self.push_state_callback(CardTestState),
                    "Controls": self.push_state_callback(ControlsHelpState),
                    "Quit": App.MAIN_APP.quit,
                },
            )
        )


class ControlsHelpState(State):
    def __init__(self):
        super().__init__()
        control_texts = (
            (
                "Keyboard and mouse:",
                (
                    "A/D to move",
                    "Right click to show/hide cards",
                    "Left click to shoot/select card",
                ),
            ),
            (
                "Controller:",
                (
                    "Left stick to move",
                    "Y/Triangle to show/hide cards",
                    "A/Cross to shoot/select card",
                    "D-pad to change selected card",
                ),
            ),
        )

        self.add(l := Text("Controls", GREEN, 72, midtop=(W / 2, 8)))
        self.line_pos = l.rect.bottom
        for title, texts in control_texts:
            l = Text(title, YELLOW, 32, midtop=l.rect.midbottom + pygame.Vector2(0, 5))
            self.add(l)
            for text in texts:
                l = Text(text, "white", 15, midtop=l.rect.midbottom)
                self.add(l)

    def draw(self, gfx: "GFX"):
        offset = 20
        super().draw(gfx)
        pygame.draw.line(
            gfx.surf, (30, 30, 30), (offset, self.line_pos), (W - offset, self.line_pos)
        )

    def create_inputs(self) -> Inputs:
        inputs = super().create_inputs()
        inputs["quit"] = Button(
            QuitEvent(), pygame.K_ESCAPE, pygame.K_q, JoyButton(JOY_BACK), JoyButton(1)
        )
        inputs["quit"].on_press(self.pop_state)
        return inputs
