import json
import time
import logging
from typing import Dict, List, Any, Optional

logger = logging.getLogger(__name__)

class DataCache:
    def __init__(self, ttl: int = 3600):
        self.cache: Dict[str, Dict[str, Any]] = {}
        self.ttl = ttl
        logger.info(f"✅ Кеш инициализирован с TTL={ttl} сек")
    
    def get(self, filename: str) -> List[Dict]:
        current_time = time.time()
        
        if filename in self.cache:
            data, timestamp = self.cache[filename]
            if current_time - timestamp < self.ttl:
                return data
        
        data = self._load_data(filename)
        self.cache[filename] = (data, current_time)
        return data
    
    def _load_data(self, filename: str) -> List[Dict]:
        try:
            with open(f'data/{filename}', 'r', encoding='utf-8') as file:
                data = json.load(file)
                logger.info(f"📁 Загружено {len(data)} записей из {filename}")
                return data
        except FileNotFoundError:
            logger.error(f"❌ Файл data/{filename} не найден")
            return []
        except Exception as e:
            logger.error(f"❌ Ошибка при загрузке {filename}: {e}")
            return []
    
    def preload_all(self):
        files = ['teachers.json', 'heads.json', 'admins.json', 'paps.json', 'links.json']
        for file in files:
            self.get(file)
        logger.info("✅ Все данные предзагружены в кеш")

cache = DataCache()