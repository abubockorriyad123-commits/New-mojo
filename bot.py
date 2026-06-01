import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_API = os.getenv("AI_API")

bot = telebot.TeleBot(BOT_TOKEN)

def ask_ai(text):
    r = requests.post(
        AI_API,
        json={
            "model": "ultraplinian/fast",
            "prompt": text,
            "stream": False
        }
    )
    data = r.json()
    return data.get("response") or str(data)

@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "🤖 Bot Ready")

@bot.message_handler(func=lambda m: True)
def chat(msg):
    bot.reply_to(msg, ask_ai(msg.text))

bot.infinity_polling()
