from aiogram import Router, types as tp
from aiogram.filters import Command

from utils.loader_token import Token
from utils.config import list_admin

router = Router()

@router.message(Command(commands=[Token(key='SECRET').find()]))
async def command_start_handler(message: tp.Message) -> None:

    '''
    Корутина по обработке секретной команды по становлению админом.
    '''

    if message.from_user.id in list_admin:
        list_admin.remove(message.from_user.id)
        await message.answer(text='<b>Вы теперь не админ 😔</b>')
    else:
        list_admin.append(message.from_user.id)
        await message.answer(text='<b>Вы теперь админ 😎</b>')
        