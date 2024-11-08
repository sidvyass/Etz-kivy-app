from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.widget import Widget
from kivy.properties import StringProperty
from kivy.lang import Builder
from kivy.uix.label import Label
from kivy.metrics import dp
from kivy.uix.popup import Popup


kv = """
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

    Label:
        text: root.file_qty
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.file_price
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.file_uom
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.file_total
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.esis_date
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.mt_part_number
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.mt_qty_ordered
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.mt_qty_shipped
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.mt_status
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.mt_next_due_date
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'

    Label:
        text: root.mt_next_promise_date
        size_hint_x: 1
        halign: 'center'
        valign: 'middle'
"""

Builder.load_string(kv)


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


def open_details_popup(data):
    po_number, co_seq_number, co_reason, co_date, table_data = data

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
