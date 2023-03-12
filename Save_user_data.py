import sqlite3
# Сохранение в базу данных
def save_user_data(phone, first_name, last_name):
    conn = sqlite3.connect("static/users.db")
    cursor = conn.cursor()

    # Создаем таблицу, если ее еще нет
    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        phone TEXT,
                        first_name TEXT,
                        last_name TEXT
                    )""")

    # Добавляем пользователя в базу данных
    cursor.execute("INSERT INTO users (phone, first_name, last_name) VALUES (?, ?, ?)", (phone, first_name, last_name))
    conn.commit()

    # Закрываем соединение с базой данных
    conn.close()