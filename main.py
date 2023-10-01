import os

import cv2
import telebot

from telegram_bot import setup_telegram_bot
from face_recognition import setup_face_recognition
from dotenv import find_dotenv, load_dotenv

if not find_dotenv():
    exit("File .env wasn't found")
else:
    load_dotenv()

bot_token = os.getenv('BOT_TOKEN')

# Create the Telegram bot instance
bot = telebot.TeleBot(bot_token)

# Set up the Telegram bot handlers
setup_telegram_bot(bot)

# Set up the face recognition system
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
setup_face_recognition(cap)

# Start the bot
bot.polling(none_stop=True, interval=0)
