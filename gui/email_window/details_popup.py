from typing import Dict
import win32com.client
from kivy.lang import Builder
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.popup import Popup
from kivy.properties import StringProperty, ObjectProperty
from kivy.lang import Builder


# TODO: dont render the open email button where the email has no location or is empty


KV = """
<EmailDetailRow>:
    size_hint_x: 1
    size_hint_y: 1
    height: dp(40)
    orientation: 'horizontal'

    Label:
        text: root.subject
        width: dp(150)
    Label:
        text: root.date
        width: dp(150)
    Label:
        text: root.attachment_count
        width: dp(150)
    Button:
        text: "Open Email"
        on_release: root.open_email()
        width: dp(100)
        background_color: (0.3, 0.3, 0.3, 1)
        color: (1, 1, 1, 1)
        pos_hint: {'center_y': 0.5}


<EmailPopup>:
    title: root.popup_title
    auto_dismiss: True

    BoxLayout:
        orientation: 'vertical'
        spacing: dp(10)
        padding: dp(10)

        Label:
            size_hint_y: 0.1
            text: "Emails"

        BoxLayout:
            size_hint_y: 0.1
            orientation: 'horizontal'
            Label:
                text: "Subject"
                width: dp(150)
            Label:
                text: "Date"
                width: dp(150)
            Label:
                text: "Attachment Count"
                width: dp(150)
            Label:
                text: "Actions"
                width: dp(100)

        RecycleView:
            size_hint_y: 0.7
            id: email_list
            viewclass: 'EmailDetailRow'

            RecycleBoxLayout:
                orientation: 'vertical'
                default_size: None, dp(60)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                spacing: dp(0)

        BoxLayout:
            size_hint_y: 0.1
            orientation: 'horizontal'

            MDButton:
                style: "filled"
                on_release: root.dismiss()
                size_hint_x: 0.33
                pos_hint: {'center_y': 0.5}
                theme_bg_color: "Custom"
                md_bg_color: 0.3, 0.3, 0.3, 1

                MDButtonText:
                    text: "Dismiss"
                    theme_text_color: "Custom"
                    text_color: "white"

            MDButton:
                style: "filled"
                on_release: root.stop_tracking()
                size_hint_x: 0.33
                pos_hint: {'center_y': 0.5}
                theme_bg_color: "Custom"
                md_bg_color: 0.3, 0.3, 0.3, 1

                MDButtonText:
                    text: "Stop Tracking"
                    theme_text_color: "Custom"
                    text_color: "white"
"""


Builder.load_string(KV)


class EmailDetailRow(BoxLayout):
    subject = StringProperty()
    date = StringProperty()
    email_location = ObjectProperty()
    attachment_count = StringProperty()

    def open_email(self):
        if not self.email_location:
            # TODO: notify the user that there is no location
            return
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        entry_id, store_id = self.email_location
        email_item = outlook.GetItemFromID(entry_id, store_id)
        email_item.display()


class EmailPopup(Popup):
    popup_title = StringProperty("Emails")

    def __init__(self, email_data, **kwargs):
        super().__init__(**kwargs)
        self.populate_email_list(email_data)

    def populate_email_list(self, email_data):
        data = []
        if not email_data:  # base case without any data
            data.append(
                {"subject": "No emails found", "date": "", "email_location": ""}
            )
        for email_details in email_data:
            subject, date, location, attachment_count = email_details
            data.append(
                {
                    "subject": subject,
                    "date": str(date),  # TODO: parse this before assignment
                    "email_location": location,
                    "attachment_count": str(attachment_count),
                }
            )

        self.ids.email_list.data = data


def open_details(data: Dict):
    email_data = data.get("email_item_obj", [])
    email_id = data.get("email_id", "Unknown")
    popup = EmailPopup(email_data=email_data, popup_title=f"Emails from {email_id}")
    popup.open()
