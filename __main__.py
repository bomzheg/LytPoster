
from aiogram import Bot, types
from aiohttp import web
from loguru import logger
import json
import config
import log

bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
log.setup()


async def hello_get(request: web.Request):
    return await post_data(request.query)


async def hello_post(request: web.Request):
    return await post_data(await request.post())


async def post_data(data):
    await bot.send_message(config.LOG_CHAT_ID, f"Получен запрос. параметры {json.dumps(data.items())}")
    try:
        text = data['text']
        photo_url = data['photo_url']
    except KeyError:
        return web.Response(text="Sorry you don't send params text and photo_url", status=400)
    else:
        await bot.send_photo(config.TARGET_CHAT_ID, photo=photo_url, caption=text)

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
            web.get(f'/lyt_poster/{config.BOT_TOKEN}/', hello_get),
            web.post(f'/lyt_poster/{config.BOT_TOKEN}/', hello_post),
        ]
    )

    app.on_shutdown.append(on_shutdown)
    app.on_startup.append(on_startup)
    return app


if __name__ == '__main__':
    web.run_app(init(), port=config.PORT_LISTEN)
