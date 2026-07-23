# Из конкретного файла импортируем класс
from .app_router import AppRouter

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['AppRouter']
__version__ = "1.0.0"
__author__ = "Andrei Dubov"