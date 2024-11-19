import sys
import aioodbc
import asyncio
import json
import aiofiles
import time
from typing import List
from pydantic import BaseModel, EmailStr, ValidationError
import asyncio
import json
import time
from typing import List
import requests
import aiofiles
import loguru
from controllers.main_email_controller import EmailItem
import win32com.client


def getlogger(name: str = "DefaultName", level="DEBUG") -> loguru.logger:  # type: ignore
    """
    Initialize and return a logger instance with the specified name and level.
    """

    logobj = loguru.logger.bind(name=name)

    logobj.remove()

    logger_format = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "{extra[name]} | "
        "<level>{level: <8}</level> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> | "
        "<level>{message}</level>"
    )

    logobj.add(
        sys.stderr,
        level=level,
        format=logger_format,
        colorize=True,
        serialize=False,
    )

    return logobj


LOGGER = getlogger("Start up script")


class EmailItemModel(BaseModel):
    email_id: EmailStr


async def pull_all_emails(email_item_list=[]) -> List[EmailItem]:
    """
    Pulls all emails from API endpoint and creates EmailItem objects. Email is validated before creation.
    """
    LOGGER.info("Pulling emails from Mie Trak...")
    async with aioodbc.connect(
        dsn="DRIVER={SQL Server};SERVER=ETZ-SQL;DATABASE=SANDBOX;Trusted_Connection=yes"
    ) as conn:
        async with await conn.cursor() as cursor:
            async with await conn.cursor() as cursor:
                await cursor.execute(
                    "SELECT DISTINCT Name, Email from party where Email is not NULL;"
                )
                values = await cursor.fetchall()

        d = {emailid: name for name, emailid in values}

    try:
        for email_id, name in d.items():  # key = email id
            try:
                validated_email = EmailItemModel(email_id=email_id)
                email_item_list.append(
                    EmailItem(validated_email.email_id, fullname=name)
                )
            except ValidationError:
                LOGGER.debug(f"Email: {email_id} is invalid. (Error in database)")

        return email_item_list

    except Exception as e:
        raise requests.exceptions.RequestException


async def scrape_outlook(email_item_list: List[EmailItem], max_tasks=20):
    """
    Collects and runs the task for all email IDs.
    The find_emails() function handles filtering, indexing and appeading data to instance.

    :param email_item_list: List of all EmailItem objects built using data from server.
    """

    semaphore = asyncio.Semaphore(max_tasks)

    async def limited_task(email_item: EmailItem):  # to queue the tasks
        async with semaphore:
            await email_item.find_emails()

    tasks = [
        limited_task(email_item)
        for email_item in email_item_list
        if isinstance(email_item, EmailItem)  # fail safe
    ]
    await asyncio.gather(*tasks)


async def write_json_file(filepath: str, email_item_list: List[EmailItem]):
    """
    Write the json file after everythin is parsed. Also save the last scraped email.

    :param email_list: List with EmailItem objects used in the function above to find emails.
    NOTE: If the same list is not used then this function will write empty dicts into the json file
    """
    LOGGER.info("Writing json data file...")

    data = {email_item.email_id: email_item.to_dict() for email_item in email_item_list}

    try:
        async with aiofiles.open(filepath, mode="w") as json_file:
            await json_file.write(json.dumps(data, indent=2))
    except Exception as e:
        LOGGER.error(e)


def save_entry_id_of_latest_email():
    """
    To run before we start scraping anything so that we know what our endpoint is.
    The listener will use this to scrape all the emails above this point.
    """
    try:
        # initialize outlook
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

        # access inbox
        inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox folder

        # get all emails and sort by received time descending
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        # get the latest email
        latest_email = messages.GetFirst()

        if latest_email:
            return latest_email.EntryID
        else:
            return None  # no emails found

    except Exception as e:
        print(f"error fetching latest email: {e}")
        return None


async def main() -> None:
    start_time = time.perf_counter()
    LOGGER.info("Running start up script...")
    try:
        email_item_list = await pull_all_emails()
    except requests.RequestException as e:
        return None

    try:
        await scrape_outlook(email_item_list)
    except Exception as e:
        print(e)

    finally:
        await write_json_file(
            r".\tracked_email_data.json",
            email_item_list,
        )
        LOGGER.info(f"Finished. Time taken - {time.perf_counter() - start_time}")
