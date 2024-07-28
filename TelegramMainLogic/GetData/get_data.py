from aiogram import Router, types as tp, Bot
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from utils.states import ContentData
from utils.config import list_admin
from TelegramMainLogic.GetData import kb_get_data as kb

router = Router()

@router.message(Command(commands=['share_content']))
async def introduction(message: tp.Message, state: FSMContext) -> None:

    '''
    Корутина по получению медиафайлов от пользователя.
    '''

    text_media = '''
Давай сделаем пост 🖌️
Для начала отправь фото/видео  которым хочешь поделиться 📸
'''

    await message.answer(
        text=text_media
    )

    await state.set_state(ContentData.file)


@router.message(ContentData.file)
async def get_media(message: tp. Message, state: FSMContext) -> None:

    '''
    Данная корутина будет получает медиафайлы от пользователей
    '''

    if message.photo:
        file_id = message.photo[-1].file_id
        category = 'photo'
    
    elif message.video:
        file_id = message.video.file_id
        category = 'video'

    else:
        await message.answer(
            text='В твоём сообщении нет медиафайлов, которые я могу использовать😕\n\
Пожалуйста отправь фото или видео 🏞',
        )
        return

    await state.update_data(file=file_id, category=category)

    await message.answer(
        text='Хочешь как-то подписать свой пост? 🧐',
        reply_markup=kb.reply.yes_no_caption_kb
        )
    
    await state.set_state(ContentData.status_caption)


@router.message(ContentData.status_caption)
async def get_status_caption(message: tp. Message, state: FSMContext) -> None:

    '''
    Данная корутина будет получать подтверждение на создания подписи к контенту.
    '''

    if message.text not in ['Да ✅', 'Нет ❌']:
        await message.answer(
            text='Мне нужен ответ "<b>Да</b> ✅" или "<b>Нет</b> ❌" 😉',
            reply_markup=kb.reply.yes_no_caption_kb
        )
        return

    if message.text == 'Нет ❌':
        await message.answer(
            text='Отлично, ты хочешь чтобы твой пост выложили анонимно или не анонимно? 🧐',
            reply_markup=kb.reply.anonymously_kb
        )
        
        await state.set_state(ContentData.author)

        return

    await message.answer(
        text='Напиши описание к видео/фото 💬 (не более 1024 символов)',
        reply_markup=kb.reply.remove
    )
    
    await state.set_state(ContentData.caption)


@router.message(ContentData.caption)
async def get_caption(message: tp. Message, state: FSMContext) -> None:

    '''
    Данная корутина будет получать подпись к контенту.
    '''

    if message.text == None:
        await message.answer(
            text='В твоём сообщении нет текста 😕'
        )
        return
    
    await state.update_data(caption=message.text)

    await message.answer(
        text='Отлично, ты хочешь чтобы твой пост выложили анонимно или не анонимно? 🧐',
        reply_markup=kb.reply.anonymously_kb
    )

    await state.set_state(ContentData.author)


@router.message(ContentData.author)
async def get_author_and_mailing(message: tp. Message, state: FSMContext, bot: Bot) -> None:

    '''
    Данная корутина получает информацию об анонимности пользователя.
    '''

    if message.text not in ['Анонимно 😈', 'Не анонимно 🌟']:
        await message.answer(
            text='Мне нужен ответ "<b>Анонимно 😈</b>" или "<b>Не анонимно 🌟</b>" 😉',
            reply_markup=kb.reply.anonymously_kb
        )
        return
    
    if message.text == 'Анонимно 😈':
        await state.update_data(
            first_name='аноним'
        )

    else:
        await state.update_data(
            first_name=message.from_user.first_name,
            last_name=message.from_user.last_name,
            username=message.from_user.username
        )

    await message.answer(
        text='Спасибо, твой пост скоро окажется на канале 😌\n\
Для повторного отправления поста введите команду /share_content ℹ️',
        reply_markup=kb.reply.remove
    )

        # Процесс рассылки постов админам.
    data: dict = await state.get_data()

    file_id = data.get('file')
    category = data.get('category')

    if data.get('first_name') == 'аноним':
        name = 'Аноним'
    else:
        name = f"{data.get('first_name')} {data.get('last_name')} (@{data.get('username')})"

    for user_id in list_admin:

        text_topic = f'''
<blockquote>{data.get('caption', 'Без комментариев')}</blockquote>

<b>Автор:</b> <i>{name}</i>
'''

        await bot.send_message(
            chat_id=user_id,
            text='<b>ВНИМАНИЕ ⚠️</b>\nНовый контент!'
        )
        
        if category == 'photo':
            await bot.send_photo(
                chat_id=user_id,
                photo=file_id,
                caption=text_topic
            )

        else:
            await bot.send_video(
                chat_id=user_id,
                video=file_id,
                caption=text_topic
            )

    await state.clear()
    