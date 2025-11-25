from kivy.uix.button import Button
from kivy.graphics import Color, RoundedRectangle
from kivy.properties import ListProperty

class StyledButton(Button):
    color_fondo = ListProperty([0.14, 0.47, 0.68, 1])
    color_hover = ListProperty([0.10, 0.40, 0.60, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.size_hint_y = None
        self.height = 60
        self.font_size = 20
        self.background_normal = ""
        self.background_down = ""
        self.background_color = (0, 0, 0, 0)
        self.color = (1, 1, 1, 1)

        with self.canvas.before:
            Color(*self.color_fondo)
            self.rect = RoundedRectangle(
                radius=[20], pos=self.pos, size=self.size
            )

        self.bind(pos=self.update_rect, size=self.update_rect)
        self.bind(on_enter=self.on_hover)
        self.bind(on_leave=self.on_leave)

    def update_rect(self, *args):
        self.rect.pos = self.pos
        self.rect.size = self.size

    def on_hover(self, *args):
        self.canvas.before.children[0].rgba = self.color_hover

    def on_leave(self, *args):
        self.canvas.before.children[0].rgba = self.color_fondo