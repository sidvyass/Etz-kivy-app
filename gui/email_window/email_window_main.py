import asyncio
from kivy.uix.widget import Widget
import datetime
import win32com.client
from typing import List
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.dialog import (
    MDDialog,
    MDDialogIcon,
    MDDialogButtonContainer,
    MDDialogHeadlineText,
    MDDialogSupportingText,
)
from kivy.uix.popup import Popup
from kivy.uix.screenmanager import Screen
from kivy.properties import StringProperty, ObjectProperty, BooleanProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock
from kivy.properties import ObjectProperty
from kivy.lang import Builder
from controllers.email_controller.email_item_class import EmailItem
from controllers.email_controller.main_email_controller import (
    EmailTrackerController,
    get_email_reply_gpt_response,
)
from gui.email_window.details_popup import open_details
from gui.email_window.config_popup import RV
from gui.email_window.edit_info_popup import EditInfoPopup


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

                MDIconButton:
                    id: back_button
                    icon: "arrow-left"
                    size_hint_y: 1
                    size_hint_x: 0.05
                    on_release: root.deselect_everything()
                    theme_text_color: "Custom"
                    text_color: 1, 0, 0, 1  # Make it red for visibility
                    opacity: 0 
                    disabled: True

                MDIconButton:
                    id: dustbin_button
                    icon: "trash-can"
                    size_hint_y: 1
                    size_hint_x: 0.05
                    on_release: root.controller.delete_selected_items(root)
                    theme_text_color: "Custom"
                    text_color: 1, 0, 0, 1
                    opacity: 0 
                    disabled: True

                MDLabel:
                    text: "Email Reply Tracker"
                    halign: "center"
                    valign: "middle"
                    font_style: "Headline"
                    role: "small"
                    size_hint_y: 1

                MDIconButton:
                    icon: "cog"
                    size_hint_y: 1
                    size_hint_x: 0.05
                    on_release: root.config_popup()
                    theme_text_color: "Custom"
                    text_color: 1, 1, 1, 1

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

            GridLayout:
                size_hint_y: None
                size_hint_x: 1
                height: dp(40)
                cols: 7
                spacing: dp(5)

                Label:
                    text: "Party Name"
                    size_hint_x: 0.2
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Type"
                    size_hint_x: 0.2
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Phone"
                    size_hint_x: 0.2
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Email ID"
                    size_hint_x: 0.2
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Inbox #"
                    size_hint_x: 0.05
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Outbox #"
                    size_hint_x: 0.05
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

                Label:
                    text: "Actions"
                    size_hint_x: 0.4
                    halign: 'center'
                    valign: 'middle'
                    text_size: self.size
                    padding_x: dp(5)

            # RecycleView Section
            RecycleView:
                id: tracker_row
                viewclass: 'EmailTrackerRow'
                size_hint_y: 0.8
                size_hint_x: 1
                do_scroll_x: False
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
    GridLayout:
        cols: 7
        size_hint_y: None
        size_hint_x: 1
        height: dp(40)
        spacing: dp(5)

        Label:
            text: root.name
            size_hint_x: 0.2
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            padding_x: dp(5)

        Label:
            text: root.type_of_contact
            size_hint_x: 0.2
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            padding_x: dp(5)

        Label:
            text: root.phone
            size_hint_x: 0.2
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            padding_x: dp(5)

        Label:
            text: root.email_id
            size_hint_x: 0.2
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            padding_x: dp(5)

        Label:
            text: root.email_count
            size_hint_x: 0.05
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            padding_x: dp(5)

        Label:
            text: root.outgoing_email_count
            size_hint_x: 0.05
            halign: 'center'
            valign: 'middle'
            text_size: self.size
            padding_x: dp(5)

        BoxLayout:
            orientation: 'horizontal'
            size_hint_x: 0.4
            padding: dp(10)
            spacing: dp(10)

            Widget:  # spacer
                size_hint_x: 0.02

            MDButton:
                on_release: root.open_details()

                MDButtonText:
                    text: "Mails"
                    theme_text_color: "Custom"
                    text_color: "white"

            MDButton:
                on_release: root.open_outgoing_details()

                MDButtonText:
                    text: "Outbox"
                    theme_text_color: "Custom"
                    text_color: "white"

            MDButton:
                on_release: root.open_send_preview()

                MDButtonText:
                    text: "Send Follow Up"
                    theme_text_color: "Custom"
                    text_color: "white"

            MDButton:
                on_release: root.edit_info()

                MDButtonText:
                    text: "Edit Info"
                    theme_text_color: "Custom"
                    text_color: "white"

            Widget:  # spacer
                size_hint_x: 0.02
