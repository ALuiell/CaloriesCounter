from __future__ import annotations

import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode

from app.core.config import get_settings
from app.core.logging import configure_logging
from app.db.database import Database
from app.db.seed import seed_products_if_empty
from app.handlers import register_handlers


async def _main() -> None:
    configure_logging()
    settings = get_settings()

    database = Database(settings.database_path, settings.app_timezone)
    database.initialize()
    seed_products_if_empty(database, settings.seed_path)

    bot = Bot(
        token=settings.bot_token,
        default=DefaultBotProperties(parse_mode=ParseMode.HTML),
    )
    dispatcher = Dispatcher()
    register_handlers(dispatcher, database)

    logging.info("Bot started")
    await dispatcher.start_polling(bot)


def run_bot() -> None:
    asyncio.run(_main())
