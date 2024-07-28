from aiogram import Bot, Dispatcher
from utils.commands_bot import set_commands

from TelegramMainLogic.Greetings import *
from TelegramMainLogic.GetData import *
from TelegramMainLogic.BecomeAdmin import *

async def HandlerUpdate(bot: Bot, dp: Dispatcher) -> None:

    '''
    Корутина по обработке Update.
    '''

        # Список отдельных блоков приложений бота. Последовательность имеет смысл!
    list_routers_file = [

            # Приветствие
        handler_greetings,

            # Получение информации для контента
        get_data,

            # Функция по становлению админом и обратно
        become_admin,

    ]

        # Распаковка router из приложений бота
    dp.include_routers(*map(lambda file: file.router, list_routers_file))

    await set_commands(bot=bot)

    await dp.start_polling(bot)
