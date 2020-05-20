
from aiogram import Bot, types
from aiohttp import web
from loguru import logger

import config
import log

bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
log.setup()


async def hello_get(request: web.Request):
    data = request.query
    one = data.get('one', "don't have one params")
    logger.debug(one)
    await bot.send_message(config.LOG_CHAT_ID, f"Получен запрос GET. параметр one = {one}")

    return web.Response(text='ok. request received')


async def hello_post(request: web.Request):
    data = await request.post()
    one = data.get('one', "don't have one params")
    logger.debug(one)
    await bot.send_message(config.LOG_CHAT_ID, f"Получен запрос POST. параметр one = {one}")

    return web.Response(text='ok. request received')


async def on_startup(_: web.Application):
    logger.debug("bot started")
    await bot.send_message(config.LOG_CHAT_ID, "Bot started")


async def on_shutdown(_: web.Application):
    await bot.send_message(config.LOG_CHAT_ID, "Bot stopped")
    await bot.close()


def init():
    app = web.Application()
    app.add_routes(
        [
            web.get('/lyt_poster/', hello_get),
            web.post('/lyt_poster/', hello_post),
            web.get('/', hello_get),
            web.post('/', hello_post),
        ]
    )

    app.on_shutdown.append(on_shutdown)
    app.on_startup.append(on_startup)
    return app


if __name__ == '__main__':
    web.run_app(init(), port=8000)
