from aiogram import Bot, Dispatcher
from aiogram.filters import Command
from aiogram.types import Message

API_TOKEN: str = '6002753499:AAHPsD8ZL_0dyvNfpMWgPxhJC22NZImPOTk'

bot: Bot = Bot(token=API_TOKEN)
dp: Dispatcher = Dispatcher()


@dp.message(Command(commands=['start']))
async def process_start_command(message: Message):
    await message.answer('Провет!\nЯ Эхо-бот.\nНапиши мне что-нибудь!')
    print(message.json(exclude_none=True, indent=4))


@dp.message(Command(commands=['help']))
async def process_help_command(message: Message):
    await message.answer('Напиши мне что-нибудь,\nа я повторю.')
    print(message.json(exclude_none=True, indent=4))


@dp.message()
async def send_echo(message: Message):
    try:
        await message.send_copy(chat_id=message.chat.id)
        print(message.json(exclude_none=True, indent=4))
    except TypeError:
        await message.reply(text='Данный тип апдейтов не поддерживается '
                                 'методом send_copy')


if __name__ == '__main__':
    dp.run_polling(bot)
