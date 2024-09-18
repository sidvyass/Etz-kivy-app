import requests
from controllers.base_logger import getlogger
import aiohttp
import time


class UserAPI:
    def __init__(self, username, password):
        self.LOGGER = getlogger(f"client {username}")
        self.url = "http://127.0.0.1:8000"
        self.data = {
            "username": username,
            "password": password,
        }
        self._is_logged_in = False

    def dummy_call(self):
        req = requests.get("http://127.0.0.1:8000/")
        print(req.json())

    def login(self):
        req = requests.post("http://127.0.0.1:8000/login", data=self.data)
        if req.status_code == 200:
            self.LOGGER.info("Authenication success!")
            token = req.json()
            self.headers = {"Authorization": f"Bearer {token['access_token']}"}
            self._is_logged_in = True
            return True
        else:
            return False

    def make_auth_call(self):
        "/document-scraped-data"
        req = requests.get(self.url + "/document-scraped-data", headers=self.headers)
        self.LOGGER.info(f"{req}")
        if req.status_code == 200:
            print(req.json())

    def start_scraper(self):
        req = requests.post(f"{self.url}/run-scraper-service", headers=self.headers)

        if req.status_code == 200:
            print(req.json())
