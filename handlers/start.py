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
            "• 👨‍🏫 Преподаватели — кто какие предметы ведёт\n"
            "• 👥 Старосты — контакты старост всех групп\n"
            "• 👔 Менеджеры — учебные менеджеры с email\n"
            "• 🆘 ПАП — помощники адаптации первокурсников\n"
            "• 👩‍🏫 Светлана Федоровна — руководитель программы\n\n"
            
            "📚 УЧЕБНЫЕ МАТЕРИАЛЫ\n"
            "• 📅 Расписание — все версии расписания\n"
            "• 📁 Портфолио — платформы для портфолио\n"
            "• 💻 LMS — Smart LMS и обычная LMS\n"
            "• 📊 Отзывы — отзывы на преподавателей\n"
            "• 💬 Полезные чаты — чаты, каналы, поддержка\n\n"
            
            "📖 ИНСТРУКЦИИ\n"
            "• 🎓 Для первокурсника:\n"
            "  - Группы, ПАП, почта, общение, предметы\n"
            "  - 📐 Проектирование\n"
            "  - 💻 Технологии\n"
            "  - 🎨 История искусств\n"
            "  - 📋 Прочее\n"
            "• 📚 Учебные платформы (LMS, расписание, портфолио)\n"
            "• 📋 Документы и планирование (РУП, ПУД, майноры)\n"
            "• 📝 Оценивание и экзамены (система оценок, метрики, прокторинг, СОП)\n"
            "• 💰 Стипендии и возможности\n"
            "• ⚠️ Отчисление: причины и как избежать\n\n"
            
            "Выбери нужный раздел в меню:",
            reply_markup=get_main_keyboard()
        )