"""


# TODO: the button here should be disabled if there are no emails to be found
class EmailTrackerRow(RecycleDataViewBehavior, BoxLayout):
    email_id = StringProperty()
    email_count = StringProperty()  # incoming emails
    name = StringProperty()
    type_of_contact = StringProperty()
    outgoing_emails = ObjectProperty()
    outgoing_email_count = StringProperty()
    is_selected = BooleanProperty()
    selectable = BooleanProperty(True)
    controller = ObjectProperty()
    phone = StringProperty()
    email_item_obj = ObjectProperty()  # NOTE: This is a list. its dumb

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    # for incoming emails
    def open_details(self):
        # TODO: change the naming for either of these two
        open_details(
            {
                "email_id": self.email_id,
                "email_item_obj": self.email_item_obj,
            }
        )

    # for outgoing emails
    def open_outgoing_details(self):
        open_details(
            {
                "email_id": self.email_id,
                "email_item_obj": self.outgoing_emails,
            }
        )

    def edit_info(self):
        # dont need loading screen, this is p fast.
        data = self.controller.fetch_party_data(self.email_id)
        name, cellphone, title, last_audit_date, customer, supplier, party_pk = data

        if customer and supplier:
            cus_sup_value = "Customer & Supplier"
        elif customer:
            cus_sup_value = "Customer"
        elif supplier:
            cus_sup_value = "Supplier"
        else:
            cus_sup_value = ""

        EditInfoPopup(
            name=name,
            email=self.email_id,
            last_audit_date=last_audit_date if last_audit_date else "",
            cell_phone=cellphone if cellphone else "",
            title=title,
            customer_or_supplier=cus_sup_value,
        ).open()

    def _find_latest_email(self):
        def parse_received_time(email_entry):
            return datetime.datetime.fromisoformat(email_entry[1])

        if self.email_item_obj:
            self.email_item_obj.sort(key=lambda email: parse_received_time(email))
        if self.outgoing_emails:
            self.outgoing_emails.sort(key=lambda email: parse_received_time(email))

        last_incoming_email = self.email_item_obj[-1] if self.email_item_obj else None
        last_outgoing_email = self.outgoing_emails[-1] if self.outgoing_emails else None

        if last_incoming_email and last_outgoing_email:
            if parse_received_time(last_incoming_email) > parse_received_time(
                last_outgoing_email
            ):
                latest_email = last_incoming_email
            else:
                latest_email = last_outgoing_email
        else:
            latest_email = last_incoming_email or last_outgoing_email

        return latest_email

    def open_send_preview(self):
        email_body = ""  # base case
        latest_email = self._find_latest_email()

        def reply_to_last(inst):
            try:
                email_item = outlook.GetItemFromID(entry_id, store_id)
                last_email_body = email_item.Body
                reply_item = email_item.Reply()
                reply_item.Body = (
                    "Hello,\n\n"
                    + get_email_reply_gpt_response(last_email_body)
                    + "\nBest Regards,\nAmir\n"
                )
                reply_item.Display()
            except Exception as e:
                # TODO: manage this more carefully
                pass

        def send_new(inst):
            outlook = win32com.client.Dispatch("Outlook.Application")
            mail = outlook.CreateItem(0)
            mail.To = self.email_id
            mail.Display()

        if latest_email:
            outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace(
                "MAPI"
            )
            latest_email_location = latest_email[2]  # location
            entry_id, store_id = latest_email_location

            dialog = MDDialog(
                MDDialogIcon(
                    icon="refresh",
                ),
                MDDialogHeadlineText(
                    text="Select reply type",
                ),
                MDDialogButtonContainer(
                    MDDialogButtonContainer(
                        Widget(),
                        MDButton(
                            MDButtonText(text="Reply to last"),
                            style="text",
                            on_release=reply_to_last,
                        ),
                        MDButton(
                            MDButtonText(text="New email"),
                            style="text",
                            on_release=send_new,
                        ),
                        spacing="8dp",
                    )
                ),
            )
            dialog.open()


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
            key=lambda email_item: int(email_item.incoming_email_count),
            reverse=True,
        )  # most replies first
        self.ids.tracker_row.data = [
            {**email_item.to_dict(), "controller": self.controller}
            for email_item in sorted_email_list
        ]

    def outlook_email_listener_wrapper(self, dt):
        if self.start_up_task.done():
            asyncio.create_task(self.controller.listen_for_emails())
        else:
            self.controller.LOGGER.info("skipping as startup is still not complete")

    # FIX:
    def config_popup(self):
        popup = Popup(
            title="RecycleView Popup",
            content=RV(
                email_ids=[key for key in self.controller.tracked_emails.keys()],
                controller=self.controller,
            ),
            size_hint=(0.8, 0.8),
            auto_dismiss=True,
        )
        popup.open()


Builder.load_string(KV)
