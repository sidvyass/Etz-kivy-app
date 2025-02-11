import win32com.client


def get_pst_folder_inbox(store_name):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    for store in outlook.Stores:
        if store.DisplayName == store_name:
            print(f"Found store: {store_name}")

            root_folder = store.GetRootFolder()  # 6 = Inbox
            for folder in root_folder.Folders:
                print(folder.Name)


get_pst_folder_inbox("test_inbox")
