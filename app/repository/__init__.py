# Из конкретного файла импортируем класс репозитория
from .counter_repository import CounterRepository

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['CounterRepository']

__version__ = "1.0.0"