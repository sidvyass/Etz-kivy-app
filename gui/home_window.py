from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


KV = """
<HomeWindow>:
    name: 'home_window'
    BoxLayout:
        orientation: 'vertical'
        padding: 20  # Adds padding around the entire layout
        spacing: 20  # Adds spacing between elements

        # First row (App Name and User ID)
        BoxLayout:
            size_hint_y: 0.1
            padding: [20, 10]  # Adds padding between the labels
            canvas.before:
                Color:
                    rgba: 0.1, 0.1, 0.1, 1  # Dark background for the header row
                Rectangle:
                    size: self.size
                    pos: self.pos
            MDIconButton:
                icon: "home"
                size_hint_y: 1
                size_hint_x: 0.1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  # White icon color
            MDLabel:
                text: "Home"
                halign: "center"
                size_hint_x: 0.9
                font_style: 'H4'
                bold: True
                color: 1, 1, 1, 1  # White color text
            MDLabel:
                text: "User_id"
                halign: "right"
                size_hint_x: 0.1
                font_style: 'Subtitle1'
                color: 1, 1, 1, 1  # White color text

        # Three Columns Section
        BoxLayout:
            size_hint_y: 0.9
            spacing: 20  # Adds spacing between columns

            # Left Column with 4 Buttons
            BoxLayout:
                orientation: 'vertical'
                size_hint_x: 0.2
                padding: [10, 10]
                spacing: 15  # Adds spacing between buttons
                canvas.before:
                    Color:
                        rgba: 0.2, 0.2, 0.2, 1  # Darker background for the button column
                    Rectangle:
                        size: self.size
                        pos: self.pos

                MDFillRoundFlatButton:
                    text: "Button 1"
                    size_hint_y: 0.25
                    size_hint_x: 1
                    height: 50
                    md_bg_color: 0.1, 0.1, 0.1, 1  # Dark button background
                    text_color: 1, 1, 1, 1  # White text color

                MDFillRoundFlatButton:
                    text: "Button 2"
                    size_hint_y: 0.25
                    size_hint_x: 1
                    height: 50
                    md_bg_color: 0.1, 0.1, 0.1, 1  # Dark button background
                    text_color: 1, 1, 1, 1  # White text color

                MDFillRoundFlatButton:
                    text: "Button 3"
                    size_hint_y: 0.25
                    size_hint_x: 1
                    height: 50
                    md_bg_color: 0.1, 0.1, 0.1, 1  # Dark button background
                    text_color: 1, 1, 1, 1  # White text color

                MDFillRoundFlatButton:
                    text: "Button 4"
                    size_hint_y: 0.25
                    size_hint_x: 1
                    height: 50
                    md_bg_color: 0.1, 0.1, 0.1, 1  # Dark button background
                    text_color: 1, 1, 1, 1  # White text color

            # Middle Column (Empty for now)
            BoxLayout:
                size_hint_x: 0.6
                padding: 10
                canvas.before:
                    Color:
                        rgba: 0.15, 0.15, 0.15, 1  # Dark background for the middle column
                    Rectangle:
                        size: self.size
                        pos: self.pos
                MDLabel:
                    text: "Data/Charts"
                    halign: "center"
                    size_hint_x: 0.9
                    font_style: 'H4'
                    bold: True
                    color: 1, 1, 1, 1  # White color text

            # Right Column (Empty for now)
            BoxLayout:
                size_hint_x: 0.2
                padding: 10
                canvas.before:
                    Color:
                        rgba: 0.15, 0.15, 0.15, 1  # Dark background for the right column
                    Rectangle:
                        size: self.size
                        pos: self.pos
                MDLabel:
                    text: "Documents"
                    halign: "center"
                    size_hint_x: 0.9
                    font_style: 'H4'
                    bold: True
                    color: 1, 1, 1, 1  # White color text
"""

Builder.load_string(KV)


class HomeWindow(Screen):
    controller = ObjectProperty()

    def __init__(self, controller, **kwargs):
        print("starting...")
        super(HomeWindow, self).__init__(**kwargs)
        self.controller = controller
