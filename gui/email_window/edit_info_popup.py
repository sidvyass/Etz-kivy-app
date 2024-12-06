from kivy.uix.popup import Popup
from kivy.properties import StringProperty
from kivy.lang import Builder


KV = """
<EditInfoPopup>:
    name: 'edit_info_popup'

    MDBoxLayout:
        orientation: 'vertical'
        padding: 20
        spacing: 20
        size_hint_y: 1
        # height: self.minimum_height
        # pos_hint: {"top": 1}

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "10dp"
            size_hint_y: 0.25
            # height: self.minimum_height

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Name: "
                    halign: "right"
                    valign: "center"
                    theme_text_color: "Custom"
                    text_color: "white"
                    size_hint_x: 0.3

                MDTextField:
                    id: name
                    text: root.name
                    mode: "outlined"
                    size_hint_x: 0.7

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Email ID: "
                    halign: "right"
                    valign: "center"
                    theme_text_color: "Custom"
                    text_color: "white"
                    size_hint_x: 0.3

                MDTextField:
                    id: email
                    text: root.email
                    mode: "outlined"
                    size_hint_x: 0.7

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "10dp"
            size_hint_y: 0.25
            # height: self.minimum_height

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Customer/Supplier: "
                    halign: "right"
                    valign: "center"
                    theme_text_color: "Custom"
                    text_color: "white"
                    size_hint_x: 0.3

                MDTextField:
                    id: customer_or_supplier
                    text: root.customer_or_supplier
                    mode: "outlined"
                    size_hint_x: 0.7

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Last Audit: "
                    halign: "right"
                    valign: "center"
                    theme_text_color: "Custom"
                    text_color: "white"
                    size_hint_x: 0.3

                MDTextField:
                    id: last_audit
                    text: root.last_audit_date
                    mode: "outlined"
                    size_hint_x: 0.7

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "10dp"
            size_hint_y: 0.25
            # height: self.minimum_height

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Title: "
                    halign: "right"
                    valign: "center"
                    theme_text_color: "Custom"
                    text_color: "white"
                    size_hint_x: 0.3

                MDTextField:
                    id: title
                    text: root.title
                    mode: "outlined"
                    size_hint_x: 0.7

            MDBoxLayout:
                orientation: "horizontal"
                spacing: "10dp"
                size_hint_y: None
                height: self.minimum_height

                MDLabel:
                    text: "Cell Phone: "
                    halign: "right"
                    valign: "center"
                    theme_text_color: "Custom"
                    text_color: "white"
                    size_hint_x: 0.3

                MDTextField:
                    id: cell_phone
                    text: root.cell_phone
                    mode: "outlined"
                    size_hint_x: 0.7

        MDBoxLayout:
            orientation: "horizontal"
            spacing: "10dp"
            size_hint_y: 0.25
            size_hint_x: 1
            # height: self.minimum_height

            MDButton:
                on_release: root.dismiss()
                size_hint_x: 0.3
                theme_bg_color: "Custom"
                md_bg_color: 0.3, 0.3, 0.3, 1

                MDButtonText:
                    text: "Dismiss"
                    theme_text_color: "Custom"
                    text_color: "white"

            MDButton:
                size_hint_x: 0.3
                theme_bg_color: "Custom"
                md_bg_color: 0.3, 0.3, 0.3, 1

                MDButtonText:
                    text: "Contacts"
                    theme_text_color: "Custom"
                    text_color: "white"

            MDButton:
                on_release: root.on_save()
                size_hint_x: 0.3
                theme_bg_color: "Custom"
                md_bg_color: 0.3, 0.3, 0.3, 1

                MDButtonText:
                    text: "Save"
                    theme_text_color: "Custom"
                    text_color: "white"
"""


class EditInfoPopup(Popup):
    name = StringProperty()
    email = StringProperty()
    last_audit_date = StringProperty()
    customer_or_supplier = StringProperty()
    cell_phone = StringProperty()
    title = StringProperty()

    def on_save(self):
        pass


Builder.load_string(KV)
