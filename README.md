# flight_project_with_weather

## 🛫 About the Project
This project automatically searches for flights based on data from Google Sheets (city, IATA code, and price), checks the weather forecast for the travel dates, finds hotel offers, and sends a WhatsApp notification using Twilio.

I’m a beginner in Python — I’ve been learning on my own for about a month.  
I created this project to practice working with multiple APIs and automation logic.  
I would really appreciate any **feedback, suggestions, or criticism** that could help me learn and improve.  
**Thank you in advance! 🙏**

---

## ⚙️ How It Works
1. Reads flight data (city, IATA code, price) from **Google Sheets**  
2. Searches flights using the **Amadeus API**  
3. Checks 7-day weather forecasts via **Visual Crossing API**  
4. Finds hotel offers through **Amadeus Hotel API**  
5. Sends notifications via **Twilio WhatsApp**

---

## 🧠 Technologies Used
- `requests` – for making API calls  
- `twilio` – for WhatsApp notifications  
- `dotenv` – for managing API keys securely  
- `os`, `datetime`, `timedelta` – for environment and date handling  

---

## 📂 Project Structure
amadeus_flight_data.py  – fetches flight info  
weather_data.py         – gets weather forecast  
google_sheet_data.py    – reads data from Google Sheets  
hotel_data.py           – finds hotel offers  
notification.py         – sends WhatsApp message via Twilio  
main.py                 – combines all modules and runs the app  
.gitignore              – excludes sensitive files (.env, __pycache__, etc.)

---

## 🧾 Setup Instructions

### 1️⃣ Requirements
- Python 3.x  
- Accounts for:
  - [Amadeus API](https://developers.amadeus.com/)
  - [Visual Crossing Weather API](https://www.visualcrossing.com/weather-api)
  - [Twilio](https://www.twilio.com/)
  - [Sheety](https://sheety.co/) (for Google Sheets integration)

### 2️⃣ Clone and Install
```bash
git clone https://github.com/MihailoMilojevic123/flight_project_with_weather.git
cd flight_project_with_weather
pip install -r requirements.txt
```

### 3️⃣ Create `.env` File
```env
SHEETY_AUTH_TOKEN=your token
FLIGHT_DATA_KEY=your amadeus flight key
FLIGHT_DATA_SECRET=your amadeus flight secret
WEATHER_API=your weather api
HOTEL_KEY=your amadeus hotel key
HOTEL_SECRET=your amadeus hotel secret
TWILIO_SID=your twilio sid
TWILIO_AUTH=your twilio auth
PHONE=your phone number for twilio
```

### 4️⃣ Run the App
```bash
python main.py
```

---

## 💬 Example Output
🌤 Good destination found!

🏙 City: PAR
✈ Airport: CDG
💵 Flight Price: 97.94 EUR
📅 Dates: 2025-11-03 → 2025-11-10
💶 Hotel: BEST WESTERN JARDIN DE CLUNY
💵 Price: 1588.16 EUR
☀ Weather score: 3.88

Notification sent via WhatsApp ✅

---

## 📢 Notes
- `.env` file is ignored for security reasons.  
- All code is commented to explain how each part works.  
- This project is purely for learning and practice purposes.

---

## 👨‍💻 Author
**Mihailo Milojević**  
Beginner Python Developer  
[GitHub Profile](https://github.com/MihailoMilojevic123)

---

## 🪪 License
MIT License © 2025 Mihailo Milojević
