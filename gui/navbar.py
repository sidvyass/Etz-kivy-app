from kivy.uix.floatlayout import FloatLayout
from kivy.uix.label import Label
from kivy.graphics import Color, Rectangle


class NavBar(FloatLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(self.navigation_widget())

    def navigation_widget(self):
        self.label = Label(
            text="Navigation",
            size_hint=(None, None),
            size=(200, 50),  # Adjust size as needed
            pos_hint={"center_x": 0.5, "top": 1},  # Position at the top center
            font_size=20,
            bold=True,
        )

        return self.label
