from twilio.rest import Client
import os
import smtplib

TWILIO_SID = os.environ.get("ACCOUNT_SID")
TWILIO_AUTH_TOKEN = os.environ.get("TWILIO_TOKEN")
TWILIO_VIRTUAL_NUMBER = os.environ.get("VIRTUAL_NUMBER")
TWILIO_VERIFIED_NUMBER = os.environ.get("VERIFIED_NUMBER")
client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

SMTP_ADDRESS = os.environ.get("MAIL_PROVIDER_SMTP_ADDRESS")
MY_EMAIL = os.environ.get("MY_EMAIL")
MY_PASSWORD = os.environ.get("MY_PASSWORD")


class NotificationManager:

    def __init__(self):
        self.client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)

    def send_sms(self, numbers, message):
        for number in numbers:
            message = self.client.messages.create(
                body=message,
                from_=TWILIO_VIRTUAL_NUMBER,
                to=f"+1{number}",
            )
        print(message.sid)

    def send_emails(self, emails, message, google_flight_link):
        with smtplib.SMTP(SMTP_ADDRESS, port=587) as connection:
            connection.starttls()
            connection.login(MY_EMAIL, MY_PASSWORD)
            for email in emails:
                connection.sendmail(
                    from_addr=MY_EMAIL,
                    to_addrs=email,
                    msg=f"Subject:New Low Price Flight!\n\n{message}\n{google_flight_link}".encode('utf-8')
                )
