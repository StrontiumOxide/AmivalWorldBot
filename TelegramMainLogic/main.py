from aiogram import Bot, Dispatcher
from utils.commands_bot import set_commands

from TelegramMainLogic.Greetings import *
from TelegramMainLogic.GetData import *
from TelegramMainLogic.BecomeAdmin import *
from TelegramMainLogic.UnloadLog import *


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

            # Функция по выгрузке лога 
        handler_unload

    ]

        # Распаковка router из приложений бота
    dp.include_routers(*map(lambda file: file.router, list_routers_file))

        # Установка меня для команд
    await set_commands(bot=bot)

        # Удаления вебхуков
    await bot.delete_webhook(drop_pending_updates=True)
    
        # Полинг
    await dp.start_polling(bot, polling_timeout=20)
    