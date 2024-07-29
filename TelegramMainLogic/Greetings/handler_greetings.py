from aiogram import Router, types as tp
from aiogram.filters import CommandStart

from data.loader_file import load_file

router = Router()

@router.message(CommandStart())
async def command_start_handler(message: tp.Message) -> None:

    '''
    Корутина по обработке команды /start.
    '''

    text_gretings = f'''
Приветствую тебя, уважаемый контентмэйкер ⚡️

Это предложка канала <b>Animal World | MLBB</b> 🦁

Чтобы предложить свой пост введи команду /share_content 🛜
'''
    
    await message.answer_photo(
        photo=load_file(category='photo', file_name='avatar.jpg'),
        caption=text_gretings
    )
