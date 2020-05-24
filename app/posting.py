from aiogram import Bot
from aiohttp import web
from aiogram.utils.exceptions import TelegramAPIError, BadRequest
from aiogram.utils.markdown import quote_html
from multidict import MultiDictProxy

from app import config


async def post_data(bot: Bot, data: MultiDictProxy):
    await bot.send_message(config.LOG_CHAT_ID, f"Получен запрос. параметры {quote_html(str(data.items()))}")
    try:
        text = data['text']
        photo_url = data['photo_url']
    except KeyError:
        return web.Response(text="Sorry you don't send params text and/or photo_url", status=400)
    else:
        return await send_photo(bot, text, photo_url)


async def send_photo(bot: Bot, text, photo_url):
    def no_public_message_link(chat_id: int, message_id: int):
        return f"https://t.me/c/{str(chat_id)[4:]}/{message_id}"
    try:
        msg = await bot.send_photo(config.TARGET_CHAT_ID, photo=photo_url, caption=text)
    except BadRequest as e:
        return web.Response(text=f"{e.__class__.__name__}\n{e.text}\n{e.args[0]}", status=400)
    except TelegramAPIError as e:
        return web.Response(text=f"{e.__class__.__name__}\n{e.args[0]}", status=400)
    else:
        msg_link = no_public_message_link(msg.chat.id, msg.message_id)
        return web.Response(text=f'ok. request received, msg was send, see it at {msg_link}')
