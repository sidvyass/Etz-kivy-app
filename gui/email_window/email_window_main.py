import win32com.client
from typing import List
import asyncio
from kivy.uix.screenmanager import Screen
import win32com.client
from kivy.properties import StringProperty, ObjectProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from controllers.email_controller.scripts import EmailItem, main
from controllers.main_email_controller import EmailTrackerController


KV = """
<EmailTrackerWindow>:
    name: 'email_window'
    Screen:
        MDBoxLayout:
            orientation: "vertical"

            MDBoxLayout: 
                orientation: "horizontal"
                size_hint_y: 0.1

                MDLabel:
                    text: "Email Reply Tracker"
                    halign: "center"
                    valign: "middle"
                    size_hint_y: 1

                MDButton:
                    style: "filled"
                    theme_bg_color: "Custom"
                    text_color: 1, 1, 1, 1
                    size_hint_y: 1
                    on_release: root.controller.show_popup()

                    MDButtonText:
                        text: "Emails"
                        theme_text_color: "Custom"
                        text_color: "white"

            RecycleView:
                id: tracker_row
                viewclass: 'EmailTrackerRow'
                size_hint_y: 0.9
                size_hint_x: 1
                do_scroll_x: True
                do_scroll_y: True

                RecycleBoxLayout:
                    id: table_layout
                    orientation: 'vertical'
                    default_size: None, dp(60)
                    default_size_hint: 1, None
                    size_hint_y: None
                    height: self.minimum_height
                    spacing: dp(0)


<EmailTrackerRow>:
    orientation: 'horizontal'
    size_hint_y: None
    height: dp(40)

    #TODO: all these needs to be centered

    Label:
        text: root.email_id
        size_hint_x: 0.2
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:
        text: "<Email Subject>"
        size_hint_x: 0.1  # change
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:
        text: "<SENDER NAME>"
        size_hint_x: 0.1  # change
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:
        text: "<Company Name>"
        size_hint_x: 0.1  # change
        halign: 'left'
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    MDButton:
        style: "filled"
        on_release: root.open_email()
        size_hint_x: 0.2
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Open Last Mail"
            theme_text_color: "Custom"
            text_color: "white"

    MDButton:
        style: "filled"
        on_release: root.controller.send_followup_email(root.email_item_obj)
        size_hint_x: 0.2
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Send Follow Up"
            theme_text_color: "Custom"
            text_color: "white"
"""


# TODO: the button here should be disabled if there are no emails to be found
class EmailTrackerRow(BoxLayout):
    email_id = StringProperty()
    email_count = StringProperty()
    email_item_obj = ObjectProperty()

    def open_email(self):
        if not self.email_item_obj.email_location:
            # TODO: notify the user that there is no location
            return
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        entry_id, store_id = self.email_item_obj.email_location
        email_item = outlook.GetItemFromID(entry_id, store_id)
        email_item.display()

    def send_follow_up_email(self):
        pass

    def open_all_emails(self):
        pass


class EmailTrackerWindow(Screen):
    controller = ObjectProperty()

    def __init__(self, controller, **kwargs) -> None:
        super(EmailTrackerWindow, self).__init__(**kwargs)
        self.controller: EmailTrackerController = controller
        self.start_up_task = asyncio.create_task(self.controller.on_start_up(self))

    def on_enter(self, *args):
        self.background_tasks = Clock.schedule_interval(
            self.outlook_email_listener_wrapper, 5
        )
        return super().on_enter(*args)

    def on_leave(self, *args):
        self.background_tasks.cancel()
        return super().on_leave(*args)

    def build_rows(self, email_list: List[EmailItem]):
        self.controller.LOGGER.info("Building rows...")
        self.ids.tracker_row.data = [email_item.to_dict() for email_item in email_list]

    def outlook_email_listener_wrapper(self, dt):
        if self.start_up_task.done():
            asyncio.create_task(self.controller.listen_for_emails())
        else:
            self.controller.LOGGER.info("skipping as startup is still not complete")


Builder.load_string(KV)
