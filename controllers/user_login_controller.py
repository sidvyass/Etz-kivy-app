from database.user_database import UserAuthentication
import asyncio
from base_logger import getlogger


class LoginController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, login_model: UserAuthentication):
        self.model: UserAuthentication = login_model  # type hint for auto complete
        self.LOGGER = getlogger("Login Controller")
        # NOTE: self.data is a coroutine object. These need to be awaited before we use the return value
        self.data = asyncio.create_task(self.model.fetch_user_data())

    async def authenticate(self, username: str, password: str) -> bool:
        self.LOGGER.info("Authenicating...")
        data: list = await self.data

        data = [tuple(d) for d in data]

        if len(data) == 0:
            raise IndexError

        match_tup = (str(username.strip()), str(password.strip()))
        if match_tup in data:
            self.LOGGER.info("Login successful")
            # here we will render the other main screen
        else:
            self.LOGGER.info("Incorrect ID or password")
            return False
