import os
import time

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()

PRAKTIKUM_ЕЩЛУТ = os.getenv('PRACTICUM_TOKEN')
TELEGRAM_TOKEN = os.getenv('TELEGRAM_TOKEN')
CHAT_ID = os.getenv('TELEGRAM_CHAT_ID')
BOT = telegram.Bot(token=TELEGRAM_TOKEN)
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses/'


def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    statuses = {
        'approved': True,
        'rejected': False,
    }
    homework_status = statuses.get(homework.get('status'))

    if homework_status is None:
        return 'Ошибка сервера'
    else:
        if homework_status:
            verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
        else:
            verdict = 'К сожалению в работе нашлись ошибки.'
        return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    headers = {'Authorization': f'OAuth {PRACTICUM_TOKEN}'}
    if current_timestamp is None:
        current_timestamp = int(time.time())
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(URL, headers=headers, params=params)
    except:
        print('Ошибка получения JSON')
    return homework_statuses.json()


def send_message(message):
    return BOT.send_message(chat_id=CHAT_ID, text=message)


def main():
    current_timestamp = int(time.time())  # начальное значение timestamp

    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]))
            current_timestamp = new_homework.get('current_date')  # обновить timestamp
            time.sleep(360)  #  опрашивать раз в десять минут

        except Exception as e:
            print(f'Бот упал с ошибкой: {e}')
            time.sleep(5)
            continue


if __name__ == '__main__':
    main()