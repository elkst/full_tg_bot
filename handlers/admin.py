from aiogram import types
from aiogram.filters import Command
from keyboards.set_menu import create_web_app_button

async def start_command(message: types.Message):
    web_app_url = "https://your-app-name.glitch.me/"  # Замените URL
    inline_kb = create_web_app_button(web_app_url)
    await message.answer("Нажми на кнопку ниже, чтобы открыть веб-приложение:", reply_markup=inline_kb)
