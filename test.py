import sqlite3

# Подключаемся к базе данных
conn = sqlite3.connect('school_data.db')
cursor = conn.cursor()

# Выполняем запрос для получения всех записей из таблицы students
cursor.execute("SELECT * FROM students")
rows = cursor.fetchall()

# Выводим полученные данные
for row in rows:
    print(f"id: {row[0]}, name: {row[1]}, age: {row[2]}, grade: {row[3]}")

# Закрываем соединение с базой данных
conn.close()