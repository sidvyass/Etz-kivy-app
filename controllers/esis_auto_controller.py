import urllib.parse
from kivy.core.window import Window
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.uix.popup import Popup
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
import os
from gui.esis_auto_window import EsisAutoGUI
from kivy.utils import get_color_from_hex
from controllers.base_logger import getlogger
from controllers.user_controller import UserAPI
import aiohttp


class EsisAutoController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app):
        self.LOGGER = getlogger("MainWindow controller")
        self.main_app = app
        self.user = UserAPI("60009", "67220")

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
                    for key in self.documents.keys():
                        if "CreateDate" in self.documents[key]["MT"].keys():

                            create_date = self.documents[key]["MT"]["CreateDate"].split(
                                "T"
                            )[0]
                        else:
                            create_date = "NA"

                        if "ShippingAddressName" in self.documents[key]["MT"].keys():
                            shipping_address_name = self.documents[key]["MT"][
                                "ShippingAddressName"
                            ]
                        else:
                            shipping_address_name = "NA"

                        row = (
                            self.documents[key]["po_number"],
                            self.documents[key]["co_seq_number"],
                            self.documents[key]["co_reason"],
                            self.documents[key]["co_date"],
                            key,
                            create_date,
                            shipping_address_name,
                        )
                        all_rows.append(row)

                    esis_window.create_table(rows=all_rows)
                    self.main_app.show_small_notification("Documents Updated!")
                else:
                    self.LOGGER.error(
                        f"Could not load documents, server returned {req.status}"
                    )
                    self.main_app.show_notification(
                        "Error", "Could not fetch documents"
                    )

    def open_file(self, row_data):
        # TODO: check to see if this is on the server or not
        file_path = self.documents[row_data[4]]["filepath"]
        self.main_app.show_small_notification(str(file_path))
        try:
            os.startfile(file_path)  # This opens the file with the default PDF viewer
            self.LOGGER.info("opened")
        except Exception as e:  # TODO:handle file checking
            self.LOGGER.error(f"{e}")

    async def approve_document(self, row_filename, esis_window):
        # show the notification bar with loading icon
        self.main_app.show_notification(
            "Starting", f"Approving file: {row_filename[4]}"
        )

        async with aiohttp.ClientSession() as session:
            async with session.put(
                f"{self.user.url}/document-scraped-data/approve/{urllib.parse.quote(row_filename[4])}",
                headers=self.user.headers,
            ) as req:
                if req.status == 200:
                    response = await req.json()
                    self.LOGGER.info(response)
                    await self.fetch_update_documents(esis_window)
                    self.main_app.show_small_notification(
                        f"{row_filename[4]} Successfully inserted"
                    )
                else:
                    response = await req.json()
                    self.LOGGER.info(response)
                    self.main_app.show_small_notification(f"{response}")

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

    def open_details(self, row_filename):
        """
        Opens a popup with the details inside.

        :param row_filename [TODO:type]: [TODO:description]
        """

        doc_details = self.documents[row_filename[4]]

        po_number = doc_details.get("po_number", "N/A")
        co_seq_number = doc_details.get("co_seq_number", "N/A")
        co_reason = doc_details.get("co_reason", "N/A")
        co_date = doc_details.get("co_date", "N/A")
        mt_data = doc_details.get("MT", {})
        file_data = doc_details.get("File Data", {})

        mt_line_numbers = set(
            key for key, value in mt_data.items() if isinstance(value, dict)
        )
        file_line_numbers = set(file_data.keys())

        line_numbers = file_line_numbers | mt_line_numbers

        table_data = []
        for line_number in sorted(line_numbers):
            file_line = file_data.get(line_number, {})
            mt_line = mt_data.get(line_number, {})

            file_qty = str(file_line.get("qty", "N/A"))
            file_price = str(file_line.get("price", "N/A"))
            file_uom = str(file_line.get("uom", "N/A"))
            file_total = str(file_line.get("total", "N/A"))

            if isinstance(mt_line, dict):
                # TODO: add qty demand
                mt_part_number = str(mt_line.get("Part_number", "N/A"))
                mt_qty_ordered = str(mt_line.get("Quantity Ordered", "N/A"))
                mt_qty_shipped = str(mt_line.get("Quantity Shipped", "N/A"))
                mt_status = str(mt_line.get("Status", "N/A"))
                mt_next_due_date = str(mt_line.get("Next Due Date", "N/A"))
                mt_next_promise_date = str(mt_line.get("Next Promise Date", "N/A"))
            else:
                mt_part_number = "N/A"
                mt_qty_ordered = "N/A"
                mt_qty_shipped = "N/A"
                mt_status = "N/A"
                mt_next_due_date = "N/A"
                mt_next_promise_date = "N/A"

            table_data.append(
                [
                    line_number,
                    file_qty,
                    file_price,
                    file_uom,
                    file_total,
                    mt_part_number,
                    mt_qty_ordered,
                    mt_qty_shipped,
                    mt_status,
                    mt_next_due_date,
                    mt_next_promise_date,
                ]
            )

        column_data = [
            ("Line Number", dp(30)),
            ("File Qty", dp(30)),
            ("File Price", dp(30)),
            ("File UOM", dp(30)),
            ("File Total", dp(30)),
            ("MT Part Number", dp(30)),
            ("MT Qty Ordered", dp(30)),
            ("MT Qty Shipped", dp(30)),
            ("MT Status", dp(30)),
            ("MT Next Due Date", dp(30)),
            ("MT Next Promise Date", dp(30)),
        ]

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

        info_scrollview = ScrollView(size_hint=(1, None), size=(Window.width, dp(200)))
        info_scrollview.add_widget(info_layout)
        layout.add_widget(info_scrollview)

        table = MDDataTable(
            size_hint=(1, None),
            height=dp(400),  # Adjust height as needed
            use_pagination=True,
            column_data=column_data,
            row_data=table_data,
            check=False,
        )

        table_scroll = ScrollView()
        table_scroll.add_widget(table)

        layout.add_widget(table_scroll)

        close_button = Button(text="Close", size_hint_y=None, height=50)
        layout.add_widget(close_button)

        popup = Popup(title="Document Details", content=layout, size_hint=(0.9, 0.9))

        close_button.bind(on_release=popup.dismiss)

        popup.open()

    def go_to_home(self):
        self.main_app.screen_manager.current = "home_window"
