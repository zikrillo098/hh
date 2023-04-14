import sqlite3
from bs4 import BeautifulSoup
import requests
from aiogram import executor, Bot, Dispatcher, types
from aiogram.types import Message, CallbackQuery
from aiogram.utils import exceptions
import asyncio
from keyboards import generate_phone_number, generate_accept

bot = Bot('6211196143:AAFE4Y9SpCnC-Qc3XMEB8SkGzDN1mzOun30', parse_mode='HTML')
dp = Dispatcher(bot)


@dp.message_handler(commands=['start'])
async def command_start(message: types.Message):
    chat_id = message.chat.id

    db = sqlite3.connect('users_hh.db')
    cursor = db.cursor()

    cursor.execute('''
    SELECT * FROM users_h WHERE telegram_id = ?  
    ''', (chat_id,))
    user = cursor.fetchone()
    if user:
        await bot.send_message(chat_id, f'Вы авторизованны Заработаем сегодня лям а Родной {message.chat.username}',
                               reply_markup=generate_accept())
    else:
        emoji = ['% крутой! Присоединяйтесь к нам и станьте частью нашего сообщества!😎',
                 '% крутой! Присоединьтесь к нам и получите доступ к уникальным привилегиям!😍',
                 '% крутой!  Присоединьтесь к нам и начните свой путь к успеху и достижению целей!✅',
                 '% присоединьтесь к нам и получите возможность общаться с единомышленниками🎉',
                 'Мы уважем и ценим % 💖',
                 'Люди говорят что % кизлани ажали😎',
                 'Красавчик😍',
                 'Дерзость в твоей крови✅',
                 'Люьи и влюбляйся🎉',
                 'Сердечко % в подарок💖']
        timer = len(emoji)
        await bot.send_message(chat_id, f'''Добро пожаловать в наш бот уважаемый <b>{message.from_user.username}</b> \n\n 
Тут вы сможете найти кучу вакансий только для начала пройдите регистрацию которая займет всего 10 секунд''')
        sent_message = await bot.send_message(chat_id,
                                              f'''Вы крутой! Присоединитесь к нам и откройте мир новых возможностей! {message.from_user.username} \n\n 
Уже осталось Мотивационные текста за 10 секунд))''')
        while timer > 0:
            await asyncio.sleep(1)
            timer -= 1
            await sent_message.edit_text(
                f''' Осталось {timer} секунд {emoji[timer].replace('%', message.from_user.username)}''')
            if timer == 0:
                await sent_message.delete()
                await bot.send_message(chat_id, f'''Отправьте ваш номер телефона нажмите на кнопку ниже''',
                                       reply_markup=generate_phone_number())


@dp.message_handler(content_types=['contact'])
async def create_user(message: Message):
    chat_id = message.chat.id
    full_name = message.chat.full_name
    if message.from_user.username:
        username = message.chat.username
    else:
        username = None
    phone = message.contact.phone_number

    db = sqlite3.connect('users_hh.db')
    cursor = db.cursor()
    try:
        cursor.execute('''
        INSERT INTO users_h(telegram_id, username, phone) VALUES (?, ?, ?)
        ''', (chat_id, username, phone))
        db.commit()
        await bot.send_message(chat_id, 'Спасибо большое за регистрацию', reply_markup=generate_accept())
    except Exception as E:
        await bot.send_message(chat_id, f'{E}')


@dp.message_handler(lambda message: 'Подобрать работу' in message.text)
async def works(message: Message):
    chat_id = message.chat.id
    await bot.send_message(chat_id,
                           'Напишите кратко какую работу ищите\n\n Пример: Python \\ но он не будет ничего показывать так как я пишу парсер')


@dp.message_handler(content_types=['text'])
async def parser(message: Message):
    job = message.text
    chat_id = message.chat.id
    job = str(job)
    url = 'https://hh.ru/search/vacancy'
    params = {'L_save_area': 'true',
              'clusters': 'true',
              'search_field': 'name',
              'area': '1',
              'enable_snippets': 'true',
              'salary': '',
              'st': 'searchVacancy',
              'text': f'{job}',
              'page': '0'
              }
    print(params)
    response = requests.get(url, params=params)
    soup = BeautifulSoup(response.text, 'html.parser')
    vacancy_items = soup.find_all('div', {'class': 'vacancy-serp-item'})
    vacancy = []
    for item in vacancy_items:
        title = item.find('a', {'class': 'serp-item__title'}).text
        print(title)
        company = item.find('a', {'class': 'bloko-link bloko-link_secondary'}).text
        salary = item.find('div', {'class': 'vacancy-serp-item__compensation'})
        vacancy_url = item.find('a', {'class': 'bloko-link'}).get('href')

        if salary:
            salary = salary.text.replace(u'\xa0', u' ')
        else:
            salary = 'З/П не указана'
        vacancy.append(f'Название компании {title}\nКомпания: {company}\nЗарплата: {salary}\n---\n{vacancy_url}')
        print(vacancy)
    await bot.send_message(chat_id, vacancy)


executor.start_polling(dp, skip_updates=True)
