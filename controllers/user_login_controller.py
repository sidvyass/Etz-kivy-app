from database.user_database import UserAuthentication
import asyncio
from base_logger import getlogger


class LoginController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, login_model: UserAuthentication, app):
        self.model: UserAuthentication = login_model  # type hint for auto complete
        self.LOGGER = getlogger("Login Controller")
        # NOTE: self.data is a coroutine object. These need to be awaited before we use the return value
        self.data = asyncio.create_task(self.model.fetch_user_data())
        self.app = app  # this is the main app by which we call mainwindow

    async def authenticate(self, username: str, password: str):
        # NOTE: dev
        self.app.load_main_window()

        # self.LOGGER.info("Authenicating...")
        # data: list = await self.data
        #
        # data = [tuple(d) for d in data]
        #
        # if len(data) == 0:
        #     raise IndexError
        #
        # match_tup = (str(username.strip()), str(password.strip()))
        # if match_tup in data:
        #     self.LOGGER.info("Login successful")
        #     self.app.load_main_window()
        #
        # else:
        #     self.LOGGER.info("Incorrect ID or password")
        #     return False
