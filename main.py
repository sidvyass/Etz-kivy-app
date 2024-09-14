# from kivy.app import App
from kivymd.app import MDApp
from database.user_database import UserAuthentication
from gui.login_window import LoginWindow
from controllers.user_login_controller import LoginController
import asyncio


class LoginApp(MDApp):
    def build(self):
        # Initialize the Model, View, and Controller
        model = UserAuthentication()
        controller = LoginController(model)
        view = LoginWindow(controller=controller)

        self.theme_cls.primary_palette = "Blue"

        return view


if __name__ == "__main__":
    asyncio.run(LoginApp().async_run(async_lib="asyncio"))
