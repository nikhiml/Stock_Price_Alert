import requests
from twilio.rest import Client
ACCOUNT_SID = 'ACf3edb3f928face31f32db8d81f6a319c'
AUTH_TOKEN = '04bed3ffc85be164e7f9c60c406521db'


STOCK = "TSLA"
COMPANY_NAME = "Tesla"

## STEP 1: Use https://www.alphavantage.co to check the movement in stock price


alpha_api_key = '*************'
news_api_key = '*******************'

parameters = {
    'function': 'TIME_SERIES_DAILY',
    'symbol': STOCK,
    'apikey': alpha_api_key
}

news_parameters = {
    'q': 'Tesla',
    'searchIn': 'title',
    'from': '2022-05-06',
    'sortBy': 'popularity',
    'apiKey': news_api_key
}

stock_data = requests.get("https://www.alphavantage.co/query", params=parameters)
tesla_data = stock_data.json()

tesla_close_values = [tesla_data['Time Series (Daily)'][n]['4. close'] for n in tesla_data['Time Series (Daily)']]

tesla_two_values = tesla_close_values[:2]


# STEP 2: If the stock price movement is more than 5%,
# then use https://newsapi.org to get top 3 news articles in the past 24 hours and sms to the customer using Twilio

diff_percent = 100 * ((float(tesla_two_values[0]) - float(tesla_two_values[1]))/float(tesla_two_values[1]))

tesla_news_string = ''
tesla_complete_news = ''

if abs(diff_percent) > .05:
    news_data = requests.get("https://newsapi.org/v2/everything", news_parameters)
    tesla_news = news_data.json()
    tesla_news_articles_title = [tesla_news['articles'][n]['title'] for n in range(3)]
    tesla_news_articles_des = [tesla_news['articles'][n]['description'] for n in range(3)]
    for n in range(3):
        tesla_complete_news = 'Headline: ' + tesla_news_articles_title[n] + '\n' + 'Brief: ' + tesla_news_articles_des[n]
        tesla_news_string += tesla_complete_news + '\n'
    # print(tesla_news_string)

    client = Client(ACCOUNT_SID, AUTH_TOKEN)
    if diff_percent > 0:
        flag = '🔺'
    else:
        flag = '🔻'

    message = client.messages.create(body=f"{STOCK}: {flag}{round(diff_percent,2)}% {tesla_news_string}",
                                              from_='+17473000192', to='*************')
    print(message.status)

