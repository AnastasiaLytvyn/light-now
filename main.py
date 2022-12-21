from dotenv import load_dotenv, find_dotenv
import requests
import schedule
import os
import telebot

import main

load_dotenv(find_dotenv())
bot = telebot.TeleBot(os.getenv("TOKEN"))
URL = str(os.getenv("URL"))
old_status = 100

@bot.message_handler(commands=["start"])
def start(msg):
    bot.send_message(
        msg.chat.id, f"Hello, {msg.from_user.first_name}! Is there light now?")

@bot.message_handler()
def send_same(status_result ):
    bot.send_message(
        442828335, status_result)


@bot.message_handler()
def check_light():
    try:
        result = requests.get(URL, timeout=15)
        status = result.status_code
    except requests.exceptions.ConnectTimeout:
        status = 404
    if status != main.old_status:
        if status == 200:
            status_result = "The light was turned on!"
        else:
            status_result = "The light was turned off!"
        main.old_status = status
        bot.send_message(
            os.getenv("USER_ID_MAIN"), status_result)
        bot.send_message(
            os.getenv("USER_ID_PRIMARY"), status_result)



schedule.every(120).seconds.do(check_light)

while True:
    try:
        schedule.run_pending()
    except KeyboardInterrupt:
        check_light()


bot.polling(non_stop=True)
