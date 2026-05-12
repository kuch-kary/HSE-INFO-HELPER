# handlers/instructions.py

from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from keyboards.reply import (
    get_instructions_keyboard, get_freshman_keyboard,
    get_platforms_keyboard, get_docs_keyboard,
    get_grading_keyboard, get_main_keyboard,
    get_subjects_keyboard
)
from utils.helpers import error_handler, split_long_message
from instructions_data import Instructions
import logging

logger = logging.getLogger(__name__)

def register_handlers(dp: Dispatcher):
    
    # Возврат к списку инструкций
    @dp.message(lambda message: message.text == "🔙 К списку инструкций")
    @error_handler
    async def back_to_instructions(message: types.Message, state: FSMContext):
        """Возврат к главному меню инструкций"""
        await show_instructions_menu(message)
    
    # Кнопка назад в главное меню
    @dp.message(lambda message: message.text == "🔙 Назад")
    @error_handler
    async def go_back(message: types.Message, state: FSMContext):
        """Обработчик кнопки назад в главное меню"""
        await state.clear()
        await message.answer(
            "🔙 Главное меню:",
            reply_markup=get_main_keyboard()
        )
    
    # Главное меню инструкций
    @dp.message(lambda message: message.text == "📖 Инструкции")
    @error_handler
    async def show_instructions_menu(message: types.Message):
        await message.answer(
            "📖 ИНСТРУКЦИИ ДЛЯ СТУДЕНТОВ\n\n"
            "Выберите категорию:",
            reply_markup=get_instructions_keyboard()
        )
    
    # ===== 1. ДЛЯ ПЕРВОКУРСНИКА =====
    
    @dp.message(lambda message: message.text == "🎓 1. Для первокурсника")
    @error_handler
    async def show_freshman_menu(message: types.Message):
        await message.answer(
            "🎓 ДЛЯ ПЕРВОКУРСНИКА\n\n"
            "Всё, что нужно знать с самого начала:",
            reply_markup=get_freshman_keyboard()
        )
    
    @dp.message(lambda message: message.text == "👥 Группы")
    @error_handler
    async def show_groups(message: types.Message):
        await message.answer(
            Instructions.groups(),
            disable_web_page_preview=True
        )
    
    @dp.message(lambda message: message.text == "🆘 Кто такой ПАП?")
    @error_handler
    async def show_pap_info(message: types.Message):
        await message.answer(
            Instructions.pap(),
            disable_web_page_preview=True
        )
    
    @dp.message(lambda message: message.text == "📧 Корпоративная почта")
    @error_handler
    async def show_email_info(message: types.Message):
        await message.answer(
            Instructions.email(),
            disable_web_page_preview=True
        )
    
    @dp.message(lambda message: message.text == "💬 Общение с преподавателями")
    @error_handler
    async def show_communication_info(message: types.Message):
        await message.answer(
            Instructions.communication(),
            disable_web_page_preview=True
        )
    
    # ===== ПРЕДМЕТЫ =====
    
    @dp.message(lambda message: message.text == "📚 Предметы")
    @error_handler
    async def show_subjects_menu(message: types.Message):
        """Меню предметов"""
        await message.answer(
            "📚 ПРЕДМЕТЫ\n\n"
            "Выберите предмет:",
            reply_markup=get_subjects_keyboard()
        )
    
    @dp.message(lambda message: message.text == "📐 Проектирование")
    @error_handler
    async def show_subjects_design(message: types.Message):
        """Информация о проектировании"""
        await message.answer(Instructions.subjects_design())
    
    @dp.message(lambda message: message.text == "💻 Технологии")
    @error_handler
    async def show_subjects_technology(message: types.Message):
        """Информация о технологиях"""
        await message.answer(Instructions.subjects_technology())
    
    @dp.message(lambda message: message.text == "🎨 История искусств")
    @error_handler
    async def show_art_history_info(message: types.Message):
        """Информация о предмете История искусств"""
        text = Instructions.art_history()
        for part in split_long_message(text):
            await message.answer(part, disable_web_page_preview=True)
    
    @dp.message(lambda message: message.text == "📋 Прочее")
    @error_handler
    async def show_subjects_other(message: types.Message):
        """Прочие предметы"""
        await message.answer(Instructions.subjects_other())
    
    # ===== 2. УЧЕБНЫЕ ПЛАТФОРМЫ =====
    
    @dp.message(lambda message: message.text == "📚 2. Учебные платформы")
    @error_handler
    async def show_platforms_menu(message: types.Message):
        await message.answer(
            "📚 УЧЕБНЫЕ ПЛАТФОРМЫ\n\n"
            "Выберите тему:",
            reply_markup=get_platforms_keyboard()
        )
    
    @dp.message(lambda message: message.text == "📚 LMS и Smart LMS")
   
