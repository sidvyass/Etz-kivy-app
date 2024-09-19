import requests


class UserAPI:
    def __init__(self, username, password):
        self.url = "http://127.0.0.1:8000"
        self.data = {
            "username": username,
            "password": password,
        }
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
        req = requests.get("http://127.0.0.1:8000/")
        if req.status_code == 200:
            return True

    def make_auth_call(self):
        """For testing authentication system"""
        req = requests.get(self.url + "/document-scraped-data", headers=self.headers)
        if req.status_code == 200:
            print(req.json())
