import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    TOKEN = os.getenv('BOT_TOKEN')
    ADMIN_IDS = []
    CACHE_TTL = 3600
    MAX_MESSAGE_LENGTH = 4000
    
    @classmethod
    def is_admin(cls, user_id: int) -> bool:
        return user_id in cls.ADMIN_IDS