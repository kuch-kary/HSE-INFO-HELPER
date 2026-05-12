from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.reply import get_search_keyboard, get_main_keyboard
from utils.helpers import error_handler, split_long_message
from utils.search_helpers import search_all
from config import Config
import logging

logger = logging.getLogger(__name__)

class SearchStates(StatesGroup):
    waiting_for_query = State()

def register_handlers(dp: Dispatcher):
    
    @dp.message(lambda message: message.text == "🔍 Поиск")
    @error_handler
    async def search_menu(message: types.Message, state: FSMContext):
        """Меню поиска"""
        await state.set_state(SearchStates.waiting_for_query)
        await message.answer(
            "🔍 **РЕЖИМ ПОИСКА**\n\n"
            "🔹 Я могу найти:\n"
            "• 👨‍🏫 Преподавателя по фамилии\n"
            "• 👥 Старосту по имени или группе\n"
            "• 🆘 ПАП по имени или группе\n"
            "• 👔 Менеджера по фамилии\n\n"
            "🔹 **Примеры запросов:**\n"
            "• `Иванов`\n"
            "• `БП25ДЗ06`\n"
            "• `Екатерина`\n\n"
            "✏️ Введи фамилию, имя или номер группы:",
            parse_mode="Markdown",
            reply_markup=get_search_keyboard()
        )
    
    @dp.message(lambda message: message.text == "❌ Выйти из поиска")
    @error_handler
    async def exit_search(message: types.Message, state: FSMContext):
        """Выход из режима поиска"""
        await state.clear()
        await message.answer(
            "🔙 Вы вышли из режима поиска.",
            reply_markup=get_main_keyboard()
        )
    
    @dp.message(SearchStates.waiting_for_query)
    @error_handler
    async def process_search(message: types.Message, state: FSMContext):
        """Обработка поискового запроса"""
        query = message.text
        
        if query == "❌ Выйти из поиска":
            await state.clear()
            await message.answer(
                "🔙 Вы вышли из режима поиска.",
                reply_markup=get_main_keyboard()
            )
            return
        
        if len(query) < 2:
            await message.answer(
                "❌ Слишком короткий запрос. Минимум 2 символа.",
                reply_markup=get_search_keyboard()
            )
            return
        
        await message.bot.send_chat_action(message.chat.id, "typing")
        
        try:
            results = search_all(query, Config.STOP_WORDS)
            
            if not results:
                if len(query) < 4:
                    await message.answer(
                        f"❌ По запросу **'{query}'** ничего не найдено.\n\n"
                        f"💡 Спросите **'что ты умеешь'** — я расскажу о своих возможностях",
                        parse_mode="Markdown"
                    )
                else:
                    await message.answer(
                        f"❌ По запросу **'{query}'** ничего не найдено.\n\n"
                        f"Попробуйте:\n"
                        f"• написать фамилию полностью\n"
                        f"• написать номер группы\n"
                        f"• спросить **'что ты умеешь'**",
                        parse_mode="Markdown"
                    )
            else:
                final_text = f"🔍 **РЕЗУЛЬТАТЫ ПОИСКА:**\n\n"
                for i, result in enumerate(results, 1):
                    final_text += f"{i}. {result}\n\n"
                
                for part in split_long_message(final_text):
                    await message.answer(part, parse_mode="Markdown")
        except Exception as e:
            logger.error(f"Ошибка при поиске: {e}", exc_info=True)
            await message.answer(
                "❌ Произошла ошибка при поиске. Попробуйте другой запрос.",
                reply_markup=get_search_keyboard()
            )
        
        await message.answer(
            "🔍 Можешь ввести еще один запрос:",
            reply_markup=get_search_keyboard()
        )