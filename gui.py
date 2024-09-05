from operator import pos
from kivy.app import App
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class NavBar(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        self.add_widget(Label(text="top"))

        self.initialize_canvas()

    def initialize_canvas(self, *args):
        if self.canvas is not None:
            with self.canvas:
                Color(1, 1, 1, 1)
                self.background = Rectangle(pos=self.pos, size=self.size)

            with self.canvas:
                Color(0, 0, 0, 0)
                self.border = Line(
                    rectangle=(self.x, self.y, self.width, self.height), width=2
                )

        self.bind(pos=self.update_graphics, size=self.update_graphics)  # type: ignore

    def update_graphics(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)


class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")

        nav_section = NavBar(size_hint=(1, 0.1))

        table_section = Label(text="bottom", size_hint=(1, 0.9))

        main_layout.add_widget(nav_section)
        main_layout.add_widget(table_section)

        return main_layout


if __name__ == "__main__":
    MyApp().run()
