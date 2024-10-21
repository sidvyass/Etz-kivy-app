import requests
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, NoTransition
from gui.login_window import LoginWindow
from controllers.login_controller import LoginController
from controllers.esis_auto_controller import EsisAutoController
from gui.esis_auto_window import EsisAutoGUI
from gui.home_window import HomeWindow
from controllers.home_controller import HomeController
from kivy.core.window import Window
import asyncio


class EsisAutoApp(MDApp):
    dialog = None

    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        Window.size = (1200, 900)

        controller = LoginController(self)
        view = LoginWindow(controller=controller)

        self.theme_cls.primary_palette = "Red"
        self.theme_cls.theme_style = "Dark"

        self.screen_manager.add_widget(view)

        # notifications
        self.current_dialog = None  # might not need to track this
        self.current_snackbar = None

        return self.screen_manager

    def load_main_window(self, user):
        """
        # NOT FOR MANUAL USE
        Called by login controller after successful auth.

        :param user UserAPI: Login controller passes the user to this.
        """
        self.user = user  # for logout

        self.home_window_controller = HomeController(self, user)
        self.home_window = HomeWindow(self.home_window_controller)

        self.esis_window_controller = EsisAutoController(self, user)
        self.esis_view = EsisAutoGUI(self.esis_window_controller)

        self.screen_manager.add_widget(self.esis_view)
        self.screen_manager.add_widget(self.home_window)
        self.screen_manager.current = "home_window"

    # *********** small notifications **************

    def show_small_notification(self, in_text: str):
        """Function to show notification used by the controllers"""
        if self.current_snackbar:
            self.current_snackbar.bind(
                on_dismiss=lambda *args: self.show_new_snackbar(in_text)
            )
            self.current_snackbar.dismiss()
        else:
            self.show_new_snackbar(in_text)

    def show_new_snackbar(self, in_text: str):
        """Helper function to show notification used by the controllers"""
        self.current_snackbar = MDSnackbar(
            MDLabel(
                text=in_text,
            ),
        )
        self.current_snackbar.open()

    # ******** large notifications ***********

    def show_notification(self, title: str, text: str):
        self.dialog = MDDialog(
            title=title,
            text=text,
            buttons=[
                MDRaisedButton(text="OK", on_release=self.close_dialog),
                MDRaisedButton(text="Cancel", on_release=self.close_dialog),
            ],
        )
        self.dialog.open()

    def close_dialog(self, *args):
        """Only called after the show notification"""
        self.dialog.dismiss()  # type: ignore

    def logout(self):
        req = requests.post(f"{self.user.url}/logout", headers=self.user.headers)
        if req.status_code == 200:
            # TODO:: add all the deactivations of the clock here
            self.esis_window_controller.cancel_background_tasks(self.esis_view)
            self.screen_manager.current = "login_screen"


if __name__ == "__main__":
    asyncio.run(EsisAutoApp().async_run(async_lib="asyncio"))
