import logging
import sqlite3
import asyncio
from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from config import API_TOKEN

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Создаём экземпляры Bot и Dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(storage=MemoryStorage())
router = Router()

# Создаем базу данных и таблицу
def create_database():
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS students (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            age INTEGER NOT NULL,
            grade TEXT NOT NULL
        )
    ''')
    conn.commit()
    conn.close()

create_database()

# Функция для сохранения данных в базу данных
def save_student_data(name, age, grade):
    conn = sqlite3.connect('school_data.db')
    cursor = conn.cursor()
    cursor.execute('INSERT INTO students (name, age, grade) VALUES (?, ?, ?)', (name, age, grade))
    conn.commit()
    conn.close()

# Команда /start
@router.message(Command(commands=['start']))
async def send_welcome(message: types.Message):
    logging.info("Получена команда /start")
    await message.answer(
        "Привет! Я бот, который собирает данные о студентах. Пожалуйста, введите ваше имя, возраст и класс (например, 'Иван Иванов, 15, 10 класс').",
        parse_mode="HTML"
    )

# Обработка текстовых сообщений
@router.message(lambda message: message.text and not message.text.startswith('/'))
async def handle_student_data(message: types.Message):
    logging.info("Получены данные студента")
    try:
        # Разделяем введенные данные на имя, возраст и класс
        data = message.text.split(',')
        name = data[0].strip()
        age = int(data[1].strip())
        grade = data[2].strip()

        # Сохраняем данные в базу данных
        save_student_data(name, age, grade)

        await message.answer(f"Данные студента успешно сохранены: {name}, {age}, {grade}.")
    except Exception as e:
        logging.error(f"Ошибка при обработке данных студента: {e}")
        await message.answer("Пожалуйста, введите данные в правильном формате: 'Имя, Возраст, Класс'.")

# Добавление маршрутизатора в диспетчер
dp.include_router(router)

# Запуск бота
async def main():
    try:
        await dp.start_polling(bot)
    except Exception as e:
        logging.error(f"Ошибка при запуске поллинга: {e}")

if __name__ == '__main__':
    asyncio.run(main())