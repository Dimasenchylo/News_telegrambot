from database import crsr_mysql, conn
from response import get_response
from keys import tg_bot_token
from telebot import types
import threading
import schedule
import telebot
import random
import time


# Current command to procces
user_states = {}
# Current user subscriptions
user_subscriptions = {}

# Define bot
bot = telebot.TeleBot(tg_bot_token)

# Command /start
@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message,"Hello, I am News Telegram Bot.")

# Command /search
@bot.message_handler(commands=['search'])
def search_news(message):
    user_id = message.chat.id
    user_states[user_id] = 'search'
    bot.reply_to(message, "Type keyword for search:")

# Search for news 
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'search')
def search_process(message):
    reqwest = message.text
    user_id = message.chat.id
    articles = get_response('everything', reqwest)
    # If news was found 
    if articles:
        send_next_news(user_id, articles)
        user_states[user_id] = None
    else:
        bot.send_message(user_id, "I'm sorry. For your search we can't find news.")

# Send news to user
def send_news(user_id, articles, max_articles=5):
    for i, article in enumerate(articles[:max_articles], start=1):
        title = article.get("title", "")
        description = article.get("description", "")
        url = article.get("url", "")
        news_text = f" {title}\n\n{description}\n\n {url}"
        bot.send_message(user_id, news_text)

# Check what send to user
def send_next_news(user_id, articles, ifbutton=True):
    # If news need next button
    if ifbutton==True:
        max_articles = 3
        index = 0
        send_news(user_id, articles, max_articles)
        insert_advert(user_id)
        if index < len(articles):
            # Next news button
            keyboard = types.InlineKeyboardMarkup()
            next_button = types.InlineKeyboardButton("Next", callback_data='next_news')
            keyboard.add(next_button)
            bot.send_message(user_id, "Press button \"Next\", for more news.", reply_markup=keyboard)
            index += 3
        else:
            bot.send_message(user_id, "That's all news for now.")
            index = 0
    else:
        max_articles = 5
        send_news(user_id, articles, max_articles)

# Command /topnews
@bot.message_handler(commands=['topnews'])
def top_news(message):
    user_id = message.chat.id
    articles = get_response('nocategory')
    send_next_news(user_id, articles)

# If button next news pressed
@bot.callback_query_handler(func=lambda call: call.data == 'next_news')
def top_news_callback(call):
    user_id = call.from_user.id
    articles = get_response('nocategory')
    send_next_news(user_id, articles)

# Command /categories
@bot.message_handler(commands=['categories'])
def categories(message):
    # Print set of buttons to show categories
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

# For each category send news
@bot.callback_query_handler(func=lambda call: call.data in ['business', 'entertainment', 'health', 'science', 'sports', 'technology'])
def category_callback(call):
    user_id = call.from_user.id
    category = call.data
    articles = get_response('category', category)
    send_next_news(user_id, articles)

# Command /subscribe
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

# Send feedback about subscribed category
@bot.callback_query_handler(func=lambda call: call.data.startswith('subscribe'))
def subscribe_callback(call):
    user_id = call.from_user.id
    category = call.data.split('_')[1]
    subscribe_category(user_id, category)
    bot.send_message(user_id, f"You have subscribed to the {category} category.")

# Subscribe to pressed category
def subscribe_category(user_id, category):
    if user_id not in user_subscriptions:
        user_subscriptions[user_id] = []

    if category not in user_subscriptions[user_id]:
        user_subscriptions[user_id].append(category)

# Command /unsubscribe
@bot.message_handler(commands=['unsubscribe'])
def unsubscribe(message):
    user_id = message.chat.id
    user_states[user_id] = 'unsubscribe'
    keyboard = types.InlineKeyboardMarkup()
    subscriptions = user_subscriptions.get(user_id, [])
    for category in subscriptions:
        keyboard.add(types.InlineKeyboardButton(category.capitalize(), callback_data=f'unsubscribe_{category}'))
    bot.reply_to(message, "Choose a category to unsubscribe:", reply_markup=keyboard)

