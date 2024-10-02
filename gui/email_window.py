import kivymd
from kivy.uix.screenmanager import Screen
from kivy.uix.popup import Popup
from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import (
    ImageLeftWidget,
    OneLineAvatarListItem,
    OneLineListItem,
    TwoLineListItem,
)
from plyer import filechooser

# TODO: comment this out when running
from controllers.email_controller import EmailController
import asyncio


KV = """
<EmailWindowGui>:
    name: 'email_gui'

    MDBoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1 

        # Search bar and buttons
        MDBoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            size_hint_y: 0.08  # MAIN HINT
            height: dp(50)  # Fixed height for the search bar

            MDTextField:
                id: search_field
                hint_text: "Search"
                mode: "rectangle"

            MDDropDownItem:
                id: type_dropdown
                text: 'Type'
                size_hint_x: 0.1
                on_release: root.open_type_selection_dropdown()

            MDRaisedButton:
                text: 'Search'
                size_hint_x: 0.4
                on_release: root.search()
                md_bg_color: 0.2, 0.2, 0.2, 1

        MDScrollView:
            size_hint_y: 0.5  # MAIN HINT
            do_scroll_y: True

            MDSelectionList:
                id: selection_list
                selected_mode: True

        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            size_hint_y: 0.2  # MAIN HINT

            # first file upload section
            BoxLayout:
                orientation: 'vertical'
                padding: 10
                size_hint_x: 0.5
                size_hint_y: 1

                MDLabel:
                    text: "Finish Attachments"
                    size_hint_y: 0.2
                    size_hint_x: 1
                    font_style: 'H5'
                    valign: 'top'
                    halign: 'center'

                MDLabel:
                    id: finish_attachments
                    text: "No files selected"
                    size_hint_x: 1 
                    valign: 'center'
                    halign: 'center'

                MDFlatButton:
                    text: "Select Files"
                    text_color: 1, 1, 1, 1 
                    size_hint_x: 1
                    md_bg_color: 0.2, 0.2, 0.2, 1
                    on_release: root.choose_files('finish_attachments')
                    valign: 'top'
                    halign: 'center'

            # 2nd file chooser
            BoxLayout:
                orientation: 'vertical'
                padding: 10
                size_hint_x: 0.5
                size_hint_y: 1

                MDLabel:
                    text: "Other Documents"
                    size_hint_y: 0.2
                    size_hint_x: 1
                    font_style: 'H5'
                    valign: 'top'
                    halign: 'center'

                MDLabel:
                    id: other_attachments
                    text: "No files selected"
                    size_hint_x: 1 
                    valign: 'center'
                    halign: 'center'

                MDFlatButton:
                    text: "Select Files"
                    text_color: 1, 1, 1, 1 
                    size_hint_x: 1
                    md_bg_color: 0.2, 0.2, 0.2, 1
                    on_release: root.choose_files('other_attachments')
                    valign: 'top'
                    halign: 'center'

        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            size_hint_y: 0.22  # MAIN HINT
            spacing: 10

            MDFlatButton:
                text: "Send Mails"
                text_color: 1, 1, 1, 1 
                size_hint_x: 0.25
                size_hint_y: 1
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.controller.send_mail(root)

            MDFlatButton:
                text: "Email Recipients"
                text_color: 1, 1, 1, 1 
                size_hint_x: 0.25
                size_hint_y: 1
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.open_popup_emailids()

            MDFlatButton:
                text: "Email Body"
                text_color: 1, 1, 1, 1 
                size_hint_x: 0.25
                size_hint_y: 1
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.open_email_body()

<EmailRecipientListPopup>:
    title: "Email Recipients"
    size_hint: 0.8, 0.8
    BoxLayout:
        size_hint: 1, 1
        orientation: 'vertical'
        padding: 10
        spacing: 10

        MDScrollView:
            size_hint_y: 0.8  # MAIN HINT
            do_scroll_y: True

            MDSelectionList:
                id: email_list_box
                selected_mode: True

        BoxLayout:
            size_hint_y: 0.2
            orientation: 'horizontal'
            padding: 10
            spacing: 10

            MDFlatButton:
                text: "Save"
                size_hint_x: 0.3
                size_hint_y: 1
                text_color: 1, 1, 1, 1 
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.dismiss()

            MDFlatButton:
                text: "Delete"
                size_hint_x: 0.3
                size_hint_y: 1
                text_color: 1, 1, 1, 1 
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.delete_emails()

            BoxLayout:
                size_hint_x: 0.3
                orientation: 'vertical'
                spacing: 5

                MDTextField:
                    id: new_email_id
                    hint_text: 'example@mailid'
                    valign: "top"

                MDFlatButton:
                    text: "Add"
                    size_hint_x: 1 
                    size_hint_y: 0.5
                    text_color: 1, 1, 1, 1 
                    md_bg_color: 0.2, 0.2, 0.2, 1
                    on_release: root.add_email()

<EmailPreview>:
    title: "Email Preview"
    size_hint: 0.8, 0.8
    BoxLayout:
        size_hint: 1, 1
        orientation: 'vertical'
        padding: 10
        spacing: 10

        MDScrollView:
            size_hint_y: 0.95  # MAIN HINT
            do_scroll_y: True

            TextInput:
                id: email_body
                text: root.get_text()
                multiline: True

        BoxLayout:
            size_hint_y: 0.05
            orientation: 'horizontal'

            MDFlatButton:
                text: "Save"
                halign: "center"
                size_hint_y: 1
                text_color: 1, 1, 1, 1 
                md_bg_color: 0.2, 0.2, 0.2, 1
                on_release: root.save_text()
    
"""


