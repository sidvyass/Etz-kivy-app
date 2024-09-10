from database.user_database import UserAuthentication
import asyncio


class LoginController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, login_model: UserAuthentication):
        self.model = login_model

    async def start_login(self, callback):
        data = await self.model.fetch_single_user()

        # NOTE: here we put all our login for login, errors, and success

        callback("login success")
