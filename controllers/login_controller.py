import requests
from controllers.base_logger import getlogger
from kivymd.uix.button import MDButton
from kivymd.uix.button import MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogHeadlineText,
    MDDialogSupportingText,
    MDDialogButtonContainer,
)
from kivy.uix.widget import Widget
from controllers.user_controller import UserAPI


class LoginController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app):
        self.app = app
        self.LOGGER = getlogger("Login controller")
        self.connection_check_dialog = None

    def authenticate(self, username: str, password: str, login_window):
        """
        Makes API request to authenticate. Calls the load_window function if successful
        """

        # FOR_LIVE:
        self.user = UserAPI(username, password)

        # # TEST:
        # self.user = UserAPI("60009", "67220")

        is_logged_in = self.user.login()  # json response if login incorrect
        if not is_logged_in:
            if not username:
                login_window.ids.username_field.error = True
            if not password:
                login_window.ids.password_field.error = True
            self.app.show_small_notification("Auth Failed, try again or contact admin.")
        else:
            self.app.load_main_window(self.user)  # NOTE: hand off

    def _try_connecting(self) -> bool:
        """
        Helper to send a get request to root of API for veryfing running state.

        """
        try:
            status = requests.get("http://127.0.0.1:8000", timeout=2)
            if status.status_code == 200:
                return True
            self.LOGGER.debug(
                f"server is not running. Status code {status.status_code}"
            )
            return False
        except requests.exceptions.ConnectionError:
            self.LOGGER.debug(f"server is not running")
            return False

    def check_server_status(self, *_):
        """
        GUI popup notifies the user if the server is not running. Retry button runs the same function again.
        """

        is_conn = self._try_connecting()
        self.LOGGER.info(is_conn)
        if not is_conn:
            if not self.connection_check_dialog:
                self.connection_check_dialog = MDDialog(
                    MDDialogHeadlineText(
                        text="Server Inactive",
                    ),
                    MDDialogSupportingText(
                        text="Server is not running or there was a network error.",
                    ),
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(
                            MDButtonText(text="Retry"),
                            style="text",
                            on_release=lambda *_: self.check_server_status(),
                        ),
                        spacing="8dp",
                    ),
                    auto_dismiss=False,
                )
                self.connection_check_dialog.open()
        else:
            if self.connection_check_dialog:
                self.connection_check_dialog.dismiss()
                self.connection_check_dialog = None
            self.LOGGER.info("Server handshake complete")
