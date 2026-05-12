from . import start
from . import contacts
from . import materials
from . import instructions

def register_all_handlers(dp):
    print("🔄 Регистрация обработчиков...")
    start.register_handlers(dp)
    print("  ✅ start.py")
    contacts.register_handlers(dp)
    print("  ✅ contacts.py")
    materials.register_handlers(dp)
    print("  ✅ materials.py")
    instructions.register_handlers(dp)
    print("  ✅ instructions.py")
    print("✅ Все обработчики зарегистрированы")