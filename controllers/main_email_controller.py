import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from pprint import pprint
import asyncio
import json
import aiofiles
import time
from controllers.base_logger import getlogger
from controllers.email_controller.scripts import main
import win32com.client
from typing import Dict, Tuple, List, Any
import pythoncom


class EmailItem:
    def __init__(
        self, email_id, email_count=0, company_name=None, fullname=None, emails_list=[]
    ):
        self.LOGGER = getlogger("Email Item")
        self.email_id = email_id
        self.company_name = company_name
        self.fullname = fullname
        self.email_count = email_count

        # (email subject, recieved time, (location))
        # TODO: One of these should also contain a datetime obj
        self.emails_list: List[Tuple[str, str, Tuple[str, str]]] = (
            emails_list  # All emails
        )

    def __repr__(self) -> str:
        return f"Email ID: {self.email_id}\nCount: {self.email_count}"

    async def find_emails(self) -> None:
        """
        finds all emails by self.email_id. Runs in an executor so that it is non-blocking.
        """

        self.LOGGER.info(f"finding {self.email_id}...")
        start_time = time.perf_counter()

        def _find_emails_sync(email_id):
            pythoncom.CoInitialize()
            try:
                outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace(
                    "MAPI"
                )

                inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
                messages = inbox.Items
                messages.Sort("[ReceivedTime]", Descending=True)
                filter_query = f"[SenderEmailAddress] = '{email_id}'"
                filtered_items = messages.Restrict(filter_query)

                self.email_count = len(filtered_items)

                for item in filtered_items:
                    self.emails_list.append(
                        (
                            item.Subject,
                            str(item.ReceivedTime),
                            (item.EntryID, inbox.StoreID),
                        )
                    )
            except Exception as e:
                self.LOGGER.error(f"{self.email_id} has an error - {e}")
            finally:
                pythoncom.CoUninitialize()
                self.LOGGER.info(
                    f"{self.email_id} task completed.\nTime Taken - {time.perf_counter() - start_time}\n*************************"
                )

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _find_emails_sync, self.email_id)

    def to_dict(self) -> dict:
        return {
            "email_id": self.email_id,
            "email_count": f"{self.email_count}",
            "email_item_obj": self.emails_list,
        }


class EmailTrackerController:
    # TODO: make sure that user is passed in the live version.
    def __init__(self):
        self.LOGGER = getlogger("Login controller")
        self.tracked_emails: Dict[str, EmailItem] = {}
        self.configs = None
        # self.user: UserAPI = user
        self.last_email_id = None
        self.config_file_path = (
            r"C:\PythonProjects\esis-auto-gui\controllers\email_controller\config.json"
        )
        self.data_file_path = r"C:\PythonProjects\esis-auto-gui\controllers\email_controller\tracked_email_data.json"

    async def on_start_up(self):
        # read config file
        self.LOGGER.info("Executing start up...")

        self.configs = await self.read_json_file(self.config_file_path)

        # Inital run complete
        if self.configs.get("outlook_indexing").get("first_run"):
            self.LOGGER.info("First run already complete. Finding data...")

            buf = await self.read_json_file(self.data_file_path)  # data file parse

            self.LOGGER.info("Data found. Building objects...")

            assert isinstance(buf, dict)  # TODO: change this to throw an actual error

            for email_id, value_dict in buf.items():  # building objs
                self.tracked_emails[email_id] = EmailItem(
                    value_dict["email_id"],  # email id
                    email_count=value_dict["email_count"],  # count
                    emails_list=value_dict.get("email_item_obj", []),  # emails
                )
        else:
            # Initial run is not complete
            # FIX: Maybe ask the user before starting to index?
            await main()

    async def read_json_file(self, filepath) -> Any:
        try:
            async with aiofiles.open(filepath, mode="r") as json_file:
                c = await json_file.read()
                return json.loads(c)

        except Exception as e:
            self.LOGGER.critical(f"Config file could not be parsed.\n{e}")
            raise ValueError

    # TEST:
    async def listen_for_emails(self):
        self.LOGGER.info("Polling outlook...")

        if not self.last_email_id:
            raise ValueError

        def _listen_process_email_sync():
            pythoncom.CoInitialize()
            try:
                outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace(
                    "MAPI"
                )

                inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
                messages = inbox.Items
                messages.Sort("[ReceivedTime]", Descending=True)

                for msg in messages:
                    while msg.EntryID != self.last_email_id:
                        self.process_email(msg, inbox)
                        self.LOGGER.info()
                    self.last_email_id = msg.EntryID
                    break

            except Exception as e:
                pass
            finally:
                pythoncom.CoUninitialize()

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _listen_process_email_sync)

    # TEST:
    def process_email(self, inbox, msg):
        if msg.SenderEmailAddress in self.tracked_emails.keys():
            self.LOGGER.info("match found. Appending to obj...")
            self.tracked_emails[msg.SenderEmailAddress].emails_list.append(
                (
                    msg.Subject,
                    str(msg.ReceivedTime),
                    (msg.EntryID, inbox.StoreID),
                )
            )
            self.LOGGER.info(f"Appended email from {msg.SenderEmailAddress} to obj.")


if __name__ == "__main__":
    e = EmailTrackerController()
    asyncio.run(e.on_start_up())
