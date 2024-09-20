from controllers.base_logger import getlogger  # type: ignore
from controllers.user_controller import UserAPI


class HomeController:
    def __init__(self, app, user: UserAPI):
        self.LOGGER = getlogger("MainWindow controller")
        self.app = app
        self.user = user
