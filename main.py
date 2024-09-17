# from kivy.app import App
from kivymd.app import MDApp
from kivy.uix.screenmanager import ScreenManager
from gui.login_window import LoginWindow
from controllers.user_login_controller import LoginController
from controllers.main_controller import MainWindowController
from gui.main_window import HomeWindow
import asyncio


class LoginApp(MDApp):
    def build(self):
        self.screen_manager = ScreenManager()
        # Initialize the Model, View, and Controller
        controller = LoginController(self)
        view = LoginWindow(controller=controller)

        self.theme_cls.primary_palette = "Blue"

        self.screen_manager.add_widget(view)

        return self.screen_manager

    def load_main_window(self, user):

        # NOTE: this is called by the login controller

        main_controller = MainWindowController(self, user)
        main_view = HomeWindow(main_controller)

        self.screen_manager.add_widget(main_view)
        self.screen_manager.current = "main_window"


if __name__ == "__main__":
    asyncio.run(LoginApp().async_run(async_lib="asyncio"))
