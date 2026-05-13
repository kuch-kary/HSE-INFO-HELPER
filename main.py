import asyncio
import logging
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update
from dotenv import load_dotenv
from flask import Flask, request, jsonify

load_dotenv()
TOKEN = os.getenv('BOT_TOKEN')
WEBHOOK_URL = os.getenv('WEBHOOK_URL')

if not TOKEN:
    print("❌ Ошибка: Токен не найден в файле .env")
    sys.exit(1)

if not WEBHOOK_URL:
    print("❌ Ошибка: WEBHOOK_URL не найден в файле .env")
    print("💡 Добавьте в Render: WEBHOOK_URL=https://hse-info-helper.onrender.com")
    sys.exit(1)

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('bot.log', encoding='utf-8'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# Создаём бота и диспетчер
bot = Bot(
    token=TOKEN,
    default=DefaultBotProperties(parse_mode=None)
)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Импортируем все обработчики
from handlers import register_all_handlers
from keyboards.reply import get_main_keyboard
from utils.cache import cache

register_all_handlers(dp)

# Предзагружаем кеш
try:
    cache.preload_all()
    logger.info("✅ Все данные предзагружены в кеш")
except Exception as e:
    logger.error(f"❌ Ошибка при предзагрузке данных: {e}")

# Обработчик неизвестных команд
@dp.message()
async def unknown_message(message: types.Message):
    logger.info(f"Неизвестная команда от {message.from_user.id}: '{message.text}'")
    await message.answer(
        "❌ Я не понимаю эту команду.\n"
        "Пожалуйста, используйте кнопки меню или /start",
        reply_markup=get_main_keyboard()
    )

# Создаём Flask приложение
web_app = Flask(__name__)

# Обычные (не асинхронные) функции для Flask
@web_app.route("/", methods=["HEAD", "GET"])
def health_check():
    """Проверка работы сервера"""
    return "Bot is running!", 200

@web_app.route("/webhook", methods=["POST"])
def webhook():
    """Получение обновлений от Telegram"""
    try:
        # Получаем обновление от Telegram
        update_data = request.get_json()
        if not update_data:
            return jsonify({"status": "error", "message": "No data"}), 400
        
        # Создаем задачу для обработки в асинхронном режиме
        update = Update.model_validate(update_data)
        
        # Запускаем асинхронную обработку
        asyncio.create_task(dp.feed_update(bot, update))
        
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"❌ Ошибка в вебхуке: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@web_app.route("/set_webhook", methods=["GET"])
def set_webhook():
    """Установка вебхука"""
    try:
        # Запускаем асинхронную функцию
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        webhook_url = f"{WEBHOOK_URL}/webhook"
        loop.run_until_complete(
            bot.set_webhook(
                webhook_url,
                drop_pending_updates=True,
                allowed_updates=["message", "callback_query"]
            )
        )
        loop.close()
        
        logger.info(f"✅ Вебхук установлен: {webhook_url}")
        return jsonify({"status": "ok", "webhook_url": webhook_url}), 200
    except Exception as e:
        logger.error(f"❌ Ошибка при установке вебхука: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@web_app.route("/delete_webhook", methods=["GET"])
def delete_webhook():
    """Удаление вебхука"""
    try:
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        loop.run_until_complete(bot.delete_webhook(drop_pending_updates=True))
        loop.close()
        
        logger.info("✅ Вебхук удален")
        return jsonify({"status": "ok"}), 200
    except Exception as e:
        logger.error(f"❌ Ошибка при удалении вебхука: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

# Запуск Flask приложения
def run_flask():
    port = int(os.environ.get("PORT", 10000))
    web_app.run(host="0.0.0.0", port=port)

if __name__ == "__main__":
    # Запускаем Flask сервер
    run_flask()
