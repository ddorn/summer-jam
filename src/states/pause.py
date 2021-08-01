from engine import *


class PauseState(State):
    BG_COLOR = None
    OPACITY = 180  # 255 is not transparent

    def __init__(self, inner_state: State):
        super().__init__()
        self.inner = inner_state

        self.add(
            Menu(
                (W / 2, 150),
                {"Resume": self.pop_state, "Restart": self.restart, "Quit": App.MAIN_APP.quit},
            )
        )

    def restart(self):
        self.pop_state()
        self.inner.__init__()

    def draw(self, gfx: "GFX"):
        self.inner.draw(gfx)
        gfx.box(gfx.surf.get_rect(), (0, 0, 0, self.OPACITY))
        super().draw(gfx)

        t = text("Paused", 64, GREEN)
        gfx.blit(t, midtop=(W / 2, 32))
