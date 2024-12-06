import pythoncom
import aioodbc
import win32com.client
import datetime
import asyncio
from typing import Tuple, List, Optional
from controllers.base_logger import getlogger

DSN = "DRIVER={SQL Server};SERVER=ETZ-SQL;DATABASE=SANDBOX;Trusted_Connection=yes"


class EmailItem:
    def __init__(
        self,
        email_id: str,  # MANDETORY
        email_count: int = 0,
        company_name: Optional[str] = None,
        fullname: Optional[str] = None,
        emails_list: Optional[List[Tuple[str, str, Tuple[str, str], int]]] = None,
        attachment_count: Optional[int] = None,
    ):
        self.LOGGER = getlogger("Email Item")
        self.email_id = email_id
        self.company_name = company_name
        self.fullname = fullname
        self.LOGGER.info(self.fullname)
        self.attachment_count = attachment_count
        self.email_count = email_count
        self.emails_list = (
            emails_list if emails_list else []
        )  # List of (subject, received_time, (EntryID, StoreID))

    def __repr__(self) -> str:
        return f"Email ID: {self.email_id}\nCount: {self.email_count}"

    async def find_emails(
        self, filter_year: int = datetime.datetime.now().year
    ) -> None:
        """
        Finds all emails by self.email_id. Runs in an executor to be non-blocking.
        """

        def _find_emails_sync():
            pythoncom.CoInitialize()
            try:
                outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace(
                    "MAPI"
                )
                inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
                messages = inbox.Items
                messages.Sort("[ReceivedTime]", Descending=True)

                start_of_year = f"{filter_year}-01-01"

                filter_query = f"[SenderEmailAddress] = '{self.email_id}' AND [ReceivedTime] >= '{start_of_year}'"
                filtered_items = messages.Restrict(filter_query)

                self.email_count = len(filtered_items)

                for item in filtered_items:
                    self.emails_list.append(
                        (
                            item.Subject,
                            str(item.ReceivedTime),
                            (item.EntryID, inbox.StoreID),
                            item.Attachments.Count,
                        )
                    )
            except Exception as e:
                self.LOGGER.error(f"Error processing {self.email_id}: {e}")
            finally:
                pythoncom.CoUninitialize()

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _find_emails_sync)

    def to_dict(self) -> dict:
        self.LOGGER.info(self.fullname)
        return {
            "email_id": self.email_id,
            "email_count": str(self.email_count),
            "email_item_obj": self.emails_list,
            "name": self.fullname if self.fullname else "",
            "is_active": False,
        }
