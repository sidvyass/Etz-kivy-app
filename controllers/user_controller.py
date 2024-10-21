import requests
import urllib.parse
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
            return False

    def test_endpoint_get(self, url_val):
        req = requests.get(
            self.url + url_val,
            headers=self.headers,
        )
        response = json.dumps(req.json(), indent=3)
        print(response)

    def test_endpoint_post(self, url_val):
        req = requests.post(
            self.url + f"{url_val}",
            headers=self.headers,
        )
        response = json.dumps(req.json(), indent=3)
        print(response)


if __name__ == "__main__":
    u = UserAPI("60009", "67220")
    u.login()
    u.test_endpoint_get("/document-scraped-data")
