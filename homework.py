import os
import time
import requests

import requests
import telegram
from dotenv import load_dotenv

load_dotenv()


PRAKTIKUM_TOKEN = 'AgAAAAAxKf_JAAYckZqsY7LWb03ciCBbXlyHVbo' #os.getenv("PRAKTIKUM_TOKEN")
TELEGRAM_TOKEN = '1470844282:AAHyF3MMOVyatAC2GXJUD0uvDzkAwkP449k' #os.getenv('TELEGRAM_TOKEN')
CHAT_ID = '924776606' #os.getenv('TELEGRAM_CHAT_ID')
URL = 'https://praktikum.yandex.ru/api/user_api/homework_statuses'

def parse_homework_status(homework):
    homework_name = homework.get('homework_name')
    if homework_name is None:
        return homework.get('unknown')
    status = homework.get('status')
    if status is None:
        homework.get('unknown')
    elif status == 'rejected':
        verdict = 'К сожалению в работе нашлись ошибки.'
    else:
        verdict = 'Ревьюеру всё понравилось, можно приступать к следующему уроку.'
    return f'У вас проверили работу "{homework_name}"!\n\n{verdict}'


def get_homework_statuses(current_timestamp):
    if current_timestamp is None:
        return int(time.time())
    headers = {'Authorization': f'OAuth {PRAKTIKUM_TOKEN}'}
    params = {'from_date': current_timestamp}
    try:
        homework_statuses = requests.get(
            url=URL,
            headers=headers,
            params=params
        )
        return homework_statuses.json()
    except Exception as e:
        print(f'Ошибка у бота {e}')


def send_message(message, bot_client):
    return bot_client.send_message(chat_id=CHAT_ID, text=message)


def main():
    bot = telegram.Bot(token=TELEGRAM_TOKEN)
    current_timestamp = int(time.time())  
    while True:
        try:
            new_homework = get_homework_statuses(current_timestamp)
            if new_homework.get('homeworks'):
                send_message(parse_homework_status(new_homework.get('homeworks')[0]), bot)
            current_timestamp = new_homework.get('current_date', current_timestamp) 
            time.sleep(300)  

        except Exception as e:
            print(f'Ошибка у бота: {e}')
            time.sleep(5)


if __name__ == '__main__':
    main()
