import asyncio
import os
from kivymd.uix.button import MDFlatButton
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from gui.base_logger import getlogger
from controllers.main_controller import MainWindowController


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
        self.controller: MainWindowController = controller
        self.create_table()
        self.LOGGER = getlogger("home window")
        Clock.schedule_interval(self.queue_update_scraper, 15)  # status LIGHT
        self.queue_update_scraper()
        Clock.schedule_interval(self.queue_update_documents, 60)
        self.queue_update_documents()

    def create_table(self, rows=[("Fetching Data...", "", "", "", "", "")]):
        column_widths = [
            ("PO Number", dp(50)),
            ("CO Number", dp(25)),
            ("Type of CO", dp(50)),
            ("Date", dp(50)),
            ("FilePath", dp(50)),  # This will act like a button (clickable text)
            ("FileName", dp(50)),
            ("Description", dp(100)),

        ]

        # Prepare row data with clickable text for FilePath column
        row_with_buttons = []
        for row in rows:
            file_path = row[4]
            file_button = f"[Open File]"  # Text that acts like a button

            # Replace the FilePath column with the clickable text (file_button)
            new_row = (row[0], row[1], row[2], row[3], file_button, row[5])
            row_with_buttons.append(new_row)

        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            column_data=column_widths,
            row_data=row_with_buttons,
        )

        # Clear existing widgets and add the new table
        self.ids.table_container.clear_widgets()
        self.ids.table_container.add_widget(self.data_tables)

        # Add a row click event
        self.data_tables.bind(on_row_press=self.on_row_press)

    def on_row_press(self, instance_table, instance_row):
        # Get the row data
        row_data = instance_row.table.recycle_data[instance_row.index]["text"]

        # Check if the clicked row contains an "Open File" text in the file path column
        if "[Open File]" in row_data:
            file_path = row_data.split("[Open File]")[0].strip()  # Extract file path
            self.controller.open_file(file_path)

    # ---------- status LIGHT --------------------

    def queue_update_scraper(self, *args):
        asyncio.create_task(self.async_start_update_scraper())

    async def async_start_update_scraper(self):
        result = await self.controller.get_scraper_status()
        if result:
            self.ids.status_light.text_color = get_color_from_hex("#00FF00")  # Green
        else:
            self.ids.status_light.text_color = get_color_from_hex("#FFFFFF")  # White

    # -------------------------------------------

    async def start_scraper_update_gui(self):
        """This just sends a requst to activate the scraper"""
        response = await self.controller.start_scraper_on_server()
        if response:
            self.ids.status_light.text_color = get_color_from_hex("#00FF00")  # Green

    # --------------- document display -------------

    def queue_update_documents(self, *args):
        asyncio.create_task(self.async_start_update_document())

    async def async_start_update_document(self):
        """Our controller calls the create table statement to update"""
        await self.controller.fetch_update_documents(self)

    # ------------------------------------------

    def on_button1_press(self):
        asyncio.create_task(self.start_scraper_update_gui())

    def on_logout_press(self):
        self.controller.logout()


class ContentNavigationDrawer(MDBoxLayout):
    pass
