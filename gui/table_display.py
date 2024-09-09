from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class DisplayDocs(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.initialize_canvas()
        self.add_widget(self.create_table())

    def initialize_canvas(self):
        if self.canvas is not None:
            with self.canvas.before:
                Color(1, 1, 1, 1)
                self.background = Rectangle(pos=self.pos, size=self.size)
        self.bind(pos=self.update_graphics, size=self.update_graphics)  # type: ignore

    def update_graphics(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size

    def create_table(self):
        table = GridLayout(cols=5, rows=10, size_hint=(1, 1))
        for row in range(10):
            for col in range(5):
                table.add_widget(
                    Label(text=f"Cell {row+1},{col+1}", color=[0, 0, 0, 1])
                )
        return table
