import typing

from aiogram import Bot, types
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.exceptions import TelegramAPIError, BadRequest
from aiogram.utils.markdown import quote_html, hide_link
from aiohttp import web
from loguru import logger
from multidict import MultiDictProxy

from app import config

CAPTION_MAX_SIZE = 1024
TEXT_MAX_SIZE = 4096


async def post_data(bot: Bot, data: MultiDictProxy) -> web.Response:
    await log_info(bot, f"Получен запрос. параметры {quote_html(str(data.items()))}")

    text: typing.Optional[str] = data.get('text', None)
    photo_url: typing.Optional[str] = data.get('photo_url', None)

    if text is None and photo_url is None:
        return web.Response(text="Sorry you don't send params text and/or photo_url", status=400)
    elif text is not None and len(text) > TEXT_MAX_SIZE:
        return web.Response(text="Sorry your text len to long (more than 4095)", status=400)

    return await send_content(
        bot,
        text=text,
        photo_url=photo_url,
        parse_mode=data.get('parse_mode', None),
        button_text=data.get('button_text', None),
        button_url=data.get('button_url', None)
    )


async def send_content(bot: Bot, **kwargs) -> web.Response:
    def can_text_be_caption(text):
        return text is None or len(text) < CAPTION_MAX_SIZE
    try:
        kb = get_inline_kb(kwargs['button_text'], kwargs['button_url'])
        if kwargs['photo_url'] is not None and can_text_be_caption(kwargs['text']):
            logger.debug(kwargs['photo_url'])
            await bot.send_photo(
                config.TARGET_CHAT_ID,
                photo=kwargs['photo_url'],
                caption=kwargs['text'],
                parse_mode=kwargs['parse_mode'],
                reply_markup=kb
            )
        elif kwargs['text'] is not None and kwargs['photo_url'] is not None:
            await bot.send_message(
                config.TARGET_CHAT_ID,
                text=kwargs['text'] + hide_link(kwargs['photo_url']),
                parse_mode=types.ParseMode.HTML,
                reply_markup=kb
            )
        elif kwargs['text'] is not None:
            await bot.send_message(
                config.TARGET_CHAT_ID,
                kwargs['text'],
                kwargs['parse_mode'],
                reply_markup=kb
            )
        else:
            return web.Response(text="Unexpected error", status=500)

    except BadRequest as e:
        log_msg = get_msg_error(e, e.text)
        await log_error(bot, log_msg)
        return web.Response(text=log_msg, status=400)
    except TelegramAPIError as e:
        log_msg = get_msg_error(e)
        await log_error(bot, log_msg)
        return web.Response(text=log_msg, status=400)
    else:
        return web.Response(text='ok')


def get_inline_kb(button_text: str, button_url: str) -> typing.Optional[InlineKeyboardMarkup]:
    if button_url is None or button_url is None:
        return None
    return InlineKeyboardMarkup(row_width=2).add(InlineKeyboardButton(
        text=button_text,
        url=button_url
    ))


def get_msg_error(e: Exception, text: str = "") -> str:
    log_msg = f"{e.__class__.__name__}\n{text}\n{e.args[0]}"
    return log_msg


async def log_info(bot: Bot, log_msg: str):
    logger.info(log_msg)
    await bot.send_message(config.LOG_CHAT_ID, quote_html(log_msg))


async def log_error(bot: Bot, log_msg: str):
    logger.error(log_msg)
    await bot.send_message(config.LOG_CHAT_ID, quote_html(log_msg))
