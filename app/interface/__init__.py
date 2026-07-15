# Из конкретного файла импортируем протоколы
from .model import CounterModelInterface

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = [
    'CounterModelInterface', 
    ]

__version__ = "1.0.0"

