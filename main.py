import threading
import requests
import telebot
from telebot import types
from keys import tg_bot_token, news_api
import time

bot = telebot.TeleBot(tg_bot_token)
def get_news_by_keyword(keyword):
    url = f"https://newsapi.org/v2/everything?q={keyword}&language=en&apiKey={news_api}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    return articles[:5]


def send_news(user_id, articles):
    for article in articles:
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")
        news_text = f" {title}\n\n{description}\n\n {url}"
        bot.send_message(user_id, news_text)


@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"Hello, I am News Telegram Bot.")

user_states = {}
user_subscriptions = {}

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
        send_news(user_id, articles)
    else:
        bot.send_message(user_id, "I'm sorry. For your search we can't find news.")

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
        bot.send_message(user_id, "That's all news for now.")

def get_top_news():
    url = f"https://newsapi.org/v2/top-headlines?country=us&apiKey={news_api}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    return articles[:60]


@bot.message_handler(commands=['categories'])
def categories(message):
    user_id = message.chat.id
    user_states[user_id] = 'categories'
    keyboard = types.InlineKeyboardMarkup()
    business_button = types.InlineKeyboardButton("Business", callback_data='business')
    entertainment_button = types.InlineKeyboardButton("Entertainment", callback_data='entertainment')
    health_button = types.InlineKeyboardButton("Health", callback_data='health')
    science_button = types.InlineKeyboardButton("Science", callback_data='science')
    sports_button = types.InlineKeyboardButton("Sports", callback_data='sports')
    technology_button = types.InlineKeyboardButton("Technology", callback_data='technology')
    keyboard.row(business_button, entertainment_button)
    keyboard.row(health_button, science_button)
    keyboard.row(sports_button, technology_button)
    bot.reply_to(message, "Choose a category:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data in ['business', 'entertainment', 'health', 'science', 'sports', 'technology'])
def category_callback(call):
    user_id = call.from_user.id
    category = call.data
    articles = get_news_by_category(category)
    user_states[user_id] = {'news': articles, 'index': 0}
    send_next_news(user_id)


def get_news_by_category(category):
    url = f"https://newsapi.org/v2/top-headlines?category={category}&country=us&apiKey={news_api}"
    response = requests.get(url)
    news_data = response.json()
    articles = news_data.get("articles", [])
    return articles[:60]


@bot.message_handler(commands=['subscribe'])
def subscribe(message):
    user_id = message.chat.id
    user_states[user_id] = 'subscribe'
    keyboard = types.InlineKeyboardMarkup()
    business_button = types.InlineKeyboardButton("Business", callback_data='subscribe_business')
    entertainment_button = types.InlineKeyboardButton("Entertainment", callback_data='subscribe_entertainment')
    health_button = types.InlineKeyboardButton("Health", callback_data='subscribe_health')
    science_button = types.InlineKeyboardButton("Science", callback_data='subscribe_science')
    sports_button = types.InlineKeyboardButton("Sports", callback_data='subscribe_sports')
    technology_button = types.InlineKeyboardButton("Technology", callback_data='subscribe_technology')
    keyboard.row(business_button, entertainment_button)
    keyboard.row(health_button, science_button)
    keyboard.row(sports_button, technology_button)
    bot.reply_to(message, "Choose a category to subscribe:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('subscribe_'))
def subscribe_callback(call):
    user_id = call.from_user.id
    category = call.data.split('_')[1]
    subscribe_category(user_id, category)
    bot.send_message(user_id, f"You have subscribed to the {category} category.")


def subscribe_category(user_id, category):
    if user_id not in user_subscriptions:
        user_subscriptions[user_id] = []

    if category not in user_subscriptions[user_id]:
        user_subscriptions[user_id].append(category)


@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    user_id = message.chat.id
    user_states[user_id] = 'unsubscribe'
    keyboard = types.InlineKeyboardMarkup()
    subscriptions = user_subscriptions.get(user_id, [])
    for category in subscriptions:
        keyboard.add(types.InlineKeyboardButton(category.capitalize(), callback_data=f'unsubscribe_{category}'))
    bot.reply_to(message, "Choose a category to unsubscribe:", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: call.data.startswith('unsubscribe_'))
def unsubscribe_callback(call):
    user_id = call.from_user.id
    category = call.data.split('_')[1]
    unsubscribe_category(user_id, category)
    bot.send_message(user_id, f"You have unsubscribed from the {category} category.")


def unsubscribe_category(user_id, category):
    if user_id in user_subscriptions and category in user_subscriptions[user_id]:
        user_subscriptions[user_id].remove(category)


@bot.message_handler(commands=['subscriptions'])
def list_subscriptions(message):
    user_id = message.chat.id
    subscriptions = user_subscriptions.get(user_id, [])
    if subscriptions:
        categories = ', '.join(subscriptions)
        bot.send_message(user_id, f"You are subscribed to the following categories: {categories}")
    else:
        bot.send_message(user_id, "You are not subscribed to any categories.")


def send_subscribed_news():
    while True:
        for user_id, categories in user_subscriptions.items():
            for category in categories:
                articles = get_news_by_category(category)
                if articles:
                    send_news(user_id, articles)
        time.sleep(3600)


if __name__ == '__main__':
    bot.polling()
    threading.Thread(target=send_subscribed_news).start()