from typing import Union

from aiogram import Bot


async def check(user_id, channel: Union[int, str]):
    bot = Bot.get_current()
    number = await bot.get_chat_member(user_id=user_id, chat_id=channel)
    return number.is_chat_member()