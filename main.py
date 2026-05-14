import logging
import os
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent))

from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.client.default import DefaultBotProperties
from aiogram.types import Update
from flask import Flask, request, jsonify
import asyncio
import threading

# Ваш токен
BOT_TOKEN = os.getenv('BOT_TOKEN')

if not BOT_TOKEN:
    print("❌ Ошибка: Токен не найден")
    sys.exit(1)

# Настройка логов
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Глобальный event loop
loop = asyncio.new_event_loop()
asyncio.set_event_loop(loop)

# Создаём бота и диспетчер
bot = Bot(token=BOT_TOKEN, default=DefaultBotProperties(parse_mode=None))
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

# Обработчик неизвестных команд с простым ответом
@dp.message()
async def unknown_message(message: types.Message):
    logger.info(f"Неизвестная команда: {message.text}")
    await message.answer(
        "❌ Я не понимаю эту команду.\n"
        "Пожалуйста, используйте кнопки меню или /start",
        reply_markup=get_main_keyboard()
    )

# Создаём Flask приложение
app = Flask(__name__)

@app.route('/', methods=['GET'])
def index():
    return "HSE INFO HELPER BOT is running!", 200

@app.route('/webhook', methods=['POST'])
def webhook():
    """Обработка входящих запросов от Telegram"""
    try:
        # Получаем данные
        update_data = request.get_json()
        
        if not update_data:
            logger.warning("Нет данных в запросе")
            return jsonify({"status": "error", "message": "No data"}), 400
        
        logger.info(f"Получен вебхук: {update_data.get('message', {}).get('text', 'no text')}")
        
        # Создаем объект Update
        update = Update.model_validate(update_data)
        
        # Запускаем обработку в глобальном event loop
        future = asyncio.run_coroutine_threadsafe(dp.feed_update(bot, update), loop)
        
        # Ждем немного, чтобы обработать
        try:
            future.result(timeout=10)
        except TimeoutError:
            logger.warning("Обработка обновления заняла слишком много времени")
        
        return jsonify({"status": "ok"}), 200
        
    except Exception as e:
        logger.error(f"Ошибка в вебхуке: {e}", exc_info=True)
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/set_webhook', methods=['GET'])
def set_webhook():
    """Установка вебхука"""
    import requests
    
    try:
        webhook_url = f"https://{request.host}/webhook"
        
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/setWebhook"
        response = requests.post(url, json={"url": webhook_url, "drop_pending_updates": True})
        
        if response.status_code == 200:
            result = response.json()
            logger.info(f"Вебхук установлен: {webhook_url}, результат: {result}")
            return jsonify({"status": "ok", "webhook_url": webhook_url, "result": result})
        else:
            return jsonify({"status": "error", "message": f"HTTP {response.status_code}"}), 500
            
    except Exception as e:
        logger.error(f"Ошибка установки вебхука: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/delete_webhook', methods=['GET'])
def delete_webhook():
    """Удаление вебхука"""
    import requests
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/deleteWebhook"
        response = requests.post(url)
        logger.info(f"Вебхук удален: {response.json()}")
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/check_webhook', methods=['GET'])
def check_webhook():
    """Проверка статуса вебхука"""
    import requests
    
    try:
        url = f"https://api.telegram.org/bot{BOT_TOKEN}/getWebhookInfo"
        response = requests.get(url)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# Функция для запуска event loop в отдельном потоке
def run_loop():
    asyncio.set_event_loop(loop)
    loop.run_forever()

# Запуск
if __name__ == "__main__":
    # Запускаем event loop в отдельном потоке
    thread = threading.Thread(target=run_loop, daemon=True)
    thread.start()
    
    # Запускаем Flask
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port, debug=False)
