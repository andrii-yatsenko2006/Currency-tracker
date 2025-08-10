from flask import Flask, render_template, request
from db import create_table, get_rate_from_db, save_rate_to_db, get_rate_from_api
from config import SECRET_KEY

app = Flask(__name__)
app.secret_key = SECRET_KEY

create_table()

@app.route('/', methods=['GET', 'POST'])
def index():
    result = None
    error = None

    if request.method == 'POST':
        # Отримуємо валюти з форми, робимо великі літери
        from_currency = request.form.get('from_currency', '').upper()
        to_currency = request.form.get('to_currency', '').upper()

        # Перевіряємо чи сума валідна
        try:
            amount = float(request.form.get('amount'))
        except (ValueError, TypeError):
            error = "Введіть правильну суму"
            return render_template('index.html', error=error)

        # Шукаємо курс у базі
        rate = get_rate_from_db(from_currency, to_currency)

        # Якщо курсу немає — запитуємо API
        if not rate:
            rate = get_rate_from_api(from_currency, to_currency)
            if rate:
                save_rate_to_db(from_currency, to_currency, rate)  # Зберігаємо курс у базу
            else:
                error = "Не вдалося отримати курс."
                return render_template('index.html', error=error)

        # Обчислюємо суму після обміну
        exchanged_amount = round(amount * rate, 2)

        # Формуємо результат для шаблону
        result = {
            'from_currency': from_currency,
            'to_currency': to_currency,
            'amount': amount,
            'exchanged_amount': exchanged_amount
        }

    # Відображаємо сторінку з результатом або помилкою
    return render_template('index.html', result=result, error=error)

if __name__ == '__main__':
    app.run()