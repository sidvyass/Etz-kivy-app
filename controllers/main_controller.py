import os
import requests
from controllers.base_logger import getlogger  # type: ignore
from controllers.user_controller import UserAPI
import aiohttp


class MainWindowController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app, user: UserAPI):
        self.LOGGER = getlogger("MainWindow controller")
        self.app = app
        self.user = user
        assert self.user._is_logged_in
        self.LOGGER.info(f"{self.user} is logged in")

    async def start_scraper_on_server(self):
        """Function that calls the API to start the scraper"""
        self.app.show_small_notification("Requested scraper to start...")
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
                    result = req.json()
                    self.app.show_notification("Done!", "Scraper is running on server!")
                    return True
                else:
                    self.app.show_notification(
                        "Error", "Scraper may or may not be running"
                    )
                    return False

    def logout(self):
        # TODO: still need to clear up data
        req = requests.post(f"{self.user.url}/logout", headers=self.user.headers)
        if req.status_code == 200:
            self.LOGGER.info(f"Logged out user {self.user.data}")
            self.app.screen_manager.current = "login_screen"
        else:
            self.LOGGER.error(f"server error")

    async def get_scraper_status(self):
        """This endpoint has to get all the data from the server about documents"""
        self.LOGGER.info("Getting scraper status...")
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.user.url}/scraper-status", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    response = await req.json()
                    self.LOGGER.info(f"Server returned - {response}")
                    return response["status"]
                else:
                    self.LOGGER.error(f"Server returned - {req.json()}")
                    return False

    async def fetch_update_documents(self, home_window):
        async with aiohttp.ClientSession() as session:
            async with session.get(
                f"{self.user.url}/document-scraped-data", headers=self.user.headers
            ) as req:
                if req.status == 200:
                    response = await req.json()
                    # TODO: need to parse the data and then send it back
                    home_window.create_table(rows=response["data"])
                    self.app.show_small_notification("Documents Updated!")
                else:
                    self.app.show_notification("Error", "Could not fetch documents")

    def open_file(self, file_path):
        # TODO: check to see if this is on the server or not
        self.app.show_small_notification("opening file...")
        if os.path.exists(file_path):
            try:
                os.startfile(
                    file_path
                )  # This opens the file with the default PDF viewer
            except Exception as e:
                self.LOGGER.error(f"Could not open file - {self.user}")
        else:
            self.app.show_small_notification("Error in opening file")
