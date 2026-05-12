from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from keyboards.reply import get_materials_keyboard, get_main_keyboard
from utils.helpers import error_handler
from utils.cache import cache
import logging

logger = logging.getLogger(__name__)

def get_links_by_category(category: str, title: str) -> str:
    """Получить все ссылки определенной категории"""
    try:
        links = cache.get('links.json')
        if not links:
            return f"❌ Нет данных"
        
        filtered = [l for l in links if l.get('category') == category]
        if not filtered:
            return f"❌ Нет ссылок в категории {category}"
        
        text = f"{title}:\n\n"
        for link in filtered:
            text += f"• {link.get('title')}\n"
            if link.get('description'):
                text += f"  {link.get('description')}\n"
            text += f"  🔗 {link.get('url')}\n\n"
        
        return text
    except Exception as e:
        logger.error(f"Ошибка в get_links_by_category: {e}")
        return f"❌ Ошибка при загрузке ссылок"

def register_handlers(dp: Dispatcher):
    
    # Обработчик кнопки назад
    @dp.message(lambda message: message.text == "🔙 Назад")
    @error_handler
    async def go_back(message: types.Message, state: FSMContext):
        """Обработчик кнопки назад в главное меню"""
        await state.clear()
        await message.answer(
            "🔙 Главное меню:",
            reply_markup=get_main_keyboard()
        )
    
    # Главное меню учебных материалов
    @dp.message(lambda message: message.text == "📚 Учебные материалы")
    @error_handler
    async def show_materials(message: types.Message):
        await message.answer(
            "📚 УЧЕБНЫЕ МАТЕРИАЛЫ\n\n"
            "Выберите раздел:",
            reply_markup=get_materials_keyboard()
        )
    
    # Расписание
    @dp.message(lambda message: message.text == "📅 Расписание")
    @error_handler
    async def show_schedule(message: types.Message):
        text = get_links_by_category('schedule', '📅 РАСПИСАНИЕ')
        await message.answer(text, disable_web_page_preview=True)
    
    # Портфолио
    @dp.message(lambda message: message.text == "📁 Портфолио")
    @error_handler
    async def show_portfolio(message: types.Message):
        text = get_links_by_category('portfolio', '📁 ПОРТФОЛИО')
        await message.answer(text, disable_web_page_preview=True)
    
    # LMS
    @dp.message(lambda message: message.text == "💻 LMS")
    @error_handler
    async def show_lms(message: types.Message):
        text = get_links_by_category('lms', '💻 LMS')
        await message.answer(text, disable_web_page_preview=True)
    
    # Отзывы
    @dp.message(lambda message: message.text == "📊 Отзывы")
    @error_handler
    async def show_reviews(message: types.Message):
        text = get_links_by_category('reviews', '📊 ОТЗЫВЫ ПО ПРЕДМЕТАМ')
        await message.answer(text, disable_web_page_preview=True)
    
    # Полезные чаты
    @dp.message(lambda message: message.text == "💬 Полезные чаты")
    @error_handler
    async def show_chats(message: types.Message):
        text = get_links_by_category('chats', '💬 ПОЛЕЗНЫЕ ЧАТЫ')
        await message.answer(text, disable_web_page_preview=True)