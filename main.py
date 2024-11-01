import requests
from kivy.metrics import dp
from kivymd.app import MDApp
from kivy.uix.widget import Widget
from kivymd.uix.snackbar.snackbar import MDSnackbar, MDSnackbarText
from kivymd.uix.button import MDButton
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
    MDDialogContentContainer,
)
from kivymd.uix.button import MDButtonText
from kivy.uix.screenmanager import ScreenManager, NoTransition
from controllers.user_controller import UserAPI
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
        self.theme_cls.theme_style = "Dark"
        self.theme_cls.primary_palette = "Ghostwhite"

        self.screen_manager = ScreenManager(transition=NoTransition())
        Window.size = (1200, 900)

        controller = LoginController(self)
        view = LoginWindow(controller=controller)

        # controller = EsisAutoController(self, UserAPI("60009", "67220"))
        # view = EsisAutoGUI(controller)

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
            MDSnackbarText(
                text=in_text,
                theme_text_color="Custom",
                text_color="white",
            ),
            background_color=(0.3, 0.3, 0.3, 1),
            y=dp(24),
            pos_hint={"center_x": 0.5},
            size_hint_x=0.5,
        )
        self.current_snackbar.open()

    # ******** large notifications ***********

    def show_notification(self, title: str, text: str):
        self.dialog = MDDialog(
            MDDialogHeadlineText(
                text=title,
            ),
            MDDialogSupportingText(
                text=text,
            ),
            MDDialogButtonContainer(
                Widget(),
                MDButton(
                    MDButtonText(text="Cancel"),
                    style="text",
                ),
                MDButton(
                    MDButtonText(text="Accept"),
                    style="text",
                ),
                spacing="8dp",
            ),
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
