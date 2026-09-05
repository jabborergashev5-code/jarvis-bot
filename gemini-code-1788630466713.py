import asyncio
import logging
from aiogram import Bot, Dispatcher, types, F
from aiogram.filters import Command
import google.generativeai as genai
from apscheduler.schedulers.asyncio import AsyncIOScheduler

# Sozlamalar
BOT_TOKEN = "8796103298:AAHFaaTzMe4oHK3JKHGGG4cdxAypWgTyGuU"
GEMINI_API_KEY = "AQ.Ab8RN6K3uP6s47XdQrIA5ZSD_tzS_RGYjDziriQGsfpD7NrlVA"
MY_TELEGRAM_ID = 1183441061

genai.configure(api_key=GEMINI_API_KEY)
model = genai.GenerativeModel('gemini-1.5-flash')

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()
scheduler = AsyncIOScheduler()

SYSTEM_PROMPT = "Sening isming JARVIS. Sen Iron Man filmi uslubida, o'z egangga 'ser' deb murojaat qiluvchi aqlli yordamchisan. Qisqa, samimiy va loqaydsiz javob ber."

@dp.message(Command("start"))
async def start_cmd(message: types.Message):
    if message.from_user.id != MY_TELEGRAM_ID:
        return
    await message.answer("Tizimlar tayyor, ser! Xizmatingizdaman.")

@dp.message(F.text)
async def handle_message(message: types.Message):
    if message.from_user.id != MY_TELEGRAM_ID:
        return
    
    prompt = f"{SYSTEM_PROMPT}\nFoydalanuvchi: {message.text}"
    response = model.generate_content(prompt)
    await message.answer(response.text)

async def main():
    scheduler.start()
    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())