import sys
import os


sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))


from pydantic import BaseModel, EmailStr, ValidationError
import asyncio
import json
import time
from typing import List
import requests
from controllers.main_email_controller import EmailItem
from controllers.base_logger import getlogger
import aiofiles


LOGGER = getlogger("start up script")
file_lock = asyncio.Lock()


class EmailItemModel(BaseModel):
    email_id: EmailStr


def pull_all_emails(email_item_list=[]) -> List[EmailItem]:
    """
    Pulls all emails from API endpoint and creates EmailItem objects. Email is validated before creation.
    """

    try:
        req = requests.get("http://127.0.0.1:8000/get_all_party_email_ids")
        d = req.json()
        for email_id, name in d.items():  # key = email id
            try:
                validated_email = EmailItemModel(email_id=email_id)
                email_item_list.append(
                    EmailItem(validated_email.email_id, fullname=name)
                )
            except ValidationError:
                LOGGER.debug(f"Email: {email_id} is invalid.")

        return email_item_list
    except Exception as e:
        LOGGER.critical(f"Server error\n{e}")
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

    data = {email_item.email_id: email_item.to_dict() for email_item in email_item_list}

    try:
        async with aiofiles.open(filepath, mode="w") as json_file:
            await json_file.write(json.dumps(data, indent=2))
    except Exception as e:
        LOGGER.critical(
            f"Could not write data into json file.\nFilepath - {filepath}.\n{e}"
        )


async def main() -> None:
    try:
        email_item_list = pull_all_emails()
    except requests.RequestException as e:
        LOGGER.debug(f"Server problem {e}")
        return None

    try:
        await scrape_outlook(email_item_list)
    except Exception as e:
        LOGGER.error(e)

    finally:
        await write_json_file(
            r"C:\PythonProjects\esis-auto-gui\controllers\email_controller\tracked_email_data.json",
            email_item_list,
        )
