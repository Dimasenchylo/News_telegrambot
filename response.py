import requests
from keys import news_api

def get_response(search, reqwest=''):
    if search=='everything':
        url = f"https://newsapi.org/v2/everything?q={reqwest}&language=en&apiKey={news_api}"
    elif search=='category':
        url = f"https://newsapi.org/v2/top-headlines?category={reqwest}&country=us&apiKey={news_api}"
    else:
        url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    return articles