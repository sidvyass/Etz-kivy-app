import asyncio
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.properties import ObjectProperty
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.clock import Clock
from kivy.utils import get_color_from_hex
from gui.base_logger import getlogger


KV = """
<ContentNavigationDrawer@MDBoxLayout>:
    orientation: 'vertical'
    padding: dp(10)
    spacing: dp(10)
    MDLabel:
        text: 'Navigation Drawer'
        font_style: 'Subtitle1'

<EsisAutoGui>:
    name: 'esis_auto_gui'

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        BoxLayout:
            size_hint_y: 0.1
            padding: [20, 10] 
            canvas.before:
                Color:
                    rgba: 0.1, 0.1, 0.1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

            MDIconButton:
                icon: "home"
                size_hint_y: 1
                size_hint_x: 0.1
                on_release: root.controller.go_to_home()
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  # White icon color

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
                md_bg_color: app.theme_cls.primary_color
                on_release: root.on_button1_press()
                size_hint: None, None
                size: dp(100), dp(36)
                pos_hint: {'center_y': 0.5}
                padding: dp(10), dp(5)

            # "Logout" Button
            MDFlatButton:
                text: "Logout"
                text_color: 1, 1, 1, 1  # White text
                on_release: root.controller.main_app.logout()
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
                    md_bg_color: 0, 0.6, 0, 1  # Green background
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


class EsisAutoGUI(Screen):
    controller = ObjectProperty()
    table_size_bound = False  # Flag to check if size event is bound

    def __init__(self, controller, **kwargs):
        super(EsisAutoGUI, self).__init__(**kwargs)
        self.controller = controller
        self.LOGGER = getlogger("home window")
        self.create_table()
        # NOTE:  This should directly link to the controller
        self.update_status_light = Clock.schedule_interval(
            self.queue_update_scraper, 15
        )  # status LIGHT
        self.queue_update_scraper()
        # NOTE:  This should directly link to the controller
        self.update_documents = Clock.schedule_interval(self.queue_update_documents, 60)
        self.queue_update_documents()

    def create_table(self, rows=[("Fetching Data...", "", "", "", "", "", "")]):
        column_widths = [
            ("PO Number", dp(50)),
            ("CO Number", dp(25)),
            ("Type of CO", dp(50)),
            ("Date", dp(50)),
            ("FilePath", dp(50)),  # This will act like a button (clickable text)
            ("FileName", dp(50)),
        ]

        row_with_buttons = []
        assert len(rows) >= 1
        for row in rows:
            file_path = row[4]
            file_button = f"[Open File]"  # Text that acts like a button

            new_row = (row[0], row[1], row[2], row[3], file_button, row[5])
            row_with_buttons.append(new_row)

        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            column_data=column_widths,
            row_data=row_with_buttons,
        )

        self.ids.table_container.clear_widgets()
        self.ids.table_container.add_widget(self.data_tables)

        self.data_tables.bind(on_row_press=self.on_row_press)

    def on_row_press(self, instance_table, instance_row):
        row_data = instance_row.table.recycle_data[instance_row.index]["text"]

        if "[Open File]" in row_data:
            file_path = row_data.split("[Open File]")[0].strip()  # Extract file path
            self.controller.open_file(file_path)

    # ---------- status LIGHT --------------------

    def queue_update_scraper(self, *args):
        asyncio.create_task(self.controller.get_scraper_status(self))

    # -------------------------------------------

    async def start_scraper_update_gui(self):
        """This just sends a requst to activate the scraper"""
        response = await self.controller.start_scraper_on_server()
        if response:
            self.ids.status_light.text_color = get_color_from_hex("#00FF00")  # Green

    # --------------- document display -------------

    def queue_update_documents(self, *args):
        asyncio.create_task(self.controller.fetch_update_documents(self))

    # ------------------------------------------

    def on_button1_press(self):
        asyncio.create_task(self.start_scraper_update_gui())


class ContentNavigationDrawer(MDBoxLayout):
    pass
