from aiogram.types import FSInputFile

def load_file(category: str, file_name: str) -> FSInputFile:

    """
    Данная функция необходима для отправки файлов в Telegram.
    """

    return FSInputFile(
        path=f"data/{category}/{file_name}",
        filename=file_name
    )
