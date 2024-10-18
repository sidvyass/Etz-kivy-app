import requests
import urllib.parse


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

    def dummy_call(self):
        """For testing async"""
        req = requests.post(
            "http://127.0.0.1:8000/get_items_from_rfq",
            json={"rfq_num": "5052"},
            headers=self.headers,
        )

        print(req.json())

    def make_auth_call(self):
        """For testing authentication system"""
        req = requests.get(self.url + "/document-scraped-data", headers=self.headers)
        if req.status_code == 200:
            print(req.json())

    def test_endpoint(self, key):
        encoded_key = urllib.parse.quote(key)
        req = requests.put(
            self.url + f"/document-scraped-data/approve/{encoded_key}",
            headers=self.headers,
        )
        print(req.json())


if __name__ == "__main__":
    u = UserAPI("60009", "67220")
    u.login()
    u.test_endpoint("PO_4502305447_CN#0001_10-15-2024.rtf")
