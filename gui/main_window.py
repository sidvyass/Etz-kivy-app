import asyncio
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
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

        # Custom Top Navigation Bar
        MDBoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(56)
            md_bg_color: app.theme_cls.primary_color
            padding: dp(10), 0
            spacing: dp(10)

            # "Home" Label
            MDLabel:
                text: "Home"
                font_style: "H6"
                halign: "left"
                valign: "center"
                size_hint_x: None
                width: dp(60)
                color: 1, 1, 1, 1  # White text
                pos_hint: {'center_y': 0.5}

            # Expandable Widget to push the buttons to the right
            Widget:
                size_hint_x: 1

            # Status label
            MDLabel:
                text: "Status"
                halign: "left"
                valign: "middle"
                size_hint_x: None
                width: dp(50)  # Adjust width of the label
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  # White text color

            # Status light icon
            MDIconButton:
                id: status_light
                icon: "circle"
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  # Default white color (not running)
                pos_hint: {'center_y': 0.5}
                size_hint: None, None
                size: dp(20), dp(20)  # Small size for the indicator

            # "Run Scraper" Button
            MDFlatButton:
                text: "Run Scraper"
                text_color: 1, 1, 1, 1  # White text
                md_bg_color: 0, 0.6, 0, 1  # Green background
                on_release: root.on_button1_press()
                size_hint: None, None
                size: dp(100), dp(36)
                pos_hint: {'center_y': 0.5}
                padding: dp(10), dp(5)

            # "Logout" Button
            MDFlatButton:
                text: "Logout"
                text_color: 1, 1, 1, 1  # White text
                on_release: root.on_logout_press()
                size_hint: None, None
                size: dp(80), dp(36)
                pos_hint: {'center_y': 0.5}
                padding: dp(10), dp(5)

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
                AnchorLayout:
                    id: table_container
                    size_hint_x: 1
                    size_hint_y: 1
"""


Builder.load_string(KV)


class HomeWindow(Screen):
    controller = ObjectProperty()
    table_size_bound = False  # Flag to check if size event is bound

    def __init__(self, controller, **kwargs):
        super(HomeWindow, self).__init__(**kwargs)
        self.controller = controller
        self.create_table()

    def create_table(self):
        column_widths = [
            ("Date of Publishing", dp(50)),
            ("Name", dp(100)),
            ("Date of Scrape", dp(60)),
            ("Type of Change", dp(100)),
        ]

        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            column_data=column_widths,
            row_data=[
                ("Document 1", "2023-01-01", "2023-01-10", "AA"),
                ("Document 2", "2023-02-01", "2023-02-05", "BB"),
            ],
        )

        self.ids.table_container.clear_widgets()
        self.ids.table_container.add_widget(self.data_tables)

    async def start_scraper_update_gui(self):
        response = await self.controller.start_scraper_on_server()
        # TODO: code to update the gui once it returns true or false

    def on_button1_press(self):
        asyncio.create_task(self.start_scraper_update_gui())

    def on_logout_press(self):
        self.controller.logout()


class ContentNavigationDrawer(MDBoxLayout):
    pass
