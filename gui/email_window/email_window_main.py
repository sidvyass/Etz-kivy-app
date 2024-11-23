from typing import List
import asyncio
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from controllers.email_controller.email_item_class import EmailItem
from controllers.email_controller.main_email_controller import EmailTrackerController
from gui.email_window.details_popup import open_details


KV = """
<EmailTrackerWindow>:
    name: 'email_window'
    Screen:
        MDBoxLayout:
            orientation: "vertical"

            MDBoxLayout: 
                orientation: "horizontal"
                size_hint_y: 0.05
                size_hint_x: 1

                MDLabel:
                    text: "Email Reply Tracker"
                    halign: "center"
                    valign: "middle"
                    size_hint_y: 1

            # Search bar
            BoxLayout:
                orientation: 'horizontal'
                spacing: dp(10)
                size_hint_y: 0.1
                size_hint_x: 1

                MDTextField:
                    id: search_field
                    pos_hint: {'center_y': 0.5}
                    size_hint_x: 0.8

                    MDTextFieldHelperText:
                        text: "Enter a valid search value."
                        mode: "on_error"

                MDButton:
                    id: search_button
                    style: "filled"
                    on_release: root.controller.search(root)
                    size_hint_x: 0.2
                    pos_hint: {'center_y': 0.5}
                    padding: dp(5), dp(5)
                    theme_bg_color: "Custom"
                    md_bg_color: 0.3, 0.3, 0.3, 1

                    MDButtonText:
                        id: search_button_text
                        text: "Search"
                        theme_text_color: "Custom"
                        text_color: "white"

            BoxLayout:
                size_hint_y: 0.05
                size_hint_x: 1  # Ensure full width
                orientation: 'horizontal'
                Label:
                    text: "  "
                    size_hint_x: 0.05
                    halign: 'center'  # Match row labels
                    valign: 'middle'
                    padding_x: dp(5)

                Label:
                    text: "Name"
                    size_hint_x: 0.05
                    halign: 'left'  # Match row labels
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: " "
                    size_hint_x: 0.05
                    halign: 'center'  # Match row labels
                    valign: 'middle'
                    padding_x: dp(5)

                Label:
                    text: "Email ID"
                    size_hint_x: 0.2
                    halign: 'left'  # Match row labels
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Attachment Count"
                    size_hint_x: 0.05
                    halign: 'center'  # Match row labels
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Actions"
                    halign: 'center'  # Match row labels
                    valign: 'middle'
                    size_hint_x: 0.1
                    padding_x: dp(5)

            RecycleView:
                id: tracker_row
                viewclass: 'EmailTrackerRow'
                size_hint_y: 0.8
                size_hint_x: 1
                do_scroll_x: False  # Disable horizontal scrolling
                do_scroll_y: True

                RecycleBoxLayout:
                    id: table_layout
                    orientation: 'vertical'
                    default_size: None, dp(60)
                    default_size_hint: 1, None
                    size_hint_y: None
                    size_hint_x: 1  # Ensure full width
                    height: self.minimum_height
                    spacing: dp(0)

<EmailTrackerRow>:
    orientation: 'horizontal'
    size_hint_x: 1  # Ensure full width
    size_hint_y: None
    height: dp(40)

    MDCheckbox:
        id: row_checkbox
        size_hint_x: 0.01
        active: root.is_active
        on_active: root.change_is_active(self, self.active)
        pos_hint: {'center_y': 0.5}

    Label:
        text: root.name
        size_hint_x: 0.05
        halign: 'center'  # Match header labels
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:
        text: root.email_id
        size_hint_x: 0.2
        halign: 'center'  # Match header labels
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    Label:
        text: root.email_count
        size_hint_x: 0.05
        halign: 'center'  # Match header labels
        valign: 'middle'
        text_size: self.size
        padding_x: dp(5)

    MDButton:
        style: "filled"
        on_release: root.open_details()
        size_hint_x: 0.1
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Mails"
            theme_text_color: "Custom"
            text_color: "white"

    MDButton:
        style: "filled"
        on_release: root.send_follow_up_email()
        size_hint_x: 0.2
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Send Follow Up"
            theme_text_color: "Custom"
            text_color: "white"

    MDButton:
        style: "filled"
        on_release: root.edit_info()
        size_hint_x: 0.1
        pos_hint: {'center_y': 0.5}
        theme_bg_color: "Custom"
        md_bg_color: 0.3, 0.3, 0.3, 1

        MDButtonText:
            text: "Edit Info"
            theme_text_color: "Custom"
            text_color: "white"
"""


# TODO: headers dont align with the rows. Needs UI fixing.


# TODO: the button here should be disabled if there are no emails to be found
class EmailTrackerRow(BoxLayout):
    email_id = StringProperty()
    email_count = StringProperty()
    name = StringProperty()
    email_item_obj = ObjectProperty()
    is_active = BooleanProperty()

    def open_details(self):
        open_details(
            {
                "email_id": self.email_id,
                "email_item_obj": self.email_item_obj,
            }
        )

    def send_follow_up_email(self):
        pass

    def edit_info(self):
        pass

    def change_is_active(self, checkbox, value):
        self.selected = value


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
        sorted_email_list = sorted(
            email_list,
            key=lambda email_item: int(email_item.email_count),
            reverse=True,
        )
        self.ids.tracker_row.data = [
            email_item.to_dict() for email_item in sorted_email_list
        ]

    def outlook_email_listener_wrapper(self, dt):
        if self.start_up_task.done():
            asyncio.create_task(self.controller.listen_for_emails())
        else:
            self.controller.LOGGER.info("skipping as startup is still not complete")


Builder.load_string(KV)
