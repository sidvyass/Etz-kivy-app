import urllib.parse
import os
from gui.esis_auto_window import EsisAutoGUI
from kivy.utils import get_color_from_hex
import requests
import json
from controllers.base_logger import getlogger  # type: ignore
from controllers.user_controller import UserAPI
import aiohttp


class EsisAutoController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app):

        self.LOGGER = getlogger("MainWindow controller")
        self.main_app = app
        self.user = UserAPI("60009", "67220")
        self.LOGGER.info(f"{self.user} is logged in")

    async def start_scraper_on_server(self):
        """Function that calls the API to start the scraper"""
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
        # TODO: still need to clear up data
        esis_window.update_status_light.cancel()
        esis_window.update_documents.cancel()

    async def get_scraper_status(self, esis_window):
        """Gets data from the API endpoint"""
        self.LOGGER.info("Getting scraper status...")
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
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.user.url}/document-scraped-data", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    self.documents = await req.json()

                    all_rows = []
                    for key, value in self.documents.items():

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
            "Starting", f"Approving file: {row_filename[4]}"
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
