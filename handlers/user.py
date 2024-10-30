from aiogram import types
from aiogram.types import Message, ReplyKeyboardMarkup, KeyboardButton, ContentType
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from lexicon.lexicon_ru import SURVEY_QUESTIONS, QUIZ_QUESTIONS

user_data = {}

# Создаем клавиатуру для выбора действия
def get_main_keyboard() -> ReplyKeyboardMarkup:
    kb_builder = ReplyKeyboardBuilder()
    kb_builder.row(KeyboardButton(text='Пройти опрос'), KeyboardButton(text='Пройти викторину'))
    return kb_builder.as_markup(resize_keyboard=True, one_time_keyboard=True)

async def cmd_start(message: Message):
    await message.answer("Привет! Выберите, что хотите сделать:", reply_markup=get_main_keyboard())

async def start_survey(message: Message):
    user_data[message.from_user.id] = {"survey_step": 0, "survey_answers": []}
    await ask_survey_question(message)

async def ask_survey_question(message: Message):
    step = user_data[message.from_user.id]["survey_step"]
    await message.answer(SURVEY_QUESTIONS[step], reply_markup=types.ReplyKeyboardRemove())

async def handle_survey_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["survey_step"]
    user_data[user_id]["survey_answers"].append(message.text)

    if step + 1 < len(SURVEY_QUESTIONS):
        user_data[user_id]["survey_step"] += 1
        await ask_survey_question(message)
    else:
        results = "\n".join(f"{q}: {a}" for q, a in zip(SURVEY_QUESTIONS, user_data[user_id]["survey_answers"]))
        await message.answer(f"Спасибо за участие!\nВаши ответы:\n{results}", reply_markup=get_main_keyboard())
        del user_data[user_id]

async def start_quiz(message: Message):
    user_data[message.from_user.id] = {"quiz_step": 0, "correct_answers": 0}
    await ask_quiz_question(message)

async def ask_quiz_question(message: Message):
    step = user_data[message.from_user.id]["quiz_step"]
    question, options, _ = QUIZ_QUESTIONS[step]
    kb_builder = ReplyKeyboardBuilder()
    for option in options:
        kb_builder.button(text=option)
    await message.answer(question, reply_markup=kb_builder.as_markup(resize_keyboard=True))

async def handle_quiz_answer(message: Message):
    user_id = message.from_user.id
    step = user_data[user_id]["quiz_step"]
    _, _, correct_answer = QUIZ_QUESTIONS[step]

    if message.text == correct_answer:
        user_data[user_id]["correct_answers"] += 1
        await message.answer("Правильно!")
    else:
        await message.answer(f"Неправильно. Правильный ответ: {correct_answer}")

    if step + 1 < len(QUIZ_QUESTIONS):
        user_data[user_id]["quiz_step"] += 1
        await ask_quiz_question(message)
    else:
        correct = user_data[user_id]["correct_answers"]
        await message.answer(f"Викторина окончена! Правильных ответов: {correct}/{len(QUIZ_QUESTIONS)}", reply_markup=get_main_keyboard())
        del user_data[user_id]

# Эхо-обработчики для различных типов контента
async def echo_text(message: Message):
    await message.answer(message.text)

async def echo_photo(message: Message):
    await message.reply_photo(message.photo[-1].file_id)

async def echo_video(message: Message):
    await message.reply_video(message.video.file_id)

async def echo_audio(message: Message):
    await message.reply_audio(message.audio.file_id)

async def echo_document(message: Message):
    await message.reply_document(message.document.file_id)

async def echo_voice(message: Message):
    await message.reply_voice(message.voice.file_id)

async def echo_video_note(message: Message):
    await message.reply_video_note(message.video_note.file_id)

async def echo_sticker(message: Message):
    await message.reply_sticker(message.sticker.file_id)

async def echo_animation(message: Message):
    await message.reply_animation(message.animation.file_id)

async def echo_contact(message: Message):
    await message.answer(f"Контакт: {message.contact.phone_number}")

async def echo_location(message: Message):
    await message.answer(f"Местоположение: {message.location.latitude}, {message.location.longitude}")

async def echo_poll(message: Message):
    await message.answer("Получен опрос.")
