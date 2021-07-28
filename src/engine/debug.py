from time import time

from pygame import Vector2

from .assets import *
from .constants import *
from .object import Object
from .utils import *

__all__ = ["Debug"]


class Debug(Object):
    """
    Class that handles the delayed drawing of points, rects, and texts.

    The draw methods .point(), .vector(), .rect() and .text()
    should be called during logic updates and will be rendered
    on screen later during the draw phase.

    The points/vectors/rects to draw are not saved every frame and need to
    be drawn every frame to persist on the screen.
    Drawn text stays on screen until it is overwritten by newer text.

    The Debug can be enabled or disabled with .toggle(). It draws nothing
    when disabled.
    The Debug can be paused, in which case its data becomes persistant and is not
    erased every frame.
    """

    # We want the debug to be in front of everything.
    Z = 1000000000

    def __init__(self):
        super().__init__((0, 0))
        self.points = []
        self.vectors = []
        self.rects = []
        self.texts = []
        # To highlight the current texts in yellow.
        self.nb_txt_this_frame = 0

        self.lasts = [[], [], [], []]

        self.enabled = False
        self.paused = False

        self.frame_times = [0]

    def logic(self):
        self.frame_times = self.frame_times[-29:] + [time()]

    def toggle(self, *_args):
        """Toggle between enabled and disabled.

        If the debug is disabled, nothing is drawn on screen.
        """
        self.enabled = not self.enabled

    def point(self, x, y, color="red"):
        """Draw a point during the draw phase."""
        if self.enabled:
            self.points.append((x, y, color))
        return x, y

    def vector(self, vec, anchor, color="red", scale=1):
        """
        Draw a vector during the draw phase.

        Args:
            anchor: Base/Start of the vector.
            scale: Multiply the magnitude for visibility.

        Returns:
            The input vector, for chaining purposes.
        """
        if self.enabled:
            self.vectors.append((Vector2(anchor), Vector2(vec) * scale, color))
        return vec

    def rectangle(self, rect, color="red"):
        """
        Draw a rectangle during the draw phase.

        Args:
            rect: Rect-like object

        Returns:
            The input rect, for chaining purposes.
        """
        if self.enabled:
            self.rects.append((rect, color))
        return rect

    def text(self, *obj):
        """
        Display the string representation of objects during the draw phase.

        Args:
            *obj: Any number of objects, display their str()
        """
        if self.enabled:
            self.texts.append(obj)
            self.nb_txt_this_frame += 1

    def draw(self, gfx):
        if not self.enabled:
            return

        fps = len(self.frame_times) / (self.frame_times[-1] - self.frame_times[0])
        s = text(f"FPS: {int(fps)}", 7, WHITE, "pixelmillennium")
        gfx.blit(s, bottomleft=(4, H - 4))

        if self.paused:
            # Restore the last data.
            # This means new data is just erased, but it shouldn't be a propblem
            # as no new input should come when paused.
            # Otherwise we will have to extend it.
            self.points, self.vectors, self.rects, self.texts = self.lasts

        for (x, y, color) in self.points:
            pygame.draw.circle(gfx.surf, color, (x, y), 1)

        for (anchor, vec, color) in self.vectors:
            pygame.draw.line(gfx.surf, color, anchor, anchor + vec)

        for rect, color in self.rects:
            pygame.draw.rect(gfx.surf, color, rect, 1)

        y = 3
        for i, obj in enumerate(self.texts):
            color = WHITE if len(self.texts) - i - 1 >= self.nb_txt_this_frame else YELLOW
            s = text(" ".join(map(str, obj)), 7, color, "pixelmillennium")
            r = gfx.blit(s, topleft=(3, y))
            y = r.bottom

        # Archiving of the data, so that we can get them back if we are paused.
        # This could go in .logic() but we don't know in which order .logic()
        # is called with respect to the other objects utilizing Debug, so we might
        # loose data. Also .logic() might be called independently from the draw.
        self.lasts = [self.points, self.vectors, self.rects, self.texts]
        self.points = []
        self.vectors = []
        self.rects = []
        self.texts = self.texts[-5:]
        if not self.paused:
            self.nb_txt_this_frame = 0
