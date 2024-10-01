from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivymd.uix.list import ImageLeftWidget, OneLineAvatarListItem, TwoLineListItem
from plyer import filechooser
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
                    on_release: root.choose_files('files_uploaded')
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
                    id: files_uploaded_1
                    text: "No files selected"
                    size_hint_x: 1 
                    valign: 'center'
                    halign: 'center'

                MDFlatButton:
                    text: "Select Files"
                    text_color: 1, 1, 1, 1 
                    size_hint_x: 1
                    md_bg_color: app.theme_cls.primary_color
                    on_release: root.choose_files('files_uploaded_1')
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


class SelectedResult(OneLineAvatarListItem):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.ids._lbl_primary.halign = "center"
        self.ids._lbl_primary.font_size = "20sp"
        self.ids._lbl_primary.bold = True


class SearchResultItem(OneLineAvatarListItem):
    def __init__(self, filepath, parent_ref, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.add_widget(ImageLeftWidget(source=filepath))
        self.parent_ref = parent_ref

    def on_release(self):
        # TODO: controller call
        self.parent_ref.on_search_selection(self.text)


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
        # TODO: add a check to see if both fields are filled
        search_value = self.ids.search_field.text
        search_type = self.ids.type_dropdown.current_item
        self.ids.selection_list.clear_widgets()
        asyncio.create_task(self._start_search(search_type, search_value))

    async def _start_search(self, search_type, search_value):
        values = await self.controller.on_search_button_press(
            search_value, search_type, self
        )
        for val in values:
            self.ids.selection_list.add_widget(
                SearchResultItem(
                    filepath=r"C:\PythonProjects\placeholder-image.jpg",
                    parent_ref=self,
                    text=f"{val}",
                    secondary_text="number 2",
                )
            )

    def choose_files(self, id):
        path = filechooser.open_file(title="Select file")  # Type: ignore
        self.controller.on_file_upload(path, id, self)

    def on_search_selection(self, rfq_or_item_selection):
        self.controller.update_email_type(rfq_or_item_selection)
        self.ids.selection_list.clear_widgets()
        self.ids.selection_list.add_widget(
            SelectedResult(text=rfq_or_item_selection.split(":")[0])
        )
