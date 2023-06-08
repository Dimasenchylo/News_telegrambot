# Newsbot

You can use this bot to view new news either collectively or by category. It is very easy to use. In addition, you can subscribe to a certain category to receive news only in this topic.

## How to Setup:

Go to https://my.telegram.org and Login.

You also need to get telegram bot token and news API key :
1) to get a bot token you need to contact https://t.me/botfather and get a bot token from him 
2) API key you can get at https://newsapi.org/

## How to Install
Install git
```
apt install git -y 
```
Clone repository
```
git clone https://github.com/Dimasenchylo/News_telegrambot.git
```
Install dependencies
```
pip install -r requirements.txt
```
Add your bot token and news API

Run main.py
```
py main.py
```

## Tests 

To run tests, type
```
pytest
```

## How to run database

1) Download XAMPP and open it
2) Start Apache and MySQL
3) Run main.py

## Commands

- ```/start``` - Start the bot
- ```/search``` - Search for news articles based on a keyword
- ```/topnews``` - Get the top news articles
- ```/categories``` -  Choose a category of news articles
- ```/subscribe``` - Subscribe to receive news updates for specific categories
- ```/unsubscribe``` - Unsubscribe from receiving news updates for specific categories
- ```/subscriptions``` - View the categories you are subscribed to
- ```/advertisement``` - add your advertisement in database
- ```/advertisement_database``` - see all database of advertisements
- ```/subscribe_premium``` - subscribe premium
- ```/unsubscribe_premium``` - unsubscribe premium
- ```/premium_status``` - check your premium status

## Example of using news bot

![Gif](Gif.gif)