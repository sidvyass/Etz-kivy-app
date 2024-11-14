import win32com.client
from typing import Optional, Tuple, Any
import pandas as pd
from kivy.uix.scrollview import ScrollView
from kivymd.uix.boxlayout import MDBoxLayout
from kivy.uix.popup import Popup
from kivymd.uix.label import MDLabel
from pprint import pprint


class EmailItem:
    def __init__(self, email_id, count, last_reply_date, email_location):
        self.email_id = email_id
        self.count = count if count else 0
        self.last_reply_date = last_reply_date
        self.email_location: Optional[Tuple[Any, Any]] = email_location

    def to_dict(self):
        if self.last_reply_date:
            return {
                "email_id": self.email_id,
                "reply_count": f"{self.count}",
                "last_reply_date": str(self.last_reply_date),
                "email_item_obj": self,  # NOTE: to open the mail
            }
        else:
            return {
                "email_id": self.email_id,
                "reply_count": f"{self.count}",
                "last_reply_date": "No reply found",
                "email_item_obj": self,
            }

    def __repr__(self) -> str:
        return f"Email ID: {self.email_id}\nCount: {self.count}\nLast Reply Date: {self.last_reply_date}"


class EmailTrackerController:
    def __init__(self):
        self.dummy_email_dict = {
            email_id: EmailItem(email_id, 0, None, None)
            for email_id in self.pull_emails_from_cognito()
        }

    def check_responses(self):
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

        inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
        messages = inbox.Items

        messages.Sort("[ReceivedTime]", Descending=True)

        for m in messages:
            if m.Class == 43:
                if m.SenderEmailAddress in self.dummy_email_dict.keys():
                    email_item_obj = self.dummy_email_dict[m.SenderEmailAddress]
                    email_item_obj.count += 1
                    email_item_obj.last_reply_date = m.ReceivedTime
                    email_item_obj.email_location = (m.EntryID, inbox.StoreID)

        # TODO: sort these values so that the one with a reply is first
        return [value.to_dict() for value in self.dummy_email_dict.values()]

    def show_popup(self):
        strings = list(self.dummy_email_dict.keys())

        content = MDBoxLayout(orientation="vertical")
        scrollview = ScrollView()
        box = MDBoxLayout(orientation="vertical", size_hint_y=None)
        box.bind(minimum_height=box.setter("height"))

        for s in strings:
            label = MDLabel(text=s, size_hint_y=None, height=40)
            box.add_widget(label)

        scrollview.add_widget(box)
        content.add_widget(scrollview)

        popup = Popup(
            title="List of Strings",
            content=content,
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()

    def pull_emails_from_cognito(self):
        # TODO: This is a dummy pull as of now, need to link this to cognito API
        df = pd.read_excel(
            r"C:\PythonProjects\esis-auto-gui\ProspectContactTrackingForm.xlsx",
            sheet_name=0,
        )

        email_ids = df["EmailAddress"].dropna().tolist()
        return email_ids

    def open_email(self, email_item_obj: EmailItem):
        if not email_item_obj.email_location:
            return
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        entry_id, store_id = email_item_obj.email_location
        email_item = outlook.GetItemFromID(entry_id, store_id)
        email_item.display()

    def send_followup_email(self, email_item_obj: EmailItem):
        pass


if __name__ == "__main__":
    s = EmailTrackerController()
    s.check_responses()
