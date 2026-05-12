import logging
from typing import List, Any
from functools import wraps
from aiogram.types import Message

logger = logging.getLogger(__name__)

def split_long_message(text: str, max_length: int = 4000) -> List[str]:
    if len(text) <= max_length:
        return [text]
    
    parts = []
    current_part = ""
    
    for line in text.split('\n'):
        if len(current_part) + len(line) + 1 > max_length:
            if current_part:
                parts.append(current_part)
            current_part = line
        else:
            if current_part:
                current_part += '\n' + line
            else:
                current_part = line
    
    if current_part:
        parts.append(current_part)
    
    return parts

def error_handler(func):
    @wraps(func)
    async def wrapper(message: Message, *args, **kwargs):
        try:
            return await func(message, *args, **kwargs)
        except Exception as e:
            logger.error(f"❌ Ошибка в {func.__name__}: {e}", exc_info=True)
            await message.answer("❌ Произошла ошибка. Попробуйте позже.")
    return wrapper