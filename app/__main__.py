from aiogram import Bot, types
from aiohttp import web
from loguru import logger
from app import log, config
from app.posting import post_data

bot = Bot(config.BOT_TOKEN, parse_mode=types.ParseMode.HTML)
log.setup()


async def hello_get(request: web.Request):
    return await post_data(bot, request.query)


async def hello_post(request: web.Request):
    return await post_data(bot, await request.post())


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
