from kivymd.uix.dialog import MDDialog, MDDialogHeadlineText, MDDialogContentContainer
from kivymd.uix.button import MDButton, MDButtonText
from kivymd.uix.list import MDListItem, MDListItemSupportingText
from typing import List
import win32com.client


def get_all_folders() -> List:
    stores_list = []
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    for store in outlook.Stores:
        stores_list.append(store.DisplayName)

    return stores_list


def open_dropdown_dialog(title, callback):
    """
    Opens an MDDialog with a list for the user to select an item.

    :param title: Title of the dialog.
    :param callback: Function to execute when an item is selected.
    """
    items = get_all_folders()

    # Generate list items dynamically
    list_items = [
        MDListItem(
            MDListItemSupportingText(text=item),
            on_release=lambda x=item: select_item(x),
        )
        for item in items
    ]

    def select_item(item):
        callback(item)
        dialog.dismiss()

    dialog = MDDialog(
        MDDialogHeadlineText(text=title, halign="left"),
        MDDialogContentContainer(*list_items, orientation="vertical"),
        MDButton(
            MDButtonText("Cancel"),
            pos_hint={"center_x": 0.5},
            on_release=lambda x: dialog.dismiss(),
        ),
    )

    dialog.open()