# Send feedback to user about unsubscribes 
@bot.callback_query_handler(func=lambda call: call.data.startswith('unsubscribe'))
def unsubscribe_callback(call):
    user_id = call.from_user.id
    category = call.data.split('_')[1]
    unsubscribe_category(user_id, category)
    bot.send_message(user_id, f"You have unsubscribed from the {category} category.")

# Delede user from subscribed category
def unsubscribe_category(user_id, category):
    if user_id in user_subscriptions and category in user_subscriptions[user_id]:
        user_subscriptions[user_id].remove(category)

# Command /subscribes
@bot.message_handler(commands=['subscribes'])
def list_subscriptions(message):
    user_id = message.chat.id
    subscriptions = user_subscriptions.get(user_id, [])
    if subscriptions:
        categories = ', '.join(subscriptions)
        bot.send_message(user_id, f"You are subscribed to the following categories: {categories}")
    else:
        bot.send_message(user_id, "You are not subscribed to any categories.")

# Send subscribed news onse per day 
def send_subscribed_news():
    for user_id, categories in user_subscriptions.items():
        for category in categories:
            articles = get_response('category', category)
            if articles:
                send_next_news(user_id, articles, False)

# Check for exact time every second
def schedule_loop():
    while True:
        schedule.run_pending()
        time.sleep(1)

# Command /advertisement
@bot.message_handler(commands=['advertisement'])
def search_news(message):
    user_id = message.chat.id
    user_states[user_id] = 'advertisement'
    bot.reply_to(message, "Type your add: title description url")

# Add user advertisement to database
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'advertisement')
def add(message):
    list_of_words = message.text.split(" ")
    user_id = message.chat.id
    if list(list_of_words) != 3:
        text = "Something went wrong, please try again"
        bot.send_message(user_id, text, parse_mode='html')
    else:
        print (list_of_words)
        title = list_of_words[0]
        desqr = list_of_words[1]
        url = list_of_words[2]
        params = (title, desqr, url)
        sql_command = "INSERT INTO orders VALUES (NULL, %s, %s, %s);"
        crsr_mysql.execute(sql_command, params)
        conn.commit()
        text = "Order correctly inserted"
        bot.send_message(user_id, text, parse_mode='html')
        user_states[user_id] = None

# Found information in database
def search_database(database):
    text = ""
    for i in database:
        id = i['id']
        title = i['title']
        descr = i['descr']
        url = i['url']
        text += "<b>"+ str(id) +"</b> | " + "<b>"+ str(title) +"</b> | " + "<b>"+ str(descr)+"</b> | " + "<b>"+ str(url)+"</b>\n"
    message = "<b>Received 📖 </b> Information about advertisement:\n\n"+text
    return message

# Command /advertisement_database
@bot.message_handler(commands=['advertisement_database'])
def select(message):
    user_id = message.chat.id
    crsr_mysql.execute("SELECT * FROM orders")
    res = crsr_mysql.fetchall()
    if(res):
        text = search_database(res)
        bot.send_message(user_id, text, parse_mode='html')
    else:
        text = "No orders found inside the database."
        bot.send_message(user_id, text, parse_mode='html')

# Add advert to news
def insert_advert(user_id):
    crsr_mysql.execute("SELECT MAX(id) FROM orders")
    res = crsr_mysql.fetchone()
    max = res['MAX(id)']
    if max == None:
        return
    random_advert = random.randint(1, max)
    crsr_mysql.execute(f"SELECT * FROM `orders` WHERE `id` = {random_advert}")
    res = crsr_mysql.fetchall()
    if(res):
        text = ""
        title = res[0]['title']
        descr = res[0]['descr']
        url = res[0]['url']
        text += f" {title}\n\n{descr}\n\n {url}"
        bot.send_message(user_id, text, parse_mode='html')
    else:
        return

# Start bot
if __name__ == '__main__':
    threading.Thread(target=schedule_loop).start()
    schedule.every().day.at("12:00").do(send_subscribed_news)
    bot.polling()
