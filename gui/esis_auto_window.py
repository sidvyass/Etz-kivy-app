import asyncio
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.uix.screenmanager import Screen
from kivy.metrics import dp
from kivy.clock import Clock
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout


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

    Label:
        text: root.co_reason
        size_hint_x: 0.2
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


<DetailTableRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(30)
    spacing: dp(5)

    Label:
        text: root.line_number
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.file_qty
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.file_price
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.file_uom
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.file_total
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.esis_date
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.mt_part_number
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.mt_qty_ordered
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.mt_qty_shipped
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.mt_status
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.mt_next_due_date
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size

    Label:
        text: root.mt_next_promise_date
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
        text_size: self.size
"""


class DetailTableRow(BoxLayout):
    line_number = StringProperty()
    file_qty = StringProperty()
    file_price = StringProperty()
    file_uom = StringProperty()
    file_total = StringProperty()
    esis_date = StringProperty()
    mt_part_number = StringProperty()
    mt_qty_ordered = StringProperty()
    mt_qty_shipped = StringProperty()
    mt_status = StringProperty()
    mt_next_due_date = StringProperty()
    mt_next_promise_date = StringProperty()


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

    def open_details(self):
        """
        Opens a popup window with the details of all the change orders.
        """

        po_number, co_seq_number, co_reason, co_date, table_data = (
            self.controller._get_data_helper(self.row_data)
        )

        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        info_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint_y=None)
        info_layout.bind(minimum_height=info_layout.setter("height"))

        info_layout.add_widget(
            Label(text="PO Number:", bold=True, size_hint_y=None, height=40)
        )
        info_layout.add_widget(Label(text=po_number, size_hint_y=None, height=40))
        info_layout.add_widget(
            Label(text="CO Sequence Number:", bold=True, size_hint_y=None, height=40)
        )
        info_layout.add_widget(Label(text=co_seq_number, size_hint_y=None, height=40))
        info_layout.add_widget(
            Label(text="CO Reason:", bold=True, size_hint_y=None, height=40)
        )
        info_layout.add_widget(Label(text=co_reason, size_hint_y=None, height=40))
        info_layout.add_widget(
            Label(text="CO Date:", bold=True, size_hint_y=None, height=40)
        )
        info_layout.add_widget(Label(text=co_date, size_hint_y=None, height=40))

        layout.add_widget(info_layout)

        layout.add_widget(Widget(size_hint_y=None, height=10))

        scroll_view = ScrollView(do_scroll_x=True, size_hint_y=1)

        table_layout = GridLayout(cols=1, size_hint_y=None, spacing=dp(5))
        table_layout.bind(minimum_height=table_layout.setter("height"))

        header_row = DetailTableRow(
            line_number="Line Number",
            file_qty="File Qty",
            file_price="File Price",
            file_uom="File UOM",
            file_total="File Total",
            esis_date="Esis Date",
            mt_part_number="MT Part Number",
            mt_qty_ordered="MT Qty Ordered",
            mt_qty_shipped="MT Qty Shipped",
            mt_status="MT Status",
            mt_next_due_date="MT Next Due Date",
            mt_next_promise_date="MT Next Promise Date",
        )
        table_layout.add_widget(header_row)

        for row_data in table_data:
            detail_row = DetailTableRow(
                line_number=row_data["line_number"],
                file_qty=row_data["file_qty"],
                file_price=row_data["file_price"],
                file_uom=row_data["file_uom"],
                file_total=row_data["file_total"],
                esis_date=row_data["esis_date"],
                mt_part_number=row_data["mt_part_number"],
                mt_qty_ordered=row_data["mt_qty_ordered"],
                mt_qty_shipped=row_data["mt_qty_shipped"],
                mt_status=row_data["mt_status"],
                mt_next_due_date=row_data["mt_next_due_date"],
                mt_next_promise_date=row_data["mt_next_promise_date"],
            )
            table_layout.add_widget(detail_row)

        scroll_view.add_widget(table_layout)
        layout.add_widget(scroll_view)

        popup = Popup(title="Document Details", content=layout, size_hint=(0.9, 0.9))
        popup.open()

    def approve_document(self):
        asyncio.create_task(
            self.controller.approve_document(self.row_data, self.parent_widget)
        )

    def discard_document(self):
        asyncio.create_task(
            self.controller.discard_document(self.row_data, self.parent_widget)
        )


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