Builder.load_string(KV)


class SelectedResult(OneLineAvatarListItem):
    """
    Widget for when the user makes a selection
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids._lbl_primary.halign = "center"
        self.ids._lbl_primary.font_size = "20sp"
        self.ids._lbl_primary.bold = True


# TODO: make this recycle view
class ResultItem(OneLineAvatarListItem):
    """
    Widget for displaying search results in the ScrollView

    NOTE: Painfully fucking slow
    """

    def __init__(self, filepath, parent_ref, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(ImageLeftWidget(source=filepath))
        self.parent_ref = parent_ref

    def on_release(self):
        # TODO: controller call
        self.parent_ref.on_search_selection(self.text)


class EmailRecipientListPopup(Popup):
    """
    Popup to review and edit E-mail IDs

    """

    def __init__(self, email_list: list, **kwargs) -> None:
        super().__init__(**kwargs)
        for email in email_list:
            self.ids.email_list_box.add_widget(OneLineListItem(text=f"{email}"))

    def add_email(self):
        if self.ids.new_email_id.text:
            self.ids.email_list_box.add_widget(
                OneLineListItem(text=f"{self.ids.new_email_id.text}")
            )
            self.ids.new_email_id.text = ""

    def delete_emails(self):
        selected_items = self.ids.email_list_box.get_selected_list_items()
        for s in selected_items:
            self.ids.email_list_box.remove_widget(s)

    def on_dismiss(self, *args):
        pass


class EmailPreview(Popup):
    """
    [TODO:description]
    """

    def __init__(self, **kwargs) -> None:
        super().__init__(**kwargs)

    def get_text(self):
        return "Trial"

    # TODO: need to have a callback here
    def save_text(self):
        text = self.ids.email_body.text
        self.dismiss()


class EmailWindowGui(Screen):

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller: EmailController = controller
        Clock.schedule_once(self.one_time_background_tasks)

    def one_time_background_tasks(self, *args):
        asyncio.create_task(self.controller.get_email_groups())

    def open_type_selection_dropdown(self):
        # TODO: figure out how to close this upon selection
        items = [
            {
                "text": "RFQ",
                "on_release": lambda x=f"RFQ": self.ids.type_dropdown.set_item(x),
            },
            {
                "text": "Item",
                "on_release": lambda x=f"Item": self.ids.type_dropdown.set_item(x),
            },
        ]
        MDDropdownMenu(caller=self.ids.type_dropdown, items=items).open()

    def search(self):
        """
        Search button on press event
        Gathers search_value, search_type and pushes controller async search to event loop.
        """
        # TODO: add a check to see if both fields are filled
        search_value = self.ids.search_field.text
        search_type = self.ids.type_dropdown.current_item
        self.ids.selection_list.clear_widgets()
        asyncio.create_task(self._start_search(search_type, search_value))

    async def _start_search(self, search_type: str, search_value: str):
        """
        Search and update results async function to push to event loop by self.search.

        :param search_type [TODO:type]: [TODO:description]
        :param search_value [TODO:type]: [TODO:description]
        """
        values = await self.controller.on_search_button_press(search_value, search_type)
        print("starting widget creation...")
        for val in values:
            self.ids.selection_list.add_widget(
                ResultItem(
                    filepath=r"C:\PythonProjects\placeholder-image.jpg",
                    parent_ref=self,
                    text=f"{val}",
                    secondary_text="number 2",
                )
            )

    def choose_files(self, id):
        path = filechooser.open_file(title="Select file")  # Type: ignore
        self.controller.on_file_upload(path, id, self)

    def on_search_selection(self, rfq_or_item_selection: str):
        """
        Event for SearchResultItem (list item in display box).
        Bound to on_press for the SearchResultItem widget.

        :param rfq_or_item_selection str: The pk: value string in SearchResultItem.
        """
        rfq_or_item_selection = rfq_or_item_selection.split(":")[0]  # PK

        self.controller.on_search_selection(
            rfq_or_item_selection, self.ids.type_dropdown.current_item
        )  # NOTE: might not need current_item: see self.search type in controller
        self.ids.selection_list.clear_widgets()
        self.ids.selection_list.add_widget(SelectedResult(text=rfq_or_item_selection))

    def open_popup_emailids(self):
        email_list = self.controller.get_email_list()
        if len(email_list) > 1:
            EmailRecipientListPopup(email_list).open()
        else:
            # TODO: notify the user that the emails are still being updated
            pass

    def open_email_body(self):
        EmailPreview().open()
