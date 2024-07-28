class Token:

    '''
    Данный класс ищет токены по ключу. Используй метод find()
    '''

    def __init__(self, key: str) -> None:
        self.key = key

    def __str__(self) -> str:
        return f'Токен: {self.key}'
    
    def __repr__(self) -> str:
        return f'Токен: {self.key}'

    def find(self) -> str:

        '''
        При не нахождении файла "tokens.py" с необходимым ключём поиск происходит\
        в виртуальном окружении.
        '''

        try:
            from utils import tokens
        except ImportError:
            from os import getenv
            return getenv(self.key)
        else:
            return tokens.__dict__.get(self.key)
