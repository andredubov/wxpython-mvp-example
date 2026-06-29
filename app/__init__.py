# Из конкретного файла импортируем класс модели
from .application import MyApplication

# Явно указываем, какие классы экспонируются наружу из этого пакета
__all__ = ['MyApplication']
__version__ = "1.0.0"
__author__ = "Andrei Dubov"