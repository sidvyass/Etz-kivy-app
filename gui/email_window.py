from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ImageLeftWidget, OneLineAvatarListItem, TwoLineListItem
from plyer import filechooser


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
                hint_text: "Search"

            MDDropDownItem:
                id: type_dropdown
                text: 'Type'
                size_hint_x: 0.1
                on_release: root.open_type_selection_dropdown()

            MDRaisedButton:
                text: 'Search'
                size_hint_x: 0.4
                on_release: root.controller.search(root)

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
                    text: "Upload Files"
                    size_hint_y: 0.2
                    size_hint_x: 1
                    font_style: 'H5'
                    valign: 'top'
                    halign: 'center'

                MDLabel:
                    id: files_uploaded
                    text: "No files selected"
                    size_hint_x: 1 
                    valign: 'center'
                    halign: 'center'

                MDFlatButton:
                    text: "Select Files"
                    text_color: 1, 1, 1, 1 
                    size_hint_x: 1
                    md_bg_color: app.theme_cls.primary_color
                    on_release: root.choose_files()
                    valign: 'top'
                    halign: 'center'

            # 2nd file chooser
            BoxLayout:
                orientation: 'vertical'
                padding: 10
                size_hint_x: 0.5
                size_hint_y: 1

                MDLabel:
                    text: "Upload Files"
                    size_hint_y: 0.2
                    size_hint_x: 1
                    font_style: 'H5'
                    valign: 'top'
                    halign: 'center'

                MDLabel:
                    id: files_uploaded
                    text: "No files selected"
                    size_hint_x: 1 
                    valign: 'center'
                    halign: 'center'

                MDFlatButton:
                    text: "Select Files"
                    text_color: 1, 1, 1, 1 
                    size_hint_x: 1
                    md_bg_color: app.theme_cls.primary_color
                    on_release: root.choose_files()
                    valign: 'top'
                    halign: 'center'

        BoxLayout:
            orientation: 'horizontal'
            padding: 10
            size_hint_y: 0.1
            spacing: 10

            MDFlatButton:
                text: "Send Mails"
                text_color: 1, 1, 1, 1 
                size_hint_x: 0.25
                md_bg_color: app.theme_cls.primary_color
                on_release: root.controller.send_mail(root)

            MDFlatButton:
                text: "Preview Mail"
                text_color: 1, 1, 1, 1 
                size_hint_x: 0.25
                md_bg_color: app.theme_cls.primary_color
                on_release: root.controller.preview_emails(root)

            MDFlatButton:
                text: "btn 3"
                text_color: 1, 1, 1, 1 
                size_hint_x: 0.25
                md_bg_color: app.theme_cls.primary_color
                on_release: root.controller.preview_emails(root)  # TODO: placeholder

"""


Builder.load_string(KV)


class SearchResultItem(OneLineAvatarListItem):
    def __init__(self, filepath, controller, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(ImageLeftWidget(source=filepath))
        self.parent_controller = controller

    def on_release(self):
        # TODO: controller call
        print(f"pressed {self.text}")


class EmailWindowGui(Screen):

    def __init__(self, controller, **kwargs):
        super().__init__(**kwargs)
        self.controller = controller

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
        # TODO: format the string so that all results are equally spaced
        for x in range(10):
            self.ids.selection_list.add_widget(
                SearchResultItem(
                    filepath=r"C:\PythonProjects\placeholder-image.jpg",
                    controller=self.controller,
                    text=f"{x}",
                    secondary_text="number 2",
                )
            )

    def choose_files(self):
        path = filechooser.open_file(title="Select file")  # Type: ignore
