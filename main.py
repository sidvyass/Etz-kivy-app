# from kivy.app import App
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.snackbar.snackbar import MDSnackbar
from kivymd.uix.dialog import MDDialog
from kivymd.uix.button import MDRaisedButton
from kivy.uix.screenmanager import ScreenManager, NoTransition
from gui.login_window import LoginWindow
from controllers.user_login_controller import LoginController
from controllers.esis_auto_controller import MainWindowController
from gui.esis_auto_window import EsisAutoGUI
from gui.home_window import HomeWindow
from controllers.home_controller import HomeController
import asyncio


class EsisAutoApp(MDApp):
    dialog = None

    def build(self):
        self.screen_manager = ScreenManager(transition=NoTransition())
        # Initialize the Model, View, and Controller
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

        # NOTE: this is called by the login controller

        # main_controller = HomeController(self, user)
        # my_view = HomeWindow(main_controller)
        main_controller = MainWindowController(self, user)
        main_view = EsisAutoGUI(main_controller)

        self.screen_manager.add_widget(main_view)
        self.screen_manager.current = "esis_auto_gui"

    # *********** small notifications **************

    def show_small_notification(self, in_text: str):
        """Helper function to show notification used by the controllers"""
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

    # ******** END ***********


if __name__ == "__main__":
    asyncio.run(EsisAutoApp().async_run(async_lib="asyncio"))
