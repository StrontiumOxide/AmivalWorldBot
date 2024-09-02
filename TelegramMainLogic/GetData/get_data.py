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
async def get_media(message: tp.Message, state: FSMContext) -> None:

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
async def get_status_caption(message: tp.Message, state: FSMContext) -> None:

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
            text='Ладно. Как ты хочешь чтобы выложили твой пост? 🥸',
            reply_markup=kb.reply.anonymously_kb
        )
        
        await state.set_state(ContentData.author)

        return

    await message.answer(
        text='Напиши описание к своему посту 💬 (не более 1024 символов)',
        reply_markup=kb.reply.remove
    )
    
    await state.set_state(ContentData.caption)


@router.message(ContentData.caption)
async def get_caption(message: tp.Message, state: FSMContext) -> None:

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
        text='Ладно. Как ты хочешь чтобы выложили твой пост? 🥸',
        reply_markup=kb.reply.anonymously_kb
    )

    await state.set_state(ContentData.author)


@router.message(ContentData.author)
async def get_author(message: tp.Message, state: FSMContext) -> None:

    '''
    Данная корутина получает информацию об анонимности пользователя.
    '''

    if message.text not in ['Анонимно 🥷', 'Не анонимно 👀']:
        await message.answer(
            text='Мне нужен ответ "<b>Анонимно 🥷</b>" или "<b>Не анонимно 👀</b>" 😉',
            reply_markup=kb.reply.anonymously_kb
        )
        return
    
    if message.text == 'Анонимно 🥷':
        await state.update_data(
            full_name='аноним'
        )
    else:
        await message.answer(
            text='Напиши свой никнейм 🔥',
            reply_markup=kb.builder.created_username_kb(username=message.from_user.username)
        )
        await state.set_state(ContentData.full_name)
        return
        
    await message.answer(
        text='Хорошо, скоро твой пост окажется на канале 💥\n\
Чтобы отправить новый контент введите команду /share_content 🛜',
        reply_markup=kb.reply.remove
    )

    await mailing_admin(state=state, bot=message.bot)


@router.message(ContentData.full_name)
async def get_full_name(message: tp.Message, state: FSMContext) -> None:

    '''
    Данная корутина получает информацию об анонимности пользователя.
    '''

    if not message.text:
        await message.answer(
            text='Ваше сообщение не содержит текст 😒'
        )
        return

    await state.update_data(
        full_name=message.text
    )

    await message.answer(
        text='Хорошо, скоро твой пост окажется на канале 💥\n\
Чтобы отправить новый контент введите команду /share_content 🛜',
        reply_markup=kb.reply.remove
    )

    await mailing_admin(state=state, bot=message.bot)


async def mailing_admin(state: FSMContext, bot: Bot) -> None:

    """
    Корутина по рассылке уведомлений админам о новых постах
    """

    data: dict = await state.get_data()

    file_id = data.get('file')
    category = data.get('category')

    if data.get('full_name') == 'аноним':
        name = 'Аноним'
    else:
        name = f"{data.get('full_name')}"

    for user_id in list_admin:

        text_topic = f'''
<blockquote>{data.get('caption', 'Без комментариев')}</blockquote>

<b>Автор:</b> <i>{name}</i>
'''

        await bot.send_message(
            chat_id=user_id,
            text='<b>⚠️ ВНИМАНИЕ ⚠️</b> <i>Новый контент!</i>'
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
    