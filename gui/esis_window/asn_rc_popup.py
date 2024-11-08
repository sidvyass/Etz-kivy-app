from kivy.app import App
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.scrollview import ScrollView


# TODO:
#   1. Layout in full screen does not cover the full screen

# NOTE: the open details popup is with size hints and not fixed sizes


kv = """
<RCRow>:
    size_hint_y: None
    height: dp(40)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: None
        width: self.minimum_width
        Label:
            text: root.advice_date
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.pack_slip
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.planned_delivery_date
            size_hint_x: None
            width: dp(150)
        Label:
            text: root.received_date
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.buyer_part
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.po_line
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.qty_received
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.uom
            size_hint_x: None
            width: dp(100)

        Button:
            text: "Open File"
            on_release: root.open_file()
            size_hint_x: None
            width: dp(100)
            background_color: (0.3, 0.3, 0.3, 1)
            color: (1, 1, 1, 1)
            pos_hint: {'center_y': 0.5}

<ASNRow>:
    size_hint_y: None
    height: dp(40)
    BoxLayout:
        orientation: 'horizontal'
        size_hint_x: None
        width: self.minimum_width
        Label:
            text: root.delivery_date
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.pack_slip
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.ship_date
            size_hint_x: None
            width: dp(150)
        Label:
            text: root.asn_line
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.buyer_part
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.po_line
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.ship_qty
            size_hint_x: None
            width: dp(100)
        Label:
            text: root.uom
            size_hint_x: None
            width: dp(100)

        Button:
            text: "Open File"
            on_release: root.open_file()
            size_hint_x: None
            width: dp(100)
            background_color: (0.3, 0.3, 0.3, 1)
            color: (1, 1, 1, 1)
            pos_hint: {'center_y': 0.5}
"""


Builder.load_string(kv)


class RCRow(BoxLayout):
    rc_id = StringProperty()
    rc_filepath = StringProperty()
    advice_date = StringProperty()
    pack_slip = StringProperty()
    planned_delivery_date = StringProperty()
    received_date = StringProperty()
    reference = StringProperty()
    shipment_id = StringProperty()
    buyer_part = StringProperty()
    po_line = StringProperty()
    po_number = StringProperty()
    qty_received = StringProperty()
    uom = StringProperty()

    def open_file(self):
        import os

        if os.path.exists(self.rc_filepath):
            os.startfile(self.rc_filepath)
        else:
            print(f"File {self.rc_filepath} does not exist.")


class ASNRow(BoxLayout):
    asn_id = StringProperty()
    asn_filepath = StringProperty()
    delivery_date = StringProperty()
    pack_slip = StringProperty()
    ship_date = StringProperty()
    asn_line = StringProperty()
    buyer_part = StringProperty()
    po_line = StringProperty()
    ship_qty = StringProperty()
    uom = StringProperty()

    def open_file(self):
        import os

        if os.path.exists(self.asn_filepath):
            os.startfile(self.asn_filepath)
        else:
            print(f"File {self.asn_filepath} does not exist.")


