import os
import requests
from dotenv import load_dotenv

# Load environment variables (API key)
load_dotenv()
API_KEY = os.getenv("WEATHER_API")


class Weather:
    """
    The Weather class handles fetching and evaluating weather data for a given location
    and time period using the Visual Crossing Weather API.
    """

    def __init__(self):
        # API endpoint for weather data
        self.weather_endpoint = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"
        self.api_key = API_KEY
        # Stores daily weather condition strings (e.g., "Partially cloudy", "Rain")
        self.weather_conditions = []

    def get_weather(self, location, date1, date2):
        """
        Fetches weather conditions between two dates for a given location.
        - location: latitude and longitude, e.g. "48.8566,2.3522"
        - date1: start date (YYYY-MM-DD)
        - date2: end date (YYYY-MM-DD)
        """
        self.weather_conditions = []

        params = {
            "key": API_KEY,
            "maxStations": 1,
            "unitGroup": "metric",
            "include": "days",
            "elements": "conditions"
        }

        response = requests.get(
            url=f"{self.weather_endpoint}/{location}/{date1}/{date2}",
            params=params
        )
        response.raise_for_status()
        data = response.json()

        # Extract weather condition (e.g. "Clear", "Rain", "Overcast") for each day
        for condition in data["days"]:
            self.weather_conditions.append(condition["conditions"])

    def calculate_score(self):
        """
        Calculates an average weather score based on the list of daily weather conditions.

        Scoring logic:
        - 5 → Excellent (clear/sunny)
        - 4 → Good (cloudy/overcast)
        - 3 → Neutral (unknown/other)
        - 2 → Poor (rain/snow/showers)
        - 1 → Bad (fog)
        - 0 → Very bad (thunder/storm)

        Returns:
            float: Average weather score (rounded to 2 decimals)
        """
        score_map = {
            "thunder": 0,
            "storm": 0,
            "snow": 2,
            "rain": 2,
            "showers": 2,
            "fog": 1,
            "clear": 5,
            "sunny": 5,
            "cloud": 4,
            "overcast": 4,
        }

        daily_scores = []

        for cond in self.weather_conditions:
            cond_lower = cond.lower()
            scores = []

            # Match words from score_map to weather condition
            for key, score in score_map.items():
                if key in cond_lower:
                    scores.append(score)

            # If no keyword matched, assign neutral score (3)
            if not scores:
                daily_scores.append(3)
            else:
                # Take the lowest score if multiple conditions (e.g., "Rain and Clouds")
                daily_scores.append(min(scores))

        # Calculate average score for the period
        return round(sum(daily_scores) / len(daily_scores), 2)







