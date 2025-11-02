import os
from dotenv import load_dotenv
import requests


# --- Load environment variables from .env file ---
# Used to hide sensitive tokens (Sheety API key)
load_dotenv()
SHEETY_TOKEN = os.getenv("SHEETY_AUTH_TOKEN")


class SheetData:
    """
    This class handles all communication with the Google Sheet
    via the Sheety API (GET and PUT requests).
    """

    def __init__(self):
        # Base URLs for Sheety API (GET all data and PUT updates)
        self.sheety_get = "https://api.sheety.co/f0b69fa7d9efb2deda9d82ae8625e7d6/flights/flights"
        self.sheety_put = "https://api.sheety.co/f0b69fa7d9efb2deda9d82ae8625e7d6/flights/flights/"

        # Authorization header for Sheety API
        self.auth_header = {
            "Authorization": f"Bearer {SHEETY_TOKEN}"
        }

    def get_data(self):
        """
        Fetches all flight data from the Google Sheet via Sheety API.
        Returns the data as a JSON object.
        """
        response = requests.get(url=self.sheety_get, headers=self.auth_header)
        response.raise_for_status()
        data = response.json()
        return data

    def edit_rows(self, row_id, code):
        """
        Updates a specific row in Google Sheet (by ID) with a new IATA code.
        :param row_id: Row ID in the Google Sheet
        :param code: IATA code for the corresponding city
        """
        params = {
            "flight": {
                "iataCode": code
            }
        }
        response = requests.put(url=f"{self.sheety_put}{row_id}", json=params, headers=self.auth_header)
        response.raise_for_status()



