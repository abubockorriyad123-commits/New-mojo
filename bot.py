import os
import telebot
import requests

BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_API = os.getenv("AI_API")   # তোমার Render backend URL
API_KEY = os.getenv("API_KEY")

bot = telebot.TeleBot(BOT_TOKEN)

def ask_ai(text):
    try:
        r = requests.post(
            AI_API,
            headers={
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "prompt": text
            },
            timeout=30
        )

        data = r.json()

        return data.get("response") or data.get("answer") or str(data)

    except Exception as e:
        return f"Error: {e}"


@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "🤖 AI Bot Ready\nMessage পাঠাও")


@bot.message_handler(func=lambda m: True)
def chat(msg):
    bot.send_chat_action(msg.chat.id, "typing")
    reply = ask_ai(msg.text)
    bot.reply_to(msg, reply)


print("Bot running...")
bot.infinity_polling()
