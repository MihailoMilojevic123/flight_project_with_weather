import os
from twilio.rest import Client
from dotenv import load_dotenv

class WhatsAppNotifier:
    def __init__(self):
        """Initialize Twilio WhatsApp client using environment variables."""
        load_dotenv()
        self.account_sid = os.getenv("TWILIO_SID")
        self.auth_token = os.getenv("TWILIO_AUTH")
        self.my_number = os.getenv("PHONE")
        self.client = Client(self.account_sid, self.auth_token)
        self.sender = "whatsapp:+14155238886"  # Twilio Sandbox number

    def send_message(self, message):
        """Send a WhatsApp message to the configured phone number."""
        try:
            msg = self.client.messages.create(
                from_=self.sender,
                to=f"whatsapp:{self.my_number}",
                body=message
            )
            print(f"✅ Message sent successfully! SID: {msg.sid}")
        except Exception as e:
            print(f"❌ Error sending WhatsApp message: {e}")
