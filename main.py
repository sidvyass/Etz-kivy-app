from kivy.app import App
from database.user_database import UserAuthentication
from gui.main_window import LoginWindow
from controllers.user_login_controller import LoginController
import asyncio


class LoginApp(App):
    def build(self):
        # Initialize the Model, View, and Controller
        model = UserAuthentication()
        view = LoginWindow(controller=None)
        controller = LoginController(model)
        view.controller = controller

        return view


if __name__ == "__main__":
    asyncio.run(LoginApp().async_run(async_lib="asyncio"))
