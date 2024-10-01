import requests
from controllers.user_controller import UserAPI
from controllers.base_logger import getlogger


class EmailController:
    # TODO: None to build then have to use login
    def __init__(self, app, user=None) -> None:
        self.root_app = app
        self.user = UserAPI("60009", "67220")  # TODO: pas this from the main
        self.finish_attachments = []
        self.other_attachments = []
        self.selection = {}
        self.LOGGER = getlogger()

    def on_rfq_select(self, email_window):
        pass

    async def on_search_button_press(
        self, search_value, search_type, email_window
    ) -> list:
        """Makes an API Call, returns data in a list"""
        self.user.login()  # TODO: remove for prod

        # NOTE: keep everything below this
        r_list = []

        self.search_type = search_type  # NOTE: this is so that we can make a json for API call and know what type of item the user has choosen

        json = {"search_value": search_value, "search_type": search_type}

        req = requests.post(
            self.user.url + "/email/search_items", json=json, headers=self.user.headers
        )
        if req.status_code == 200:
            r_dict = req.json()
            r_list = [f"{key}: {value}" for key, value in r_dict.items()]
        return r_list

    def on_file_upload(self, filepath, id, email_window):
        assert id in ["files_uploaded", "files_uploaded_1"]
        filepath_list = (
            self.finish_attachments
            if id == "files_uploaded"
            else self.other_attachments
        )
        filepath_list.append(*filepath)
        getattr(email_window.ids, id).text = "\n".join(filepath_list)

    def update_email_type(self, rfq_or_item_selection):
        # TODO: assert that self.rfq_or_email_type is not none in send mail
        rfq_or_item_pk = rfq_or_item_selection.split(":")[0]
        self.rfq_or_item_pk = rfq_or_item_pk
        print(self.rfq_or_item_pk)

    def preview_emails(self, email_window):
        pass

    def send_mail(self, **kwargs):
        pass
