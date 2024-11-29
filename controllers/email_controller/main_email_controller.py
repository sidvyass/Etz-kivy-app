from typing import List
import os
import asyncio
import json
import aiofiles
from kivy.uix.popup import ModalView
import pythoncom
import win32com.client
from typing import Dict, Any
from controllers.user_controller import UserAPI  # only for type hints
from controllers.email_controller.email_item_class import EmailItem
from controllers.base_logger import getlogger
from controllers.email_controller.scripts import main
from gui.email_window.config_popup import RV


DATA_FILE_PATH = r".\controllers\email_controller\configs\tracked_email_data.json"
CONFIG_FILE_PATH = r".\controllers\email_controller\configs\client_data.json"
EMAIL_PROCESS_LIMIT = 50  # WARNING: Do not remove.


class EmailTrackerController:
    def __init__(self, main_app, user, loading_screen):
        self.main_app = main_app
        self.loading_screen = loading_screen
        self.tracked_emails: Dict[str, EmailItem] = {}
        self.user: UserAPI = user  # NOTE: for live
        self.LOGGER = getlogger("Login controller")

    async def on_start_up(self, window_inst):
        """
        Runs to either build objects back up or start running the start up script.
        :param window_inst Screen(KivyMD): The instance of the GUI.
        """

        # TODO: ask the user to supply the file
        # TODO: ask the user before running the script

        if not (os.path.exists(DATA_FILE_PATH) and os.path.exists(CONFIG_FILE_PATH)):
            await self._run_indexing_script()

        self.configs = await self.read_json_file(CONFIG_FILE_PATH)
        self.last_entry_id = self.configs.get("last_entry_id", None)

        if not self.last_entry_id:
            self.LOGGER.critical("Entry ID for last email is None.")
            return

        data_buf = await self.read_json_file(DATA_FILE_PATH)
        await self._build_objects(data_buf)

        self.LOGGER.info("Initial setup complete. Loading email window...")
        self.main_app.screen_manager.current = "email_window"

        window_inst.build_rows(self.tracked_emails.values())  # "email_window" instance

    async def _run_indexing_script(self):
        """
        Wrapper to run the script that scrapes outlook and builds data files.
        """

        filepaths = {
            "tracked_emails": DATA_FILE_PATH,
            "config_file": CONFIG_FILE_PATH,
        }

        self.LOGGER.info("No config found. Running script...")
        self.main_app.screen_manager.current = "loading_screen_email_app"

        try:
            last_entry_id = await main(self.loading_screen.update_progress, filepaths)
            return last_entry_id
        except Exception as e:
            self.LOGGER.error(f"Failed to run indexing script: {e}")
            # TODO: notify the user of the error here
            return None

    async def _build_objects(self, data_dict: dict):
        """
        Runs on startup to build objects from the stored json file.
        """

        for email_id, value_dict in data_dict.items():
            try:
                required_keys = {"email_id", "email_count"}
                if not required_keys.issubset(value_dict.keys()):
                    raise ValueError(f"Missing required keys in {value_dict}")

                self.tracked_emails[email_id] = EmailItem(
                    value_dict["email_id"],
                    email_count=value_dict["email_count"],
                    emails_list=value_dict.get("email_item_obj", []),
                )

            except Exception as e:
                self.LOGGER.warning(
                    f"Could not build obj for {value_dict["email_id"]}\n{e}"
                )

    async def read_json_file(self, filepath: str) -> Any:
        """
        Reads a JSON file asynchronously and returns its content.

        :param filepath: The path to the JSON file.
        :return: Parsed JSON content.
        :raises FileNotFoundError: If the file does not exist.
        :raises ValueError: If the file cannot be parsed as JSON.
        """

        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        try:
            async with aiofiles.open(filepath, mode="r") as json_file:
                content = await json_file.read()
                return json.loads(content)
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON format in {filepath}: {e}")
        except Exception as e:
            raise ValueError(f"Failed to read JSON file at {filepath}: {e}")

    async def listen_for_emails(self):
        """
        Checks outlook for new emails.
        Breaks when self.last_entry_id (last scraped email) id matches.
        New self.last_entry_id is the first email checked.
        NOTE: This will not run if self.last_entry_id is not found.

        """

        self.LOGGER.info("Polling outlook...")

        if not hasattr(self, "last_entry_id"):
            self.LOGGER.info("No last entry ID found. Listener is not running.")
            return

        def _listen_process_email_sync():
            pythoncom.CoInitialize()

            try:
                outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace(
                    "MAPI"
                )

                inbox = outlook.GetDefaultFolder(6)
                messages = inbox.Items
                messages.Sort("[ReceivedTime]", Descending=True)

                temp_entry_id = messages[0].EntryID  # first message

                for idx, msg in enumerate(messages):
                    if msg.EntryID == self.last_entry_id:
                        self.last_entry_id = temp_entry_id
                        self.LOGGER.info(
                            f"Breaking. New last entry ID: {temp_entry_id}"
                        )
                        break
                    elif idx == EMAIL_PROCESS_LIMIT:
                        break
                    self.process_email(msg, inbox)

            except Exception as e:
                self.LOGGER.warning(e)
            finally:
                pythoncom.CoUninitialize()

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _listen_process_email_sync)

    def process_email(self, msg, inbox):
        """
        Adds the email's contents to the email obj that it belongs to.

        :param msg: win32com message obj
        :param inbox: outlook.GetDefaultFolder to store the location.
        """

        if msg.SenderEmailAddress in self.tracked_emails.keys():
            self.tracked_emails[msg.SenderEmailAddress].emails_list.append(
                (
                    msg.Subject,
                    str(msg.ReceivedTime),
                    (msg.EntryID, inbox.StoreID),
                    msg.Attachments.Count,
                )
            )
            self.LOGGER.info(f"Appended email from {msg.SenderEmailAddress} to obj.")

    def search(self, window_inst):
        pass
