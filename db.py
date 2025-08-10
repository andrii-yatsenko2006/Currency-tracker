import sqlite3
import requests
from config import API_KEY

def get_connection():
    # Підключення до бази даних SQLite
    conn = sqlite3.connect('exchange_rates.db')
    return conn

def create_table():
    # Створення таблиці rates
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
            CREATE TABLE IF NOT EXISTS rates (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                from_currency TEXT,
                to_currency TEXT,
                rate REAL,
                last_updated TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')
    conn.commit()
    conn.close()

def get_rate_from_db(from_currency, to_currency):
    # Отримання останнього курсу з бази за заданими валютами
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT rate FROM rates
        WHERE from_currency = ? AND to_currency = ?
        ORDER BY last_updated DESC
        LIMIT 1
    ''', (from_currency, to_currency))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    return None

def save_rate_to_db(from_currency, to_currency, rate):
    # Збереження курсу валют у базу даних
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO rates (from_currency, to_currency, rate)
        VALUES (?, ?, ?)
    ''', (from_currency, to_currency, rate))
    conn.commit()
    conn.close()

def get_rate_from_api(from_currency, to_currency):
    # Запит курсу валют з зовнішнього API
    url = f"https://v6.exchangerate-api.com/v6/{API_KEY}/latest/{from_currency}"
    response = requests.get(url)
    data = response.json()

    # Якщо запит успішний — отримуємо потрібний курс
    if data['result'] == 'success':
        rates = data.get('conversion_rates', {})
        rate = rates.get(to_currency)
        if rate:
            return rate
    return None