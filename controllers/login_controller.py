from controllers.base_logger import getlogger
from controllers.user_controller import UserAPI


class LoginController:
    """The controller handles interactions between the view and the model."""

    def __init__(self, app):
        self.app = app
        self.LOGGER = getlogger("Login controller")

    def authenticate(self, username: str, password: str, login_window):
        """Makes API request to authenticate. Calls the load_window function if successful"""
        # self.user = UserAPI(username, password)

        # NOTE: for testing
        self.user = UserAPI("60009", "67220")

        is_logged_in = self.user.login()  # json response if login incorrect
        if not is_logged_in:
            if not username:
                login_window.ids.username_field.error = True
            if not password:
                login_window.ids.password_field.error = True
            self.app.show_small_notification("Auth Failed, try again or contact admin.")
        else:
            self.app.load_main_window(self.user)  # NOTE: hand off
