import logging
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from flask import Flask, request, jsonify
import json
import requests

# Ваш токен (получаем из переменных окружения Render)
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ Ошибка: Токен не найден")
    sys.exit(1)

# Настройка логов
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(storage=storage)

# Импортируем все обработчики
from handlers import register_all_handlers
from keyboards.reply import get_main_keyboard
from utils.cache import cache

# Регистрируем обработчики
register_all_handlers(dp)

# Предзагружаем кеш
try:
    cache.preload_all()
    logger.info("✅ Все данные предзагружены в кеш")
except Exception as e:
    logger.error(f"❌ Ошибка при предзагрузке данных: {e}")

# Создаём Flask приложение
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "HSE INFO HELPER BOT is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка входящих запросов от Telegram (синхронная версия)"""
    try:
        # Получаем данные от Telegram
        update_data = request.get_json()
        
        if not update_data:
            return jsonify({"status": "error", "message": "No data"}), 400
        
        # Импортируем asyncio для запуска асинхронного обработчика
        import asyncio
        
        # Создаем новый event loop для этого запроса
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        
        try:
            # Создаем объект Update и передаем его в диспетчер
            update = types.Update.model_validate(update_data)
            loop.run_until_complete(dp.feed_update(bot, update))
        finally:
            loop.close()
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Ошибка в вебхуке: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка вебхука (один раз в браузере)"""
    try:
        # Получаем URL сервера
        webhook_url = f"https://{request.host}/webhook"
        
        # Отправляем запрос к Telegram API
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        response = requests.post(url, json={"url": webhook_url})
        
        if response.status_code == 200:
            result = response.json()
            if result.get('ok'):
                return jsonify({"status": "ok", "webhook_url": webhook_url, "result": result})
            else:
                return jsonify({"status": "error", "message": result.get('description')}), 500
        else:
            return jsonify({"status": "error", "message": f"HTTP {response.status_code}"}), 500
            
    except Exception as e:
        logger.error(f"Ошибка установки вебхука: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Удаление вебхука"""
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
        response = requests.post(url)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Запуск
if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
