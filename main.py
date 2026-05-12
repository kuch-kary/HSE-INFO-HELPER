import asyncio
import logging
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("❌ Ошибка: Токен не найден в файле .env")
    sys.exit(1)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

session = AiohttpSession()
bot = Bot(token=TOKEN, session=session)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

from handlers import register_all_handlers
from keyboards.reply import get_main_keyboard
from utils.cache import cache

register_all_handlers(dp)

try:
    cache.preload_all()
    logger.info("✅ Все данные предзагружены в кеш")
except Exception as e:
    logger.error(f"❌ Ошибка при предзагрузке данных: {e}")

@dp.message()
async def unknown_message(message: types.Message):
    logger.info(f"Неизвестная команда от {message.from_user.id}: '{message.text}'")
    await message.answer(
        "❌ Я не понимаю эту команду.\n"
        "Пожалуйста, используйте кнопки меню или /start",
        reply_markup=get_main_keyboard()
    )

async def main():
    try:
        logger.info("✅ Бот запущен!")
        logger.info("🤖 Жду сообщения от пользователей...")
        await dp.start_polling(bot)
    except Exception as e:
        logger.error(f"❌ Ошибка при работе бота: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("👋 Бот остановлен")

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)