import requests
import telebot
from keys import tg_bot_token , news_api

bot = telebot.TeleBot(tg_bot_token)

def get_news_by_keyword(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&apiKey={news_api}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    return articles[:5]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "Hello, I am News Telegram Bot.")

@bot.message_handler(commands=['search'])
def search_news(message):
    bot.reply_to(message,"Type keyword for search:")

@bot.message_handler(func=lambda message: True)
def process_search(message):
    keyword = message.text
    user_id = message.chat.id

    articles = get_news_by_keyword(keyword)

    if articles:
        for article in articles:
            title = article.get("title", "")
            description = article.get("description", "")
            url = article.get("url", "")
            news_text = f"{title}\n\n{description}\n\n{url}"
            bot.send_message(user_id, news_text)
    else:
        bot.send_message(user_id, "I\'m sorry. For your search we can\'t find news.")


bot.polling()