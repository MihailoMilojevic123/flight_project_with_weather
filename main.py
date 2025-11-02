# --- Importing modules ---
from google_sheet_data import SheetData
from amadeus_flight_data import FlightData
from weather_data import Weather
from datetime import timedelta, datetime
from hotel_data import Hotel
from notification import WhatsAppNotifier

# --- Initialize Google Sheet ---
# Used to read city names and flight prices, and later write IATA codes.
data = SheetData()
sheet_data = data.get_data()

# Extracting data from Google Sheet
city_names = [item['city'].upper() for item in sheet_data['flights']]  # City names for IATA code search
item_id = [item['id'] for item in sheet_data['flights']]               # Row IDs for updating the sheet
prices = [item['price'] for item in sheet_data['flights']]             # Flight price limits for each city


# --- Initialize all classes (API handlers) ---
flight_data = FlightData()
flight_data.get_access_token()  # Get Amadeus API access token
iata_codes = []
weather = Weather()
hotel = Hotel()
hotel.hotel_acc_token()  # Get Amadeus Hotel API access token
whatsapp = WhatsAppNotifier()  # Initialize WhatsApp notifier


# --- Get IATA codes for all cities from Google Sheet ---
for item in city_names:
    iata_codes.append(flight_data.get_iata_codes(item))

# Optional: update Google Sheet with IATA codes (I already did that.)
# for i in range(len(item_id)):
#     data.edit_rows(row_id=item_id[i], code=iata_codes[i])


# --- Main loop: process each destination ---
for i in range(len(iata_codes)):
    code = iata_codes[i]
    max_price = prices[i]  # take corresponding price limit for each destination

    # Search for flights for this destination with its specific price limit
    flights = flight_data.search_for_flights(des_code=code, price=max_price, days=7)

    if not flights:
        print(f"There are no flights for {code}")
        continue

    # Process each found flight
    for flight in flights:
        airport = flight["airport"]
        departure_date = datetime.strptime(flight["departureDate"], "%Y-%m-%d")
        start_date = departure_date.strftime("%Y-%m-%d")
        end_date = (departure_date + timedelta(days=7)).strftime("%Y-%m-%d")

        # --- Get geographic coordinates for weather data ---
        location_data = flight_data.get_coordinate(airport=airport)
        geo_location = f'{location_data["data"][0]["geoCode"]["latitude"]},{location_data["data"][0]["geoCode"]["longitude"]}'

        # --- Get weather and calculate score ---
        weather.weather_conditions = []
        weather.get_weather(location=geo_location, date1=start_date, date2=end_date)
        score = weather.calculate_score()
        print(f"\n✈️ Flight: {flight['cityCode']} | Weather score: {score}")

        # --- If weather is good, search for hotels ---
        if score >= 3.5:
            hotel_list = hotel.hotel_list(flight["cityCode"])
            found_offer = False

            for h in hotel_list:
                hotel_id = h["hotelId"]
                offer = hotel.offers(hotel_id=hotel_id, check_in=start_date, check_out=end_date)

                # If offer exists
                if offer and "data" in offer and len(offer["data"]) > 0:
                    hotel_data = offer["data"][0]
                    hotel_offers = hotel_data.get("offers", [])

                    if hotel_offers:
                        first_offer = hotel_offers[0]
                        price_info = first_offer.get("price", {})

                        # Extract all relevant data
                        total_price = price_info.get("total", "N/A")
                        currency = price_info.get("currency", "EUR")
                        check_in_date = first_offer.get("checkInDate", start_date)
                        check_out_date = first_offer.get("checkOutDate", end_date)
                        name = h.get("name", "Unknown hotel name")

                        print(f"✅ Pronađena ponuda za hotel: {name} ({hotel_id})")

                        # --- Format WhatsApp message ---
                        message = (
                            f"🌤️ *Good destination found!*\n\n"
                            f"🏙️ City: *{flight['cityCode']}*\n"
                            f"✈️ Airport: *{flight['airport']}*\n"
                            f"💵 Flight Price: *{flight['price']} EUR*\n"
                            f"📅 Dates: {check_in_date} → {check_out_date}\n"
                            f"💶 Hotel: *{name}*\n"
                            f"💵 Price: {total_price} {currency}\n"
                            f"☀️ Weather score: *{score}*\n"
                        )

                        # --- Send WhatsApp message ---
                        whatsapp.send_message(message)

                        found_offer = True
                        break  # Stop after first valid hotel offer

            # If no hotels found
            if not found_offer:
                print("❌ No available offers from hotels.")

        # --- If weather is bad, skip destination ---
        else:
            print("🌧️ Bad weather – skip this destination.")











