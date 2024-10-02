import aiohttp
from controllers.user_controller import UserAPI
from controllers.base_logger import getlogger

# FOR TYPE HINTS
from kivy.uix.screenmanager import Screen

# TODO: add the create task function in GUI CLOCK


class EmailController:
    # TODO: None to build then have to use login
    def __init__(self, app, user=None) -> None:
        self.root_app = app
        self.user = UserAPI("60009", "67220")  # TODO: pas this from the main
        self.finish_attachments = []
        self.other_attachments = []
        self.email_list = []  # placeholder to render the popup
        self.LOGGER = getlogger()

    # SEARCH ------------------
    def on_search_selection(self, pk, rfq_or_item):
        """
        Called when the user selects an Item from the search results. Assigns the pk and the type to class variables.

        :param pk: ItemPK or RequestForQuotePK
        :param rfq_or_item: Either "RFQ" or "Item"
        """
        self.selection = {pk: rfq_or_item}

    async def on_search_button_press(
        self, search_value: str, search_type: str
    ) -> list[str]:
        """
        Quries the API for search results. For SQL query see /email/search_items endpoint on server

        :param search_value str: partial or whole pk value
        :param search_type str: Either "RequestForQuote" or "Item"
        :return: list[str] - "pk: value". Value is PartNumber if searching Item and CustomerRFQNumber if searching for RFQ
        """

        self.user.login()  # TODO: remove for prod

        # NOTE: keep everything below this
        r_list = []

        self.search_type = search_type  # NOTE: this is so that we can make a json for API call and know what type of item the user has choosen

        json = {"search_value": search_value, "search_type": search_type}

        async with aiohttp.ClientSession() as session:
            async with session.post(
                self.user.url + "/email/search_items",
                json=json,
                headers=self.user.headers,
            ) as req:
                self.LOGGER.info(
                    f"User - {self.user.data['username']} got - {req.status}"
                )
                if req.status == 200:
                    r_dict = await req.json()
                    r_list = [f"{key}: {value}" for key, value in r_dict.items()]
                else:
                    r_list = ["Something went wrong"]

        return r_list

    # OTHER ------------------
    def on_file_upload(self, filepath: str, id: str, email_window: Screen) -> None:
        """
        Called when the user uploades a file from the GUI.
        Appends the filepaths to the file upload that triggered the event.
        Filepaths for Finish and Other attachments are different

        :param filepath str: filepath that the user selected
        :param id [TODO:type]: id of the widget that triggered the event
        :param email_window : GUI instance to update the filepaths
        """
        assert id in ["finish_attachments", "other_attachments"]
        filepath_list = (
            self.finish_attachments
            if id == "finish_attachments"
            else self.other_attachments
        )
        filepath_list.append(*filepath)
        getattr(email_window.ids, id).text = "\n".join(filepath_list)

    def preview_emails(self, email_window):
        pass

    def send_mail(self, **kwargs):
        pass

    # GET EMAILS
    async def get_email_groups(self):
        self.email_dict = {}
        parties = {
            "fin": 3755,
            "mat-al": 3744,
            "mat-steel": 3747,
            "ht": 3764,
            "hardware": 3867,
        }
        json = {"party_type": "fin", "party_fk": "3755"}

        self.user.login()  # TODO: remove for prod

        for party_type, partyfk in parties.items():
            json = {"party_type": party_type, "party_fk": str(partyfk)}
            async with aiohttp.ClientSession() as session:
                async with session.post(
                    self.user.url + "/email/get_email_groups",
                    json=json,
                    headers=self.user.headers,
                ) as req:
                    if req.status == 200:
                        r = await req.json()
                        key, value = next(iter(r.items()))
                        self.email_dict[key] = value
                        self.LOGGER.info(key)

        self.email_list = []
        for key, value in self.email_dict.items():
            for email in value.split(", "):
                self.email_list.append(f"{email} - {key.upper()}")

    def get_email_list(self):
        return self.email_list

    def update_email_list(self):
        pass