def open_asn_rcs_popup(data):
    # Create the main layout for the popup
    layout = BoxLayout(orientation="vertical", spacing=10, padding=10)

    # Label for RCs
    rc_label = Label(text="Receiving Confirmations (RCs)", size_hint_y=None, height=30)
    layout.add_widget(rc_label)

    # Header for RCs
    rc_header = BoxLayout(orientation="horizontal", size_hint=(None, None), height=30)
    rc_header.bind(minimum_width=rc_header.setter("width"))
    rc_header.add_widget(Label(text="Advice Date", size_hint_x=None, width=dp(100)))
    rc_header.add_widget(Label(text="Pack Slip", size_hint_x=None, width=dp(100)))
    rc_header.add_widget(
        Label(text="Planned Delivery Date", size_hint_x=None, width=dp(150))
    )
    rc_header.add_widget(Label(text="Received Date", size_hint_x=None, width=dp(100)))
    rc_header.add_widget(Label(text="Buyer Part", size_hint_x=None, width=dp(100)))
    rc_header.add_widget(Label(text="PO Line", size_hint_x=None, width=dp(100)))
    rc_header.add_widget(Label(text="Qty Received", size_hint_x=None, width=dp(100)))
    rc_header.add_widget(Label(text="UOM", size_hint_x=None, width=dp(100)))
    rc_header.add_widget(Label(text="Action", size_hint_x=None, width=dp(100)))

    # ScrollView for RCs
    rc_scroll = ScrollView(size_hint=(1, 0.4), do_scroll_x=True)

    # Create a container to hold both the header and data rows
    rc_box = BoxLayout(orientation="vertical", size_hint=(None, None))
    rc_box.bind(minimum_height=rc_box.setter("height"))
    rc_box.bind(minimum_width=rc_box.setter("width"))

    # Add header to the container
    rc_box.add_widget(rc_header)

    # Container for RC data rows
    rc_container = BoxLayout(orientation="vertical", size_hint=(None, None))
    rc_container.bind(minimum_height=rc_container.setter("height"))
    rc_container.bind(minimum_width=rc_container.setter("width"))
    rc_box.add_widget(rc_container)

    # Add the container to the ScrollView
    rc_scroll.add_widget(rc_box)
    layout.add_widget(rc_scroll)

    # Populate RCs
    for rc_dict in data.get("RCs", []):
        for rc_key, rc_value in rc_dict.items():
            rc_row = RCRow()
            rc_row.rc_id = rc_key
            rc_row.rc_filepath = rc_value.get("RC Filepath", "")
            rc_headers = rc_value.get("RC Headers", {})
            rc_data = rc_value.get("RC data", {})

            rc_row.advice_date = rc_headers.get("advice_date", "")
            rc_row.pack_slip = rc_headers.get("pack_slip", "")
            rc_row.planned_delivery_date = rc_headers.get("planned_delivery_date", "")
            rc_row.received_date = rc_headers.get("received_date", "")
            rc_row.buyer_part = rc_data.get("buyer_part", "")
            rc_row.po_line = rc_data.get("po_line", "")
            rc_row.qty_received = rc_data.get("qty_received", "")
            rc_row.uom = rc_data.get("uom", "")

            rc_container.add_widget(rc_row)

    # Label for ASNs
    asn_label = Label(text="Advance Ship Notices (ASNs)", size_hint_y=None, height=30)
    layout.add_widget(asn_label)

    # Header for ASNs
    asn_header = BoxLayout(orientation="horizontal", size_hint=(None, None), height=30)
    asn_header.bind(minimum_width=asn_header.setter("width"))
    asn_header.add_widget(Label(text="Delivery Date", size_hint_x=None, width=dp(100)))
    asn_header.add_widget(Label(text="Pack Slip", size_hint_x=None, width=dp(100)))
    asn_header.add_widget(Label(text="Ship Date", size_hint_x=None, width=dp(150)))
    asn_header.add_widget(Label(text="ASN Line", size_hint_x=None, width=dp(100)))
    asn_header.add_widget(Label(text="Buyer Part", size_hint_x=None, width=dp(100)))
    asn_header.add_widget(Label(text="PO Line", size_hint_x=None, width=dp(100)))
    asn_header.add_widget(Label(text="Ship Qty", size_hint_x=None, width=dp(100)))
    asn_header.add_widget(Label(text="UOM", size_hint_x=None, width=dp(100)))
    asn_header.add_widget(Label(text="Action", size_hint_x=None, width=dp(100)))

    # ScrollView for ASNs
    asn_scroll = ScrollView(size_hint=(1, 0.4), do_scroll_x=True)

    # Create a container to hold both the header and data rows
    asn_box = BoxLayout(orientation="vertical", size_hint=(None, None))
    asn_box.bind(minimum_height=asn_box.setter("height"))
    asn_box.bind(minimum_width=asn_box.setter("width"))

    # Add header to the container
    asn_box.add_widget(asn_header)

    # Container for ASN data rows
    asn_container = BoxLayout(orientation="vertical", size_hint=(None, None))
    asn_container.bind(minimum_height=asn_container.setter("height"))
    asn_container.bind(minimum_width=asn_container.setter("width"))
    asn_box.add_widget(asn_container)

    # Add the container to the ScrollView
    asn_scroll.add_widget(asn_box)
    layout.add_widget(asn_scroll)

    # Populate ASNs
    for asn_dict in data.get("ASNs", []):
        for asn_key, asn_value in asn_dict.items():
            asn_row = ASNRow()
            asn_row.asn_id = asn_key
            asn_row.asn_filepath = asn_value.get("ASN Filepath", "")
            asn_headers = asn_value.get("ASN Headers", {})
            asn_data = asn_value.get("ASN data", {})

            asn_row.delivery_date = asn_headers.get("delivery_date", "")
            asn_row.pack_slip = asn_headers.get("pack_slip", "")
            asn_row.ship_date = asn_headers.get("ship_date", "")
            asn_row.asn_line = asn_data.get("asn_line", "")
            asn_row.buyer_part = asn_data.get("buyer_part", "")
            asn_row.po_line = asn_data.get("po_line", "")
            asn_row.ship_qty = asn_data.get("ship_qty", "")
            asn_row.uom = asn_data.get("uom", "")

            asn_container.add_widget(asn_row)

    # Create and open the popup
    popup = Popup(title="ASN and RC Details", content=layout, size_hint=(0.9, 0.9))
    popup.open()


# Test Data for Popup
test_data = {
    "RCs": [
        {
            "RC 4502156637": {
                "RC Filepath": "C:\\PythonProjects\\auto-server\\services\\scraper\\downloads\\rc_1.rtf",
                "RC Headers": {
                    "advice_date": "10/30/24",
                    "pack_slip": "31101",
                    "planned_delivery_date": "10/29/24",
                    "received_date": "10/30/24",
                    "reference": "20241030173459",
                    "shipment_id": "UN962676958H000117932",
                },
                "RC data": {
                    "buyer_part": "141T5332-7",
                    "po_line": "00010",
                    "po_number": "4502156637",
                    "qty_received": "4",
                    "uom": "EA",
                },
            }
        }
    ],
    "ASNs": [
        {
            "ASN 1234567890": {
                "ASN Filepath": "C:\\PythonProjects\\auto-server\\services\\scraper\\downloads\\asn_1.rtf",
                "ASN Headers": {
                    "delivery_date": "10/28/24",
                    "pack_slip": "31100",
                    "ship_date": "10/27/24",
                },
                "ASN data": {
                    "asn_line": "00010",
                    "buyer_part": "141T5332-7",
                    "po_line": "00010",
                    "ship_qty": "4",
                    "uom": "EA",
                },
            }
        }
    ],
}


# Kivy App for Testing the Popup
class TestPopupApp(App):
    def build(self):
        open_asn_rcs_popup(test_data)
        return BoxLayout()


if __name__ == "__main__":
    TestPopupApp().run()
