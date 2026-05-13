import asyncio
import logging
import os
import sys
from pathlib import Path
from threading import Thread

sys.path.append(str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.session.aiohttp import AiohttpSession
from aiogram.client.default import DefaultBotProperties
from dotenv import load_dotenv
from flask import Flask

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')

if not TOKEN:
    print("❌ Ошибка: Токен не найден в файле .env")
    sys.exit(1)

# Flask для Render Health Check
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Bot is running!", 200

def run_web_server():
    web_app.run(host='0.0.0.0', port=10000)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Создаём сессию с увеличенным таймаутом
session = AiohttpSession()
bot = Bot(
    token=TOKEN, 
    session=session,
    default=DefaultBotProperties(parse_mode=None)
)
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
        
        # Удаляем вебхук и запускаем polling с увеличенным таймаутом
        await bot.delete_webhook(drop_pending_updates=True)
        await dp.start_polling(
            bot,
            polling_timeout=60,
            handle_as_tasks=True
        )
    except Exception as e:
        logger.error(f"❌ Ошибка при работе бота: {e}", exc_info=True)
    finally:
        await bot.session.close()
        logger.info("👋 Бот остановлен")

if __name__ == "__main__":
    # Запускаем Flask в отдельном потоке
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("👋 Бот остановлен пользователем (Ctrl+C)")
    except Exception as e:
        logger.error(f"❌ Критическая ошибка: {e}", exc_info=True)
