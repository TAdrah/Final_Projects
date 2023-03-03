import requests
import datetime
from twilio.rest import Client
import os

account_sid = os.environ.get("account_sid")
auth_token = os.environ.get("auth_token")
client = Client(account_sid, auth_token)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
ALPHA_KEY = os.environ.get("alpha_key")
NEWS_KEY = os.environ.get("news_key")
TWILIO_VIRTUAL_NUMBER = os.environ.get("v_number")
MY_NUMBER = os.environ.get("my_number")


today = datetime.datetime.today()
temp_yesterday = today - datetime.timedelta(days=1)
yesterday = str(temp_yesterday)[0:10] + " 13:00:00"

url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_NAME}&interval=30min&apikey={ALPHA_KEY}'
r = requests.get(url)
data = r.json()

# Get yesterday's closing stock price
temp_yesterdays_closing_price = [data["Time Series (30min)"][yesterday]["4. close"] for (key, value) in data.items()]
yesterday_closing_price = float(temp_yesterdays_closing_price[0:9][0])
print(yesterday_closing_price)

# Get day before yesterday's closing stock price
temp_before_yesterday = (temp_yesterday - datetime.timedelta(days=1))
before_yesterday = str(temp_before_yesterday)[0:10] + " 13:00:00"
temp_before_yesterdays_closing_price = [data["Time Series (30min)"][before_yesterday]["4. close"] for (key, value) in
                                        data.items()]
before_yesterday_closing_price = float(temp_before_yesterdays_closing_price[0:9][0])
print(before_yesterday_closing_price)

# get absolute difference & % between yesterday & before yesterday prices
delta = abs(yesterday_closing_price - before_yesterday_closing_price)
print(round(delta, 3))

percent = (delta / (yesterday_closing_price + before_yesterday_closing_price / 2)) * 100
print(percent)

# get the first 3 news pieces for the company name if theres a greater than 5 % diff
if percent > 5:
    url = f"{NEWS_ENDPOINT}?q={COMPANY_NAME}&apiKey={NEWS_KEY}"
    r = requests.get(url)
    news_data = r.json()
    top_3_news = news_data["articles"][:3]
    top_3_data = [(top_3_news[0]["title"], top_3_news[0]["content"]) for item in top_3_news]

    for i in top_3_data:
        message = client.messages \
            .create(
            body=f"Title: {i[0][0]} \nContent: {i[0][1]}",
            from_=TWILIO_VIRTUAL_NUMBER,
            to= MY_NUMBER,
        )
