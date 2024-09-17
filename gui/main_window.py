from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivy.core.window import Window
from kivy.clock import Clock

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
            ScrollView:
                do_scroll_x: True
                do_scroll_y: False
                MDBoxLayout:
                    id: table_container
                    orientation: 'vertical'
                    size_hint_y: None
                    height: self.minimum_height
                    size_hint_x: None
                    width: self.minimum_width
"""

Builder.load_string(KV)


class HomeWindow(Screen):
    controller = ObjectProperty()
    table_size_bound = False  # Flag to check if size event is bound

    def __init__(self, controller, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.controller = controller
        Clock.schedule_once(self.create_table, 0)

    def create_table(self, dt):
        total_width = self.ids.table_container.width

        if total_width == 0:
            total_width = Window.width - dp(40)  # Adjust for padding if any

        column_ratios = [0.25, 0.25, 0.25, 0.25]

        column_widths = [
            ("Name", dp(200)),
            ("Date of Publishing", dp(200)),
            ("Date of Scrape", dp(200)),
            ("Type of Change", dp(200)),
        ]

        print(f"Total width: {total_width}")
        for name, width in column_widths:
            print(f"Column '{name}' width: {width}")

        self.data_tables = MDDataTable(
            size_hint=(None, None),
            size=(dp(800), dp(400)),  # Adjust size as needed
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

        self.ids.table_container.clear_widgets()
        self.ids.table_container.add_widget(self.data_tables)

        if not self.table_size_bound:
            self.ids.table_container.bind(size=self.update_table_columns)
            self.table_size_bound = True

    def update_table_columns(self, instance, value):
        # Unbind the size event to prevent recursion
        self.ids.table_container.unbind(size=self.update_table_columns)
        self.table_size_bound = False

        # Remove the old table
        self.ids.table_container.clear_widgets()

        # Recreate the table with updated widths
        self.create_table(None)

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
