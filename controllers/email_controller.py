from controllers.user_controller import UserAPI
from controllers.base_logger import getlogger


class EmailController:
    # TODO: None to build then have to use login
    def __init__(self, app, user=None) -> None:
        self.root_app = app
        self.user = user
        self.LOGGER = getlogger()

    def on_rfq_select(self, email_window):
        pass

    def on_search_button_press(self, email_window):
        pass

    def on_file_upload(self, email_window):
        pass

    def preview_emails(self, email_window):
        pass

    def send_mail(self, **kwargs):
        pass
