from aiogram.fsm.state import State, StatesGroup

class ContentData(StatesGroup):

    '''
    Класс для хранения информации для создания контента.
    '''

    file = State()
    category = State()
    status_caption = State()
    caption = State()
    author = State()

    full_name = State()
    