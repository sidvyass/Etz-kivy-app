import asyncio
import re
from kivy.uix.widget import Widget
from kivy.uix.scrollview import ScrollView
from kivy.uix.boxlayout import BoxLayout
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder
from kivy.uix.modalview import ModalView
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

            Button:
                text: "Run Scraper"
                text_color: 1, 1, 1, 1  # White text
                # md_bg_color: app.theme_cls.primary_color
                on_release: root.start_scraper_on_server()
                size_hint: None, None
                size: dp(100), dp(36)
                pos_hint: {'center_y': 0.5}
                padding: dp(10), dp(5)

            Button:
                text: "Logout"
                text_color: 1, 1, 1, 1  # White text
                on_release: root.controller.main_app.logout()
                size_hint: None, None
                size: dp(80), dp(36)
                pos_hint: {'center_y': 0.5}
                padding: dp(10), dp(5)

        BoxLayout:
            orientation: 'vertical'
            padding: dp(20)
            spacing: dp(10)  # Adjusted spacing

            BoxLayout:
                orientation: 'horizontal'
                spacing: dp(10)
                size_hint_y: 0.1
                size_hint_x: 1

                MDTextField:
                    id: search_field
                    hint_text: "Search"
                    mode: "outlined"
                    size_hint_x: 0.8

                Button:
                    text: "Search"
                    size_hint_x: 0.2
                    on_release: root.on_search_button()
                    background_color: 0, 0.6, 0, 1  # Green background

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
                    default_size: None, dp(30)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height

<TableRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(30)
    spacing: dp(5)

    # Adjust the size_hint_x and width for each widget
    Label:
        text: root.po_number
        size_hint_x: None
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        size_hint_x: 0.14

    Label:
        text: root.co_number
        size_hint_x: None
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        size_hint_x: 0.14

    Label:
        text: root.co_reason
        size_hint_x: None
        halign: 'left'
        valign: 'middle'
        size_hint_x: 0.14
        text_size: self.size

    Label:
        text: root.co_date
        size_hint_x: None
        halign: 'left'
        valign: 'middle'
        size_hint_x: 0.14
        text_size: self.size

    Button:
        text: 'Open Details'
        on_release: root.open_details()
        size_hint_x: 0.14
        halign: 'center'

    Button:
        text: 'Open File'
        on_release: root.controller.open_file(root.row_data)
        size_hint_x: 0.14
        halign: 'center'

    Button:
        text: 'Approve'
        on_release: root.approve_document()
        halign: 'center'
        size_hint_x: 0.14

    Button:
        text: 'Discard'
        on_release: root.discard_document()
        size_hint_x: 0.14
        halign: 'center'


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

    def _get_data_helper(self):
        """
        [TODO:description]
        """
        doc_details = self.controller.documents[self.row_data[4]]
        headers = doc_details.get("headers", {})
        po_number = headers.get("PO #", "N/A")
        co_seq_number = headers.get("CO Seq #", "N/A")
        co_reason = headers.get("CO Reason", "N/A")
        co_date = headers.get("CO Date", "N/A")
        mt_data = doc_details.get("MT", {})
        file_data = doc_details.get("lines", {})
        mt_line_numbers = set(
            key for key, value in mt_data.items() if isinstance(value, dict)
        )
        file_line_numbers = set(file_data.keys())
        line_numbers = file_line_numbers | mt_line_numbers

        def remove_whitespace(s):
            return re.sub(r"\s+", "", s)

        table_data = []
        for line_number in sorted(line_numbers):
            file_line = file_data.get(line_number, {})
            mt_line = mt_data.get(line_number, {})

            file_qty = remove_whitespace(str(file_line.get("Qty", "N/A")))
            file_price = remove_whitespace(str(file_line.get("Price", "N/A")))
            file_uom = remove_whitespace(str(file_line.get("Uom", "N/A")))
            file_total = remove_whitespace(str(file_line.get("Total", "N/A")))
            esis_date = remove_whitespace(str(file_line.get("Scheduled Date", "N/A")))

            if isinstance(mt_line, dict):
                mt_part_number = remove_whitespace(
                    str(mt_line.get("Part_number", "N/A"))
                )
                mt_qty_ordered = remove_whitespace(
                    str(mt_line.get("Quantity Ordered", "N/A"))
                )
                mt_qty_shipped = remove_whitespace(
                    str(mt_line.get("Quantity Shipped", "N/A"))
                )
                mt_status = remove_whitespace(str(mt_line.get("Status", "N/A")))
                mt_next_due_date = remove_whitespace(
                    str(mt_line.get("Next Due Date", "N/A"))
                )
                mt_next_promise_date = remove_whitespace(
                    str(mt_line.get("Next Promise Date", "N/A"))
                )
            else:
                mt_part_number = "N/A"
                mt_qty_ordered = "N/A"
                mt_qty_shipped = "N/A"
                mt_status = "N/A"
                mt_next_due_date = "N/A"
                mt_next_promise_date = "N/A"

            table_data.append(
                {
                    "line_number": line_number,
                    "file_qty": file_qty,
                    "file_price": file_price,
                    "file_uom": file_uom,
                    "file_total": file_total,
                    "esis_date": esis_date,
                    "mt_part_number": mt_part_number,
                    "mt_qty_ordered": mt_qty_ordered,
                    "mt_qty_shipped": mt_qty_shipped,
                    "mt_status": mt_status,
                    "mt_next_due_date": mt_next_due_date,
                    "mt_next_promise_date": mt_next_promise_date,
                }
            )

        return po_number, co_seq_number, co_reason, co_date, table_data

    def open_details(self):
        """
        [TODO:description]
        """
        self.parent_widget.loading_modal.open()

        po_number, co_seq_number, co_reason, co_date, table_data = (
            self._get_data_helper()
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

        self.parent_widget.loading_modal.dismiss()

    def approve_document(self):
        asyncio.create_task(
            self.controller.approve_document(self.row_data, self.parent_widget)
        )

    def discard_document(self):
        asyncio.create_task(
            self.controller.discard_document(self.row_data, self.parent_widget)
        )


class LoadingModal(ModalView):
    """
    To show a loading icon to the user when doing compute intensive tasks.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.add_widget(Label(text="Loading...", font_size="20sp"))


class EsisAutoGUI(Screen):
    controller = ObjectProperty()
    table_size_bound = False  # Flag to check if size event is bound

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller
        self.create_table()
        self.update_status_light = Clock.schedule_interval(
            self.queue_update_scraper, 15
        )
        self.update_documents = Clock.schedule_interval(self.queue_update_documents, 60)
        self.queue_update_documents()

        self.loading_modal = LoadingModal(size_hint=(0.3, 0.3))

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

    def queue_update_scraper(self, *args):
        asyncio.create_task(self.controller.get_scraper_status(self))

    def queue_update_documents(self, *args):
        asyncio.create_task(self.controller.fetch_update_documents(self))

    def start_scraper_on_server(self, *args):
        asyncio.create_task(self.controller.start_scraper_on_server())


Builder.load_string(KV)
