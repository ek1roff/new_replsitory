import random
from aiogram import Bot, Dispatcher
from aiogram.filters import Command, Text
from aiogram.types import Message

API_TOKEN: str = '6002753499:AAHPsD8ZL_0dyvNfpMWgPxhJC22NZImPOTk'

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()

ATTEMPTS: int = 7

users: dict = {}

def get_random_number() -> int:
    return random.randint(1, 100)


@dp.message(Command(commands=['start']))
async def start_command(message: Message):
    await message.answer('Это игра "Угадай число"\n'
                         'Чтобы узнать правила оправь\n/help')
    if message.from_user.id not in users:
        users[message.from_user.id] = {'in_game': False,
                                       'secret_number': None,
                                        'attempts': None,
                                        'total_games': 0,
                                        'wins': 0}


@dp.message(Command(commands=['help']))
async def help_command(message: Message):
    await message.answer(f'Я загадал число от 1 до 100, '
                         f'угадай его за {ATTEMPTS} попыток!'
                         f'/cancel - выйти из игры\n'
                         f'/stat - статистика игр\n'
                         f'Напиши Игра, чтобы начать игру')


@dp.message(Command(commands=['stat']))
async def stat_command(message: Message):
    await message.answer(f'Сыграно игр: '
                         f'{users[message.from_user.id]["total_games"]}\n'
                         f'Выйграно {users[message.from_user.id]["wins"]} игр')


@dp.message(Command(commands=['cancel']))
async def cancel_command(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Вы вышли из игры'
                             '/start, чтобы сыграть')
        users[message.from_user.id]['in_game'] = False
    else:
        await message.answer('Мы уже играем')


@dp.message(Text(text=['Да', 'Давай', 'Сыграем', 'Игра']))
async def positive_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Я загадал число от 1 до 100.\nУгадай')
        users[message.from_user.id]['in_game'] = True
        users[message.from_user.id]['secret_number'] = get_random_number()
        users[message.from_user.id]['attempts'] = ATTEMPTS
    else:
        await message.answer('Пиши числа от 1 до 100'
                             'или команды')


@dp.message(Text(text=['Нет', 'Не', 'Не хочу', 'Потом']))
async def negative_answer(message: Message):
    if not users[message.from_user.id]['in_game']:
        await message.answer('Жаль...')
    else:
        await message.answer('Мы уже играем')


@dp.message(lambda x: x.text and x.text.isdigit() and 1 <= int(x.text) <= 100)
async def numbers_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        if int(message.text) == users[message.from_user.id]['secret_number']:
            await message.answer('Вы угадали!\nСыграем ещё?')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]["total_games"] += 1
            users[message.from_user.id]['wins'] += 1
        elif int(message.text) > users[message.from_user.id]['secret_number']:
            await message.answer('Моё число меньше')
            users[message.from_user.id]['attempts'] -= 1
        elif int(message.text) < users[message.from_user.id]['secret_number']:
            await message.answer('Моё число больше')
            users[message.from_user.id]['attempts'] -= 1

        if users[message.from_user.id]['attempts'] == 0:
            await message.answer('У вас не осталось попыток'
                                 'Моё число {user["secret_number"]}')
            users[message.from_user.id]['in_game'] = False
            users[message.from_user.id]['total_games'] += 1
    else:
        await message.answer('Игра ещё не началась.\nНачать?')


@dp.message()
async def other_text_answer(message: Message):
    if users[message.from_user.id]['in_game']:
        await message.answer('Мы уже играем\nПрисылай числа от 1 до 100')
    else:
        await message.answer('Я не создан для разговоров.'
                             'Но зато, я могу сыграть с тобой'
                             'Отправь /start')


if __name__ == '__main__':
    dp.run_polling(bot)
