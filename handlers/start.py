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
            "👋 **Привет! Я бот-помощник для студентов.**\n\n"
            "Я помогу найти:\n"
            "• 👨‍🏫 Преподавателей и контакты\n"
            "• 📚 Учебные материалы\n"
            "• 💬 Полезные чаты\n"
            "• 📖 Инструкции для первокурсников\n\n"
            "Выбери нужный раздел в меню:",
            parse_mode="Markdown",
            reply_markup=get_main_keyboard()
        )