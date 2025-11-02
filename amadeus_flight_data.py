import os
from dotenv import load_dotenv
import requests
from datetime import datetime, timedelta
import time

# Load environment variables from .env file
load_dotenv()

# API credentials
FLIGHT_KEY = os.getenv("FLIGHT_DATA_KEY")
FLIGHT_SECRET = os.getenv("FLIGHT_DATA_SECRET")

# Amadeus API endpoints
IATA_ENDPOINT = "https://test.api.amadeus.com/v1/reference-data/locations/cities"
FLIGHT_SRC_END = "https://test.api.amadeus.com/v2/shopping/flight-offers"
ORIGIN_DESTINATION = "BEG"  # Origin airport (Belgrade)
LOCATION_END = "https://test.api.amadeus.com/v1/reference-data/locations"


class FlightData:
    """
    The FlightData class handles:
      - Authentication with the Amadeus API
      - Retrieving IATA codes for city names
      - Searching available flight offers
      - Fetching airport or city coordinates
    """

    def __init__(self):
        # Endpoint for authentication
        self.flight_post = "https://test.api.amadeus.com/v1/security/oauth2/token"

        # Headers and payload for token request
        self.auth_header = {"Content-Type": "application/x-www-form-urlencoded"}
        self.post_params = {
            "grant_type": "client_credentials",
            "client_id": FLIGHT_KEY,
            "client_secret": FLIGHT_SECRET
        }

        # Store token and date variables
        self.access_token = None
        self.today = datetime.now()
        self.tomorrow = self.today + timedelta(days=1)
        self.future = None

    def get_access_token(self):
        """
        Requests an access token from the Amadeus API.
        The token is stored in the instance to prevent multiple requests.
        """
        if self.access_token is not None:
            return self.access_token

        try:
            response = requests.post(
                url=self.flight_post,
                headers=self.auth_header,
                data=self.post_params
            )
            response.raise_for_status()
            self.access_token = response.json()["access_token"]
            return self.access_token
        except Exception as error:
            print(f"Token request failed: {error}")
            return None

    def get_iata_codes(self, city):
        """
        Returns the IATA code for a given city name.
        If the city is not found, returns None.
        """
        iata_params = {"keyword": city, "max": 1}
        auth_header = {"Authorization": f"Bearer {self.access_token}"}

        try:
            response = requests.get(url=IATA_ENDPOINT, params=iata_params, headers=auth_header)
            response.raise_for_status()
            data = response.json()

            if "data" in data and len(data["data"]) > 0:
                return data["data"][0].get("iataCode")
            else:
                return None
        except Exception as e:
            print(f"Error fetching IATA code for {city}: {e}")
            return None

    def search_for_flights(self, des_code, price, days):
        """
        Searches for available flights from Belgrade (BEG) to a destination city.
        - des_code: Destination IATA code
        - price: Maximum price limit
        - days: Number of days to search ahead from tomorrow

        Returns a list of flights with:
          - airport: destination airport code
          - departureDate: flight date
          - departureTime: time of departure
          - price: total price
          - cityCode: destination city code
        """
        self.future = self.today + timedelta(days=days)
        current_date = self.tomorrow
        about_flight = []

        while current_date < self.future:
            auth_header = {
                "accept": "application/vnd.amadeus+json",
                "Authorization": f"Bearer {self.access_token}"
            }
            params = {
                "originLocationCode": ORIGIN_DESTINATION,
                "destinationLocationCode": des_code,
                "departureDate": current_date.strftime("%Y-%m-%d"),
                "adults": 1,
                "maxPrice": price,
                "max": 1
            }

            try:
                response = requests.get(url=FLIGHT_SRC_END, headers=auth_header, params=params)
                response.raise_for_status()
                data = response.json()

                if data.get("data"):
                    flight = data["data"][0]
                    segments = flight["itineraries"][0]["segments"]

                    # Extract flight information
                    departure_at = segments[0]["departure"]["at"].split("T")
                    arrival_place = segments[-1]["arrival"]["iataCode"]
                    total_price = flight["price"]["grandTotal"]
                    city_code = des_code

                    about_flight.append({
                        "airport": arrival_place,
                        "departureDate": departure_at[0],
                        "departureTime": departure_at[1],
                        "price": total_price,
                        "cityCode": city_code
                    })

            except Exception as e:
                print(f"Error searching flights on {current_date}: {e}")

            # Move to the next day and avoid hitting the API too frequently
            current_date += timedelta(days=1)
            time.sleep(0.2)

        return about_flight

    def get_coordinate(self, airport):
        """
        Retrieves coordinates (latitude/longitude) for a specific airport or city.
        """
        auth_header = {"Authorization": f"Bearer {self.access_token}"}
        params = {"subType": "AIRPORT,CITY", "keyword": airport}

        try:
            response = requests.get(url=LOCATION_END, headers=auth_header, params=params)
            response.raise_for_status()
            data = response.json()
            return data
        except Exception as e:
            print(f"Error fetching coordinates for {airport}: {e}")
            return None











