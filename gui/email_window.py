from kivy.properties import ListProperty
from kivy.uix.screenmanager import Screen
from kivy.lang import Builder
from kivymd.uix.menu import MDDropdownMenu
from kivy.uix.recycleview import RecycleView
from kivy.uix.recycleview.views import RecycleDataViewBehavior
from kivy.uix.label import Label
from kivy.properties import BooleanProperty
from kivy.uix.recycleboxlayout import RecycleBoxLayout
from kivy.uix.behaviors import FocusBehavior
from kivy.uix.recycleview.layout import LayoutSelectionBehavior

KV = """
<SelectableLabel>:
    canvas.before:
        Color:
            rgba: (.0, 0.9, .1, .3) if self.selected else (0.1, 0.1, 0.1, 1)
        Rectangle:
            pos: self.pos
            size: self.size

<EmailWindowGui>:
    name: 'email_gui'

    MDBoxLayout:
        orientation: 'vertical'
        canvas.before:
            Color:
                rgba: 0.1, 0.1, 0.1, 1  # Dark background

        # Search bar and buttons
        MDBoxLayout:
            orientation: 'horizontal'
            padding: 10
            spacing: 10
            size_hint_y: 0.08
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
                on_release: root.search()

        RecycleView:
            viewclass: 'SelectableLabel'
            data: [{'text': str(x)} for x in root.data_items]
            size_hint_y: 0.8 
            SelectableRecycleGridLayout:
                cols: 2
                default_size: None, dp(26)
                default_size_hint: 1, None
                size_hint_y: None
                height: self.minimum_height
                orientation: 'vertical'
                multiselect: False
"""


Builder.load_string(KV)


class SelectableRecycleGridLayout(
    FocusBehavior, LayoutSelectionBehavior, RecycleBoxLayout
):
    """Adds selection and focus behavior to the view."""


class SelectableLabel(RecycleDataViewBehavior, Label):
    """Add selection support to the Label"""

    index = None
    selected = BooleanProperty(False)
    selectable = BooleanProperty(True)

    def refresh_view_attrs(self, rv, index, data):
        """Catch and handle the view changes"""
        self.index = index
        return super(SelectableLabel, self).refresh_view_attrs(rv, index, data)

    def on_touch_down(self, touch):
        """Add selection on touch down"""
        if super(SelectableLabel, self).on_touch_down(touch):
            return True
        if self.collide_point(*touch.pos) and self.selectable:
            return self.parent.select_with_touch(self.index, touch)

    def apply_selection(self, rv, index, is_selected):
        """Respond to the selection of items in the view."""
        self.selected = is_selected
        if is_selected:
            print("selection changed to {0}".format(rv.data[index]))
        else:
            print("selection removed for {0}".format(rv.data[index]))


class EmailWindowGui(Screen):
    data_items = ListProperty([])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.data_items = [{"text": str(x)} for x in range(100)]

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
        # NOTE: probably a controller call
        pass
