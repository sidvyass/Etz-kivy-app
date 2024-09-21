from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen


KV = """
<HomeWindow>:
    name: 'home_window'
    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        # First row (App Name and User ID)
        BoxLayout:
            size_hint_y: 0.1
            canvas.before:
                Color:
                    rgba: 0.1, 0.1, 0.1, 1  # Dark background for the header row
            BoxLayout:
                orientation: 'horizontal'
                spacing: 10  # Adds spacing between columns
                size_hint_x: 0.1
                padding: [10, 10]
                halign: "left"
                canvas.before:
                    Rectangle:
                        size: self.size
                        pos: self.pos

                MDRaisedButton:
                    text: " ESIS  "
                    size_hint_y: 1
                    size_hint_x: 0.025
                    md_bg_color: 0.1, 0.3, 0.5, 1  # Muted blue button background
                    on_release: root.on_esis_scraper_press()
                    text_color: 1, 1, 1, 1  # White text color

                MDRaisedButton:
                    text: "Button 2"
                    size_hint_y: 1
                    size_hint_x: 0.025
                    height: 50
                    md_bg_color: 0.3, 0.5, 0.5, 1  # Muted teal secondary color
                    text_color: 1, 1, 1, 1  # White text color

                MDRaisedButton:
                    text: "Button 3"
                    size_hint_y: 1
                    size_hint_x: 0.025
                    md_bg_color: 0.9, 0.4, 0.3, 1  # Soft coral accent color
                    text_color: 1, 1, 1, 1  # White text color

                MDRaisedButton:
                    text: "Button 4"
                    size_hint_y: 1
                    size_hint_x: 0.025
                    md_bg_color: 0.2, 0.3, 0.4, 1  # Blue-gray button background
                    text_color: 1, 1, 1, 1  # White text color
            MDLabel:
                text: "Home"
                halign: "center"
                size_hint_x: 0.8
                font_style: 'H4'
                bold: True
                color: 1, 1, 1, 1  # White color text
            MDFlatButton:
                text: "Logout"
                size_hint_y: 1
                size_hint_x: 0.1
                md_bg_color: 0.2, 0.2, 0.2, 1  # Dark gray button background
                text_color: 1, 1, 1, 1  # White text
                on_release: root.on_logout_press()

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

    def on_esis_scraper_press(self):
        self.controller.go_to_esis_window()

    def on_logout_press(self):
        self.controller.logout()
