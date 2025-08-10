import os
from dotenv import load_dotenv

load_dotenv()

API_KEY = os.getenv('API_KEY')  # Ключ API для отримання курсів валют
DATABASE_PATH = os.getenv('DATABASE_PATH')  # Шлях до файлу бази даних
SECRET_KEY = os.getenv('SECRET_KEY')  # Секретний ключ для Flask

