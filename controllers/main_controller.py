import asyncio
from base_logger import getlogger  # type: ignore
from controllers.user_controller import UserAPI
import aiohttp


class MainWindowController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app, user: UserAPI):
        self.app = app
        self.user = user
        assert self.user
        self.LOGGER = getlogger("main window controller, ")

    async def get_scraped_documents(self):
        pass
