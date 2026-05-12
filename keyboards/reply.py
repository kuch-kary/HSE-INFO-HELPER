# keyboards/reply.py

from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📞 Контакты"), KeyboardButton(text="📚 Учебные материалы")],
            [KeyboardButton(text="💬 Полезные чаты"), KeyboardButton(text="📖 Инструкции")]
        ],
        resize_keyboard=True
    )

def get_contacts_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👨‍🏫 Преподаватели"), KeyboardButton(text="👥 Старосты")],
            [KeyboardButton(text="👔 Менеджеры"), KeyboardButton(text="🆘 ПАП")],
            [KeyboardButton(text="👩‍🏫 Светлана Федоровна")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def get_materials_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📅 Расписание"), KeyboardButton(text="📁 Портфолио")],
            [KeyboardButton(text="💻 LMS"), KeyboardButton(text="📊 Отзывы")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def get_instructions_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🎓 1. Для первокурсника")],
            [KeyboardButton(text="📚 2. Учебные платформы")],
            [KeyboardButton(text="📋 3. Документы и планирование")],
            [KeyboardButton(text="📝 4. Оценивание и экзамены")],
            [KeyboardButton(text="💰 5. Стипендии и возможности")],
            [KeyboardButton(text="🔙 Назад")]
        ],
        resize_keyboard=True
    )

def get_freshman_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="👥 Группы")],
            [KeyboardButton(text="🆘 Кто такой ПАП?")],
            [KeyboardButton(text="📧 Корпоративная почта")],
            [KeyboardButton(text="💬 Общение с преподавателями")],
            [KeyboardButton(text="🎨 История искусств")],  # Новая кнопка
            [KeyboardButton(text="🔙 К списку инструкций")]
        ],
        resize_keyboard=True
    )

def get_platforms_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📚 LMS и Smart LMS")],
            [KeyboardButton(text="📅 Расписание")],
            [KeyboardButton(text="📁 Портфолио")],
            [KeyboardButton(text="🔙 К списку инструкций")]
        ],
        resize_keyboard=True
    )

def get_docs_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📋 РУП (учебный план)")],
            [KeyboardButton(text="📄 ПУД (программа дисциплин)")],
            [KeyboardButton(text="📘 Майноры")],
            [KeyboardButton(text="🔙 К списку инструкций")]
        ],
        resize_keyboard=True
    )

def get_grading_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="📊 Система оценивания")],
            [KeyboardButton(text="📐 Метрики и доп. баллы")],
            [KeyboardButton(text="🎥 Прокторинг")],
            [KeyboardButton(text="📝 СОП")],
            [KeyboardButton(text="🔙 К списку инструкций")]
        ],
        resize_keyboard=True
    )

def get_back_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="🔙 Назад")]],
        resize_keyboard=True
    )

def get_search_keyboard() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="❌ Выйти из поиска")]
        ],
        resize_keyboard=True
    )