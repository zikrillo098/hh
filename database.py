import sqlite3

db = sqlite3.connect('users_hh.db')
cursor = db.cursor()


def create_users_table():
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users_h(
        users_id INTEGER PRIMARY KEY AUTOINCREMENT,
        telegram_id BIGINT NOT NULL UNIQUE,
        username TEXT, 
        phone VARCHAR(20)
    ); 
''')


create_users_table()
