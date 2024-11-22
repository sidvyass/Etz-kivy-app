import pythoncom
import win32com.client
import aioodbc
import time
import datetime
import asyncio
import json
import aiofiles
from pydantic import BaseModel, EmailStr, ValidationError
from typing import Tuple, List, Dict, Optional
from controllers.base_logger import getlogger

DSN = "DRIVER={SQL Server};SERVER=ETZ-SQL;DATABASE=SANDBOX;Trusted_Connection=yes"

LOGGER = getlogger("Start up script")


class EmailItem:
    def __init__(
        self,
        email_id: str,
        email_count: int = 0,
        company_name: Optional[str] = None,
        fullname: Optional[str] = None,
        emails_list: Optional[List[Tuple[str, str, Tuple[str, str]]]] = None,
    ):
        self.LOGGER = getlogger("Email Item")
        self.email_id = email_id
        self.company_name = company_name
        self.fullname = fullname
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
                        )
                    )
            except Exception as e:
                self.LOGGER.error(f"Error processing {self.email_id}: {e}")
            finally:
                pythoncom.CoUninitialize()

        loop = asyncio.get_running_loop()
        await loop.run_in_executor(None, _find_emails_sync)

    def to_dict(self) -> dict:
        return {
            "email_id": self.email_id,
            "email_count": str(self.email_count),
            "email_item_obj": self.emails_list,
        }


class EmailItemModel(BaseModel):
    email_id: EmailStr


async def fetch_email_data() -> Optional[List[EmailItem]]:
    """
    Fetches email data from the database, validates email addresses, and creates EmailItem objects.
    """
    LOGGER.info("Pulling emails from the database...")
    email_item_list: List[EmailItem] = []
    try:
        async with aioodbc.connect(dsn=DSN) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT DISTINCT Name, Email FROM party WHERE Email IS NOT NULL;"
                )
                values = await cursor.fetchall()
    except Exception as e:
        LOGGER.critical(f"Database connection error: {e}")
        return None

    # Validate and create EmailItem objects
    for name, email_id in values:
        try:
            validated_email = EmailItemModel(email_id=email_id)
            email_item_list.append(EmailItem(validated_email.email_id, fullname=name))
        except ValidationError:
            LOGGER.debug(f"Invalid email found: {email_id}")

    if not email_item_list:
        LOGGER.warning("No valid email items found.")
        return None

    return email_item_list


async def process_emails(
    email_item_list: List[EmailItem], progress_bar_func, max_tasks: int = 20
) -> bool:
    """
    Scrapes emails from Outlook and processes them.
    """
    progress_bar_func(update_text="Processing emails from Outlook...")
    if not email_item_list:
        LOGGER.warning("Email item list is empty.")
        return False

    progress_increment = 100 / len(email_item_list)
    semaphore = asyncio.Semaphore(max_tasks)

    async def limited_task(email_item: EmailItem):
        async with semaphore:
            await email_item.find_emails()
            progress_bar_func(val=progress_increment)

    tasks = [limited_task(email_item) for email_item in email_item_list]
    try:
        await asyncio.gather(*tasks)
        return True
    except Exception as e:
        LOGGER.critical(f"Error processing emails: {e}")
        return False


def save_entry_id_of_latest_email() -> Optional[str]:
    """
    Retrieves the EntryID of the latest email in the inbox.
    """
    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    except Exception as e:
        LOGGER.critical(f"Error initializing Outlook: {e}")
        return None

    try:
        inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox folder
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        latest_email = messages.GetFirst()

        if latest_email:
            return latest_email.EntryID
        else:
            return None  # No emails found
    except Exception as e:
        LOGGER.error(f"Error fetching latest email: {e}")
        return None


async def save_configuration(
    tracked_emails_file: str,
    config_file_path: str,
    email_item_list: List[EmailItem],
    latest_entry_id: str,
) -> bool:
    """
    Saves the tracked email data and configuration to JSON files.
    """
    data = {email_item.email_id: email_item.to_dict() for email_item in email_item_list}
    config = {
        "tracked_email_filepath": tracked_emails_file,
        "email_indexing": True,
        "last_entry_id": latest_entry_id,
    }

    try:
        async with aiofiles.open(tracked_emails_file, mode="w") as json_file:
            await json_file.write(json.dumps(data, indent=2))

        async with aiofiles.open(config_file_path, mode="w") as json_file:
            await json_file.write(json.dumps(config, indent=2))

        LOGGER.info("Configuration saved successfully.")
        return True
    except Exception as e:
        LOGGER.critical(f"Error saving configuration: {e}")
        return False


async def main(progress_bar_func, filepaths: Dict[str, str]) -> None:
    """
    Main entry point for scraping and processing emails.
    """
    tracked_emails_file = filepaths.get("tracked_emails")
    config_file_path = filepaths.get("config_file")

    if not tracked_emails_file or not config_file_path:
        LOGGER.critical("Invalid file paths provided. Exiting.")
        return

    progress_bar_func(update_text="Recording last email...")

    latest_email_entry_id = save_entry_id_of_latest_email()
    if not latest_email_entry_id:
        LOGGER.error("No latest email found. Exiting.")
        return

    start_time = time.perf_counter()

    email_item_list = await fetch_email_data()
    if not email_item_list:
        LOGGER.error("Email data could not be fetched. Exiting.")
        return

    success = await process_emails(email_item_list, progress_bar_func)
    if not success:
        LOGGER.error("Email processing failed. Exiting.")
        return

    save_status = await save_configuration(
        tracked_emails_file,
        config_file_path,
        email_item_list,
        latest_email_entry_id,
    )
    if not save_status:
        LOGGER.error("Failed to save configuration. Exiting.")
        return

    elapsed_time = time.perf_counter() - start_time
    LOGGER.info(f"Finished in {elapsed_time:.2f} seconds.")
