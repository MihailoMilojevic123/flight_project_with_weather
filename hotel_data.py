import os
from dotenv import load_dotenv
import requests

# Load environment variables (API credentials)
load_dotenv()

HOTEL_KEY = os.getenv("HOTEL_KEY")
HOTEL_SECRET = os.getenv("HOTEL_SECRET")

# Amadeus API endpoints
HOTEL_END = "https://test.api.amadeus.com/v1/reference-data/locations/hotels/by-city"
OFFER_END = "https://test.api.amadeus.com/v3/shopping/hotel-offers"


class Hotel:
    """
    Handles fetching hotel data and available offers using the Amadeus API.
    """

    def __init__(self):
        # Endpoint for getting an access token
        self.hotel_post = "https://test.api.amadeus.com/v1/security/oauth2/token"

        # Required headers and parameters for authentication
        self.auth_header = {
            "Content-Type": "application/x-www-form-urlencoded"
        }
        self.auth_params = {
            "grant_type": "client_credentials",
            "client_id": HOTEL_KEY,
            "client_secret": HOTEL_SECRET
        }

        # Access token will be stored here once retrieved
        self.access_token = None

    def hotel_acc_token(self):
        """
        Retrieves the access token from the Amadeus API.
        If the token already exists, it will reuse the stored one.
        """
        if self.access_token is not None:
            return self.access_token

        try:
            response = requests.post(
                url=self.hotel_post,
                headers=self.auth_header,
                data=self.auth_params
            )
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            return self.access_token
        except Exception as error:
            print(f"Token request failed: {error}")
            return None

    def hotel_list(self, code):
        """
        Fetches a list of hotels in a given city based on its IATA code.

        Args:
            code (str): City IATA code (e.g., 'PAR' for Paris)

        Returns:
            list: A list of up to 10 hotels found in that city.
        """
        params = {
            "cityCode": code,
            "radius": 2,
            "ratings": "3"  # Example: get 3-star hotels
        }

        auth_header = {
            "Authorization": f"Bearer {self.access_token}"
        }

        response = requests.get(url=HOTEL_END, headers=auth_header, params=params)
        response.raise_for_status()
        data = response.json()

        # Return only the first 10 hotels to limit API usage
        first_10 = data["data"][:10]
        return first_10

    def offers(self, hotel_id, check_in, check_out):
        """
        Retrieves hotel offers (room prices and availability) for given dates.

        Args:
            hotel_id (str): Unique hotel ID from Amadeus.
            check_in (str): Check-in date (YYYY-MM-DD)
            check_out (str): Check-out date (YYYY-MM-DD)

        Returns:
            dict | None: JSON response with offer details or None if request fails.
        """
        params = {
            "hotelIds": [hotel_id],
            "checkInDate": check_in,
            "checkOutDate": check_out,
            "currency": "EUR"
        }

        auth_header = {
            "Authorization": f"Bearer {self.access_token}"
        }

        try:
            response = requests.get(url=OFFER_END, headers=auth_header, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except requests.exceptions.HTTPError:
            # Some hotels may not have available offers — return None to skip them
            return None



