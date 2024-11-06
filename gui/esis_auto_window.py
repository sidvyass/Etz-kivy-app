import asyncio
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen
from kivy.clock import Clock
from kivy.uix.boxlayout import BoxLayout
from gui.esis_window.asn_rc_popup import open_asn_rcs_popup
from gui.esis_window.detail_popup import open_details


KV = """
<EsisAutoGui>:
    name: 'esis_auto_gui'

    BoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20

        # Top navigation bar with home, run scraper, and logout buttons
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
                text_color: 1, 1, 1, 1


            Widget:
                size_hint_x: 1

            MDButton:
                id: run_scraper
                style: "filled"
                on_release: root.start_scraper_on_server()
                size_hint_x: None
                width: dp(100)
                height: dp(36)
                pos_hint: {'center_y': 0.5}
                padding: dp(10), dp(5)
                theme_bg_color: "Custom"
                md_bg_color: 0.3, 0.3, 0.3, 1

                MDButtonText:
                    text: "Run Scraper"
                    theme_text_color: "Custom"
                    text_color: "white"

            MDIconButton:
                icon: "cloud-upload"
                size_hint_y: 1
                size_hint_x: 0.1
                on_release: root.controller.open_file_upload_popup()
                text_color: 1, 1, 1, 1

            MDIconButton:
                on_release: root.controller.main_app.logout()
                icon: "logout"
                size_hint_y: 1
                size_hint_x: 0.1
                text_color: 1, 1, 1, 1


        # Search bar section
        BoxLayout:
            orientation: 'horizontal'
            spacing: dp(10)
            size_hint_y: 0.1
            size_hint_x: 1

            MDTextField:
                id: search_field
                pos_hint: {'center_y': 0.5}
                size_hint_x: 0.8

                MDTextFieldHintText:
                    text: "Search by PO #, CO Seq #"

                MDTextFieldHelperText:
                    text: "Enter a valid search value."
                    mode: "on_error"

            MDButton:
                id: search_button
                style: "filled"
                on_release: root.controller.search(root)
                size_hint_x: 0.2
                pos_hint: {'center_y': 0.5}
                padding: dp(5), dp(5)
                theme_bg_color: "Custom"
                md_bg_color: 0.3, 0.3, 0.3, 1

                MDButtonText:
                    id: search_button_text
                    text: "Search"
                    theme_text_color: "Custom"
                    text_color: "white"

        # Headers for the table
        BoxLayout:
            orientation: 'horizontal'
            size_hint_y: None
            height: dp(40)
            padding: dp(10)

            Label:
                text: "PO Number"
                bold: True
                size_hint_x: 0.2
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                padding_x: dp(5)

            Label:
                text: "CO Number"
                bold: True
                size_hint_x: 0.1
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                padding_x: dp(5)

            Label:
                text: "CO Reason"
                bold: True
                size_hint_x: 0.2
                halign: 'left'
                valign: 'middle'
                text_size: self.size
                padding_x: dp(5)

            Label:
                text: "CO Date"
                bold: True
                size_hint_x: 0.1
                halign: 'center'
                valign: 'middle'
                text_size: self.size
                padding_x: dp(5)

            Label:
                text: "Actions"
                bold: True
                size_hint_x: 0.4
                halign: 'center'
                valign: 'middle'
                text_size: self.size


        # The RecycleView for the table data
        RecycleView:
            id: table_view
            viewclass: 'TableRow'
            size_hint_y: 0.9
            size_hint_x: 1
            do_scroll_x: True
            do_scroll_y: True

            RecycleBoxLayout:
                id: table_layout
                orientation: 'vertical'
                default_size: None, dp(60)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(0)

<TableRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(40)

    Label:
        text: root.po_number
        size_hint_x: 0.2
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:
        text: root.co_number
        size_hint_x: 0.1
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:  # this is latest change order
        text: root.co_reason
        size_hint_x: 0.1
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:
        text: root.co_date
        size_hint_x: 0.1
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    MDButton:
        style: "filled"
        on_release: root.open_details()
        size_hint_x: 0.1
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Open Details"
            theme_text_color: "Custom"
            text_color: "white"

    MDButton:
        style: "filled"
        on_release: root.controller.open_file(root.row_data)
        size_hint_x: 0.1
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Open File"
            theme_text_color: "Custom"
            text_color: "white"

    MDButton:
        style: "filled"
        on_release: root.approve_document()
        size_hint_x: 0.1
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Approve"
            theme_text_color: "Custom"
            text_color: "white"

    MDButton:
        style: "filled"
        on_release: root.discard_document()
        size_hint_x: 0.1
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Discard"
            theme_text_color: "Custom"
            text_color: "white"

    MDButton:
        style: "filled"
        on_release: root.open_asn_rcs_popup()
        size_hint_x: 0.1
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "ASNs/RCs"
            theme_text_color: "Custom"
            text_color: "white"


"""


class TableRow(BoxLayout):
    po_number = StringProperty()
    co_number = StringProperty()
    co_reason = StringProperty()
    co_date = StringProperty()
    filename = StringProperty()
    mt_createdate = StringProperty()
    mt_shippingaddress = StringProperty()
    controller = ObjectProperty()
    row_data = ObjectProperty()
    parent_widget = ObjectProperty()

    # TODO: map these to the controller so that we can log it
    def open_details(self):
        open_details(self.controller._get_data_helper(self.row_data))

    def approve_document(self):
        asyncio.create_task(
            self.controller.approve_document(self.row_data, self.parent_widget)
        )

    def discard_document(self):
        asyncio.create_task(
            self.controller.discard_document(self.row_data, self.parent_widget)
        )

    # TODO: map these to the controller so that we can log it
    def open_asn_rcs_popup(self):
        data = self.controller.documents[self.row_data[4]]
        open_asn_rcs_popup(data)


class EsisAutoGUI(Screen):
    controller = ObjectProperty()
    table_size_bound = False  # Flag to check if size event is bound

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.create_table()
        self.update_documents = Clock.schedule_interval(self.queue_background_tasks, 60)
        self.queue_background_tasks()

    def create_table(
        self, rows=[("Fetching Data...", "more data", "more data", "", "", "", "")]
    ):

        data = []
        for row in rows:
            row_data = (
                row[0],
                row[1],
                row[2],
                row[3].split(" ")[0],
                row[4],
                row[5],
                row[6],
            )
            data.append(
                {
                    "po_number": row_data[0],
                    "co_number": row_data[1],
                    "co_reason": row_data[2],
                    "co_date": row_data[3],
                    "filename": row_data[4],
                    "mt_createdate": row_data[5],
                    "mt_shippingaddress": row_data[6],
                    "controller": self.controller,
                    "row_data": row_data,
                    "parent_widget": self,
                }
            )
        self.ids.table_view.data = data

    # ---------- WRAPPERS --------------------
    # To be compatible with clock in kivy we need to wrap async funcs.
    # NOTE: You cannot do this in any other way. ITS DUMB.

    def queue_background_tasks(self, *args):
        asyncio.create_task(self.controller.fetch_update_documents(self))
        asyncio.create_task(self.controller.fetch_scraper_status(self))

    def start_scraper_on_server(self, *args):
        self.ids.run_scraper.disabled = (
            True  # TODO: enable this button once the scraper service ends
        )
        asyncio.create_task(self.controller.start_scraper_on_server(self))
        # For testing
        asyncio.create_task(self.controller.fetch_scraper_status(self))


Builder.load_string(KV)
