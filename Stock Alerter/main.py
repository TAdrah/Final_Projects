import requests
import datetime
from twilio.rest import Client

account_sid = "AC49110fd25d034a5d5ef7359ef62b4b95"
auth_token = "4eb361f77f58b17ce7277371bae1e06b"
client = Client(account_sid, auth_token)

STOCK_NAME = "TSLA"
COMPANY_NAME = "Tesla Inc"
STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"
ALPHA_KEY = "PPD85BO6E2QFIH5D"
NEWS_KEY = "b8cf107f3c344697bd2569985bb02e4f"

    ## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
today = datetime.datetime.today()
temp_yesterday = today - datetime.timedelta(days=1)
yesterday = str(temp_yesterday)[0:10] + " 13:00:00"


url = f'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol={STOCK_NAME}&interval=30min&apikey={ALPHA_KEY}'
r = requests.get(url)
data = r.json()


#TODO 1. - Get yesterday's closing stock price. Hint: You can perform list comprehensions on Python dictionaries. e.g. [new_value for (key, value) in dictionary.items()]
temp_yesterdays_closing_price = [data["Time Series (30min)"][yesterday]["4. close"] for (key, value) in data.items()]
yesterday_closing_price = float(temp_yesterdays_closing_price[0:9][0])
print(yesterday_closing_price)


#TODO 2. - Get the day before yesterday's closing stock price
temp_before_yesterday = (temp_yesterday - datetime.timedelta(days=1))
before_yesterday = str(temp_before_yesterday)[0:10] + " 13:00:00"


temp_before_yesterdays_closing_price = [data["Time Series (30min)"][before_yesterday]["4. close"] for (key, value) in data.items()]
before_yesterday_closing_price = float(temp_before_yesterdays_closing_price[0:9][0])
print(before_yesterday_closing_price)

#TODO 3. - Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
delta = abs(yesterday_closing_price - before_yesterday_closing_price)
print(round(delta, 3))

#TODO 4. - Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
percent = (delta / (yesterday_closing_price + before_yesterday_closing_price/2)) * 100
print(percent)

#TODO 5. - If TODO4 percentage is greater than 5 then print("Get News").
if percent > 5:
    print("get news")


# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

#TODO 6. - Instead of printing ("Get News"), use the News API to get articles related to the COMPANY_NAME.
    url = f"{NEWS_ENDPOINT}?q={COMPANY_NAME}&apiKey={NEWS_KEY}"
    r = requests.get(url)
    news_data = r.json()
    top_3_news = news_data["articles"][:3]


#TODO 7. - Use Python slice operator to create a list that contains the first 3 articles. Hint: https://stackoverflow.com/questions/509211/understanding-slice-notation
#    print(top_3_news)

    ## STEP 3: Use twilio.com/docs/sms/quickstart/python
    #to send a separate message with each article's title and description to your phone number. 

#TODO 8. - Create a new list of the first 3 article's headline and description using list comprehension.
    top_3_data = [(top_3_news[0]["title"], top_3_news[0]["content"]) for item in top_3_news]



#TODO 9. - Send each article as a separate message via Twilio.

    for i in top_3_data:
        message = client.messages \
            .create(
            body=f"Title: {i[0][0]} \nContent: {i[0][1]}",
            from_="+18559106714",
            to="INSERT NUMBER HERE as +1xxxxxxxxxx"
    )


#Optional TODO: Format the message like this: 
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""

