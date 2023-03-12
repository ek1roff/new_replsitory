import requests
import time


API_URL: str = 'https://api.telegram.org/bot'
API_CAT_URL: str = 'https://aws.random.cat/meow'
BOT_TOKEN: str = '6002753499:AAHPsD8ZL_0dyvNfpMWgPxhJC22NZImPOTk'
TEXT_ERROR: str = 'Котики заняты'

offset: int = -2
timeout: int = 60
updates: dict
cat_response: requests.Response
chat_id: int


def do_something() -> None:
    print('Был апдейт')


while True:
    start_time = time.time()
    updates = requests.get(f'{API_URL}{BOT_TOKEN}/getUpdates?offset={offset + 1}').json()

    if updates['result']:
        for result in updates['result']:
            offset = result['update_id']
            chat_id = result['message']['from']['id']
            cat_response = requests.get(API_CAT_URL)
            if cat_response.status_code == 200:
                cat_link = cat_response.json()['file']
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={cat_link}')
            else:
                requests.get(f'{API_URL}{BOT_TOKEN}/sendPhoto?chat_id={chat_id}&photo={TEXT_ERROR}')
            do_something()

    end_time = time.time()
    print(f'Время между запросами к Telegram Bot API: {end_time - start_time}')
