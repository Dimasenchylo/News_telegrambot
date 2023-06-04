import requests
import telebot
from telebot import types
from keys import tg_bot_token, news_api

bot = telebot.TeleBot(tg_bot_token)
def get_news_by_keyword(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&apiKey={news_api}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    return articles[:5]

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"Hello, I am News Telegram Bot.")

user_states = {}

@bot.message_handler(commands=['search'])
def search_news(message):
    user_id = message.chat.id
    user_states[user_id] = 'search'
    bot.reply_to(message, "Type keyword for search:")

@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'search')
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

@bot.message_handler(commands=['topnews'])
def top_news(message):
    user_id = message.chat.id
    articles = get_top_news()
    user_states[user_id] = {'news': articles, 'index': 0}
    send_next_news(user_id)

@bot.callback_query_handler(func=lambda call: call.data == 'next_news')
def next_news_callback(call):
    user_id = call.from_user.id
    send_next_news(user_id)

def send_next_news(user_id):
    state = user_states.get(user_id)
    if not state:
        return

    news = state['news']
    index = state['index']

    for i in range(index, index + 3):
        if i >= len(news):
            break

        article = news[i]
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")
        news_text = f"{title}\n\n{description}\n\n {url}"
        bot.send_message(user_id, news_text)

    state['index'] = index + 3

    if state['index'] < len(news):
        keyboard = types.InlineKeyboardMarkup()
        next_button = types.InlineKeyboardButton("Next", callback_data='next_news')
        keyboard.add(next_button)
        bot.send_message(user_id, "Press button \"Next\", for more news.", reply_markup=keyboard)
    else:
        bot.send_message(user_id, "Thats all news for now.")

def get_top_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    return articles[:60]

def main():
    bot.polling()

if __name__ == "__main__":
    main()