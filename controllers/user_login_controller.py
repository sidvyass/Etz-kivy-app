import asyncio
from base_logger import getlogger
from controllers.user_controller import UserAPI


class LoginController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app):
        self.app = app
        self.LOGGER = getlogger("Login controller")

    async def authenticate(self, username: str, password: str):
        # NOTE: dev
        self.user = UserAPI(username, password)
        # auth = await self.user.login()
        #
        # if not auth:
        #     return False
        # else:
        self.app.load_main_window(self.user)
