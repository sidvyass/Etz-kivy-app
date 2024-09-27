from kivy.clock import Clock
from kivy.lang import Builder
from kivymd.app import MDApp
from kivy.metrics import dp
from kivymd.uix.datatables import MDDataTable
from kivy.core.window import Window
from kivy.uix.label import Label

KV = """
<EmailWindow>:
    name: 'email_window'

    BoxLayout:
        orientation: 'vertical'
        padding: dp(20)
        spacing: dp(20)

        # First Row - Heading
        BoxLayout:
            size_hint_y: 0.1
            padding: [20, 10]
            canvas.before:
                Color:
                    rgba: 0.1, 0.1, 0.1, 1
                Rectangle:
                    size: self.size
                    pos: self.pos

            MDLabel:
                text: "Auto Email"
                halign: "center"
                valign: "middle"
                size_hint_x: 1
                theme_text_color: "Custom"
                text_color: 1, 1, 1, 1  # White text color

        # Second Row - Selection Box, Search Bar, Search Button
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            padding: dp(10)
            spacing: dp(10)

            MDDropDownItem:
                id: selection_box
                text: "Select Type"
                size_hint_x: 0.3
                on_release: app.open_menu()

            MDTextField:
                id: search_field
                hint_text: "Search"
                mode: "rectangle"
                size_hint_x: 0.5

            MDRaisedButton:
                text: "Search"
                size_hint_x: 0.2
                on_release: app.search()

        # Third Row - Data Table Container (if needed)
        ScrollView:
            size_hint_y: 0.4
            do_scroll_x: True
            do_scroll_y: False
            AnchorLayout:
                id: table_container
                size_hint_x: 1
                size_hint_y: 1

        # Fourth Row - Attachments and Quantity
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.2
            padding: dp(10)
            spacing: dp(10)

            MDTextField:
                hint_text: "Other Attachments"
                mode: "rectangle"
                size_hint_x: 0.3

            MDTextField:
                hint_text: "Finish Attachments"
                mode: "rectangle"
                size_hint_x: 0.3

            MDTextField:
                hint_text: "Item Quantity"
                mode: "rectangle"
                size_hint_x: 0.3

        # Fifth Row - Preview and Send Email Buttons
        BoxLayout:
            orientation: "horizontal"
            size_hint_y: 0.1
            padding: dp(10)
            spacing: dp(10)

            MDRaisedButton:
                text: "Preview Email"
                size_hint_x: 0.5
                on_release: app.preview_email()

            MDRaisedButton:
                text: "Send Email"
                size_hint_x: 0.5
                on_release: app.send_email()

        # Drag-and-Drop Label to Show Dropped Files
        Label:
            id: drop_label
            text: "Drag and drop files here"
            size_hint_y: 0.1
            halign: "center"
"""


class EmailWindow(MDApp):
    def build(self):
        # Load the KV string and return the root widget
        root = Builder.load_string(KV)
        self.theme_cls.theme_style = "Dark"

        # Schedule the table creation after build
        Clock.schedule_once(self.create_table, 0)

        # Bind drag and drop functionality
        Window.bind(on_dropfile=self._on_file_drop)

        return root

    def create_table(self, *args, rows=[("Fetching Data...", "", "", "", "", "", "")]):
        column_widths = [
            ("PO Number", dp(50)),
            ("CO Number", dp(25)),
            ("Type of CO", dp(50)),
            ("Date", dp(50)),
            ("FilePath", dp(50)),  # This will act like a button (clickable text)
            ("FileName", dp(50)),
        ]

        row_with_buttons = []
        assert len(rows) >= 1
        for row in rows:
            file_path = row[4]
            file_button = f"[Open File]"  # Text that acts like a button

            new_row = (row[0], row[1], row[2], row[3], file_button, row[5])
            row_with_buttons.append(new_row)

        self.data_tables = MDDataTable(
            size_hint=(1, 1),
            use_pagination=True,
            check=True,
            column_data=column_widths,
            row_data=row_with_buttons,
        )

        # Now self.ids is available because the root widget is returned from build()
        self.root.ids.table_container.add_widget(self.data_tables)

    def _on_file_drop(self, window, file_path):
        # Convert byte string to a regular string (Python 3)
        file_path = file_path.decode("utf-8")

        # Display the dropped file in the label
        self.root.ids.drop_label.text = f"File dropped: {file_path}"

    def open_menu(self):
        pass

    def search(self):
        pass

    def preview_email(self):
        pass

    def send_email(self):
        pass


if __name__ == "__main__":
    EmailWindow().run()
