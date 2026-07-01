# Из конкретного файла импортируем класс репозитория
from .counter_repository import CounterRepository

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['CounterRepository']