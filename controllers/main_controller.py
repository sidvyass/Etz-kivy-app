import asyncio
import requests
from kivy.resources import resource_add_path
from controllers.base_logger import getlogger  # type: ignore
from controllers.user_controller import UserAPI
import aiohttp


class MainWindowController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app, user: UserAPI):
        self.app = app
        self.user = user
        print("logging in.. ")
        self.user.login()
        self.LOGGER = getlogger("main window controller")

    async def start_scraper_on_server(self):
        self.app.show_small_notification("Requested scraper to start...")
        # TODO: production code comments

        # if not self.user._is_logged_in:
        #     self.LOGGER.critical(
        #         f"User - {self.user.data}! Is accessing this without loggin in"
        #     )
        #     return False
        # else:
        # async with aiohttp.ClientSession() as session:
        #     async with session.post(
        #         f"{self.user.url}/run-scraper-service", headers=self.user.headers
        #     ) as req:
        #         if req.status == 200:
        #             result = await req.json()
        #             self.LOGGER.info(f"Success - {result}")
        #             self.app.show_notification("Done!", "Scraper is running on server!")
        #             return True
        #         else:
        #             self.LOGGER.error(f"server error {req.status}")
        #             self.app.show_notification(
        #                 "Error", "Scraper may or may not be running"
        #             )
        #             return False

    # NOTE: this is not async bc common sense
    def logout(self):
        req = requests.post(f"{self.user.url}/logout", headers=self.user.headers)
        if req.status_code == 200:
            self.LOGGER.info(f"Logged out user {self.user.data}")
            self.app.screen_manager.current = "login_screen"

        else:
            self.LOGGER.error(f"server error")
