# gui/home_window.py

from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.core.window import Window

from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout

KV = """
<ContentNavigationDrawer@MDBoxLayout>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    MDLabel:
        text: 'Navigation Drawer'
        font_style: 'Subtitle1'

<HomeWindow>:
    name: 'main_window'

    BoxLayout:
        orientation: 'vertical'

        # Top Navigation Bar
        MDTopAppBar:
            title: "Home"
            elevation: 0  # Flat design
            md_bg_color: app.theme_cls.primary_color
            # left_action_items: [["menu", lambda x: root.toggle_nav_drawer()]]
            right_action_items:
                [
                ["button1", lambda x: root.on_button1_press()],
                ["button2", lambda x: root.on_button2_press()],
                ["button3", lambda x: root.on_button3_press()],
                ["button4", lambda x: root.on_button4_press()],
                ["button5", lambda x: root.on_button5_press()]
                ]
            size_hint_y: None
            height: dp(56)

        # Rest of the screen
        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(10)  # Adjusted spacing

            # Search Bar
            BoxLayout:
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
                    md_bg_color: app.theme_cls.primary_color
                    elevation: 0

            # Data Table Container
            BoxLayout:
                id: table_container
                orientation: 'vertical'
                size_hint_y: 1
                size_hint_x: 1
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
        # Calculate total available width
        total_width = self.ids.table_container.width

        # If total_width is 0, default to Window width minus padding
        if total_width == 0:
            total_width = Window.width - dp(40)  # Adjust for padding if any

        # Define proportional widths (percentages)
        column_ratios = [0.4, 0.2, 0.2, 0.2]  # Adjust as needed

        # Calculate column widths based on ratios
        column_widths = [
            ("Name", total_width * column_ratios[0]),
            ("Date of Publishing", total_width * column_ratios[1]),
            ("Date of Scrape", total_width * column_ratios[2]),
            ("Type of Change", total_width * column_ratios[3]),
        ]

        # Create the data table with dynamic column widths
        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            column_data=column_widths,
            row_data=[
                # Dummy data
                ("Document 1", "2023-01-01", "2023-01-10", "AA"),
                ("Document 2", "2023-02-01", "2023-02-05", "BB"),
                # ... more data
            ],
        )

        # Add the data table to the container
        self.ids.table_container.clear_widgets()
        self.ids.table_container.add_widget(self.data_tables)

        # Bind to size changes
        self.ids.table_container.bind(size=self.update_table_columns)

    def update_table_columns(self, *args):
        # Remove the old table
        self.ids.table_container.clear_widgets()
        # Recreate the table with updated widths
        self.create_table()

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


class ContentNavigationDrawer(MDBoxLayout):
    pass
