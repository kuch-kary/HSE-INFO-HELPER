from aiogram import types, Dispatcher
from aiogram.fsm.context import FSMContext
from keyboards.reply import get_contacts_keyboard, get_main_keyboard
from utils.helpers import error_handler, split_long_message
from utils.cache import cache
import logging

logger = logging.getLogger(__name__)

def register_handlers(dp: Dispatcher):
    
    # Обработчик кнопки назад
    @dp.message(lambda message: message.text in ["🔙 Назад", "Назад"])
    @error_handler
    async def go_back(message: types.Message, state: FSMContext):
        await state.clear()
        await message.answer("🔙 Главное меню:", reply_markup=get_main_keyboard())
    
    # Контакты
    @dp.message(lambda message: message.text == "📞 Контакты")
    @error_handler
    async def show_contacts(message: types.Message):
        await message.answer("📞 КОНТАКТЫ:", reply_markup=get_contacts_keyboard())
    
    # Преподаватели
    @dp.message(lambda message: message.text in ["👨‍🏫 Преподаватели", "Преподаватели"])
    @error_handler
    async def show_teachers(message: types.Message):
        try:
            teachers = cache.get('teachers.json')
            if not teachers:
                await message.answer("📭 Нет данных о преподавателях")
                return
            
            text = "👨‍🏫 ПРЕПОДАВАТЕЛИ:\n\n"
            for teacher in teachers:
                name = teacher.get('name', 'Неизвестно')
                subject = teacher.get('subject', 'Не указан')
                group = teacher.get('group', 'Не указана')
                text += f"• {name}\n  📚 {subject}\n  👥 Группа: {group}\n\n"
            
            for part in split_long_message(text):
                await message.answer(part)
        except Exception as e:
            logger.error(f"Ошибка в show_teachers: {e}")
            await message.answer("❌ Ошибка при загрузке данных преподавателей")
    
    # Старосты
    @dp.message(lambda message: message.text in ["👥 Старосты", "Старосты"])
    @error_handler
    async def show_heads(message: types.Message):
        try:
            heads = cache.get('heads.json')
            if not heads:
                await message.answer("📭 Нет данных о старостах")
                return
            
            text = "👥 СТАРОСТЫ:\n\n"
            for head in heads:
                name = head.get('name', 'Неизвестно')
                tg = head.get('tg_username', '')
                group = head.get('group', 'Не указана')
                
                text += f"• {name}\n"
                if tg:
                    text += f"  {tg}\n"
                if group != 'Не указана':
                    text += f"  🎓 Группа: {group}\n"
                text += "\n"
            
            await message.answer(text)
        except Exception as e:
            logger.error(f"Ошибка в show_heads: {e}")
            await message.answer("❌ Ошибка при загрузке данных старост")
    
    # Менеджеры
    @dp.message(lambda message: message.text in ["👔 Менеджеры", "Менеджеры"])
    @error_handler
    async def show_managers(message: types.Message):
        try:
            admins = cache.get('admins.json')
            if not admins:
                await message.answer("📭 Нет данных о менеджерах")
                return
            
            text = "👔 МЕНЕДЖЕРЫ ГРУПП:\n\n"
            for admin in admins:
                name = admin.get('name', 'Неизвестно')
                email = admin.get('email', '')
                groups = admin.get('groups', [])
                
                text += f"• {name}\n"
                if email:
                    text += f"  📧 {email}\n"
                
                if groups:
                    groups_str = ', '.join(groups) if isinstance(groups, list) else str(groups)
                    text += f"  👥 Группы: {groups_str}\n"
                text += "\n"
            
            await message.answer(text)
        except Exception as e:
            logger.error(f"Ошибка в show_managers: {e}")
            await message.answer("❌ Ошибка при загрузке данных менеджеров")
    
    # ПАП
    @dp.message(lambda message: message.text in ["🆘 ПАП", "ПАП", "sos"])
    @error_handler
    async def show_paps(message: types.Message):
        try:
            paps = cache.get('paps.json')
            if not paps:
                await message.answer("📭 Нет данных о ПАП")
                return
            
            text = "🆘 ПОМОЩНИКИ АДАПТАЦИИ (ПАП):\n\n"
            for pap in paps:
                name = pap.get('name', 'Неизвестно')
                tg = pap.get('tg_username', '')
                direction = pap.get('direction', '')
                groups = pap.get('groups', [])
                
                text += f"• {name}\n"
                if tg:
                    text += f"  {tg}\n"
                if direction:
                    text += f"  📌 {direction}\n"
                
                if groups:
                    groups_str = ', '.join(groups) if isinstance(groups, list) else str(groups)
                    text += f"  👥 Группы: {groups_str}\n"
                text += "\n"
            
            await message.answer(text)
        except Exception as e:
            logger.error(f"Ошибка в show_paps: {e}")
            await message.answer("❌ Ошибка при загрузке данных ПАП")
    
    # Светлана Федоровна
    @dp.message(lambda message: any(word in message.text for word in ["Светлана", "Федоровна"]))
    @error_handler
    async def show_svetlana(message: types.Message):
        text = (
            "👩‍🏫 СВЕТЛАНА ФЕДОРОВНА\n\n"
            "Руководитель образовательной программы\n"
            "Email: sfedorova@hse.ru"
        )
        await message.answer(text)