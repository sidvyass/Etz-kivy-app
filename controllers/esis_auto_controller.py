import urllib.parse
from fuzzywuzzy import fuzz
from gui.esis_auto_window import EsisAutoGUI
from controllers.base_logger import getlogger
from controllers.user_controller import UserAPI
import aiohttp
import os
import re


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

    def go_to_home(self, row_data):
        self.main_app.screen_manager.current = "home_window"

    def search(self, esis_window):
        """
        Perform fuzzy search on CO Seq # or PO #. Update results.

        """
        if esis_window.ids.search_button_text.text == "Reset":
            esis_window.create_table(rows=self.all_rows)
            esis_window.ids.search_button_text.text = "Search"
            esis_window.ids.search_button.md_bg_color = (0.3, 0.3, 0.3, 1)
            return

        search_val = esis_window.ids.search_field.text
        search_results = []
        if search_val:
            if len(search_val) < 5:  # CO Seq #
                for row in self.all_rows:
                    if 50 < fuzz.partial_ratio(search_val, row[1]):
                        search_results.append(row)
            else:
                for row in self.all_rows:
                    if 50 < fuzz.partial_ratio(search_val, row[2]):
                        search_results.append(row)

            if len(search_results) >= 1:
                esis_window.create_table(rows=search_results)
                esis_window.ids.search_button_text.text = "Reset"
                esis_window.ids.search_button.md_bg_color = (1, 0, 0, 1)

            else:
                self.main_app.show_small_notification(
                    "Search results were none. Check search value."
                )

        else:
            esis_window.ids.search_field.error = True

    async def start_scraper_on_server(self, esis_window):
        """
        Makes a requst to the server to start the scraper. Updates on GUI when response.
        """

        async with aiohttp.ClientSession() as session:
            async with session.post(
                f"{self.user.url}/run-scraper-service", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    self.main_app.show_small_notification(
                        "Success! Scraper is running."
                    )
                else:
                    self.main_app.show_notification(
                        "Error", "Scraper may or may not be running"
                    )
                    esis_window.ids.run_scraper.disabled = False

    def cancel_background_tasks(self, esis_window):
        """
        Only run at when exiting the esis window.

        :param esis_window ScreenKivy: Kivy UI instance to cancel clock
        """
        # TODO: still need to clear up data
        esis_window.update_documents.cancel()

    async def fetch_scraper_status(self, esis_window):
        """
        Get status, enable disable button
        """

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.user.url}/scraper-status", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    is_running = await req.json()
                    if is_running["status"]:
                        esis_window.ids.run_scraper.disabled = True
                    else:
                        esis_window.ids.run_scraper.disabled = False

                else:
                    self.main_app.show_small_notification(
                        f"Server did not return a proper response. {req.status}"
                    )

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

                    self.all_rows = []
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
                            key,
                            create_date,
                            shipping_address_name,
                        )
                        self.all_rows.append(row)

                    esis_window.create_table(rows=self.all_rows)
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

    def _get_data_helper(self, row_data):
        """
        Prepares all the data for the GUI.
        """
        doc_details = self.documents[row_data[4]]
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
