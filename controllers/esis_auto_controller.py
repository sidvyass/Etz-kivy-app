import urllib.parse
from kivy.core.window import Window
from kivy.metrics import dp
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from gui.esis_auto_window import EsisAutoGUI
from kivy.utils import get_color_from_hex
from controllers.base_logger import getlogger
from controllers.user_controller import UserAPI
import aiohttp
import os
import re
from kivy.properties import StringProperty


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


class EsisAutoController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app, user: UserAPI):
        self.LOGGER = getlogger("Esis Auto")
        self.main_app = app
        # self.user = UserAPI("60009", "67220")
        self.user = user
        self.user.login()

        # for prod

        self.LOGGER.info(self.user)

    async def start_scraper_on_server(self):
        """
        Makes a requst to the server to start the scraper. Updates on GUI when response.
        """
        self.main_app.show_small_notification("Requested scraper to start...")
        self.LOGGER.info(
            f"{self.user.data['username']} requested to start the scraper, awaiting response..."
        )
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.user.url}/run-scraper-service", headers=self.user.headers
            ) as req:
                self.LOGGER.info(
                    f"User - {self.user.data['username']} got - {req.status}"
                )
                if req.status == 200:
                    self.main_app.show_notification(
                        "Done!", "Scraper is running on server!"
                    )
                    return True
                else:
                    self.main_app.show_notification(
                        "Error", "Scraper may or may not be running"
                    )
                    return False

    def cancel_background_tasks(self, esis_window):
        """
        Only run at when exiting the esis window.

        :param esis_window ScreenKivy: Kivy UI instance to cancel clock
        """
        # TODO: still need to clear up data
        esis_window.update_status_light.cancel()
        esis_window.update_documents.cancel()

    async def get_scraper_status(self, esis_window):
        """Gets data from the API endpoint"""
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.user.url}/scraper-status", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    response = await req.json()
                    self.LOGGER.info(f"Server returned - {response}")
                    if response["status"]:
                        esis_window.ids.status_light.text_color = get_color_from_hex(
                            "#00FF00"
                        )  # Green
                    else:
                        esis_window.ids.status_light.text_color = get_color_from_hex(
                            "#FFFFFF"
                        )  # White
                else:
                    self.LOGGER.error(f"Server returned - {req.json()}")
                    return False

    async def fetch_update_documents(self, esis_window: EsisAutoGUI):
        """
        Get the latest scraped documents from the server. Save it in self.documents class instance variable.

        :param esis_window: instance of the window to build table UI.
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.user.url}/document-scraped-data", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    self.documents = await req.json()

                    all_rows = []
                    if not self.documents:
                        return

                    for key in self.documents.keys():
                        document = self.documents[key]
                        headers = document.get("headers", {})

                        po_number = headers.get("PO #", "NA")
                        co_seq_number = headers.get("CO Seq #", "NA")
                        co_reason = headers.get("CO Reason", "NA")
                        co_date = headers.get("CO Date", "NA")
                        create_date = headers.get(
                            "PO Date", "NA"
                        )  # Using 'PO Date' as 'CreateDate'
                        shipping_address_name = headers.get(
                            "ShippingAddressName", "NA"
                        )  # If not present, 'NA'

                        row = (
                            po_number,
                            co_seq_number,
                            co_reason,
                            co_date,
                            key,  # Key is likely the document identifier
                            create_date,
                            shipping_address_name,
                        )
                        all_rows.append(row)

                    esis_window.create_table(rows=all_rows)
                    self.main_app.show_small_notification("Documents Updated!")

                elif req.status == 401:
                    self.main_app.show_notification("Logged Out", "Please login again.")
                    self.main_app.logout()

                else:
                    self.LOGGER.error(
                        f"Could not load documents, server returned {req.status}"
                    )

    def open_file(self, row_data):
        """
        Opens file from the server location.

        :param row_data [TODO:type]: [TODO:description]
        """
        # TODO: check to see if this is on the server or not
        file_path = self.documents[row_data[4]]["filepath"]
        self.main_app.show_small_notification(str(file_path))
        try:
            os.startfile(file_path)  # This opens the file with the default PDF viewer
            self.LOGGER.info("opened")
        except Exception as e:  # TODO:handle file checking
            self.LOGGER.error(f"{e}")

    async def approve_document(self, row_values, esis_window):
        # show the notification bar with loading icon

        if "Cancel Item" in row_values:
            self.main_app.show_notification(
                "Operation not supported",
                f"Due to safety concerns, cancel item CO is currently not supported to be approved from this app",
            )

        else:
            async with aiohttp.ClientSession() as session:
                async with session.put(
                    f"{self.user.url}/document-scraped-data/approve/{urllib.parse.quote(row_values[4])}",
                    headers=self.user.headers,
                ) as req:
                    if req.status == 200:
                        response = await req.json()
                        self.LOGGER.info(response)
                        await self.fetch_update_documents(esis_window)
                        self.main_app.show_small_notification(
                            f"{row_values[4]} Successfully inserted"
                        )
                    else:
                        response = await req.json()
                        self.LOGGER.info(response)
                        self.main_app.show_small_notification(f"{response}")

            esis_window.loading_modal.dismiss()

    async def discard_document(self, row_filename, esis_window):
        # show the notification bar with loading icon
        self.main_app.show_notification(
            "Starting", f"Discarding file: {row_filename[4]}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.user.url}/document-scraped-data/discard/{urllib.parse.quote(row_filename[4])}",
                headers=self.user.headers,
            ) as req:
                if req.status == 200:
                    response = await req.json()
                    self.LOGGER.info(response)
                    await self.fetch_update_documents(esis_window)

                    self.main_app.show_small_notification(
                        f"{row_filename[4]} Successfully Deleted"
                    )
                else:
                    response = await req.json()
                    self.LOGGER.info(response)
                    self.main_app.show_small_notification(f"{response}")

    def go_to_home(self):
        self.main_app.screen_manager.current = "home_window"

    async def open_details(self, row_filename, spinner):
        """
        Opens a popup with the details inside.

        :param row_filename: The selected row's data.
        :param spinner: The loading spinner instance.
        """

        # Extract the document details using the appropriate key
        doc_details = self.documents[row_filename[4]]

        # Extract headers from the document details
        headers = doc_details.get("headers", {})

        # Extract required fields from headers
        po_number = headers.get("PO #", "N/A")
        co_seq_number = headers.get("CO Seq #", "N/A")
        co_reason = headers.get("CO Reason", "N/A")
        co_date = headers.get("CO Date", "N/A")

        # Extract 'MT' and 'lines' data
        mt_data = doc_details.get("MT", {})
        file_data = doc_details.get("lines", {})

        # Get line numbers from both 'MT' and 'lines' data
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

            # Extract data from 'lines' (ESIS) section
            file_qty = remove_whitespace(str(file_line.get("Qty", "N/A")))
            file_price = remove_whitespace(str(file_line.get("Price", "N/A")))
            file_uom = remove_whitespace(str(file_line.get("Uom", "N/A")))
            file_total = remove_whitespace(str(file_line.get("Total", "N/A")))
            esis_date = remove_whitespace(
                str(file_line.get("Scheduled Date", "N/A"))
            )  # New line added

            # Extract data from 'MT' section
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

            # Append the extracted data to the table data
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

        # Define the column headers
        column_headers = [
            "Line Number",
            "ESIS Qty",
            "ESIS Price",
            "ESIS UOM",
            "ESIS Total",
            "ESIS Date",
            "MT Part Number",
            "MT Qty Ordered",
            "MT Qty Shipped",
            "MT Status",
            "MT Next Due Date",
            "MT Next Promise Date",
        ]

        # Create the layout for the popup
        layout = BoxLayout(orientation="vertical", padding=10, spacing=10)

        # Create a grid layout for the header information
        info_layout = GridLayout(cols=2, padding=10, spacing=10, size_hint_y=None)
        info_layout.bind(minimum_height=info_layout.setter("height"))

        # Add header information to the grid layout
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

        # Create a scrollable view for the header information
        info_scrollview = ScrollView(size_hint=(1, None), size=(Window.width, dp(200)))
        info_scrollview.add_widget(info_layout)
        layout.add_widget(info_scrollview)

        # Create the header row for the table
        header_row = BoxLayout(
            orientation="horizontal", size_hint_y=None, height=dp(30), spacing=dp(5)
        )
        header_labels = [
            {"text": h, "width": dp(80)} if i == 0 else {"text": h, "width": dp(60)}
            for i, h in enumerate(column_headers)
        ]
        header_widths = [
            dp(80),
            dp(60),
            dp(60),
            dp(60),
            dp(60),
            dp(80),
            dp(100),
            dp(80),
            dp(80),
            dp(80),
            dp(100),
            dp(120),
        ]
        for i, header in enumerate(column_headers):
            lbl = Label(
                text=header,
                bold=True,
                size_hint_x=None,
                width=header_widths[i],
                halign="center",
            )
            header_row.add_widget(lbl)

        # Create the RecycleView
        rv = RecycleView(size_hint=(1, 1), do_scroll_x=True)
        rv.viewclass = "DetailTableRow"

        # Define the RecycleBoxLayout
        rv_layout = RecycleBoxLayout(
            orientation="vertical",
            default_size=(None, dp(30)),
            default_size_hint=(None, None),
            size_hint=(None, None),
            width=sum(header_widths) + dp(5) * (len(header_widths) - 1),
            height=dp(30) * len(table_data),
        )
        rv_layout.bind(minimum_height=rv_layout.setter("height"))
        rv_layout.bind(minimum_width=rv_layout.setter("width"))

        rv.add_widget(rv_layout)

        rv.layout_manager = rv_layout

        # Prepare data for the RecycleView
        rv.data = table_data

        # Create a container layout for the table
        table_container = BoxLayout(orientation="vertical", size_hint=(None, None))
        table_container.bind(minimum_height=table_container.setter("height"))
        table_container.bind(minimum_width=table_container.setter("width"))
        table_container.width = rv_layout.width
        table_container.add_widget(header_row)
        table_container.add_widget(rv)

        # Add the table_container to a ScrollView
        table_scroll = ScrollView(size_hint=(1, 1), do_scroll_x=True)
        table_scroll.add_widget(table_container)

        layout.add_widget(table_scroll)

        # Add a close button to the popup
        close_button = Button(text="Close", size_hint_y=None, height=50)
        layout.add_widget(close_button)

        # Create and open the popup
        popup = Popup(title="Document Details", content=layout, size_hint=(0.9, 0.9))

        close_button.bind(on_release=popup.dismiss)

        spinner.dismiss()

        popup.open()
