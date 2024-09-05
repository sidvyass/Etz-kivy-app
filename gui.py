from operator import pos
from kivy.app import App
from kivy.graphics import Line, Color, Rectangle
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.anchorlayout import AnchorLayout
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label


class NavBar(AnchorLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Set the layout anchor to the top center (default is center)
        self.anchor_x = "center"
        self.anchor_y = "top"

        self.initialize_canvas()

        # Navigation label at the top center
        nav_label = Label(
            text="Navigation",
            size_hint=(None, None),  # Disable automatic resizing
            size=(200, 50),  # Fixed size
            pos_hint={
                "center_x": 0.5,
                "top": 1,
            },  # Center horizontally and align to top
            color="000000",
        )
        self.add_widget(nav_label)

        # Create a BoxLayout to hold the other widgets
        content_layout = BoxLayout(
            orientation="vertical", size_hint=(1, None), height=200
        )

        # Add labels and button to the content layout
        content_layout.add_widget(
            Label(
                text="Last Run: ",
                color=[0, 0, 0, 1],
                size_hint=(None, None),
                size=(150, 40),
                pos_hint={"center_x": 0.5},
            )
        )
        content_layout.add_widget(
            Label(
                text="Count: ",
                color=[0, 0, 0, 1],
                size_hint=(None, None),
                size=(150, 40),
                pos_hint={"center_x": 0.5},
            )
        )
        content_layout.add_widget(
            Label(
                text="Active Status: ",
                color=[0, 0, 0, 1],
                size_hint=(None, None),
                size=(150, 40),
                pos_hint={"center_x": 0.5},
            )
        )
        content_layout.add_widget(
            Button(
                text="Run Script",
                size_hint=(None, None),
                size=(150, 50),
                pos_hint={"center_x": 0.5},
            )
        )

        # Add the content layout to the NavBar
        self.add_widget(content_layout)

    def initialize_canvas(self, *args):
        if self.canvas is not None:
            with self.canvas.before:
                Color(1, 1, 1, 1)  # White background
                self.background = Rectangle(pos=self.pos, size=self.size)

            with self.canvas.before:
                Color(0, 0, 0, 1)  # Black border
                self.border = Line(
                    rectangle=(self.x, self.y, self.width, self.height), width=2
                )

        self.bind(pos=self.update_graphics, size=self.update_graphics)

    def update_graphics(self, *args):
        self.background.pos = self.pos
        self.background.size = self.size
        self.border.rectangle = (self.x, self.y, self.width, self.height)


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


class MyApp(App):
    def build(self):
        main_layout = BoxLayout(orientation="vertical")

        nav_section = NavBar(size_hint=(1, 0.2))
        display_doc = DisplayDocs(size_hint=(1, 0.8))

        main_layout.add_widget(nav_section)
        main_layout.add_widget(display_doc)

        return main_layout


if __name__ == "__main__":
    MyApp().run()
