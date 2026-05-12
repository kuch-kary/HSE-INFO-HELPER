from aiogram import types, Dispatcher
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from keyboards.reply import get_main_keyboard
from utils.helpers import error_handler
import logging

logger = logging.getLogger(__name__)

def register_handlers(dp: Dispatcher):
    
    @dp.message(Command("start"))
    @error_handler
    async def cmd_start(message: types.Message, state: FSMContext):
        user_id = message.from_user.id
        username = message.from_user.username or "без username"
        
        await state.clear()
        logger.info(f"Новый пользователь: @{username} (ID: {user_id})")
        
        await message.answer(
            "👋 Привет! Я бот-помощник для студентов.\n\n"
            "Вот, что я умею:\n\n"
            
            "📞 КОНТАКТЫ\n"
            "• Преподаватели (32 чел.)\n"
            "• Старосты (25 чел.)\n"
            "• Менеджеры (4 чел.)\n"
            "• ПАП (9 чел.)\n"
            "• Светлана Федоровна\n\n"
            
            "📚 УЧЕБНЫЕ МАТЕРИАЛЫ\n"
            "• Расписание (7 ссылок)\n"
            "• Портфолио (3 ссылки)\n"
            "• LMS (2 ссылки)\n"
            "• Отзывы (2 ссылки)\n"
            "• Полезные чаты (5 ссылок)\n\n"
            
            "📖 ИНСТРУКЦИИ\n"
            "1. Для первокурсника\n"
            "   - Группы\n"
            "   - Кто такой ПАП?\n"
            "   - Корпоративная почта\n"
            "   - Общение с преподавателями\n"
            "   - Предметы\n"
            "     • Проектирование\n"
            "     • Технологии\n"
            "     • История искусств\n"
            "     • Прочее\n\n"
            
            "2. Учебные платформы\n"
            "   - LMS и Smart LMS\n"
            "   - Расписание\n"
            "   - Портфолио\n\n"
            
            "3. Документы и планирование\n"
            "   - РУП (учебный план)\n"
            "   - ПУД (программа дисциплин)\n"
            "   - Майноры\n"
            "   - КУД\n"
            "   - ИУП\n\n"
            
            "4. Оценивание и экзамены\n"
            "   - Система оценивания\n"
            "   - Метрики и доп. баллы\n"
            "   - Прокторинг\n"
            "   - СОП\n\n"
            
            "5. Стипендии и возможности\n\n"
            
            "6. Отчисление\n\n"
            
            "Выбери нужный раздел в меню:",
            reply_markup=get_main_keyboard()
        )
