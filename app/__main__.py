from aiogram import Bot
from aiohttp import web
from loguru import logger
from app import log, config
from app.posting import process_request_posting

bot = Bot(config.BOT_TOKEN)
log.setup()


async def hello_get(request: web.Request) -> web.Response:
    return await process_request_posting(bot, request.query)


async def hello_post(request: web.Request) -> web.Response:
    return await process_request_posting(bot, await request.post())


async def on_startup(_: web.Application):
    logger.debug("bot started")
    await bot.send_message(config.LOG_CHAT_ID, "Bot started")


async def on_shutdown(_: web.Application):
    await bot.send_message(config.LOG_CHAT_ID, "Bot stopped")
    await bot.close()


def init() -> web.Application:
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
