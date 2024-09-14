# gui/home_window.py

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivymd.uix.datatables import MDDataTable
from kivy.metrics import dp

KV = """
<HomeWindow>:
    name: 'main_window'

    MDBoxLayout:
        orientation: 'vertical'

        # Top Navigation Bar (10% of screen height)
        MDTopAppBar:
            title: "Home"
            elevation: 10
            left_action_items: [["menu", lambda x: root.toggle_nav_drawer()]]
            right_action_items:
                [
                ["button1", lambda x: root.on_button1_press()],
                ["button2", lambda x: root.on_button2_press()],
                ["button3", lambda x: root.on_button3_press()],
                ["button4", lambda x: root.on_button4_press()],
                ["button5", lambda x: root.on_button5_press()]
                ]
            height: self.theme_cls.standard_increment
            size_hint_y: None

        # Rest of the screen (90%)
        MDBoxLayout:
            orientation: 'vertical'
            padding: dp(10)
            spacing: dp(10)

            MDBoxLayout:
                orientation: 'horizontal'
                spacing: dp(10)
                size_hint_y: None
                height: dp(48)

                MDTextField:
                    id: search_field
                    hint_text: "Search"
                    mode: "rectangle"
                    size_hint_x: 0.8

                MDRaisedButton:
                    text: "Search"
                    size_hint_x: 0.2
                    on_release: root.on_search_button()

            ScrollView:
                MDList:
                    id: table_container

    MDNavigationDrawer:
        id: nav_drawer

        ContentNavigationDrawer:
            id: content_drawer
"""

Builder.load_string(KV)


class HomeWindow(Screen):
    controller = ObjectProperty()

    def __init__(self, controller, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.controller = controller
        self.create_table()

    def toggle_nav_drawer(self):
        self.ids.nav_drawer.set_state("toggle")

    def on_search_button(self):
        search_text = self.ids.search_field.text
        self.controller.perform_search(search_text)

    def create_table(self):
        # Create the data table with dummy data
        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,  # Include checkboxes for each row
            column_data=[
                ("Name", dp(30)),
                ("Date of Publishing", dp(30)),
                ("Date of Scrape", dp(30)),
                ("Type of Change", dp(30)),
            ],
            row_data=[
                # Dummy data
                ("Document 1", "2023-01-01", "2023-01-10", "AA"),
                ("Document 2", "2023-02-01", "2023-02-05", "BB"),
                ("Document 3", "2023-03-15", "2023-03-20", "CC"),
                ("Document 4", "2023-04-10", "2023-04-18", "DD"),
                ("Document 5", "2023-05-25", "2023-05-30", "EE"),
                ("Document 6", "2023-06-12", "2023-06-22", "FF"),
                ("Document 7", "2023-07-01", "2023-07-05", "GG"),
                ("Document 8", "2023-08-09", "2023-08-14", "HH"),
            ],
        )

        # Add the data table to the container in the KV layout
        self.ids.table_container.add_widget(self.data_tables)

    # Button event handlers
    def on_button1_press(self):
        pass  # Implement as needed

    def on_button2_press(self):
        pass  # Implement as needed

    def on_button3_press(self):
        pass  # Implement as needed

    def on_button4_press(self):
        pass  # Implement as needed

    def on_button5_press(self):
        pass  # Implement as needed


class ContentNavigationDrawer(Screen):
    pass
