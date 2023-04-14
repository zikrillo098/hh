from aiogram.types import KeyboardButton, ReplyKeyboardMarkup, InlineKeyboardButton, InlineKeyboardMarkup


def generate_phone_number():
    return ReplyKeyboardMarkup([[KeyboardButton(text='Поделиться контактами ✔', request_contact=True)]],
                               resize_keyboard=True)


def generate_accept():
    return ReplyKeyboardMarkup([[KeyboardButton(text='Подобрать работу🎁')]],
                               resize_keyboard=True)
