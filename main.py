from aiogram import Dispatcher, Bot, F
from aiogram.filters import Command
from aiogram.types import ContentType

from config_data.config import BOT_TOKEN
from handlers import user, admin
from lexicon.lexicon_ru import QUIZ_QUESTIONS

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

# Регистрация основных команд
dp.message.register(user.cmd_start, Command("start"))
dp.message.register(admin.start_command, Command("start"))
dp.message.register(user.start_survey, lambda msg: msg.text == 'Пройти опрос')
dp.message.register(user.handle_survey_answer, lambda msg: msg.from_user.id in user.user_data and "survey_step" in user.user_data[msg.from_user.id])
dp.message.register(user.start_quiz, lambda msg: msg.text == 'Пройти викторину')
dp.message.register(user.handle_quiz_answer, lambda msg: msg.text in [opt for q, opts, a in QUIZ_QUESTIONS for opt in opts])

# Регистрация эхо-обработчиков для различных типов контента
dp.message.register(user.echo_text, F.content_type == ContentType.TEXT)
dp.message.register(user.echo_photo, F.content_type == ContentType.PHOTO)
dp.message.register(user.echo_video, F.content_type == ContentType.VIDEO)
dp.message.register(user.echo_audio, F.content_type == ContentType.AUDIO)
dp.message.register(user.echo_document, F.content_type == ContentType.DOCUMENT)
dp.message.register(user.echo_voice, F.content_type == ContentType.VOICE)
dp.message.register(user.echo_video_note, F.content_type == ContentType.VIDEO_NOTE)
dp.message.register(user.echo_sticker, F.content_type == ContentType.STICKER)
dp.message.register(user.echo_animation, F.content_type == ContentType.ANIMATION)
dp.message.register(user.echo_contact, F.content_type == ContentType.CONTACT)
dp.message.register(user.echo_location, F.content_type == ContentType.LOCATION)
dp.message.register(user.echo_poll, F.content_type == ContentType.POLL)

if __name__ == '__main__':
    dp.run_polling(bot)
