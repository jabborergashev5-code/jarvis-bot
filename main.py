import os
import threading
from flask import Flask
from aiogram import Bot, Dispatcher, executor, types
import google.generativeai as genai

# Render uchun soxta veb-server (Port xatoligini oldini olish uchun)
app = Flask(__name__)

@app.route('/')
def home():
    return "JARVIS Bot Alive!"

def run_flask():
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

# Veb-serverni alohida oqimda (thread) ishga tushirish
threading.Thread(target=run_flask, daemon=True).start()

# --- SIZNING BOT KODINGIZ SHU YERDAN DAVOM ETADI ---
BOT_TOKEN = "8796103298:AAHFaaTzMe4oHK3JKHGGG4cdxAypWgTyGuU"
GEMINI_API_KEY = "AQ.Ab8RN6K3uP6s47XdQrIA5ZSD_tzS_RGYjDziriQGsfpD7NrlVA"

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher(bot)

@dp.message_handler(commands=['start'])
async def send_welcome(message: types.Message):
    await message.reply("Xizmatingizdaman, ser! JARVIS tizimlari tayyor.")

@dp.message_handler()
async def echo(message: types.Message):
    try:
        response = model.generate_content(message.text)
        await message.reply(response.text)
    except Exception as e:
        await message.reply(f"Xatolik yuz berdi: {e}")

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
