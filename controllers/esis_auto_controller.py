import os
from kivy.utils import get_color_from_hex
import requests
from controllers.base_logger import getlogger  # type: ignore
from controllers.user_controller import UserAPI
import aiohttp


class EsisAutoController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app, user: UserAPI):
        self.LOGGER = getlogger("MainWindow controller")
        self.main_app = app
        self.user = user
        assert self.user._is_logged_in
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

    async def fetch_update_documents(self, esis_window):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.user.url}/document-scraped-data", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    response = await req.json()
                    esis_window.create_table(rows=response["data"])
                    self.main_app.show_small_notification("Documents Updated!")
                else:
                    self.LOGGER.error(
                        f"Could not load documents, server returned {req.status}"
                    )
                    self.main_app.show_notification(
                        "Error", "Could not fetch documents"
                    )

    def open_file(self, file_path):
        # TODO: check to see if this is on the server or not
        self.main_app.show_small_notification("opening file...")
        if os.path.exists(file_path):
            try:
                os.startfile(
                    file_path
                )  # This opens the file with the default PDF viewer
            except Exception as e:
                self.LOGGER.error(f"Could not open file - {self.user}")
        else:
            self.main_app.show_small_notification("Error in opening file")

    def go_to_home(self):
        self.main_app.screen_manager.current = "home_window"
