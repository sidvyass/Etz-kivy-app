import matplotlib.pyplot as plt
import pandas as pd
from collections import Counter
import requests
import urllib.parse
import os
import json


# TODO: need to display bad server error to the user.
# Have some way to estabilish a connection and then start the app.


class UserAPI:
    def __init__(self, username, password):
        self.url = "http://127.0.0.1:8000"
        self.data = {
            "username": str(username),
            "password": str(password),
        }
        self.login()
        self._is_logged_in = False

    def __repr__(self) -> str:
        return self.data["username"]

    def login(self):
        req = requests.post("http://127.0.0.1:8000/login", data=self.data)
        if req.status_code == 200:
            token = req.json()
            self.headers = {"Authorization": f"Bearer {token['access_token']}"}
            self._is_logged_in = True
            return True
        else:
            return False  # NOTE: DO NOT CHANGE

    def test_endpoint_get(self, url):
        print(self.url + url)
        req = requests.get(
            self.url + url,
            headers=self.headers,
        )
        response = json.dumps(req.json(), indent=3)
        print(response)

        return req.json()

    def test_endpoint_post(self, file_path):
        print(f"{self.url}/document-scraped-data/upload_file")
        with open(file_path, "rb") as file:
            files = {"file": (os.path.basename(file_path), file)}
            response = requests.post(
                f"{self.url}/document-scraped-data/upload_file",
                files=files,
                headers=self.headers,
            )
            print(response.json())
            if response.status_code == 200:
                print("success")


if __name__ == "__main__":
    u = UserAPI("60009", "67220")
    u.login()
    u.test_endpoint_get("/get_all_party_email_ids")
