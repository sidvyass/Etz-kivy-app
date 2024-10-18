import asyncio
from kivy.lang import Builder
from kivymd.uix.button import MDFlatButton
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
                on_release: root.start_scraper_on_server()
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
        super().__init__(**kwargs)
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

    def create_table(
        self, rows=[("Fetching Data...", "", "", "", "", "", "", "", "", "", "")]
    ):
        print(rows)
        column_widths = [
            ("PO Number", dp(30)),
            ("CO Number", dp(25)),
            ("CO Reason", dp(25)),
            ("CO Date", dp(30)),
            ("FileName", dp(100)),  # very IMP
            ("MT CreateDate", dp(100)),
            ("MT ShippingAddress", dp(100)),
            ("Open Details", dp(30)),  # This will act like a button (clickable text)
            ("Open File", dp(30)),  # This will act like a button (clickable text)
            ("Approval", dp(30)),
            ("Discard", dp(30)),
        ]

        row_with_buttons = []
        assert len(rows) >= 1
        for idx, row in enumerate(rows):
            new_row = (
                row[0],
                row[1],
                row[2],
                row[3].split(" ")[0],
                row[4],
                row[5],
                row[6],
                "[[OPEN DETAILS]]",
                "[[OPEN FILE]]",
                "[[APPROVE]]",
                "[[DISCARD]]",
            )
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
        pressed_row_index = instance_row.index // len(self.data_tables.column_data)
        pressed_row_data = self.data_tables.row_data[pressed_row_index]
        if "[[APPROVE]]" == row_data:
            asyncio.create_task(
                self.controller.approve_document(pressed_row_data, self)
            )
        elif "[[DISCARD]]" == row_data:
            asyncio.create_task(
                self.controller.discard_document(pressed_row_data, self)
            )
        elif "[[OPEN FILE]]" == row_data:
            self.controller.open_file(pressed_row_data)

    # ---------- status LIGHT --------------------

    def queue_update_scraper(self, *args):
        asyncio.create_task(self.controller.get_scraper_status(self))

    # --------------- document display -------------

    def queue_update_documents(self, *args):
        asyncio.create_task(self.controller.fetch_update_documents(self))

    # ------------------------------------------

    def start_scraper_on_server(self, *args):
        asyncio.create_task(self.controller.start_scraper_on_server())


class ContentNavigationDrawer(MDBoxLayout):
    pass
