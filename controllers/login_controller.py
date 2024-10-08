from controllers.base_logger import getlogger
from controllers.user_controller import UserAPI


class LoginController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app):
        self.app = app
        self.LOGGER = getlogger("Login controller")

    def authenticate(self, username: str, password: str, login_window):
        """Makes API request to authenticate. Calls the load_window function if successful"""
        login_window.ids.loading_spinner.active = True
        self.user = UserAPI(username, password)
        self.LOGGER.info(f"{username} - Logging in...")

        is_logged_in = self.user.login()
        self.LOGGER.info(f"{username} - Login {is_logged_in}...")
        login_window.ids.loading_spinner.active = False
        if is_logged_in:
            self.app.show_small_notification("Success...")

            # NOTE: we hand it off to the mainwindow by calling MAIN app's load function
            self.app.load_main_window(self.user)
        else:
            self.app.show_small_notification("Incorrect username or password")
