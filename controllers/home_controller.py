import requests
from controllers.base_logger import getlogger  # type: ignore
from controllers.user_controller import UserAPI


class HomeController:
    def __init__(self, app, user: UserAPI):
        self.LOGGER = getlogger("MainWindow controller")
        self.app = app
        self.user = user

        # for production
        assert self.user._is_logged_in

    def go_to_esis_window(self):
        self.app.screen_manager.current = "esis_auto_gui"

    def logout(self):
        req = requests.post(f"{self.user.url}/logout", headers=self.user.headers)
        if req.status_code == 200:
            self.LOGGER.info(f"Logged out user {self.user.data}")
            self.app.screen_manager.current = "login_screen"
        else:
            self.LOGGER.error(f"server error")
