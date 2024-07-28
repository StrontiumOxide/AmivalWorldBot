import asyncio
from aiogram import Bot, Dispatcher
from aiogram.enums.parse_mode import ParseMode
from utils.loader_token import Token

from TelegramMainLogic.main import HandlerUpdate

bot = Bot(token=Token('TELEGRAM').find(), parse_mode=ParseMode.HTML)
dp = Dispatcher()

async def main() -> None:

    '''
    Главная корутина по запуску Telegram-бота.
    '''
    
        # Уведомление о запуске бота 
    await bot.send_message(
        chat_id=Token('MY_ID').find(),
        text='<b>[INFO]</b> <i>Telegram-бот запущен!</i>'
    )

        # Добавление в Цикл Событий отдельных корутин(задач)
    await asyncio.gather(
        HandlerUpdate(bot=bot, dp=dp)
    )

if __name__ == "__main__":
    asyncio.run(main())
    