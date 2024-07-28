from aiogram import Bot
from aiogram.types import BotCommand, BotCommandScopeDefault

async def set_commands(bot: Bot) -> None:

    '''
    Данная функция добавляет меню в бота с командами ниже.
    '''

    commands = [
        BotCommand(
            command="start",
            description="Запуск бота ⚠️"
        ),
        BotCommand(
            command="share_content",
            description="Поделиться контентом ℹ️"
        ),
    ]

    await bot.set_my_commands(commands=commands, scope=BotCommandScopeDefault())
    