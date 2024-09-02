from aiogram import Router, types as tp
from aiogram.filters import Command
from datetime import datetime as dt

router = Router()


@router.message(Command(commands=['unload_log']))
async def unload_log(message: tp.Message) -> None:

    """
    Функция по выгрузке лога
    """

    await message.answer_document(
        document=tp.FSInputFile(
            path='bot_logging.log', 
            filename=f'Журнал учёта {dt.now().strftime("%d-%m-%Y %H-%M-%S")}.txt'),
        caption='Здесь содержится информация об ошибках, произошедших в боте на данный момент времени🚫',
        protect_content=False
    )
    await message.delete()
    