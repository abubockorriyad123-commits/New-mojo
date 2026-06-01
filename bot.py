import os
import telebot
import requests

# ENV VARIABLES
BOT_TOKEN = os.getenv("BOT_TOKEN")
AI_API = os.getenv("AI_API")

bot = telebot.TeleBot(BOT_TOKEN)


def ask_ai(text):
    try:
        r = requests.post(
            AI_API,
            headers={"Content-Type": "application/json"},
            json={
                "model": "ultraplinian/fast",
                "messages": [
                    {"role": "user", "content": text}
                ],
                "stream": False
            },
            timeout=30
        )

        data = r.json()

        # safe response parsing
        return (
            data.get("response")
            or data.get("answer")
            or data.get("message")
            or data.get("output")
            or str(data)
        )

    except Exception as e:
        return f"Error: {e}"


@bot.message_handler(commands=["start"])
def start(msg):
    bot.reply_to(msg, "🤖 AI Bot Ready\nএখন message পাঠাও")


@bot.message_handler(func=lambda m: True)
def chat(msg):
    bot.send_chat_action(msg.chat.id, "typing")

    reply = ask_ai(msg.text)
    bot.reply_to(msg, reply)


print("Bot is running...")
bot.infinity_polling()
