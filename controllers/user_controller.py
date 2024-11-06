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

    def test_endpoint_get(self):
        req = requests.get(
            self.url + "/dashboards/attendance/",
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
    data = u.test_endpoint_get()

    df = pd.DataFrame(data)

    # Fill None values with an empty string for display
    df = df.fillna("")

    # Create a figure with a dark background
    fig, ax = plt.subplots(figsize=(12, len(df) * 0.6))  # Adjust height based on rows
    fig.patch.set_facecolor("#2e2e2e")  # Dark gray background color
    ax.axis("off")  # Hide the axes

    # Create the table with dark mode styling
    table = ax.table(
        cellText=df.values.tolist(),
        colLabels=df.columns.tolist(),
        cellLoc="center",
        loc="center",
    )

    # Set background color for table cells and headers
    for i in range(len(df) + 1):  # +1 to include header row
        for j in range(len(df.columns)):
            cell = table[i, j]
            cell.set_text_props(color="white")  # White text for dark mode
            if i == 0:  # Header row
                cell.set_facecolor("#404040")  # Darker background for header
            else:
                cell.set_facecolor("#333333")  # Slightly lighter for body rows

    # Adjust font size and make sure columns fit
    table.auto_set_font_size(False)
    table.set_fontsize(8)
    table.auto_set_column_width(col=list(range(len(df.columns))))

    # Save the figure as an image
    output_path = "dark_mode_employee_data_table.png"
    plt.savefig(
        output_path, bbox_inches="tight", dpi=150, facecolor=fig.get_facecolor()
    )  # Match figure background
    plt.show()
