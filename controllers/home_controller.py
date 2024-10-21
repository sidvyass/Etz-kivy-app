from controllers.base_logger import getlogger
from controllers.user_controller import UserAPI


class HomeController:
    def __init__(self, app, user: UserAPI):
        self.LOGGER = getlogger("MainWindow controller")
        self.main_app = app
        self.user = user

        # for production
        # assert self.user._is_logged_in

    def go_to_esis_window(self):
        self.main_app.screen_manager.current = "esis_auto_gui"

    def cancel_background_tasks(self, home_window):
        pass
