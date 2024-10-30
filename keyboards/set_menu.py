from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo

def create_web_app_button(url: str) -> InlineKeyboardMarkup:
    web_app_button = InlineKeyboardButton(text="Открыть Web App", web_app=WebAppInfo(url=url))
    inline_kb = InlineKeyboardMarkup(inline_keyboard=[[web_app_button]])
    return inline_kb
